"""Tests for the cleaner. All numbers below are MADE-UP test strings, not real leads."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from cleaner import clean_name, clean_phone, normalize_location  # noqa: E402

PHONE_CASES = [
    ("9000000001", "9000000001"),
    ("+91 90000 00001", "9000000001"),
    ("+919000000001", "9000000001"),
    ("91-9000000001", "9000000001"),
    ("09000000001", "9000000001"),
    ("(90000) 00001", "9000000001"),
    ("5000000001", None),      # starts with 5: not a mobile number
    ("12345", None),           # too short
    ("90000000011", None),     # 11 digits, too long
    ("1800 123 4567", None),   # toll-free helpline style, not a prospect
    ("", None),
    (None, None),
]

NAME_CASES = [
    ("kailash", "Kailash"),
    ("  smith   aggewal ", "Smith Aggewal"),
    ("Deepa , Apartment Resident", "Deepa, Apartment Resident"),
    ("", "Valued Prospect"),
    ("   ", "Valued Prospect"),
    (None, "Valued Prospect"),
]

# Each case: (list of texts to search in order, expected area)
LOCATION_CASES = [
    (["Buying property in Hadapasr", "How far from Phursungi IT Park?"], "Hadapsar"),
    (["Residential property at Ramtekdi Industrial area", ""], "Ramtekdi"),
    (["Flats in Phursungi", ""], "Fursungi"),
    (["Water problem", "Is there a water problem in handewadi area?"], "Handewadi"),
    (["Konark Bella Vista", "2BHK flats in Mararpatta"], "Magarpatta"),
    (["Vastu review for kumar prospera Pune", "five walls in the main bed room"], None),
    ([None, ""], None),
]


def run():
    failed = 0
    total = 0

    def check(label, given, got, expected):
        nonlocal failed, total
        total += 1
        ok = got == expected
        failed += not ok
        print("PASS" if ok else "FAIL", label, repr(given), "->", repr(got), "(expected", repr(expected) + ")")

    for given, expected in PHONE_CASES:
        check("phone", given, clean_phone(given), expected)
    for given, expected in NAME_CASES:
        check("name", given, clean_name(given), expected)
    for texts, expected in LOCATION_CASES:
        check("location", texts, normalize_location(*texts), expected)

    print(f"\n{total - failed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
