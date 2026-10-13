# CANDIDATE DAILY PROGRESS REPORT (DPR)
- **Candidate Name:** Shubham Khandare | **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 2 | **Date:** 13/10/2026 | **Git Commit Hash:** 894ce71

## 1. Daily Engineering Tasks Completed
- [+] Wrote scripts/fetch_page.py: robots.txt check, 1.5-3.0 s random delay, own User-Agent, stop on HTTP 403/429.
- [+] Wrote scripts/parse_forum.py: parses forum posts (title, question, poster name, date, thread URL) from page HTML.
- [+] Wrote scripts/scrape_commonfloor_forum.py: fetch, parse and save to raw JSON and CSV with a scraped_at timestamp.
- [+] Wrote scripts/make_sample.py: creates a name-masked sample so no personal data is committed to the public repo.
- [+] Reviewed further public sources (see section 5).

## 2. Technical Stack Utilized
Python 3, Requests, BeautifulSoup4 with lxml, urllib.robotparser, csv and json modules, Git, GitHub, VS Code.

## 3. Compliance & Scraping Throttling Audit
- **Target URL / Directory:** CommonFloor Hadapsar forum page (www.commonfloor.com/forum/a4321-hadapsar-pune), public, no login.
- **Robots.txt Adherence:** Confirmed. The script reads robots.txt on every run and stops if the URL is disallowed or robots.txt cannot be read. /forum/ is not disallowed for User-agent *. Search and listing paths are never requested.
- **Terms of Use:** Keyword check (scrap, crawl, automated, bot) found no restriction.
- **Rate Limiting:** Random 1.5-3.0 s delay before the page request. One page per run. From the local machine: 0 HTTP 429 and 0 HTTP 403. See section 5 for one early 403.

## 4. Pipeline Operational Metrics
- Raw Ingestion Count: 10 records (1 page) | Records Dropped (Invalid/Junk): 0 (cleaning starts Day 3)
- Duplicate Count Removed: 0 (1 duplicate pair observed, to be removed Day 3) | Cumulative Clean Prospects Stored: 0 / 100
- Extraction rate: 10 posts from 1 page; 4 requests from the local machine today (2 robots.txt, 2 page).
- Preliminary manual observation: about 4 of 10 posts look like buyer intent; others are rental, vastu, water or a builder advertisement. Not yet validated.

## 5. Technical Challenges & Proof of Concept (PoC) Solutions
- Blocker 1: An early test from Google Colab (a bare request, before the polite scraper existed, no robots check or delay) got HTTP 403. Resolution: stopped immediately, did not retry, did not change headers, did not use a proxy. Moved to my own machine and used the polite scraper, which got HTTP 200.
- Blocker 2: Data quality. The posts date from 2016 to 2019, there is no phone number, and about half are not buyer intent. Resolution: reported honestly in the metrics. Phone numbers are never guessed or fabricated; the field stays empty.
- Other sources reviewed: NoBroker forum (allowed, only 2 relevant posts, no phone), Square Yards (agent pages, not buyers), Quikr and Clickindia (ad pages disallowed in robots.txt), Indian Real Estate Forum (not reachable). None of these were scraped.

## 6. Attached Deliverables
- scripts/fetch_page.py, scripts/parse_forum.py, scripts/scrape_commonfloor_forum.py, scripts/make_sample.py
- data/samples/forum_sample_masked.csv (names masked). Full raw JSON and CSV stay local in data/raw/ and are git-ignored for privacy.
