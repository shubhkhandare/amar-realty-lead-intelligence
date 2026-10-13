"""Read a SAVED CommonFloor forum page (offline, no internet) and list the questions."""
import json
import sys

from bs4 import BeautifulSoup

PAGE_URL = "https://www.commonfloor.com/forum/a4321-hadapsar-pune"


def parse(html, page_url):
    soup = BeautifulSoup(html, "lxml")
    rows = []
    for d in soup.select("div.topic-discussion"):
        def text(sel):
            el = d.select_one(sel)
            return el.get_text(" ", strip=True) if el else ""

        link = d.select_one("div.topic-title a")
        rows.append({
            "title": text("div.topic-title"),
            "question": text("span.topic-question-description"),
            "poster_name": text("div.topic-started-user-name"),
            "posted_date": text("div.topic-start-date"),
            "thread_url": link["href"] if link else "",
            "source_url": page_url,
        })
    return rows


if __name__ == "__main__":
    html = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    rows = parse(html, PAGE_URL)
    print(len(rows), "posts found")
    for r in rows:
        print("-", r["posted_date"], "|", r["poster_name"], "|", r["title"])
    with open("data/raw/forum_test.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
