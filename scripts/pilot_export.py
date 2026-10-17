"""Day 6  build the pilot batch and an empty self-review sheet."""
import csv
import os
import sqlite3
from datetime import date

from cleaner import mask_name
from score_leads import parse_date, score_lead

PILOT_SIZE = 20                                   # a pilot is a small test batch
REVIEW_FILE = "data/samples/self_review_tags.csv"
PILOT_FILE = "data/samples/pilot_batch_masked.csv"

con = sqlite3.connect("db/leads.db")
con.row_factory = sqlite3.Row
leads = [dict(r) for r in con.execute("SELECT * FROM leads")]
con.close()

today = date.today()
for lead in leads:
    lead.update(score_lead(lead, today))          # adds score + intent_level + points
leads.sort(key=lambda r: (-r["score"], -(parse_date(r["posted_date"]) or date.min).toordinal()))
pilot = leads[:PILOT_SIZE]
for rank, lead in enumerate(pilot, start=1):
    lead["rank"] = rank

os.makedirs("data/samples", exist_ok=True)
columns = ["rank", "lead_id", "name", "location", "intent_level", "score",
           "posted_date", "title", "thread_url"]
with open(PILOT_FILE, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
    w.writeheader()
    w.writerows([dict(r, name=mask_name(r["name"])) for r in pilot])

# Empty review sheet: we fill the 'tag' column by hand. Never overwrite our own work.
if not os.path.exists(REVIEW_FILE):
    with open(REVIEW_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lead_id", "tag", "note"])
        for r in pilot:
            w.writerow([r["lead_id"], "", ""])
    print("Created empty review sheet:", REVIEW_FILE)
else:
    print("Review sheet already exists, left untouched:", REVIEW_FILE)

print("Pilot batch size:", len(pilot), "->", PILOT_FILE)
print()
print("Read each post, then tag it in", REVIEW_FILE)
print("-" * 70)
for r in pilot:
    text = " ".join((r["question"] or "").split())[:260]
    print(f'lead {r["lead_id"]} | rank {r["rank"]} | rule says: {r["intent_level"]} | score {r["score"]}')
    print("  TITLE:", r["title"])
    print("  TEXT :", text)
    print()