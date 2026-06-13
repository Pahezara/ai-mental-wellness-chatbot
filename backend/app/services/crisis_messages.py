# backend/app/services/crisis_messages.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CrisisResponse:
    reply_en: str
    follow_up_en: str | None


def build_crisis_response(*, language: str = "en") -> CrisisResponse:
    """
    Deterministic crisis messaging. No model generation.
    Keep it short, direct, and safe.
    language: "en" or "si" (if you already translate later, keep English here).
    """
    # English only; translate later if your pipeline translates replies.
    reply = (
        "I’m really sorry you’re feeling this way. You don’t have to handle this alone.\n\n"
        "If you’re in immediate danger right now, please contact local emergency services or go to the nearest hospital.\n\n"
        "**Sri Lanka:** Call **1926** (National Mental Health Helpline).\n"
        "If possible, reach out to someone you trust and stay with them while you get help."
    )

    follow_up = "Are you safe right now, and is there someone nearby you can contact?"
    return CrisisResponse(reply_en=reply, follow_up_en=follow_up)