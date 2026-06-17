from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.commands import setup_chat_commands
from bot.keyboards.language import language_keyboard
from db.repositories import UserRepository
from services.i18n import t

router = Router()


@router.message(CommandStart())
async def start(message: Message, db_sessionmaker: async_sessionmaker) -> None:
    if message.from_user is None:
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        user = await users.get_or_create(message.from_user.id)
        await session.commit()

    if user.language_code is None:
        await message.answer(t(None, "choose_language"), reply_markup=language_keyboard())
        return

    await message.answer(t(user.language_code, "start"), parse_mode="Markdown")


@router.message(Command("language"))
async def language(message: Message) -> None:
    await message.answer(t(None, "choose_language"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("language:"))
async def choose_language(
    callback: CallbackQuery,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if callback.from_user is None or callback.data is None:
        return

    language_code = callback.data.split(":", 1)[1]
    async with db_sessionmaker() as session:
        users = UserRepository(session)
        user = await users.set_language(callback.from_user.id, language_code)
        await session.commit()

    if callback.message is not None:
        await setup_chat_commands(callback.bot, callback.message.chat.id, user.language_code)
        await callback.message.edit_text(t(user.language_code, "language_saved"), parse_mode="Markdown")
    await callback.answer()
