from __future__ import annotations

import asyncio
import random
from typing import Optional

import httpx

from app.core.config import settings
from app.services.planner import ResponsePlan


class LLMWriterOllama:
    def __init__(self) -> None:
        self.base_url = settings.OLLAMA_BASE_URL.rstrip("/")

    async def write(
        self,
        *,
        user_message_en: str,
        emotion: str,
        risk: str,
        style: str,
        plan: ResponsePlan,
    ) -> tuple[str, Optional[str]]:
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": settings.OLLAMA_MODEL,
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": user_message_en,
                }
            ],
        }

        retries = max(0, int(getattr(settings, "LLM_MAX_RETRIES", 1)))
        base_sleep = 0.7 + random.random() * 0.3
        timeout = httpx.Timeout(float(getattr(settings, "LLM_TIMEOUT_S", 30)))

        last_err: Exception | None = None

        for attempt in range(retries + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    r = await client.post(url, json=payload)
                    r.raise_for_status()
                    data = r.json()

                reply = ((data.get("message") or {}).get("content") or "").strip()

                if not reply:
                    raise RuntimeError("Empty reply from Ollama")

                return reply, None

            except Exception as e:
                last_err = e
                if attempt >= retries:
                    break
                await asyncio.sleep(base_sleep * (2 ** attempt))

        raise RuntimeError(f"Ollama writer failed: {last_err}")