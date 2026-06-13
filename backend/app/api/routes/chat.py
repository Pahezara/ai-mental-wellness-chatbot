from __future__ import annotations

import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas import ChatRequest, ChatResponse, EmotionPrediction
from app.db.database import AsyncSessionLocal
from app.db.models import Session as DbSession, EmotionLog
from app.core.config import settings

from app.services.lang_detect import detect_language
from app.services.google_translator import GoogleCloudTranslator
from app.services.emotion import EmotionClassifier
from app.services.risk import assess_risk
from app.services.planner import Planner
from app.services.llm_writer_ollama import LLMWriterOllama
from app.services.crisis_messages import build_crisis_response

router = APIRouter()
logger = logging.getLogger(__name__)

google_translator = GoogleCloudTranslator()
emotion_model = EmotionClassifier()
planner = Planner()
llm_writer = LLMWriterOllama()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def google_si_to_en(text_si: str) -> str:
    try:
        return await google_translator.si_to_en(text_si)
    except Exception as e:
        logger.exception("Google Sinhala->English translation failed: %s", str(e))
        raise HTTPException(
            status_code=503,
            detail=f"Google Sinhala->English translation failed: {str(e)}",
        )


async def google_en_to_si(text_en: str) -> str:
    try:
        return await google_translator.en_to_si(text_en)
    except Exception as e:
        logger.exception("Google English->Sinhala translation failed: %s", str(e))
        raise HTTPException(
            status_code=503,
            detail=f"Google English->Sinhala translation failed: {str(e)}",
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)) -> ChatResponse:
    session_id = req.session_id or str(uuid.uuid4())

    existing = await db.execute(select(DbSession).where(DbSession.id == session_id))
    sess = existing.scalar_one_or_none()

    if sess is None:
        sess = DbSession(id=session_id, user_id=req.user_id)
        db.add(sess)
        await db.commit()

    lang = detect_language(req.message)

    if lang == "si":
        text_en = await google_si_to_en(req.message)
        reply_language = "si"
    else:
        text_en = req.message
        reply_language = "en"

    emotion_label, conf = emotion_model.predict_top(text_en)
    risk = assess_risk(text_en=text_en, text_original=req.message)

    low = text_en.lower().strip()
    emotional_keywords = [
        "sad",
        "angry",
        "anxious",
        "panic",
        "stress",
        "lonely",
        "sleep",
        "hopeless",
        "nightmare",
        "nightmares",
        "fear",
        "tired",
        "overthinking",
        "depressed",
        "depression",
    ]

    if len(low.split()) <= 7 and not any(w in low for w in emotional_keywords):
        emotion_label = "neutral"

    logger.info(
        "chat user=%s session=%s lang=%s emotion=%s risk=%s translation=google model=%s",
        req.user_id,
        session_id,
        lang,
        emotion_label,
        risk,
        settings.OLLAMA_MODEL,
    )

    plan = planner.build_plan(
        emotion=emotion_label,
        risk=risk,
        style=req.style,
        user_message_en=text_en,
    )

    if risk == "high":
        crisis = build_crisis_response(language="en")
        reply_en = crisis.reply_en
        follow_up = crisis.follow_up_en
        writer_source = "crisis_template_google_translate"
    else:
        try:
            reply_en, follow_up = await llm_writer.write(
                user_message_en=text_en,
                emotion=emotion_label,
                risk=risk,
                style=req.style,
                plan=plan,
            )
            writer_source = "ollama_google_translate"
        except Exception as e:
            logger.exception("Ollama writer failed. Using safe fallback: %s", str(e))
            reply_en = (
                "I’m here with you. Tell me a little more about what’s happening right now, "
                "and we can take it slowly together."
            )
            follow_up = None
            writer_source = "ollama_failed_fallback_google_translate"

    if reply_language == "si":
        reply_final = await google_en_to_si(reply_en)
        follow_up_final = await google_en_to_si(follow_up) if follow_up else None
    else:
        reply_final = reply_en
        follow_up_final = follow_up

    raw_text = req.message if (settings.STORE_RAW_TEXT and req.consent_store_text) else ""

    log = EmotionLog(
        session_id=session_id,
        user_id=req.user_id,
        timestamp=datetime.utcnow(),
        language=lang,
        emotion=emotion_label,
        confidence=conf,
        raw_text=raw_text,
    )

    db.add(log)
    await db.commit()

    return ChatResponse(
        session_id=session_id,
        detected_language=lang,
        translated_to_english=text_en,
        emotion=EmotionPrediction(label=emotion_label, confidence=conf),
        risk_level=risk,
        reply=reply_final,
        follow_up_question=follow_up_final,
        writer_source=writer_source,
    )