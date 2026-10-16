"""Day 5 scoring: Location (40) + Intent (35) + Recency (25) = 0..100."""
import csv
import os
import re
import sqlite3
from datetime import date, datetime

from cleaner import mask_name

TARGET_AREAS = {"Hadapsar", "Fursungi"}                       # the areas Amar Realty cares about
NEARBY_AREAS = {"Handewadi", "Magarpatta", "Ramtekdi"}        # neighbouring micro-markets
RECENCY_ZERO_AFTER_DAYS = 730                                 # a post older than 2 years gets 0

# Intent rules. The first group that matches decides the level.
SELLER_WORDS = [r"for sale", r"book now", r"pre-?launch", r"newly launched", r"starting (at|from)",
                r"\bdiscover\b", r"invest your"]
RENT_WORDS = [r"\brent\b", r"\brental\b", r"\bleave and license\b"]
BUY_WORDS = [r"\bbuy(ing)?\b", r"\bpurchase\b", r"looking for", r"want to (buy|purchase)",
             r"interested in", r"planning to", r"(wise|good|better|safe) to invest",
             r"(want|wish|plan|planning|looking|thinking)( to)? invest"]
ENQUIRY_WORDS = [r"contact", r"price", r"\bcost\b", r"details", r"review", r"suggest", r"\?"]


def location_points(location, source):
    if location in TARGET_AREAS:
        return 40 if source == "text" else 30      # area named in the post > only on the forum page
    if location in NEARBY_AREAS:
        return 25
    return 0


def _any(patterns, text):
    return any(re.search(p, text) for p in patterns)


def intent_level_and_points(title, question):
    text = f"{title or ''} {question or ''}".lower()
    if _any(SELLER_WORDS, text):
        return "seller_or_ad", 0
    if _any(RENT_WORDS, text):
        return "rental", 5
    if _any(BUY_WORDS, text):
        return "explicit_buy", 35
    if _any(ENQUIRY_WORDS, text):
        return "enquiry", 20
    return "generic", 5


def parse_date(text):
    cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", (text or "").strip())
    for fmt in ("%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            pass
    return None


def recency_points(posted, today):
    if posted is None:
        return 0
    age_days = max(0, (today - posted).days)
    return round(max(0, 25 * (1 - age_days / RECENCY_ZERO_AFTER_DAYS)))


def score_lead(row, today):
    loc = location_points(row["location"], row["location_source"])
    level, intent = intent_level_and_points(row["title"], row["question"])
    rec = recency_points(parse_date(row["posted_date"]), today)
    return {"intent_level": level, "location_pts": loc, "intent_pts": intent,
            "recency_pts": rec, "score": min(100, loc + intent + rec)}


def main():
    today = date.today()
    con = sqlite3.connect("db/leads.db")
    con.row_factory = sqlite3.Row
    leads = [dict(r) for r in con.execute("SELECT * FROM leads")]

    for lead in leads:
        lead.update(score_lead(lead, today))
        con.execute("UPDATE leads SET score = ? WHERE lead_id = ?", (lead["score"], lead["lead_id"]))
    con.commit()
    con.close()

    leads.sort(key=lambda r: (-r["score"], -(parse_date(r["posted_date"]) or date.min).toordinal()))
    for rank, lead in enumerate(leads, start=1):
        lead["rank"] = rank

    columns = ["rank", "lead_id", "name", "location", "intent_level", "location_pts",
               "intent_pts", "recency_pts", "score", "posted_date", "title", "thread_url"]
    os.makedirs("data/clean", exist_ok=True)
    os.makedirs("data/samples", exist_ok=True)

    def write(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

    write(f"data/clean/leads_scored_{today.isoformat()}.csv", leads)          # full, local only
    write("data/samples/leads_scored_masked.csv",
          [dict(r, name=mask_name(r["name"])) for r in leads])               # masked, safe for Git

    print("Scored leads:", len(leads))
    print("rank | loc | intent | recent | SCORE | intent_level | location | title")
    for r in leads:
        print(f'{r["rank"]:>4} | {r["location_pts"]:>3} | {r["intent_pts"]:>6} | {r["recency_pts"]:>6} | '
              f'{r["score"]:>5} | {r["intent_level"]:<12} | {r["location"]:<10} | {r["title"][:40]}')


if __name__ == "__main__":
    main()