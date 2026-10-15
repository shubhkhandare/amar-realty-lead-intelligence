"""Day 4 loader:  newest clean CSV into db/leads.db and write a pipeline log line."""
import csv
import glob
import os
import sqlite3
from datetime import datetime

DB_PATH = "db/leads.db"
LOG_PATH = "reports/pipeline_log.csv"   # counts only, no personal data, safe for Git

src = sorted(glob.glob("data/clean/forum_clean_*.csv"))[-1]
with open(src, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

con = sqlite3.connect(DB_PATH)
con.execute("PRAGMA foreign_keys = ON")
with open("db/schema.sql", encoding="utf-8") as f:
    con.executescript(f.read())          # make sure the tables exist

inserted = 0
for r in rows:
    cur = con.execute(
        """INSERT OR IGNORE INTO leads
           (name, phone, location, location_source, title, question,
            posted_date, thread_url, source_url, scraped_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            r["poster_name"] or "Valued Prospect",
            r["phone"] or None,              # empty text -> real NULL, we never invent a phone
            r["location"] or None,
            r["location_source"] or None,
            r["title"],
            r["question"],
            r["posted_date"] or None,
            r["thread_url"],
            r["source_url"] or None,
            r["scraped_at"] or None,
        ),
    )
    inserted += cur.rowcount                 # 1 if added, 0 if thread_url already existed
con.commit()
total = con.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
con.close()

skipped = len(rows) - inserted
os.makedirs("reports", exist_ok=True)
new_file = not os.path.exists(LOG_PATH)
with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new_file:
        w.writerow(["run_at", "source_file", "rows_read", "inserted", "skipped_already_in_db", "total_in_db"])
    w.writerow([datetime.now().isoformat(timespec="seconds"), os.path.basename(src),
                len(rows), inserted, skipped, total])

print("Source file:", os.path.basename(src))
print("Rows read:", len(rows))
print("Inserted:", inserted)
print("Skipped (already in DB):", skipped)
print("Total leads in DB:", total)