# CANDIDATE DAILY PROGRESS REPORT (DPR)
- **Candidate Name:** Shubham Khandare | **Target Role:** Lead Intelligence & Data Engineer
- **Evaluation Day:** Day 6 | **Date:** 17/10/2026 | **Git Commit Hash:** Pending

## 1. Daily Engineering Tasks Completed
- [+] Created `scripts/pilot_export.py` to select and rank the top 20 leads (9 available in the database) and export a masked pilot dataset to `data/samples/pilot_batch_masked.csv`.
- [+] Created `data/samples/self_review_tags.csv` containing human-reviewed pilot labels with `lead_id`, `tag`, and `note` fields.
- [+] Reviewed 9 leads using five categories: `genuine_buyer`, `enquiry_only`, `not_a_buyer`, `rental_only`, and `off_topic`.
- [+] Stored the reviewed labels in the SQLite `feedback` table, mapping CSV fields to `sales_tag` and `notes`.
- [+] Detected and removed duplicate feedback entries: 18 rows reduced to 9, with no leads having multiple feedback rows.
- [+] Created `scripts/validate_feedback.py` to compare rule-based intent predictions against the self-review labels.
- [+] Achieved 7/9 agreement (77.8%) on the reviewed pilot. Mismatches were identified for Lead 2 (rental vs. off-topic) and Lead 3 (genuine buyer vs. enquiry only).
- [+] Added data-quality flags in `scripts/score_leads.py` for missing post text and missing phone/contact information.
- [+] Verified date parsing for all 9 stored posts, including ordinal dates such as "28th July 2019".
- [+] Confirmed that all 9 posts receive zero recency points because their dates are older than the configured 730-day window.

## 2. Technical Stack Utilized
Python, SQLite (`sqlite3`), CSV, regex (`re`), `datetime`, PowerShell, Git.

## 3. Compliance & Scraping Throttling Audit
- **Target URL / Directory:** No new scraping was performed during Day 6. The work used the 9 leads already stored in `db/leads.db`.
- **Robots.txt Adherence:** No new requests were made during this validation work; the earlier robots.txt check remains the recorded compliance evidence.
- **Rate Limiting:** Not applicable during Day 6 validation because no new HTTP requests were made.
- **Privacy:** The pilot export masks poster names. The validation report `reports/pilot_validation.csv` contains lead IDs, predictions, labels, and scoring information, with no names or phone numbers.
- **Feedback Provenance:** The labels are self-review labels drafted with AI assistance, not confirmed sales-team feedback.

## 4. Pipeline Operational Metrics
- **Stored Leads Reviewed:** 9.
- **Feedback Rows Before Cleanup:** 18.
- **Duplicate Feedback Rows Removed:** 9.
- **Feedback Rows After Cleanup:** 9, with one row per lead.
- **Rule-Review Agreement:** 7/9 (77.8%) on this small pilot.
- **Mismatches:** 2 — Lead 2 and Lead 3.
- **Top 3 by Rule Score:** 2 of the top 3 leads were labelled `genuine_buyer` in the self-review.
- **Missing Post Text:** 1 record (Lead 6).
- **Phone/Contact Quality Flag:** All 9 records were flagged as missing phone information by the current check. The actual database contact-field schema still requires verification before confirming that no contact details exist.
- **Recency Points:** 0 for all 9 records; all post dates are from 2016–2019 and exceed the 730-day cutoff.
- **Score Range:** 25–75 in the current dataset.

## 5. Technical Challenges & Proof of Concept (PoC) Solutions
- **Challenge 1: Duplicate feedback records inflated validation counts.** The validation output initially showed 18 rows because each lead appeared twice. Resolution: created `scripts/dedupe_feedback.py`, removed 9 duplicate rows, and reran validation. The corrected output showed 9 unique leads and 7/9 agreement.
- **Challenge 2: Rule-based intent classification disagreed with manual review.** Lead 2 was classified as rental while the review label was off-topic. Lead 3 was classified as a genuine buyer while the review label was enquiry-only. Resolution: documented both mismatches for further review rather than changing the rules to fit only two examples.
- **Challenge 3: Missing source information could produce misleading classifications.** Lead 6 has no post text, but the title triggers the enquiry rule. Resolution: added a `text_missing` quality flag so missing text can be identified separately from the score.
- **Challenge 4: Date parsing and recency needed verification.** All nine dates parsed correctly. The zero recency scores were expected because the posts are older than 730 days; no date-parsing fix was required.
- **Limitation:** The validation sample contains only 9 leads. The 77.8% agreement is a pilot result, not a reliable estimate of production accuracy. The self-review labels are not independent sales feedback, and the phone/contact-column mapping remains to be verified.

## 6. Attached Deliverables
- `scripts/pilot_export.py`
- `scripts/validate_feedback.py`
- `scripts/dedupe_feedback.py`
- `scripts/fix_feedback_notes.py`
- `scripts/score_leads.py` (updated with data-quality flags)
- `data/samples/pilot_batch_masked.csv`
- `data/samples/self_review_tags.csv`
- `reports/pilot_validation.csv`

## 7. Pending Tasks
- [ ] Verify the actual phone/contact column names in the `leads` table.
- [ ] Confirm that self-review notes are clearly labelled in the database.
- [ ] Run the relevant scoring tests after the quality-flag changes.
- [ ] Review the final Git status and ensure private data files are not staged.
- [ ] Commit and push the verified Day 6 deliverables.
