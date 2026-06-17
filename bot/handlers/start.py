from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Hi! Send an expense like `coffee 250` or `taxi 800`.\n\n"
        "Commands:\n"
        "/summary - totals for today, week, and month\n"
        "/undo - delete the latest expense",
        parse_mode="Markdown",
    )
