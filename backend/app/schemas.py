from pydantic import BaseModel, Field
from typing import Optional, Literal, List


Style = Literal["gentle_friend", "coach", "practical", "short"]


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=64)
    session_id: Optional[str] = Field(default=None, max_length=128)
    message: str = Field(min_length=1, max_length=2000)
    style: Style = "gentle_friend"
    consent_store_text: bool = False
    consent_send_to_llm: bool = False


class EmotionPrediction(BaseModel):
    label: str
    confidence: float


class ChatResponse(BaseModel):
    session_id: str
    detected_language: str
    translated_to_english: str
    emotion: EmotionPrediction
    risk_level: Literal["low", "medium", "high"]
    reply: str
    follow_up_question: Optional[str] = None
    writer_source: str


class TrendPoint(BaseModel):
    date: str
    emotion: str
    count: int


class TrendsResponse(BaseModel):
    user_id: str
    points: List[TrendPoint]