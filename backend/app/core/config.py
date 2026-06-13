from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    APP_NAME: str = "MentalHealthChatbot"
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./mental.db"

    # Privacy
    STORE_RAW_TEXT: bool = False

    # Ollama - Main Mental Chat Writer
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "qwen-friendly-300"
    ENABLE_LLM_WRITER: bool = True
    REQUIRE_LLM_CONSENT: bool = False
    LLM_TIMEOUT_S: int = 45
    LLM_MAX_RETRIES: int = 1

    # Translation provider: "google" or "nllb"
    TRANSLATION_PROVIDER: str = "google"

    # Google Cloud Translation
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # NLLB fallback translator
    TRANSLATION_MODEL: str = "facebook/nllb-200-distilled-600M"
    NLLB_SINHALA_CODE: str = "sin_Sinh"
    NLLB_ENGLISH_CODE: str = "eng_Latn"

    # Disabled translation experiments / compatibility flags
    ENABLE_LLM_TRANSLATION: bool = False
    ENABLE_SINHALA_POLISH: bool = False
    ENABLE_SINHALA_DIRECT_WRITER: bool = False

    # Legacy optional fields kept to prevent config/import errors
    LLM_TRANSLATION_MODEL: str = "qwen2.5:7b-instruct"
    LLM_TRANSLATION_TIMEOUT_S: int = 45
    SINHALA_WRITER_MODEL: str = "qwen2.5:7b-instruct"

    # Emotion model
    EMOTION_MODEL: str = "SamLowe/roberta-base-go_emotions"

    # Hugging Face
    HF_TOKEN: str | None = None


settings = Settings()