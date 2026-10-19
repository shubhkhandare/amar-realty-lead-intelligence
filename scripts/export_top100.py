"""Day 7 final export."""
import csv
import os
import sqlite3
from datetime import date

from cleaner import mask_name
from score_leads import data_quality_flags, parse_date, score_lead

TOP_N = 100
SOURCE_NAME = "CommonFloor forum"
# Posts that are not purchase prospects are left out, and every exclusion is logged.
EXCLUDE_LEVELS = {
    "seller_or_ad": "builder or seller advertisement, not a prospect",
    "rental": "rental topic, not a purchase prospect",
}
COLUMNS = ["rank", "name", "phone", "location", "score", "intent_level",
           "posted_date", "source_name", "source_url", "data_quality_flags"]

today = date.today()
con = sqlite3.connect("db/leads.db")
con.row_factory = sqlite3.Row
leads = [dict(r) for r in con.execute("SELECT * FROM leads")]
con.close()

eligible, excluded = [], []
for lead in leads:
    lead.update(score_lead(lead, today))
    lead.update(data_quality_flags(lead))
    reason = EXCLUDE_LEVELS.get(lead["intent_level"])
    if reason:
        excluded.append({"lead_id": lead["lead_id"], "intent_level": lead["intent_level"],
                         "score": lead["score"], "reason": reason})
    else:
        eligible.append(lead)

eligible.sort(key=lambda r: (-r["score"], -(parse_date(r["posted_date"]) or date.min).toordinal()))
top = eligible[:TOP_N]
for rank, lead in enumerate(top, start=1):
    phone = (lead.get("phone") or "").strip()
    lead["rank"] = rank
    lead["phone"] = phone if (phone.isdigit() and len(phone) == 10) else ""   # real phone only, else empty
    lead["source_name"] = SOURCE_NAME
    lead["source_url"] = lead["thread_url"]


def write_csv(path, fieldnames, rows, encoding="utf-8"):
    with open(path, "w", newline="", encoding=encoding) as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


os.makedirs("data/clean", exist_ok=True)
os.makedirs("data/samples", exist_ok=True)
os.makedirs("reports", exist_ok=True)
full_path = f"data/clean/top100_{today.isoformat()}.csv"
write_csv(full_path, COLUMNS, top, encoding="utf-8-sig")                          # real names: send by email, never commit
write_csv("data/samples/top100_masked.csv", COLUMNS,
          [dict(r, name=mask_name(r["name"])) for r in top])                       # masked copy for the repo
write_csv("reports/export_exclusions.csv", ["lead_id", "intent_level", "score", "reason"], excluded)

print("Leads in database:", len(leads))
print("Excluded (not prospects):", len(excluded))
print("Exported:", len(top), "(target was up to", TOP_N, ")")
print("Exported with a phone number:", sum(1 for r in top if r["phone"]))
print("Score range:", min(r["score"] for r in top), "-", max(r["score"] for r in top))
print("Full file (email, do NOT commit):", full_path)
print("Masked file (repo): data/samples/top100_masked.csv")