"""Day 6 step 2: load self-review tags into the feedback table and compare them with the rule's guess.
NOTE: these tags come from our own manual review, NOT from the sales team."""
import csv
import os
import sqlite3
from collections import Counter
from datetime import date

from score_leads import score_lead

REVIEW_FILE = "data/samples/self_review_tags.csv"
SUMMARY_FILE = "reports/pilot_feedback_summary.md"
ALLOWED = {"genuine_buyer", "enquiry_only", "not_a_buyer", "rental_only", "off_topic"}
# Which rule level counts as "the rule got it right" for each human tag.
EXPECTED_RULE_LEVEL = {
    "genuine_buyer": "explicit_buy",
    "enquiry_only": "enquiry",
    "not_a_buyer": "seller_or_ad",
    "rental_only": "rental",
    "off_topic": "generic",
}
NOTE_PREFIX = "self-review (not sales feedback): "

con = sqlite3.connect("db/leads.db")
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys = ON")
leads = {r["lead_id"]: dict(r) for r in con.execute("SELECT * FROM leads")}

with open(REVIEW_FILE, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

reviewed, skipped = [], []
for r in rows:
    tag = (r["tag"] or "").strip()
    lead_id = int(r["lead_id"])
    if not tag:
        skipped.append((lead_id, "no tag yet"))
    elif tag not in ALLOWED:
        skipped.append((lead_id, f"unknown tag '{tag}'"))
    elif lead_id not in leads:
        skipped.append((lead_id, "lead_id not in database"))
    else:
        reviewed.append((lead_id, tag, (r["note"] or "").strip()))

# Rebuild our self-review rows each run, so running twice never duplicates them.
con.execute("DELETE FROM feedback WHERE notes LIKE ?", (NOTE_PREFIX + "%",))
for lead_id, tag, note in reviewed:
    con.execute("INSERT INTO feedback (lead_id, sales_tag, notes) VALUES (?, ?, ?)",
                (lead_id, "self_" + tag, NOTE_PREFIX + note))
con.commit()

today = date.today()
results = []
for lead_id, tag, note in reviewed:
    level = score_lead(leads[lead_id], today)["intent_level"]
    results.append({"lead_id": lead_id, "human": tag, "rule": level,
                    "agree": level == EXPECTED_RULE_LEVEL[tag], "title": leads[lead_id]["title"]})
con.close()

total = len(results)
agree = sum(r["agree"] for r in results)
rule_buy = [r for r in results if r["rule"] == "explicit_buy"]
real_buy = [r for r in results if r["human"] == "genuine_buyer"]
precision = sum(r["human"] == "genuine_buyer" for r in rule_buy)
recall = sum(r["rule"] == "explicit_buy" for r in real_buy)

print("Reviewed leads loaded into feedback table:", total, "| skipped:", skipped or "none")
print("Human tags:", dict(Counter(r["human"] for r in results)))
print(f"Rule agrees with human on {agree} of {total} leads")
print(f"Rule said explicit_buy for {len(rule_buy)}; truly genuine_buyer: {precision}")
print(f"Human found {len(real_buy)} genuine buyers; rule caught: {recall}")
print("Disagreements:")
for r in results:
    if not r["agree"]:
        print(f'  lead {r["lead_id"]}: rule={r["rule"]}, human={r["human"]} | {r["title"][:60]}')

os.makedirs("reports", exist_ok=True)
with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
    f.write("# Pilot feedback summary (self-review, NOT sales-team feedback)\n\n")
    f.write(f"- Leads reviewed: {total}\n")
    f.write(f"- Human tags: {dict(Counter(r['human'] for r in results))}\n")
    f.write(f"- Rule agrees with human review: {agree} of {total}\n")
    f.write(f"- Rule said explicit_buy for {len(rule_buy)} leads; {precision} were genuine buyers\n")
    f.write(f"- Human found {len(real_buy)} genuine buyers; rule caught {recall}\n")
    f.write("- Disagreements (lead_id: rule vs human): ")
    f.write(", ".join(f"{r['lead_id']}: {r['rule']} vs {r['human']}" for r in results if not r["agree"]) or "none")
    f.write("\n")