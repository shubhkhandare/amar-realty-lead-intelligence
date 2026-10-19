# Repo Defense: Questions and Answers

## Why this source?
The CommonFloor forum is public, needs no login, and robots.txt allows the pages used. It had posts about Hadapsar and Fursungi with real buyer intent signals. No paid data was used.

## Why 7 prospects and not 100?
Only 9 public posts were found, all from 2016 to 2019. Two were not purchase prospects (a builder advertisement and a rental topic), so 7 were exported. Reaching 100 would need more public sources, or inventing data, which the brief forbids.

## Why were builder ads and rental posts excluded?
They are not buyers. Including them would fill the list with noise. Each exclusion is logged by lead id in `reports/export_exclusions.csv`, so the decision can be checked.

## How is the score built?
Location 40 + Intent 35 + Recency 25, total 100. Location rewards the target areas named in the post. Intent is keyword and regex rules checked in a fixed order. Recency falls linearly to 0 at 730 days. Every score can be explained from its three parts.

## Why is Recency 0 for every lead?
All posts are older than 2 years. This also caps the best score at 75. The scoring rule is correct. The source is old.

## How were the rules validated?
By a self-review of all 9 posts. The rule agreed with the review on 7 of 9 leads, and the top 3 contained 2 genuine buyers. This is a self-review, not sales feedback, and the sample is tiny. It shows direction only.

## Why were the rules not changed for the 2 disagreements?
Lead 2 gets the same low score either way. Lead 3 is a borderline case. Changing rules to fit one example would overfit. The answer key was also not edited after seeing the rule output.

## Why are there no phone numbers?
The source does not show them publicly. A missing phone stays empty and is flagged `no_phone`. No contact data was invented.

## How is personal data protected?
Raw data, cleaned data and the database are git-ignored. The repo holds only masked names (`A***`) and counts-only logs. The file with real names goes only by email.

## How does the pipeline stay polite?
robots.txt check, a random 1.5 to 3.0 second delay, a descriptive User-Agent, public pages only, and back-off on blocks.

## What went wrong and how was it fixed?
* Unsaved files caused a stale module and an empty report once. Fixed by checking file size and content before each commit.
* Duplicate feedback rows inflated the validation counts. Fixed with a dedupe step.
* Two intent misreads (a builder promotion containing "invest" and a buyer saying "want to invest") were fixed and covered by regression tests.

## What would be done next?
Add more public sources with robots.txt checks, collect real sales feedback to replace the self-review, and re-tune the rules on a larger sample.