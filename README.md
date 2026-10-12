# Amar Realty - Lead Intelligence & Data Engineering (7-Day Evaluation)

Open-source pipeline that discovers public buyer-intent signals for the Pune
micro-markets of **Hadapsar** and **Fursungi**, cleans and stores them, scores
them, and exports a Top 100 prospect sheet.

## Compliance rules this repo follows

- Open-source stack only (Python, Pandas, BeautifulSoup, Playwright, SQLite). No paid APIs or lead databases.
- robots.txt is checked before any source is scraped.
- 1.5-3.0 s random jitter delay between requests; descriptive User-Agent; back off on HTTP 429/403.
- Public, non-authenticated pages only. No login walls, no bypassing blocks.
- No secrets in code (use .env, see .env.example). No fabricated contact data.
- Scraped data, databases and logs are git-ignored (personal data stays out of the repo).

## Repository layout

    scripts/     scrapers, cleaner, loader, scoring (one deliverable per day)
    data/raw/    raw JSON/CSV extracts (contents git-ignored)
    data/clean/  cleaned datasets and final Top 100 export (contents git-ignored)
    db/          SQLite database (git-ignored) and DDL scripts
    docs/        Scope and architecture documents
    reports/     Daily Progress Reports (DPR)
    logs/        run and dedupe logs (git-ignored)
    tests/       unit tests

## Setup (Windows PowerShell)

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    playwright install chromium
    copy .env.example .env

Then edit `.env` with your own values. Never commit `.env`.

## 7-day roadmap

| Day | Focus | Deliverable |
|---|---|---|
| 1 | Scope and Setup | Repo + Scope and Architecture Memo |
| 2 | Web Scraping | Scraper scripts + raw JSON/CSV |
| 3 | Hygiene and Regex | Cleaning module + dedupe logs |
| 4 | Database and ETL | DDL scripts + automated pipeline log |
| 5 | Lead Scoring | Scoring script + ranked dataset |
| 6 | Pilot and Feedback | Pipeline optimization diff + audit report |
| 7 | Final Export | Top 100 clean prospects + repo defense |
