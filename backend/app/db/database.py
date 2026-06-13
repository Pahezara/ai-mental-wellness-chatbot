from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from app.core.config import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)