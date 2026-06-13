from __future__ import annotations

import asyncio
import html
import os
from typing import Literal

from google.cloud import translate_v2 as translate

from app.core.config import settings
from app.services.token_protect import protect, unprotect, ProtectedText


Lang = Literal["en", "si"]


class GoogleCloudTranslator:
    def __init__(self) -> None:
        self.creds_path = getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", "").strip()

        if self.creds_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.creds_path

        self._client: translate.Client | None = None

    def _load(self) -> translate.Client:
        if not self.creds_path:
            raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS is empty in .env")

        if not os.path.exists(self.creds_path):
            raise RuntimeError(f"Google credentials file not found: {self.creds_path}")

        if self._client is None:
            self._client = translate.Client()

        return self._client

    def _translate_sync(self, text: str, source: Lang, target: Lang) -> str:
        client = self._load()

        protected = protect(text)

        result = client.translate(
            protected.text,
            source_language=source,
            target_language=target,
            format_="text",
        )

        translated = result.get("translatedText", "") or ""
        translated = html.unescape(translated).strip()

        if not translated:
            raise RuntimeError("Google returned empty translation")

        return unprotect(ProtectedText(text=translated, mapping=protected.mapping))

    async def translate(self, text: str, source: Lang, target: Lang) -> str:
        if not text:
            return ""
        return await asyncio.to_thread(self._translate_sync, text, source, target)

    async def si_to_en(self, text_si: str) -> str:
        return await self.translate(text_si, "si", "en")

    async def en_to_si(self, text_en: str) -> str:
        return await self.translate(text_en, "en", "si")