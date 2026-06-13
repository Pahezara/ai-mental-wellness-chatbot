import re

_SINHALA_RE = re.compile(r"[\u0D80-\u0DFF]")


def detect_language(text: str) -> str:
    """
    Returns: "si" (Sinhala) or "en" (English).
    Simple + reliable for Sinhala script detection.
    """
    return "si" if _SINHALA_RE.search(text) else "en"