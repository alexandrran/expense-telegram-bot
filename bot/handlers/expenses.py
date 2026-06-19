from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.keyboards.expenses import expense_history_keyboard
from bot.keyboards.language import language_keyboard
from db.models import Expense
from db.repositories import ExpenseRepository, UserRepository
from services.category_matcher import match_category
from services.expense_parser import ExpenseParseError, parse_expense
from services.history_service import build_expense_history
from services.i18n import category_title, t

router = Router()
HISTORY_LIMIT = 10


class EditExpense(StatesGroup):
    waiting_for_value = State()


def _expense_id_from_callback(data: str | None) -> int | None:
    if data is None:
        return None
    try:
        return int(data.rsplit(":", 1)[1])
    except (IndexError, ValueError):
        return None


async def _refresh_history_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    expenses: list[Expense],
    language_code: str | None,
) -> None:
    text = (
        build_expense_history(expenses, language_code)
        if expenses
        else t(language_code, "no_expenses")
    )
    keyboard = expense_history_keyboard(expenses, language_code) if expenses else None
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard,
        )
    except TelegramBadRequest:
        # The history message may have been deleted while the user was editing.
        return


@router.message(EditExpense.waiting_for_value, Command("cancel"))
async def cancel_expense_edit(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    language_code = (await state.get_data()).get("language_code")
    await state.clear()
    await message.answer(t(language_code, "edit_cancelled"))


@router.message(EditExpense.waiting_for_value)
async def save_expense_edit(
    message: Message,
    state: FSMContext,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if message.text is None or message.from_user is None:
        return

    state_data = await state.get_data()
    expense_id = state_data.get("expense_id")
    if not isinstance(expense_id, int):
        await state.clear()
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(message.from_user.id)

        try:
            parsed = parse_expense(
                message.text,
                default_description=t(user.language_code, "default_description"),
            )
        except ExpenseParseError as error:
            await message.answer(t(user.language_code, error.message_key), parse_mode="Markdown")
            return

        updated = await expenses.update(
            user_id=user.id,
            expense_id=expense_id,
            amount=parsed.amount,
            description=parsed.description,
            category_name=match_category(parsed.description),
        )
        recent_expenses = await expenses.list_recent(user.id, HISTORY_LIMIT)
        await session.commit()

    await state.clear()
    if updated is None:
        await message.answer(t(user.language_code, "expense_not_found"))
        return

    await message.answer(t(user.language_code, "expense_updated", expense_id=expense_id))

    history_chat_id = state_data.get("history_chat_id")
    history_message_id = state_data.get("history_message_id")
    if isinstance(history_chat_id, int) and isinstance(history_message_id, int):
        await _refresh_history_message(
            message.bot,
            history_chat_id,
            history_message_id,
            recent_expenses,
            user.language_code,
        )


@router.message(Command("expenses"))
async def show_expenses(
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

        recent_expenses = await expenses.list_recent(user.id, HISTORY_LIMIT)
        await session.commit()

    if not recent_expenses:
        await message.answer(t(user.language_code, "no_expenses"))
        return

    await message.answer(
        build_expense_history(recent_expenses, user.language_code),
        reply_markup=expense_history_keyboard(recent_expenses, user.language_code),
    )


@router.callback_query(F.data.startswith("expense:edit:"))
async def begin_expense_edit(
    callback: CallbackQuery,
    state: FSMContext,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if callback.from_user is None or callback.message is None:
        await callback.answer()
        return

    expense_id = _expense_id_from_callback(callback.data)
    if expense_id is None:
        await callback.answer()
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(callback.from_user.id)
        expense = await expenses.get_by_id(user.id, expense_id)
        await session.commit()

    if expense is None:
        await callback.answer(t(user.language_code, "expense_not_found"), show_alert=True)
        return

    await state.set_state(EditExpense.waiting_for_value)
    await state.set_data(
        {
            "expense_id": expense_id,
            "history_chat_id": callback.message.chat.id,
            "history_message_id": callback.message.message_id,
            "language_code": user.language_code,
        }
    )
    await callback.bot.send_message(
        callback.message.chat.id,
        t(user.language_code, "edit_prompt"),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("expense:delete:"))
async def delete_expense(
    callback: CallbackQuery,
    db_sessionmaker: async_sessionmaker,
) -> None:
    if callback.from_user is None or callback.message is None:
        await callback.answer()
        return

    expense_id = _expense_id_from_callback(callback.data)
    if expense_id is None:
        await callback.answer()
        return

    async with db_sessionmaker() as session:
        users = UserRepository(session)
        expenses = ExpenseRepository(session)
        user = await users.get_or_create(callback.from_user.id)
        deleted = await expenses.delete_by_id(user.id, expense_id)
        recent_expenses = await expenses.list_recent(user.id, HISTORY_LIMIT)
        await session.commit()

    if deleted is None:
        await callback.answer(t(user.language_code, "expense_not_found"), show_alert=True)
        return

    await _refresh_history_message(
        callback.bot,
        callback.message.chat.id,
        callback.message.message_id,
        recent_expenses,
        user.language_code,
    )
    await callback.answer(t(user.language_code, "expense_deleted", expense_id=expense_id))


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
