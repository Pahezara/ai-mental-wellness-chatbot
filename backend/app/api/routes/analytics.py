from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.db.database import AsyncSessionLocal
from app.db.models import EmotionLog
from app.schemas import TrendsResponse, TrendPoint

router = APIRouter()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/analytics/emotions/{user_id}", response_model=TrendsResponse)
async def emotion_trends(user_id: str, days: int = 14, db: AsyncSession = Depends(get_db)) -> TrendsResponse:
    since = datetime.utcnow() - timedelta(days=days)

    stmt = (
        select(
            func.date(EmotionLog.timestamp).label("d"),
            EmotionLog.emotion,
            func.count().label("c"),
        )
        .where(EmotionLog.user_id == user_id)
        .where(EmotionLog.timestamp >= since)
        .group_by(func.date(EmotionLog.timestamp), EmotionLog.emotion)
        .order_by(func.date(EmotionLog.timestamp))
    )

    rows = (await db.execute(stmt)).all()
    points = [TrendPoint(date=str(r.d), emotion=str(r.emotion), count=int(r.c)) for r in rows]

    return TrendsResponse(user_id=user_id, points=points)