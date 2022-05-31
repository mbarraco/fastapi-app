from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

DB_URL = settings.SQLALCHEMY_DATABASE_URI.replace(
    "postgresql://", "postgresql+asyncpg://"
)


def get_engine() -> AsyncEngine:
    return create_async_engine(DB_URL)


def db_session() -> AsyncSession:
    engine = create_async_engine(DB_URL)
    return sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
