from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.keyboards.language import language_keyboard
from db.repositories import ExpenseRepository, UserRepository
from services.category_matcher import match_category
from services.expense_parser import ExpenseParseError, parse_expense
from services.i18n import category_title, t

router = Router()


@router.message(Command("undo"))
async def undo_last_expense(
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

        deleted = await expenses.delete_last(user.id)
        await session.commit()

    if deleted is None:
        await message.answer(t(user.language_code, "no_expenses"))
        return

    await message.answer(
        t(
            user.language_code,
            "deleted_expense",
            amount=deleted.amount,
            description=deleted.description,
        )
    )


@router.message()
async def add_expense(
    message: Message,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if message.text is None or message.from_user is None:
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(message.from_user.id)
        if user.language_code is None:
            await session.commit()
            await message.answer(t(None, "choose_language"), reply_markup=language_keyboard())
            return

        try:
            parsed = parse_expense(
                message.text,
                default_description=t(user.language_code, "default_description"),
            )
        except ExpenseParseError as error:
            await message.answer(t(user.language_code, error.message_key), parse_mode="Markdown")
            return

        category = match_category(parsed.description)
        expense = await expenses.create(
            user_id=user.id,
            amount=parsed.amount,
            description=parsed.description,
            category_name=category,
        )
        await session.commit()

    await message.answer(
        t(
            user.language_code,
            "expense_recorded",
            amount=expense.amount,
            description=expense.description,
            category=category_title(user.language_code, expense.category_name),
        )
    )
