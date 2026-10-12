# Scope & Architecture Memo - Day 1

- **Candidate:** Shubham Khandare | **Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** 1 | **Prepared:** 13/10/2026 (submitted after the 7:00 PM IST cutoff)
- **Target micro-markets:** Hadapsar and Fursungi belt, Pune

## 1. Objective

Find publicly visible buyer-intent signals for the target micro-markets, clean and
store them, score them, and export a Top 100 clean prospect sheet by Day 7, using
only open-source tools and compliant scraping.

## 2. Compliance framework

| Rule | How it is enforced |
|---|---|
| Respect robots.txt | Checked per source before scraping (scripts/check_robots.py, results in logs/robots_audit.csv) |
| Rate limit 1.5-3.0 s | Random jitter delay between every request; honour Crawl-delay if larger |
| Public, non-authenticated only | No logins, no CAPTCHA bypass, no private groups |
| No paid APIs or lead databases | Python, Pandas, BeautifulSoup, Playwright, SQLite only |
| No hardcoded secrets | Settings in .env (git-ignored); .env.example committed |
| No fabricated data | Only values seen on the public page are stored, each with source URL; missing values stay empty (NULL) |
| No IP bans | Descriptive User-Agent, stop on repeated 429/403 |
| DPDP Act 2023 awareness | Minimum fields only; raw data and database never committed to Git |

## 3. Source mapping

Checks were done on 13/10/2026.

| # | Source | Purpose | robots.txt | Terms of Use | Decision |
|---|---|---|---|---|---|
| 1 | CommonFloor Hadapsar forum (www.commonfloor.com/forum/a4321-hadapsar-pune) | Buyer-intent signals (public questions) | User-agent * does not disallow /forum/. Search and listing paths are disallowed | Keyword check (scrap, crawl, automated, bot): no restriction found | Provisional: use for intent signals |
| 2 | CityAir (cityair.in) - MahaRERA project pages for Hadapsar and Fursungi | Location and project context for scoring | Allow: / (no Disallow, no Crawl-delay) | Keyword check pending | Provisional: context data only |
| 3 | MahaRERA public portal (official) | Verified project registrations | Not yet checked | Not yet checked | Pending |
| 4 | Housing.com project pages | Listings | Many paths blocked (search, community, review) | Not read; contacts shown are sellers/agents, not buyers | Not used |

Paths never requested on CommonFloor: /search, /property-search, /project-search,
/for_sale, /for_rent, /location-listing/, /property-listing-public/, /authorize/
and any page behind a login.

## 4. Definition of a buyer-intent signal

A public forum post in which a person asks about buying a flat or house in Hadapsar
or Fursungi (for example BHK type, budget, project name or timeline).

## 5. Architecture

    Public source -> polite request (robots check + jitter + retry)
        -> scraper -> data/raw (JSON/CSV)
        -> cleaner (name cleanup, location normalisation, phone regex if present, dedupe)
        -> SQLite (leads, feedback)
        -> scoring (Location 40 + Intent 35 + Recency 25)
        -> Top 100 export (data/clean)

## 6. Planned lead fields

name (as publicly posted, title-cased, default "Valued Prospect"), phone (empty if not public),
location, intent_text, intent_level, source_url, source_name, posted_at, scraped_at, score (0-100).

## 7. Known limitation and open question

The CommonFloor forum posts show a name and a question but no phone number. Phone numbers
will not be guessed, inferred or fabricated; the field stays empty. Open question for the
technical desk (with a screenshot as proof): is a phone number mandatory for the final
Top 100 sheet, and what are the remaining schema columns?

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Not enough intent posts for 100 leads | Add more public sources after checking them; track the count in every DPR |
| Source blocks the scraper | Stop on repeated 403/429; do not retry aggressively |
| Terms change or are unclear | Re-check before each run; drop the source if scraping is banned |
| Personal data in public posts | Keep only needed fields; never commit raw data |
| Duplicates | Dedupe on name + location + intent text; log every drop |

## 9. Plan

See the roadmap table in README.md.
