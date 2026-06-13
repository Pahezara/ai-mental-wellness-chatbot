from __future__ import annotations

BANNED_MEDICAL_CLAIMS = [
    "you have depression",
    "you have anxiety disorder",
    "diagnose",
    "prescribe",
]

def is_safe(text: str) -> bool:
    low = text.lower()
    return not any(p in low for p in BANNED_MEDICAL_CLAIMS)