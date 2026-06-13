from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResponsePlan:
    mode: str  # "talk" | "support"
    tone: str  # "warm" | "practical" | "brief" | "motivational"
    acknowledge: str
    validate: str
    suggestions: list[str]
    follow_up_question: Optional[str]


class Planner:
    def build_plan(self, *, emotion: str, risk: str, style: str, user_message_en: str) -> ResponsePlan:
        text = (user_message_en or "").strip()
        low = text.lower()

        # Detect "just want to talk" messages (avoid giving exercises)
        talk_intent = any(p in low for p in [
            "can you talk", "talk with me", "talk to me", "are you there", "can we chat",
            "i need someone", "i need to talk", "just talk", "can you listen",
        ]) or (len(low.split()) <= 10 and any(g in low for g in ["hey", "hi", "hello"]))

        asks_for_advice = any(p in low for p in [
            "what should i do", "what do i do", "help me", "advice", "how do i", "how can i",
            "guide me", "tell me what to do",
        ])

        clear_distress = any(p in low for p in [
            "can't sleep", "cant sleep", "insomnia", "panic", "overthinking", "anxious", "stress",
            "depressed", "sad", "angry", "lonely", "hopeless",
        ])

        # Style tone mapping
        tone = {
            "gentle_friend": "warm",
            "coach": "motivational",
            "practical": "practical",
            "short": "brief",
        }.get(style, "warm")

        # If risk is high, planner still provides a base structure (chat.py will override with deterministic crisis)
        if risk == "high":
            return ResponsePlan(
                mode="support",
                tone="warm",
                acknowledge="I’m really sorry you’re feeling this overwhelmed.",
                validate="You don’t have to go through this alone.",
                suggestions=[],
                follow_up_question="Are you safe right now, and is there someone nearby who can support you?",
            )

        # TALK MODE: keep it natural, curious, human.
        if talk_intent and not asks_for_advice and not clear_distress and emotion in ["neutral", "confused", "positive"]:
            return ResponsePlan(
                mode="talk",
                tone=tone,
                acknowledge="Of course. I’m here with you.",
                validate="You can take your time — no pressure to explain perfectly.",
                suggestions=[],
                follow_up_question="What’s been on your mind lately, or what made you reach out right now?",
            )

        # SUPPORT MODE: only small, relevant steps (no long lists).
        ack_map = {
            "sad": "That sounds really heavy.",
            "anxious": "That sounds stressful and exhausting.",
            "angry": "I hear how frustrating this feels.",
            "confused": "It makes sense that you feel unsure about this.",
            "positive": "I’m glad you shared that.",
            "neutral": "Thanks for telling me.",
        }
        acknowledge = ack_map.get(emotion, "Thanks for telling me.")
        validate = "I’m with you. Let’s take it one step at a time."

        suggestions: list[str] = []

        # Situation-aware small suggestions (max 2–3)
        if "sleep" in low or "can't sleep" in low or "cant sleep" in low:
            suggestions = [
                "Try a quick ‘thought dump’: write whatever is in your head for 3 minutes, no structure.",
                "Relax the body first: slow exhale for 10 seconds + drop shoulders + unclench jaw.",
            ]
        elif "overthinking" in low or "racing" in low:
            suggestions = [
                "Let’s shrink the problem: what’s the one thought that keeps repeating most?",
                "Try a 2-minute reset: inhale 4, exhale 6, repeat 6 times.",
            ]
        elif emotion == "anxious":
            suggestions = [
                "Try one calm cycle: inhale 4, exhale 6 (repeat 6 times).",
                "Name 3 things you see + 2 you feel + 1 you hear (quick grounding).",
            ]
        elif emotion == "sad":
            suggestions = [
                "What’s one tiny thing you can do in 5 minutes (water, shower, walk, message someone)?",
                "If you can, tell me what part hurts the most right now.",
            ]
        elif emotion == "angry":
            suggestions = [
                "Give yourself 60 seconds to cool down: slow exhale + loosen hands/shoulders.",
                "Then we can separate what you can control vs what you can’t here.",
            ]
        elif emotion == "confused":
            suggestions = [
                "Let’s simplify it: what are the 2–3 facts you’re sure about?",
                "What’s the one decision or worry you feel stuck on?",
            ]

        follow_up = None if style == "short" else "Do you want me to just listen, or would you like advice?"

        return ResponsePlan(
            mode="support",
            tone=tone,
            acknowledge=acknowledge,
            validate=validate,
            suggestions=suggestions,
            follow_up_question=follow_up,
        )