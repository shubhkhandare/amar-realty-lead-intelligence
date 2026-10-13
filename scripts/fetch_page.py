import random
import time
import urllib.robotparser

import requests

# Who we are. Put your real email here.
UA = "AmarRealtyEvalBot/1.0 (contact: your-email@example.com)"
URL = "https://www.commonfloor.com/forum/a4321-hadapsar-pune"
ROBOTS_URL = "https://www.commonfloor.com/robots.txt"

# 1. Read robots.txt and ask: are we allowed to fetch this page?
robots = requests.get(ROBOTS_URL, headers={"User-Agent": UA}, timeout=20)
if robots.status_code != 200:
    raise SystemExit("Could not read robots.txt. Stopping to be safe.")
rp = urllib.robotparser.RobotFileParser()
rp.parse(robots.text.splitlines())
if not rp.can_fetch(UA, URL):
    raise SystemExit("robots.txt says NO. Stopping.")

# 2. Wait a random 1.5 to 3 seconds (be polite).
time.sleep(random.uniform(1.5, 3.0))

# 3. Ask for the page.
resp = requests.get(URL, headers={"User-Agent": UA}, timeout=20)
print("Status:", resp.status_code)
if resp.status_code in (403, 429):
    raise SystemExit("The site said no. Stopping. We do not bypass it.")

# 4. Save the page.
with open("data/raw/forum_live.html", "w", encoding="utf-8") as f:
    f.write(resp.text)
print("Saved", len(resp.text), "characters")
