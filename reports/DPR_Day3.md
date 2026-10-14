# CANDIDATE DAILY PROGRESS REPORT (DPR)
- **Candidate Name:** Shubham Khandare | **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 3 | **Date:** 14/10/2026 | **Git Commit Hash:** b62b136

## 1. Daily Engineering Tasks Completed
- [+] Wrote `scripts/cleaner.py`: Indian mobile regex cleaner (strips +91 / 91 / leading 0, accepts only 10 digits starting 6-9, otherwise returns None), name cleaner (title case, default "Valued Prospect"), location normaliser (Fursungi, Handewadi, Ramtekdi, Magarpatta, Hadapsar; specific areas matched before general), phone finder for free text, name masker.
- [+] Wrote `tests/test_cleaner.py`: 25 test cases, 25 passed, 0 failed (phone, name, location).
- [+] Wrote `scripts/clean_forum.py` (Pandas): drops junk rows, cleans names and locations, finds phones typed in post text, removes duplicates (same poster + title + question), writes a dedupe log.
- [+] Added masked outputs for Git: `data/samples/forum_clean_sample_masked.csv` and `data/samples/dedupe_log_masked.csv`. Full cleaned file stays local and git-ignored.

## 2. Technical Stack Utilized
Python, Pandas, re (regex), csv, Git.

## 3. Compliance & Scraping Throttling Audit
- **Target URL / Directory:** No new scraping on Day 3. Cleaned the Day 2 raw file from the CommonFloor Hadapsar forum page (public, non-authenticated).
- **Robots.txt Adherence:** Checked on Day 2 for that page; no new requests today.
- **Rate Limiting:** Not applicable today (zero requests, zero HTTP 429/403).
- **Privacy:** Raw and cleaned files with real poster names are not committed. Committed samples show masked names (first letter + ***).

## 4. Pipeline Operational Metrics
- Raw Ingestion Count: 10 records | Records Dropped (Invalid/Junk): 0
- Duplicate Count Removed: 1 (logged in `data/samples/dedupe_log_masked.csv`)
- Phone numbers found in post text: 0
- Cleaned records: 9 (Hadapsar 6, Handewadi 1, Ramtekdi 1, Magarpatta 1)
- Cumulative Clean Prospects Stored: 0 / 100 (database load is Day 4). 9 records are cleaned but not yet intent-filtered; some are not buyers (for example a builder advertisement and a rental-rules post).

## 5. Technical Challenges & Proof of Concept (PoC) Solutions
- Blocker 1: The source has no phone numbers, so the phone cleaner cannot be tested on real data. Resolution: verified it on made-up test strings kept in `tests/` (valid, +91, leading 0, spaces/dashes, too short, wrong start digit, toll-free style). No contact data was invented for the dataset. Phone is left empty where the source has none.
- Blocker 2: 4 of 9 posts do not mention an area in their text. Resolution: they are labelled Hadapsar because they came from the Hadapsar forum page, and the `location_source` column records `forum_page` instead of `text`, so the origin is visible.
- Blocker 3: Pandas first failed to load on my machine (numpy DLL blocked by Windows Application Control). Resolution: reinstalled numpy and pandas in the virtual environment; both load and the pipeline runs.
- Data quality note: the forum posts are old (2016-2019 era), so recency scoring on Day 5 will be low. Reported honestly, not hidden.

## 6. Attached Deliverables
- `scripts/cleaner.py`
- `scripts/clean_forum.py`
- `tests/test_cleaner.py`
- `data/samples/forum_clean_sample_masked.csv`
- `data/samples/dedupe_log_masked.csv`