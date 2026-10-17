"""Day 6 step 3: compare what the scoring rules said with what the human review said."""
import csv
import os
import sqlite3
from collections import Counter
from datetime import date

from score_leads import score_lead

# Rule level -> the human tag it should agree with.
TAG_MAP = {"explicit_buy": "genuine_buyer", "enquiry": "enquiry_only",
           "rental": "rental_only", "seller_or_ad": "not_a_buyer", "generic": "off_topic"}
# Intent points the rules would give if the human tag were right.
HUMAN_INTENT_POINTS = {"genuine_buyer": 35, "enquiry_only": 20, "rental_only": 5,
                       "off_topic": 5, "not_a_buyer": 0}

con = sqlite3.connect("db/leads.db")
con.row_factory = sqlite3.Row
rows = [dict(r) for r in con.execute(
    "SELECT l.*, f.sales_tag FROM leads l JOIN feedback f ON f.lead_id = l.lead_id ORDER BY l.lead_id")]
con.close()

today = date.today()
results = []
for r in rows:
    s = score_lead(r, today)
    predicted = TAG_MAP[s["intent_level"]]
    human = (r["sales_tag"] or "").removeprefix("self_")
    results.append({
        "lead_id": r["lead_id"], "rule_level": s["intent_level"], "rule_tag": predicted,
        "human_tag": human, "match": predicted == human, "rule_score": s["score"],
        "intent_pts_rule": s["intent_pts"], "intent_pts_human": HUMAN_INTENT_POINTS[human],
        "text_missing": not (r["question"] or "").strip(),
    })

print("lead | rule level   | rule tag       | human tag      | match | score | intent pts (rule -> human)")
for x in results:
    print(f'{x["lead_id"]:>4} | {x["rule_level"]:<12} | {x["rule_tag"]:<14} | {x["human_tag"]:<14} | '
          f'{"YES" if x["match"] else "NO ":<5} | {x["rule_score"]:>5} | '
          f'{x["intent_pts_rule"]:>3} -> {x["intent_pts_human"]:<3}'
          f'{"   (post text missing)" if x["text_missing"] else ""}')

hits = sum(x["match"] for x in results)
print(f"\nAgreement: {hits}/{len(results)} = {100 * hits / len(results):.1f}%  (pilot of {len(results)} leads only)")

by_score = sorted(results, key=lambda x: -x["rule_score"])[:3]
top_ok = sum(x["human_tag"] == "genuine_buyer" for x in by_score)
print(f"Top 3 by score that the review calls genuine_buyer: {top_ok}/3")

print("\nHuman tag counts:", dict(Counter(x["human_tag"] for x in results)))
print("Mismatches:")
for x in results:
    if not x["match"]:
        print(f'  lead {x["lead_id"]}: rule said {x["rule_tag"]}, review said {x["human_tag"]}, '
              f'intent points {x["intent_pts_rule"]} vs {x["intent_pts_human"]}')

os.makedirs("reports", exist_ok=True)
with open("reports/pilot_validation.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    w.writerows(results)
print("\nWrote reports/pilot_validation.csv (no names, no phones)")