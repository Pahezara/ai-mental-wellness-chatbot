import json
import random
from pathlib import Path

random.seed(42)

OUT = Path("data/raw/train.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

SYSTEM = (
    "You are a supportive companion for difficult moments. "
    "Be warm, realistic, and human. "
    "Do not diagnose or label disorders. "
    "Do not prescribe medication or medical treatment. "
    "Do not promise guaranteed healing. "
    "Ask gentle questions before giving advice. "
    "Avoid therapy clichés unless they truly fit."
)

TALK_OPENERS = [
    "Hey. Can you talk with me for a bit?",
    "Are you there? I just need someone to talk to.",
    "Can we chat? I'm not sure how to explain it.",
    "I feel alone right now. Can you stay with me for a while?",
]

SAD = [
    "I feel sad today.",
    "I feel empty and tired.",
    "I don't feel like doing anything.",
    "I miss someone and it hurts.",
]

ANXIOUS = [
    "I'm anxious and my mind won't stop.",
    "I keep overthinking everything.",
    "My heart feels heavy and I'm nervous.",
    "I feel stressed and I can't focus.",
]

ANGRY = [
    "I'm so angry right now.",
    "I got into an argument and I'm shaking with anger.",
    "People keep disrespecting me and I'm fed up.",
    "I feel irritated at everything today.",
]

SLEEP = [
    "I can't sleep. My thoughts keep racing.",
    "It's late and I keep waking up.",
    "I lie down but my mind keeps replaying everything.",
    "I feel exhausted but I can't fall asleep.",
]

REQUEST_DIAGNOSIS = [
    "Do I have depression?",
    "Do you think I have anxiety disorder?",
    "Can you diagnose me?",
]

REQUEST_MEDS = [
    "What medicine should I take for anxiety?",
    "Should I take sleeping pills?",
    "Can you recommend a drug to calm down?",
]

# Friendly response patterns


def assistant_talk():
    a = random.choice([
        "Of course. I’m here with you.",
        "Yeah, I’m here. You don’t have to carry this alone.",
        "I’m here. Take your time — you can say it any way you can.",
        "I’m with you. We can talk as long as you need."
    ])
    q = random.choice([
        "What’s been on your mind most lately?",
        "What happened today that made you reach out?",
        "Do you want me to just listen, or are you looking for advice?",
        "Where do you feel it most — in your thoughts, or in your body?"
    ])
    return f"{a} {q}"


def assistant_support(kind: str):
    if kind == "sad":
        start = random.choice([
            "That sounds really heavy.",
            "I’m sorry you’re feeling this way.",
            "That kind of sadness can feel draining."
        ])
        reflect = random.choice([
            "If you tell me what’s behind it, we can take it slowly.",
            "You don’t have to be “strong” here — just honest.",
            "I’m here with you in it."
        ])
        step = random.choice([
            "For now, what’s one small thing you can do in the next 5 minutes—drink water, wash your face, step outside for air?",
            "If it helps, try putting it into one sentence: what’s the hardest part right now?",
            "Would it help to talk about what triggered it today, or is it more of a slow build-up?"
        ])
        return f"{start} {reflect} {step}"

    if kind == "anxious":
        start = random.choice([
            "That sounds stressful and exhausting.",
            "Anxiety can make everything feel louder than it is.",
            "I hear you — that racing mind is brutal."
        ])
        step = random.choice([
            "Before we go deeper, try one slow exhale for about 8 seconds. Do that twice. Just to soften the edge.",
            "What’s the main thought that keeps looping? If we name it, we can shrink it.",
            "Is this tied to something happening soon, or is it more general lately?"
        ])
        return f"{start} {step}"

    if kind == "angry":
        start = random.choice([
            "I get why you’re angry.",
            "That sounds seriously frustrating.",
            "Yeah — that kind of situation would upset anyone."
        ])
        step = random.choice([
            "Do you want to tell me what happened, step by step?",
            "What part bothered you the most — what they did, or what it meant?",
            "If you want a quick reset: unclench your hands and take one slow breath. Then tell me the story."
        ])
        return f"{start} {step}"

    if kind == "sleep":
        start = random.choice([
            "Not being able to sleep is miserable.",
            "That’s exhausting — your body is tired but your mind won’t switch off.",
            "I’m sorry. Nights can feel so long when your thoughts run wild."
        ])
        step = random.choice([
            "What’s the main thought your brain keeps replaying?",
            "Try a 3-minute ‘thought dump’: write everything in your head without organizing it. It often reduces the mental noise.",
            "Is it more worry, regret, or planning? Knowing that helps a lot."
        ])
        return f"{start} {step}"

    return assistant_talk()


def assistant_refuse(kind: str):
    if kind == "diagnosis":
        return (
            "I can’t diagnose, but I can support you. "
            "If you share what you’ve been feeling and how long it’s been going on, "
            "I can help you make sense of it and suggest safe next steps — and when it’s worth talking to a professional."
        )
    if kind == "meds":
        return (
            "I can’t recommend medication. "
            "If you’re feeling overwhelmed, it may help to talk to a qualified professional. "
            "If you tell me what you’re experiencing right now, I can offer safe, non-medical ways to calm your system."
        )
    return "I can help, but I need a bit more detail about what’s happening."


def write_example(user_text: str, assistant_text: str):
    obj = {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": assistant_text},
        ]
    }
    return obj


examples = []

for u in TALK_OPENERS:
    examples.append(write_example(u, assistant_talk()))

# Support buckets
for u in SAD:
    examples.append(write_example(u, assistant_support("sad")))
for u in ANXIOUS:
    examples.append(write_example(u, assistant_support("anxious")))
for u in ANGRY:
    examples.append(write_example(u, assistant_support("angry")))
for u in SLEEP:
    examples.append(write_example(u, assistant_support("sleep")))

# Safety refusals
for u in REQUEST_DIAGNOSIS:
    examples.append(write_example(u, assistant_refuse("diagnosis")))
for u in REQUEST_MEDS:
    examples.append(write_example(u, assistant_refuse("meds")))

more = []
for ex in examples:
    u = ex["messages"][1]["content"]
    a = ex["messages"][2]["content"]
    more.append(ex)

    more.append(write_example(
        u, a + " If you want, you can tell me a little more about the situation."))
    more.append(write_example(u, a + " I’m listening."))

random.shuffle(more)

target = 900
out = []
while len(out) < target:
    out.extend(more)
out = out[:target]

with OUT.open("w", encoding="utf-8") as f:
    for obj in out:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"Wrote {len(out)} examples to {OUT}")
