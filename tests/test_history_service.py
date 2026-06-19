from datetime import datetime
from decimal import Decimal

from db.models import Expense
from services.history_service import build_expense_history


def test_build_expense_history() -> None:
    expense = Expense(
        id=7,
        user_id=1,
        amount=Decimal("250.00"),
        description="coffee",
        category_name="cafe",
        spent_at=datetime(2026, 6, 19, 14, 30),
    )

    history = build_expense_history([expense], "en")

    assert "Recent expenses:" in history
    assert "#7 | 19.06.2026 14:30" in history
    assert "250.00 - coffee (Cafe)" in history
