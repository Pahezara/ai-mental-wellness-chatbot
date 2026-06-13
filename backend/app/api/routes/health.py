from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/healthz")
def healthz():
    return {"ok": True}


@router.get("/debug/config")
def debug_config():
    return {
        "TRANSLATION_PROVIDER": getattr(settings, "TRANSLATION_PROVIDER", None),
        "GOOGLE_APPLICATION_CREDENTIALS": getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", None),
        "OLLAMA_BASE_URL": getattr(settings, "OLLAMA_BASE_URL", None),
        "OLLAMA_MODEL": getattr(settings, "OLLAMA_MODEL", None),
        "ENABLE_LLM_TRANSLATION": getattr(settings, "ENABLE_LLM_TRANSLATION", None),
        "ENABLE_SINHALA_POLISH": getattr(settings, "ENABLE_SINHALA_POLISH", None),
    }


@router.get("/debug/google/si-to-en")
async def debug_google_si_to_en(text: str):
    from app.services.google_translator import GoogleCloudTranslator

    translator = GoogleCloudTranslator()
    return {
        "provider": "google",
        "input": text,
        "translation": await translator.si_to_en(text),
    }


@router.get("/debug/google/en-to-si")
async def debug_google_en_to_si(text: str):
    from app.services.google_translator import GoogleCloudTranslator

    translator = GoogleCloudTranslator()
    return {
        "provider": "google",
        "input": text,
        "translation": await translator.en_to_si(text),
    }