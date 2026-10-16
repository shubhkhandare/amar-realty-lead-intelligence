"""Small checks for scoring rules. Run: python tests/test_scoring.py"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from score_leads import intent_level_and_points, location_points, parse_date, recency_points

TODAY = date(2026, 10, 16)
CHECKS = [
    ("location named in post", location_points("Hadapsar", "text"), 40),
    ("location only from page", location_points("Hadapsar", "forum_page"), 30),
    ("nearby area", location_points("Magarpatta", "text"), 25),
    ("unknown area", location_points(None, "text"), 0),
    ("explicit buy", intent_level_and_points("Buying property in Hadapasr", "")[1], 35),
    ("enquiry", intent_level_and_points("Whom should I contact for details?", "")[1], 20),
    ("seller ad", intent_level_and_points("2BHK for sale in Hadapsar", "")[1], 0),
    ("rental", intent_level_and_points("Rental housing rules", "")[1], 5),
    ("generic", intent_level_and_points("About water problem", "")[1], 5),
    ("buyer who says 'available'", intent_level_and_points("Flat in Ramtekdi", "Is it wise to invest in a flat? Some ready flats available.")[1], 35),
    ("real buyer text", intent_level_and_points("Dreams Aakruti", "I am looking to buy a resale property.")[1], 35),
    ("concern from site visitor", intent_level_and_points("About water problem", "I visited the site. Is there any problem of water?")[1], 20),
    ("date with th", parse_date("28th July 2019"), date(2019, 7, 28)),
    ("date with nd", parse_date("2nd August 2018"), date(2018, 8, 2)),
    ("bad date", parse_date("soon"), None),
    ("posted today", recency_points(TODAY, TODAY), 25),
    ("about 1 year old", recency_points(date(2025, 10, 16), TODAY), 12),
    ("older than 2 years", recency_points(date(2019, 7, 28), TODAY), 0),
    ("missing date", recency_points(None, TODAY), 0),
]
passed = 0
for name, got, want in CHECKS:
    ok = got == want
    passed += ok
    print("PASS" if ok else "FAIL", "-", name, "" if ok else f"(got {got!r}, wanted {want!r})")
print(f"{passed} passed, {len(CHECKS) - passed} failed")