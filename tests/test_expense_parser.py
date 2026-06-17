from decimal import Decimal

import pytest

from services.expense_parser import ExpenseParseError, parse_expense


def test_parse_expense_description_then_amount() -> None:
    parsed = parse_expense("coffee 250")

    assert parsed.amount == Decimal("250.00")
    assert parsed.description == "coffee"


def test_parse_expense_amount_then_description() -> None:
    parsed = parse_expense("1200 groceries")

    assert parsed.amount == Decimal("1200.00")
    assert parsed.description == "groceries"


def test_parse_expense_decimal_comma() -> None:
    parsed = parse_expense("latte 4,50")

    assert parsed.amount == Decimal("4.50")
    assert parsed.description == "latte"


def test_parse_expense_uses_default_description() -> None:
    parsed = parse_expense("500")

    assert parsed.amount == Decimal("500.00")
    assert parsed.description == "Expense"


def test_parse_expense_without_amount() -> None:
    with pytest.raises(ExpenseParseError):
        parse_expense("coffee")
