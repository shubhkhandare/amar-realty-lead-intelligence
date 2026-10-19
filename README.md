# Amar Realty - Lead Intelligence & Data Engineering (7-Day Evaluation)

Open-source pipeline that finds public buyer-intent signals for the Pune
micro-markets **Hadapsar** and **Fursungi**, cleans and stores them, scores
them, and exports a ranked prospect sheet.

## Final result (honest summary)

| Item | Value |
|---|---|
| Source used | CommonFloor public forum (robots.txt checked) |
| Posts collected | 9 (all dated 2016-2019) |
| Excluded from export | 2 (1 builder advertisement, 1 rental topic) |
| Prospects exported | 7 (the brief asks for up to 100) |
| Prospects with a phone number | 0 (no public phone numbers were found; none were invented) |
| Score range | 45 to 75 (Recency is 0 for every post because all are old) |

The 100-prospect target was **not** reached. This one public source does not
contain enough recent, relevant posts. More public sources would be needed.

## Compliance rules this repo follows

- Open-source stack only (Python, requests, BeautifulSoup, Pandas, SQLite). No paid APIs or lead databases.
- robots.txt is checked before scraping.
- 1.5-3.0 s random delay between requests; descriptive User-Agent; back off on HTTP 429/403.
- Public, non-authenticated pages only. No login walls, no bypassing blocks.
- No secrets in code. No fabricated contact data: a missing phone stays empty.
- Raw data, cleaned data and the database are git-ignored. Only masked samples (names shown as `A***`) and counts-only logs are committed.

## Pipeline

    check_robots.py -> scrape_commonfloor_forum.py (+ parse_forum.py)   Extract
    clean_forum.py (+ cleaner.py)                                       Transform
    init_db.py -> load_leads.py                                         Load (SQLite)
    score_leads.py                                                      Score
    export_top100.py                                                    Export

## Scoring (0-100, every score is explainable)

| Part | Max | Rule |
|---|---|---|
| Location | 40 | 40 if Hadapsar/Fursungi is named in the post, 30 if only the forum page says so, 25 for nearby areas (Handewadi, Magarpatta, Ramtekdi) |
| Intent | 35 | explicit buy 35, enquiry 20, generic 5, rental 5, builder/seller ad 0 |
| Recency | 25 | falls linearly to 0 at 730 days |

Intent uses keyword/regex rules checked in a fixed order. The rules were
tested on a small self-review of the 9 posts (7 of 9 agreed). This is a
self-review, not sales feedback.

## Export rules

- Builder advertisements and rental-only posts are not purchase prospects, so they are left out. Each exclusion is logged by lead id in `reports/export_exclusions.csv`.
- Columns: rank, name, phone, location, score, intent_level, posted_date, source_name, source_url, data_quality_flags.
- The file with real names stays local and goes only by email. The repo has the masked copy `data/samples/top100_masked.csv`.

## How to run (Windows PowerShell)

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

    python scripts\check_robots.py
    python scripts\scrape_commonfloor_forum.py
    python scripts\clean_forum.py
    python scripts\init_db.py
    python scripts\load_leads.py
    python scripts\score_leads.py
    python scripts\export_top100.py

    python tests\test_cleaner.py
    python tests\test_scoring.py

## Repository layout

    scripts/   pipeline scripts, one job per file
    tests/     unit tests (cleaner, scoring)
    db/        schema.sql (the database file is git-ignored)
    data/      raw and clean are git-ignored; samples/ has masked files
    reports/   daily progress reports (DPR_Day1 to Day7), logs, audit notes
    docs/      scope and architecture memo

## Known limits

- Only 9 posts, all 2016-2019, so Recency is 0 and the top score is 75.
- No phone numbers are public on the source, so exports have an empty phone.
- Intent is keyword-based and can misread tone; a human should review before outreach.
- Scoring was checked against a self-review, not against real sales outcomes.