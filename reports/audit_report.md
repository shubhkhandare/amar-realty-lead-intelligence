# Audit Report (Day 6 Pilot)

## 1. Data summary

| Item | Count |
|---|---|
| Raw forum posts | 10 |
| Duplicates removed | 1 |
| Clean leads in database | 9 |
| Leads with a phone number | 0 |
| Leads with missing post text | 1 |
| Date range of posts | 2016 to 2019 |

## 2. Compliance audit

| Rule | Status |
|---|---|
| Open-source tools only | Yes |
| robots.txt checked before scraping | Yes |
| Random delay 1.5 to 3.0 s | Yes |
| Public, non-authenticated pages only | Yes |
| No paid APIs or lead databases | Yes |
| No fabricated contact data | Yes, missing phone stays empty |
| No secrets in code | Yes |
| Raw data, cleaned data and database kept out of Git | Yes |
| Names masked in committed samples | Yes (`A***`) |
| HR or tech desk contacted | No |

## 3. Pilot review

* The pilot reviewed all 9 leads by hand. These tags are a **self-review, not sales-team feedback**.
* The rule agreed with the review on **7 of 9** leads.
* The top 3 ranked leads contained **2** genuine buyers.

| Lead | Rule said | Review said | Note |
|---|---|---|---|
| 2 | rental | off_topic | Both mean "not a buyer"; same score effect (5 points) |
| 3 | explicit_buy | enquiry_only | Title says buying, text only asks reasons and distance. Borderline case |

## 4. What the pilot changed

* Added `data_quality_flags` (`text_missing`, `no_phone`). Flags do not change the score.
* Added 2 regression tests: builder promotion containing "invest", and a buyer saying "want to invest".
* No scoring rules were changed for leads 2 and 3. Lead 2 has the same effect either way. Lead 3 is borderline, and changing rules for one example would overfit.
* Full change list: `reports/pipeline_optimization.diff`.

## 5. Limitations

* Only 9 posts, so these numbers show direction only and are not proof.
* All posts are old, so Recency is 0 and the maximum score is 75.
* No phone numbers are public on this source.
* The review was done by the project author with AI assistance, so it can share the same blind spots as the rules.
* Real sales feedback is needed before trusting the scores.