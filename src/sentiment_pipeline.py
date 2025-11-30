# src/sentiment_pipeline.py
"""
Batch sentiment using distilbert-base-uncased-finetuned-sst-2-english.
Saves augmented CSV: data/processed/all_reviews_with_sentiment.csv
"""
import pandas as pd
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from tqdm import tqdm

IN = Path("data/cleaned/all_reviews_clean.csv")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "all_reviews_with_sentiment.csv"

df = pd.read_csv(IN)
texts = df['review'].fillna('').astype(str).tolist()

# model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# pipeline (device=-1 CPU; set device=0 if GPU available)
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=-1, truncation=True)

labels = []
scores = []
batch_size = 32

for i in tqdm(range(0, len(texts), batch_size)):
    batch = texts[i:i+batch_size]
    out = nlp(batch)  # returns list of dicts
    for r in out:
        labels.append(r['label'])
        scores.append(r['score'])

df['sentiment_label'] = labels
df['sentiment_score'] = scores
df.to_csv(OUT, index=False)
print("Saved sentiment file:", OUT)
