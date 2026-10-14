"""Cleaner for Day 3 
"""

import re

def clean_phone(raw):
     """Return a clean 10-digit Indian mobile number, or None if it is not valid.
     We never guess: if the value is not a valid mobile number, we return None.
     """

     if raw is None:
          return None

     #1. KEEP ONLY DIGITS, REMOVE SPACES, + , -, ()

     digits = re.sub(r"\D", "",str(raw))

     #2. drop country code or 0

     if len(digits) == 12 and digits.startswith("91"):
          digits = digits[2:]
     elif len(digits) == 11 and digits.startswith("0"):
          digits = digits[1:]

     #3. Validate final mobile number
     if len(digits) != 10 or not digits.startswith(("6", "7", "8", "9")):
          return None

     return digits
        


