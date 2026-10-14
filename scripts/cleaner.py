"""Cleaning helpers for Day 3. Each function does one small job."""
import re


def clean_phone(raw):
    """Return a clean 10-digit Indian mobile number, or None if it is not valid.
    We never guess: if the value is not a valid mobile number, we return None.
    """
    if raw is None:
        return None
    digits = re.sub(r"\D", "", str(raw))          # keep only digits
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]                       # drop country code 91
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]                       # drop leading 0
    if re.fullmatch(r"[6-9]\d{9}", digits):       # 10 digits, starts with 6-9
        return digits
    return None


def clean_name(raw):
    """Tidy a name: one space between words, Title Case. Empty -> 'Valued Prospect'."""
    if raw is None:
        return "Valued Prospect"
    name = re.sub(r"\s+", " ", str(raw)).strip()
    name = re.sub(r"\s+,", ",", name)
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


def find_phone_in_text(text):
    """Look inside free text for a phone number the poster typed. Return a clean number or None."""
    if not text:
        return None
    for candidate in re.findall(r"\+?\d[\d\s\-()]{8,}\d", str(text)):
        phone = clean_phone(candidate)
        if phone:
            return phone
    return None


def mask_name(name):
    """Hide a name for files that go into Git: first letter + ***."""
    name = (name or "").strip()
    return (name[:1] + "***") if name else ""