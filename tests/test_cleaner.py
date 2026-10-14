"""Tests for the cleaner. All numbers below are MADE-UP test strings, not real leads."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from cleaner import clean_phone  # noqa: E402

PHONE_CASES = [
    # (input, expected result)
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


def run():
    failed = 0
    for given, expected in PHONE_CASES:
        got = clean_phone(given)
        ok = got == expected
        failed += not ok
        print("PASS" if ok else "FAIL", repr(given), "->", repr(got), "(expected", repr(expected) + ")")
    print(f"\n{len(PHONE_CASES) - failed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
