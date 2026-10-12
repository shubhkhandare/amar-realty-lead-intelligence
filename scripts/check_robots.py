#!/usr/bin/env python3
"""Check whether a URL may be fetched according to the site's robots.txt.

Usage:
    python scripts/check_robots.py URL [URL ...] [--user-agent UA]

Appends results to logs/robots_audit.csv as a compliance audit trail.
"""
import argparse
import csv
import datetime as dt
import os
import sys
import urllib.robotparser
from urllib.parse import urlparse

import requests

DEFAULT_UA = "AmarRealtyEvalBot/1.0"
AUDIT_PATH = os.path.join("logs", "robots_audit.csv")


def check(url, user_agent):
    parts = urlparse(url)
    robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
    result = {
        "checked_at": dt.datetime.now().isoformat(timespec="seconds"),
        "url": url,
        "robots_url": robots_url,
        "status": "",
        "allowed": "",
        "crawl_delay": "",
    }
    try:
        resp = requests.get(robots_url, headers={"User-Agent": user_agent}, timeout=15)
        result["status"] = resp.status_code
        rp = urllib.robotparser.RobotFileParser()
        if resp.status_code == 200:
            rp.parse(resp.text.splitlines())
            result["allowed"] = rp.can_fetch(user_agent, url)
            delay = rp.crawl_delay(user_agent)
            result["crawl_delay"] = delay if delay is not None else ""
        elif resp.status_code in (401, 403):
            result["allowed"] = False
        else:
            result["allowed"] = "no-robots-file (verify ToS manually)"
    except requests.RequestException as exc:
        result["status"] = "error: " + exc.__class__.__name__
        result["allowed"] = "unknown"
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--user-agent", default=DEFAULT_UA)
    args = ap.parse_args()

    rows = [check(u, args.user_agent) for u in args.urls]
    for r in rows:
        print(f"{r['url']}\n  robots: {r['robots_url']} (HTTP {r['status']})"
              f"  allowed={r['allowed']}  crawl_delay={r['crawl_delay'] or '-'}")

    os.makedirs("logs", exist_ok=True)
    new = not os.path.exists(AUDIT_PATH)
    with open(AUDIT_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
