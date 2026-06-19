from collections.abc import Sequence

from db.models import Expense
from services.i18n import category_title, t


def build_expense_history(
    expenses: Sequence[Expense],
    language_code: str | None,
) -> str:
    lines = [t(language_code, "history_title")]
    for expense in expenses:
        lines.append(
            t(
                language_code,
                "history_item",
                expense_id=expense.id,
                date=expense.spent_at.strftime("%d.%m.%Y %H:%M"),
                amount=expense.amount,
                description=expense.description,
                category=category_title(language_code, expense.category_name),
            )
        )
    return "\n\n".join(lines)
