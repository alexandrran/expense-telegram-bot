from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.keyboards.language import language_keyboard
from db.repositories import ExpenseRepository, UserRepository
from services.i18n import t
from services.report_service import build_summary

router = Router()


@router.message(Command("summary"))
async def summary(
    message: Message,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if message.from_user is None:
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(message.from_user.id)
        if user.language_code is None:
            await session.commit()
            await message.answer(t(None, "choose_language"), reply_markup=language_keyboard())
            return

        totals = await expenses.get_totals(user.id)

    await message.answer(build_summary(totals, user.language_code))
