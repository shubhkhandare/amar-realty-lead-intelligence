import csv
import glob
import os

# Take the newest raw CSV and write a copy with poster names masked.
src = sorted(glob.glob("data/raw/forum_hadapsar_*.csv"))[-1]
os.makedirs("data/samples", exist_ok=True)

with open(src, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

for r in rows:
    name = r["poster_name"].strip()
    r["poster_name"] = (name[:1] + "***") if name else ""

out = "data/samples/forum_sample_masked.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
print("Wrote", out, "with", len(rows), "rows")
