from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.db.init_db import init_db

setup_logging()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
def root():
    return {"ok": True, "app": settings.APP_NAME}


@app.get("/debug/direct-config")
def debug_direct_config():
    return {
        "TRANSLATION_PROVIDER": getattr(settings, "TRANSLATION_PROVIDER", None),
        "GOOGLE_APPLICATION_CREDENTIALS": getattr(settings, "GOOGLE_APPLICATION_CREDENTIALS", None),
        "OLLAMA_BASE_URL": getattr(settings, "OLLAMA_BASE_URL", None),
        "OLLAMA_MODEL": getattr(settings, "OLLAMA_MODEL", None),
    }


@app.get("/debug/direct-google/si-to-en")
async def debug_direct_google_si_to_en(text: str):
    from app.services.google_translator import GoogleCloudTranslator

    translator = GoogleCloudTranslator()
    return {
        "provider": "google",
        "input": text,
        "translation": await translator.si_to_en(text),
    }


@app.get("/debug/direct-google/en-to-si")
async def debug_direct_google_en_to_si(text: str):
    from app.services.google_translator import GoogleCloudTranslator

    translator = GoogleCloudTranslator()
    return {
        "provider": "google",
        "input": text,
        "translation": await translator.en_to_si(text),
    }