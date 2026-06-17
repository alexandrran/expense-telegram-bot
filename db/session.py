from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings
from db.models import Base, User

engine = create_async_engine(settings.database_url, echo=False)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.run_sync(_ensure_user_language_column)


def _ensure_user_language_column(connection) -> None:
    columns = {column["name"] for column in inspect(connection).get_columns(User.__tablename__)}
    if "language_code" not in columns:
        connection.exec_driver_sql("ALTER TABLE users ADD COLUMN language_code VARCHAR(8)")
