from __future__ import annotations

import re
from dataclasses import dataclass

_URL_RE = re.compile(r"https?://\S+")
_EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
_CODE_RE = re.compile(r"`[^`]+`")
_NUM_RE = re.compile(r"\b\d{2,}\b")


@dataclass
class ProtectedText:
    text: str
    mapping: dict[str, str]


def protect(text: str) -> ProtectedText:
    mapping: dict[str, str] = {}
    idx = 0

    def sub(pattern: re.Pattern, s: str, tag: str) -> str:
        nonlocal idx

        def repl(m: re.Match) -> str:
            nonlocal idx
            key = f"__{tag}_{idx}__"
            mapping[key] = m.group(0)
            idx += 1
            return key

        return pattern.sub(repl, s)

    s = text or ""
    s = sub(_URL_RE, s, "URL")
    s = sub(_EMAIL_RE, s, "EMAIL")
    s = sub(_CODE_RE, s, "CODE")
    s = sub(_NUM_RE, s, "NUM")

    if "1926" in s:
        key = "__HELPLINE_1926__"
        mapping[key] = "1926"
        s = s.replace("1926", key)

    return ProtectedText(text=s, mapping=mapping)


def unprotect(p: ProtectedText) -> str:
    s = p.text or ""
    for key in sorted(p.mapping.keys(), key=len, reverse=True):
        s = s.replace(key, p.mapping[key])
    return s