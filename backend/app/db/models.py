from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Float


class Base(DeclarativeBase):
    pass


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EmotionLog(Base):
    __tablename__ = "emotion_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String, index=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    language: Mapped[str] = mapped_column(String)
    emotion: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)

    # store only if user explicitly consented; otherwise keep empty
    raw_text: Mapped[str] = mapped_column(String, default="")