# backend/app/api/router.py
from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.chat import router as chat_router
from app.api.routes.analytics import router as analytics_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(analytics_router, tags=["analytics"])