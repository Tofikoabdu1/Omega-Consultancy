# src/postgres_insert.py
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()  # optional: read DB creds from .env
DB = {
    'dbname': os.getenv('DB_NAME','bank_reviews'),
    'user': os.getenv('DB_USER','postgres'),
    'password': os.getenv('DB_PASS','yourpassword'),
    'host': os.getenv('DB_HOST','localhost'),
    'port': os.getenv('DB_PORT',5432)
}

CSV = Path("data/processed/all_reviews_with_themes.csv")
if not CSV.exists():
    raise SystemExit("Run thematic step first")

df = pd.read_csv(CSV)

conn = psycopg2.connect(**DB)
cur = conn.cursor()

# Upsert banks
banks = df['bank'].dropna().unique().tolist()
cur.execute("SELECT bank_name, bank_id FROM banks WHERE bank_name = ANY(%s)", (banks,))
existing = dict(cur.fetchall())
to_insert = [(b, None) for b in banks if b not in existing]

if to_insert:
    execute_values(cur, "INSERT INTO banks (bank_name, app_id) VALUES %s RETURNING bank_id, bank_name", to_insert)
    rows = cur.fetchall()
    for bank_id, bank_name in rows:
        existing[bank_name] = bank_id
conn.commit()

# Prepare review rows
rows = []
for _, r in df.iterrows():
    bank_id = existing.get(r['bank'])
    rows.append((
        r.get('reviewId') if 'reviewId' in r else None,
        bank_id,
        r.get('review'),
        int(r['rating']) if pd.notna(r['rating']) else None,
        r.get('date') if pd.notna(r.get('date')) and r.get('date')!='' else None,
        r.get('sentiment_label') if 'sentiment_label' in r else None,
        float(r.get('sentiment_score')) if pd.notna(r.get('sentiment_score')) else None,
        r.get('themes') if 'themes' in r else None,
        r.get('source') if 'source' in r else 'google_play'
    ))
execute_values(cur,
    """INSERT INTO reviews(external_review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, themes, source)
       VALUES %s""",
    rows)
conn.commit()
cur.close()
conn.close()
print("Inserted", len(rows), "rows into reviews")
