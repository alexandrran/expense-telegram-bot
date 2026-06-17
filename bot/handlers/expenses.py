from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from db.repositories import ExpenseRepository, UserRepository
from services.category_matcher import match_category
from services.expense_parser import ExpenseParseError, parse_expense

router = Router()


@router.message(Command("undo"))
async def undo_last_expense(
    message: Message,
    db_sessionmaker: async_sessionmaker,
) -> None:
    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(message.from_user.id)
        deleted = await expenses.delete_last(user.id)
        await session.commit()

    if deleted is None:
        await message.answer("No expenses yet.")
        return

    await message.answer(f"Deleted latest expense: {deleted.amount:.2f} - {deleted.description}")


@router.message()
async def add_expense(
    message: Message,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if message.text is None or message.from_user is None:
        return

    try:
        parsed = parse_expense(message.text)
    except ExpenseParseError as error:
        await message.answer(str(error))
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(message.from_user.id)
        category = match_category(parsed.description)
        expense = await expenses.create(
            user_id=user.id,
            amount=parsed.amount,
            description=parsed.description,
            category_name=category,
        )
        await session.commit()

    await message.answer(
        f"Recorded {expense.amount:.2f}: {expense.description}, category: {expense.category_name}"
    )
