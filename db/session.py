from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings
from db.models import Base

engine = create_async_engine(settings.database_url, echo=False)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
