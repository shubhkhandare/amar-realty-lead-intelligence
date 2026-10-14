"""Day 3 pipeline: clean the newest raw forum CSV and remove duplicates."""
import glob
import os

import pandas as pd

from cleaner import clean_name, find_phone_in_text, mask_name, normalize_location

# The page we scraped is the Hadapsar forum page, so posts with no area in the text
# are labelled Hadapsar, and we record that this came from the page, not the text.
PAGE_AREA = "Hadapsar"

src = sorted(glob.glob("data/raw/forum_hadapsar_*.csv"))[-1]
raw = pd.read_csv(src, dtype=str, keep_default_na=False)
print("Raw records:", len(raw))

# 1. Drop junk: rows with no title.
data = raw[raw["title"].str.strip() != ""].copy()
junk_dropped = len(raw) - len(data)

# 2. Clean the columns.
data["poster_name"] = data["poster_name"].apply(clean_name)


def find_area(row):
    area = normalize_location(row["title"], row["question"])
    return (area, "text") if area else (PAGE_AREA, "forum_page")


data[["location", "location_source"]] = data.apply(lambda r: pd.Series(find_area(r)), axis=1)
data["phone"] = data.apply(
    lambda r: find_phone_in_text(r["title"]) or find_phone_in_text(r["question"]) or "", axis=1
)

# 3. Remove duplicates: same poster + same title + same question.
data["dedupe_key"] = (
    data["poster_name"].str.lower() + "|"
    + data["title"].str.lower().str.strip() + "|"
    + data["question"].str.lower().str.strip()
)
is_dup = data.duplicated("dedupe_key", keep="first")
first_url = data[~is_dup].set_index("dedupe_key")["thread_url"]
dups = data[is_dup]
log = pd.DataFrame({
    "poster_initial": dups["poster_name"].apply(mask_name),
    "title": dups["title"],
    "dropped_thread_url": dups["thread_url"],
    "kept_thread_url": dups["dedupe_key"].map(first_url),
    "reason": "same poster, title and question",
})
clean = data[~is_dup].drop(columns="dedupe_key")

# 4. Save. Full file stays local (git-ignored). Masked copies go to data/samples.
day = os.path.basename(src).replace("forum_hadapsar_", "").replace(".csv", "")
os.makedirs("data/clean", exist_ok=True)
os.makedirs("data/samples", exist_ok=True)
clean.to_csv(f"data/clean/forum_clean_{day}.csv", index=False)
masked = clean.copy()
masked["poster_name"] = masked["poster_name"].apply(mask_name)
masked.to_csv("data/samples/forum_clean_sample_masked.csv", index=False)
log.to_csv("data/samples/dedupe_log_masked.csv", index=False)

print("Junk rows dropped:", junk_dropped)
print("Duplicates removed:", len(dups))
print("Phone numbers found in text:", int((clean["phone"] != "").sum()))
print("Clean records:", len(clean))
print(clean["location"].value_counts().to_string())
