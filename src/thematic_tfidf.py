# src/thematic_tfidf.py
"""
Compute TF-IDF top keywords per bank and assign simple themes using rules.
Saves:
- data/processed/top_keywords_per_bank.csv
- data/processed/all_reviews_with_themes.csv
"""
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
nlp = spacy.load("en_core_web_sm", disable=["parser","ner"])

IN = Path("data/processed/all_reviews_with_sentiment.csv")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(IN)
# clean text
def spacy_clean(text):
    doc = nlp(str(text).lower())
    tokens = [t.lemma_ for t in doc if t.is_alpha and not t.is_stop and len(t)>2]
    return " ".join(tokens)

df['clean'] = df['review'].apply(spacy_clean)

# TF-IDF
vec = TfidfVectorizer(ngram_range=(1,2), max_features=4000)
X = vec.fit_transform(df['clean'])
features = vec.get_feature_names_out()

top_keywords = {}
for bank in df['bank'].unique():
    idx = df[df['bank']==bank].index.tolist()
    if not idx:
        top_keywords[bank] = []
        continue
    mean_tfidf = X[idx,:].mean(axis=0).A1
    topn = mean_tfidf.argsort()[-30:][::-1]
    top_keywords[bank] = [features[i] for i in topn]

pd.DataFrame(dict([(k, pd.Series(v)) for k,v in top_keywords.items()])).to_csv(OUT_DIR/"top_keywords_per_bank.csv", index=False)

# Simple rule-based theme assignment using keywords (you will refine)
theme_rules = {
    "Account Access": ["login","password","otp","biometric","pin","signin","sign in"],
    "Transactions": ["transfer","send","payment","transaction","txn","failed","processing"],
    "Performance": ["slow","lag","loading","crash","crashed","freeze"],
    "UI/UX": ["ui","ux","design","navigation","button","layout","menu"],
    "Support": ["support","customer","service","agent","call","help","respond"]
}

def assign_themes(text):
    text = str(text).lower()
    hits = []
    for theme, kws in theme_rules.items():
        if any(k in text for k in kws):
            hits.append(theme)
    if not hits:
        return "Other"
    return ";".join(hits[:2])

df['themes'] = df['review'].apply(assign_themes)
df.to_csv(OUT_DIR/"all_reviews_with_themes.csv", index=False)
print("Saved keywords and themed CSVs to", OUT_DIR)
