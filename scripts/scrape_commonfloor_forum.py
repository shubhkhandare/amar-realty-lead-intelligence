"""Day 2 scraper: fetch ONE public forum page politely, parse the posts, save JSON and CSV."""
import csv
import datetime as dt
import json
import random
import time
import urllib.robotparser

import requests

from parse_forum import parse  # the parser we already wrote

UA = "AmarRealtyEvalBot/1.0 (contact: your-email@example.com)"
URL = "https://www.commonfloor.com/forum/a4321-hadapsar-pune"
ROBOTS_URL = "https://www.commonfloor.com/robots.txt"


def allowed(url):
    """Ask robots.txt if we may fetch this URL."""
    r = requests.get(ROBOTS_URL, headers={"User-Agent": UA}, timeout=20)
    if r.status_code != 200:
        return False  # cannot read the rules, so do not scrape
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(r.text.splitlines())
    return rp.can_fetch(UA, url)


def main():
    if not allowed(URL):
        raise SystemExit("robots.txt says NO (or could not be read). Stopping.")

    time.sleep(random.uniform(1.5, 3.0))  # polite random delay
    resp = requests.get(URL, headers={"User-Agent": UA}, timeout=20)
    print("Status:", resp.status_code)
    if resp.status_code in (403, 429):
        raise SystemExit("The site said no. Stopping. We do not bypass it.")
    resp.raise_for_status()

    rows = parse(resp.text, URL)
    if not rows:
        raise SystemExit("No posts found. The page shape may have changed.")
    scraped_at = dt.datetime.now().isoformat(timespec="seconds")
    for row in rows:
        row["scraped_at"] = scraped_at
    print(len(rows), "posts parsed")

    day = dt.date.today().isoformat()
    json_path = f"data/raw/forum_hadapsar_{day}.json"
    csv_path = f"data/raw/forum_hadapsar_{day}.csv"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print("Saved:", json_path, "and", csv_path)


if __name__ == "__main__":
    main()
