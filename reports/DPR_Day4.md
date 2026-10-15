# CANDIDATE DAILY PROGRESS REPORT (DPR)
- **Candidate Name:** Shubham Khandare | **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 4 | **Date:** 15/10/2026 | **Git Commit Hash:** a90bc3b

## 1. Daily Engineering Tasks Completed
- [+] Wrote `db/schema.sql` (DDL): `leads` and `feedback` tables with constraints: thread_url UNIQUE, phone must be NULL or exactly 10 digits, score NULL or 0-100, feedback.lead_id FOREIGN KEY to leads, index on location.
- [+] Wrote `scripts/init_db.py`: builds `db/leads.db` from the schema; safe to run repeatedly (CREATE TABLE IF NOT EXISTS).
- [+] Wrote `scripts/load_leads.py`: reads the newest cleaned CSV and loads it with INSERT OR IGNORE using parameterised SQL; empty phone is stored as NULL (no contact data is invented).
- [+] Automated pipeline log: each load run appends one line to `reports/pipeline_log.csv` (rows read, inserted, skipped, total in DB). Counts only, no personal data.
- [+] Verified constraints and idempotency: first run inserted 9 rows; second run inserted 0 and skipped 9.

## 2. Technical Stack Utilized
Python, SQLite (sqlite3), SQL DDL, csv, Git.

## 3. Compliance & Scraping Throttling Audit
- **Target URL / Directory:** No new scraping on Day 4. Loaded the Day 3 cleaned data (source: CommonFloor Hadapsar forum page, public, non-authenticated).
- **Robots.txt Adherence:** Checked on Day 2 for that page; no new requests today.
- **Rate Limiting:** Not applicable today (zero requests, zero HTTP 429/403).
- **Privacy:** `db/leads.db` and the cleaned CSV hold real poster names and are git-ignored. Only code and the counts-only log are committed.

## 4. Pipeline Operational Metrics
- Raw Ingestion Count: 10 records (Day 2) | Records Dropped (Invalid/Junk): 0
- Duplicate Count Removed: 1 (Day 3 dedupe log) + 9 re-load attempts skipped by the UNIQUE rule in the idempotency test
- Loaded into database: 9 leads (Hadapsar 6, Handewadi 1, Magarpatta 1, Ramtekdi 1); phones filled: 0; feedback rows: 0
- Cumulative Clean Prospects Stored: 9 / 100. These 9 are cleaned and stored but not yet intent-filtered or scored (Day 5).

## 5. Technical Challenges & Proof of Concept (PoC) Solutions
- Blocker 1: First run of `init_db.py` failed with `sqlite3.OperationalError: near "CEEATE": syntax error`. Cause: a typo in `schema.sql`. Resolution: corrected to `CREATE`; the script then reported tables `['feedback', 'leads']`.
- Blocker 2: Re-running a loader must not create duplicates. Resolution: UNIQUE on `thread_url` plus INSERT OR IGNORE; re-run inserted 0 and skipped 9.
- Data limitation (unchanged): the public source has no phone numbers and its posts are old (2016-2019), so the cumulative count stays far below 100 and recency scoring will be low. Reported as it is; nothing fabricated.

## 6. Attached Deliverables
- `db/schema.sql`
- `scripts/init_db.py`
- `scripts/load_leads.py`
- `reports/pipeline_log.csv`