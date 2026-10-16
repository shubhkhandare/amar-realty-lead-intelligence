# CANDIDATE DAILY PROGRESS REPORT (DPR)
- **Candidate Name:** Shubham Khandare | **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 5 | **Date:** 16/10/2026 | **Git Commit Hash:** 146d933

## 1. Daily Engineering Tasks Completed
- [+] Wrote `scripts/score_leads.py`: score = Location (40) + Intent (35) + Recency (25), integer 0-100. Writes the score back to `leads.score` in SQLite and produces a ranked dataset.
- [+] Location rule: Hadapsar/Fursungi named in the post = 40; same areas but only from the forum page = 30; nearby Handewadi/Magarpatta/Ramtekdi = 25; otherwise 0.
- [+] Intent rule (keyword-based, on title + question): seller/ad = 0, rental = 5, explicit buy = 35, enquiry = 20, generic = 5.
- [+] Recency rule: 25 for a post from today, falling linearly to 0 at 730 days; missing or unreadable date = 0. Handles dates like "28th July 2019".
- [+] Wrote `tests/test_scoring.py`: 19 checks for location, intent, date parsing and recency; all 19 pass.
- [+] Exported the ranked dataset: full file stays local (git-ignored); masked sample committed as `data/samples/leads_scored_masked.csv`.

## 2. Technical Stack Utilized
Python, SQLite (sqlite3), regex (re), csv, datetime, Git.

## 3. Compliance & Scraping Throttling Audit
- **Target URL / Directory:** No new scraping on Day 5. Scored the 9 leads already stored in `db/leads.db` (source: CommonFloor Hadapsar forum page, public, non-authenticated).
- **Robots.txt Adherence:** Checked on Day 2 for that page; no new requests today.
- **Rate Limiting:** Not applicable today (zero requests, zero HTTP 429/403).
- **Privacy:** The committed ranked sample shows masked poster names only (first letter + ***). The full ranked file and the database are git-ignored.

## 4. Pipeline Operational Metrics
- Raw Ingestion Count: 10 records (Day 2) | Records Dropped (Invalid/Junk): 0
- Duplicate Count Removed: 1 (Day 3)
- Scored today: 9 leads. Intent mix: explicit buy 3, enquiry 4, rental 1, seller/ad 1. Highest score 75, lowest 25.
- Recency points: 0 for all 9, because every post is from 2016-2019 (older than the 730-day window). The maximum possible score for this source is therefore 75, not 100.
- Cumulative Clean Prospects Stored: 9 / 100 (scored, in database). The source has no phone numbers, so none of these 9 has a contact number.

## 5. Technical Challenges & Proof of Concept (PoC) Solutions
- Challenge 1: Keyword rules misjudge posts. I checked the real post text of the leads against the rules and found two errors. (a) A genuine buyer ("wise to invest in a flat ... ready flats available") was marked as a seller ad because of the word "available". Fix: removed generic words like "available" and "offer" from the seller list and added a regression test. (b) After accepting "invest" as a buying word, a builder promotion ("Invest your money in right property") scored as a buyer. Fix: "invest" now counts only in buyer phrases such as "wise to invest" / "want to invest"; builder phrases ("discover", "invest your") mark an ad. The seller check runs before the buyer check, so a post with both kinds of words is treated as an ad.
- Challenge 2: Edits that were not saved before running tests produced stale results. Resolution: checked the file on disk with Select-String and re-ran the tests until the results matched.
- Challenge 3: The first `git push` failed with "Could not resolve host: github.com" (no internet). Resolution: retried after the connection returned; the push succeeded (8f6f286..146d933).
- Limitation (reported, not hidden): the intent rules are heuristic keyword matching, checked by hand on only 9 leads, so they may be wrong on new data. The source data is old and has no phone numbers, so the Top 100 target cannot be reached from this source alone.

## 6. Attached Deliverables
- `scripts/score_leads.py`
- `tests/test_scoring.py`
- `data/samples/leads_scored_masked.csv`