from collections.abc import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.models import Expense
from services.i18n import t


def expense_history_keyboard(
    expenses: Sequence[Expense],
    language_code: str | None,
) -> InlineKeyboardMarkup:
    rows = []
    for expense in expenses:
        rows.append(
            [
                InlineKeyboardButton(
                    text=t(language_code, "edit_button", expense_id=expense.id),
                    callback_data=f"expense:edit:{expense.id}",
                ),
                InlineKeyboardButton(
                    text=t(language_code, "delete_button", expense_id=expense.id),
                    callback_data=f"expense:delete:{expense.id}",
                ),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)
