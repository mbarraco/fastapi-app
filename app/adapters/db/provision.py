from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app.config import DB_URL

DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://")


async def create_database(db_name: str = "app") -> None:
    drop_sql = f"DROP DATABASE IF EXISTS {db_name}"
    create_sql = f"CREATE DATABASE {db_name} ENCODING 'utf8'"
    engine = create_async_engine(
        DB_URL, future=True, poolclass=NullPool
    ).execution_options(isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        await conn.execute(text(drop_sql))
        await conn.execute(text(create_sql))


async def delete_database(db_name: str) -> None:
    drop_sql = f"DROP DATABASE IF EXISTS {db_name}"
    engine = create_async_engine(
        DB_URL, future=True, poolclass=NullPool
    ).execution_options(isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        await conn.execute(text(drop_sql))
