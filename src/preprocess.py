# src/preprocess.py
"""
Read data/raw/*_raw.csv, clean, dedupe, normalize dates to YYYY-MM-DD,
and save single cleaned CSV to data/cleaned/all_reviews_clean.csv
"""
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/cleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*_raw.csv"))
if not files:
    raise SystemExit("No raw files in data/raw. Run scraper first.")

dfs = []
for f in files:
    df = pd.read_csv(f, dtype=str)
    df['source_file'] = f.name
    dfs.append(df)
df = pd.concat(dfs, ignore_index=True)

# Ensure columns exist
for c in ['review','rating','date','bank','source','reviewId']:
    if c not in df.columns:
        df[c] = None

# Strip review text
df['review'] = df['review'].fillna('').astype(str).str.strip()
# Drop empty review rows
df = df[df['review'] != '']

# Convert rating to numeric and clamp
df['rating'] = pd.to_numeric(df['rating'], errors='coerce').astype('Int64')

# Normalize dates: keep YYYY-MM-DD if possible, else empty
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
df['date'] = df['date'].astype('str').replace('NaT','')

# Deduplicate using reviewId if present else text
if df['reviewId'].notna().sum() > 0:
    df = df.drop_duplicates(subset=['reviewId'], keep='first')
df = df.drop_duplicates(subset=['review'], keep='first')

# Save cleaned CSV
out_path = OUT_DIR / "all_reviews_clean.csv"
df.to_csv(out_path, index=False)
print("Saved cleaned dataset:", out_path)
print("Shape:", df.shape)
# Print per-bank counts
print(df['bank'].value_counts())
print("Missing % per column:")
print(df.isna().mean().round(4) * 100)
