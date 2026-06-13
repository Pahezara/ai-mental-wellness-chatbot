from __future__ import annotations

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.config import settings


EMOTION_MAP = {
    "admiration": "positive",
    "amusement": "positive",
    "approval": "positive",
    "caring": "positive",
    "desire": "positive",
    "excitement": "positive",
    "gratitude": "positive",
    "joy": "positive",
    "love": "positive",
    "optimism": "positive",
    "pride": "positive",
    "relief": "positive",

    "sadness": "sad",
    "grief": "sad",
    "disappointment": "sad",
    "remorse": "sad",
    "embarrassment": "sad",

    "anger": "angry",
    "annoyance": "angry",
    "disapproval": "angry",
    "disgust": "angry",

    "fear": "anxious",
    "nervousness": "anxious",

    "confusion": "confused",
    "realization": "confused",
    "surprise": "confused",
    "curiosity": "confused",

    "neutral": "neutral",
}

FALLBACK = "neutral"


class EmotionClassifier:
    def __init__(self) -> None:
        self.model_name = settings.EMOTION_MODEL
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

        self._tokenizer = None
        self._model = None
        self._id2label = None

    def _load(self) -> None:
        if self._tokenizer is not None and self._model is not None and self._id2label is not None:
            return

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self._model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            torch_dtype=self.dtype,
            use_safetensors=True,
        )
        self._model.to(self.device)
        self._model.eval()
        self._id2label = self._model.config.id2label

    @torch.inference_mode()
    def predict_top(self, text: str) -> tuple[str, float]:
        self._load()
        assert self._tokenizer is not None
        assert self._model is not None
        assert self._id2label is not None

        inputs = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
        ).to(self.device)

        logits = self._model(**inputs).logits

        # GoEmotions models are usually multi-label.
        probs = torch.sigmoid(logits)[0]

        top_idx = int(torch.argmax(probs).item())
        top_prob = float(probs[top_idx].item())
        raw_label = str(self._id2label[top_idx]).lower()

        mapped = EMOTION_MAP.get(raw_label, FALLBACK)

        # Practical override for weak emotional confidence
        if top_prob < 0.35:
            mapped = "neutral"

        return mapped, top_prob