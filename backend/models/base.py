from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from settings import settings

__all__ = [
    'Base',
    'get_db',
]


Base = declarative_base()

async_session_maker = async_sessionmaker(
    bind=create_async_engine(settings.DATABASE_URL, echo=True),
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
