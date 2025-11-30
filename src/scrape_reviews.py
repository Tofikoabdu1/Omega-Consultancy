# src/scrape_reviews.py
"""
Scrape Google Play reviews for a list of apps (banks).
Saves one CSV per bank in data/raw/.
"""
import csv
from pathlib import Path
from google_play_scraper import reviews, Sort
from datetime import datetime
import time

OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Map of bank short name -> app package id (YOU MUST REPLACE the app IDs below with the real ones)
APPS = {
    "CBE": "com.combanketh.mobilebanking",         # <-- replace with actual Play Store package id
    "BOA": "com.boa.boaMobileBanking",     # <-- replace
    "Dashen": "com.dashen.dashensuperapp"  # <-- replace
}

TARGET_PER_BANK = 500  # aim a bit higher

def scrape_bank(bank_name, package_name, target=TARGET_PER_BANK):
    all_reviews = []
    # google_play_scraper.reviews returns up to 'count' reviews; we'll call repeatedly if needed
    cursor = None
    total = 0
    while total < target:
        # get up to 200 per call (max safe)
        cnt = min(200, target - total)
        rvws, cursor = reviews(
            package_name,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=cnt,
            continuation_token=cursor
        )
        if not rvws:
            break
        for r in rvws:
            all_reviews.append({
                "reviewId": r.get("reviewId") or r.get("id") or "",
                "review": r.get("content") or r.get("text") or "",
                "rating": r.get("score"),
                "date": r.get("at").isoformat() if r.get("at") else "",
                "bank": bank_name,
                "app_id": package_name,
                "source": "google_play"
            })
        total = len(all_reviews)
        print(f"{bank_name}: collected {total}")
        # politeness delay
        time.sleep(0.6)
        if cursor is None:
            # no more pages
            break
    return all_reviews

def write_csv(bank_name, rows):
    path = OUT_DIR / f"{bank_name.replace(' ','_')}_raw.csv"
    with open(path, "w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=["reviewId","review","rating","date","bank","app_id","source"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("Saved:", path, "rows:", len(rows))

def main():
    for bank, pkg in APPS.items():
        print("Scraping", bank, pkg)
        rows = scrape_bank(bank, pkg, TARGET_PER_BANK)
        write_csv(bank, rows)

if __name__ == "__main__":
    main()
