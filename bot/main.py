import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.commands import setup_bot_commands
from bot.handlers import expenses, reports, start
from core.config import settings
from db.session import create_db, session_maker


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    await create_db()

    bot = Bot(token=settings.bot_token)
    await setup_bot_commands(bot)

    dispatcher = Dispatcher(db_sessionmaker=session_maker)
    dispatcher.include_router(start.router)
    dispatcher.include_router(reports.router)
    dispatcher.include_router(expenses.router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
