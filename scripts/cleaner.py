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
        




def clean_name(raw):
    """Tidy a name: one space between words, Title Case. Empty -> 'Valued Prospect'."""
    if raw is None:
        return "Valued Prospect"
    name = re.sub(r"\s+", " ", str(raw)).strip()   # collapse extra spaces
    name = re.sub(r"\s+,", ",", name)               # no space before a comma
    if not name:
        return "Valued Prospect"
    return name.title()


# Most specific areas first, the general one (Hadapsar) last.
LOCATION_PATTERNS = [
    ("Fursungi", r"fursung\w*|phursung\w*"),
    ("Handewadi", r"handewadi"),
    ("Ramtekdi", r"ramtekdi"),
    ("Magarpatta", r"magarpatta|mararpatta"),
    ("Hadapsar", r"hadap\w*"),
]


def normalize_location(*texts):
    """Look for a known area in each text, in order. Return its standard spelling or None."""
    for text in texts:
        if not text:
            continue
        for standard, pattern in LOCATION_PATTERNS:
            if re.search(pattern, str(text), flags=re.IGNORECASE):
                return standard
    return None


def clean_name(raw):
    """Tidy a name: one space between words, Title Case. Empty -> 'Valued Prospect'."""
    if raw is None:
        return "Valued Prospect"
    name = re.sub(r"\s+", " ", str(raw)).strip()   # collapse extra spaces
    name = re.sub(r"\s+,", ",", name)               # no space before a comma
    if not name:
        return "Valued Prospect"
    return name.title()


# Most specific areas first, the general one (Hadapsar) last.
LOCATION_PATTERNS = [
    ("Fursungi", r"fursung\w*|phursung\w*"),
    ("Handewadi", r"handewadi"),
    ("Ramtekdi", r"ramtekdi"),
    ("Magarpatta", r"magarpatta|mararpatta"),
    ("Hadapsar", r"hadap\w*"),
]


def normalize_location(*texts):
    """Look for a known area in each text, in order. Return its standard spelling or None."""
    for text in texts:
        if not text:
            continue
        for standard, pattern in LOCATION_PATTERNS:
            if re.search(pattern, str(text), flags=re.IGNORECASE):
                return standard
    return None
