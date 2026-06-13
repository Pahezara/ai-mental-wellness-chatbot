from __future__ import annotations

import re

# Minimal keyword-based risk detection (upgrade later to a classifier).
# Includes English + Sinhala common crisis phrases.
HIGH_RISK_PATTERNS = [
    r"\b(suicide|kill myself|end my life|want to die|self harm)\b",
    r"මරන්න", r"මැරෙන්න", r"ජීවිතේ ඉවර", r"ආත්මහත්‍ය", r"මම මැරෙනවා",
]
_MED_RE = [
    r"\b(hopeless|no point|can't go on|give up)\b",
    r"බැහැ", r"ඉවසන්න බැහැ", r"කිසිම වටිනාකමක් නැහැ",
]

_HIGH = [re.compile(p, re.IGNORECASE) for p in HIGH_RISK_PATTERNS]
_MED = [re.compile(p, re.IGNORECASE) for p in _MED_RE]


def assess_risk(text_en: str, text_original: str) -> str:
    combined = f"{text_en}\n{text_original}"
    if any(p.search(combined) for p in _HIGH):
        return "high"
    if any(p.search(combined) for p in _MED):
        return "medium"
    return "low"