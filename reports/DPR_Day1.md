# CANDIDATE DAILY PROGRESS REPORT (DPR)
- **Candidate Name:** Shubham Khandare | **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 1 | **Date:** 12/10/2026 (submitted late, 13/10/2026 after 7:00 PM IST cutoff) | **Git Commit Hash:** 2f4d651

## 1. Daily Engineering Tasks Completed
- [+] Created Git repository with structured layout (scripts, data, db, docs, reports, logs, tests).
- [+] Added .gitignore (blocks .env, raw data, databases, logs), .env.example and requirements.txt.
- [+] Expanded README with compliance rules, layout, setup steps and 7-day roadmap.
- [+] Wrote scripts/check_robots.py to verify robots.txt and keep an audit trail.
- [+] Checked robots.txt for candidate sources and mapped them (docs/scope_architecture_memo.md).
- [+] Wrote Scope and Architecture Memo with compliance framework, source mapping, architecture, risks.

## 2. Technical Stack Utilized
Python, Requests, Pandas, BeautifulSoup, Playwright (planned), SQLite (planned), Git, GitHub, VS Code.

## 3. Compliance & Scraping Throttling Audit
- **Target URL / Directory:** CommonFloor Hadapsar forum (www.commonfloor.com/forum/a4321-hadapsar-pune); CityAir MahaRERA project pages (cityair.in). Shortlist is provisional.
- **Robots.txt Adherence:** Verified on 13/10/2026. CommonFloor: User-agent * does not disallow /forum/ (search and listing paths are disallowed and will not be requested). CityAir: Allow /. MahaRERA portal: pending.
- **Terms of Use:** CommonFloor keyword check (scrap, crawl, automated, bot) found no restriction. CityAir and MahaRERA: pending.
- **Rate Limiting:** 1.5-3.0 s random jitter planned. No scraping performed on Day 1 (zero HTTP 429/403 encountered).

## 4. Pipeline Operational Metrics
- Raw Ingestion Count: 0 records | Records Dropped (Invalid/Junk): 0
- Duplicate Count Removed: 0 | Cumulative Clean Prospects Stored: 0 / 100
- Extraction rate: not applicable (no extraction run yet).

## 5. Technical Challenges & Proof of Concept (PoC) Solutions
- Blocker: The CommonFloor forum posts show a name and a question but no phone number.
- Resolution: Phone numbers will not be inferred or fabricated; the field stays empty. A query with a screenshot as PoC will be sent to the technical desk asking whether phone is mandatory and for the full schema.

## 6. Attached Deliverables
- docs/scope_architecture_memo.md
- scripts/check_robots.py
- README.md, .gitignore, .env.example, requirements.txt
