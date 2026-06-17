from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re


class ExpenseParseError(ValueError):
    def __init__(self, message_key: str) -> None:
        self.message_key = message_key
        super().__init__(message_key)


@dataclass(frozen=True)
class ParsedExpense:
    amount: Decimal
    description: str


AMOUNT_PATTERN = re.compile(r"(?<!\w)(\d+(?:[.,]\d{1,2})?)(?!\w)")


def parse_expense(text: str, default_description: str = "Expense") -> ParsedExpense:
    normalized = text.strip()
    if not normalized:
        raise ExpenseParseError("expense_example")

    match = AMOUNT_PATTERN.search(normalized)
    if match is None:
        raise ExpenseParseError("expense_amount_missing")

    raw_amount = match.group(1).replace(",", ".")
    try:
        amount = Decimal(raw_amount).quantize(Decimal("0.01"))
    except InvalidOperation as exc:
        raise ExpenseParseError("expense_amount_invalid") from exc

    if amount <= 0:
        raise ExpenseParseError("expense_amount_positive")

    description = (normalized[: match.start()] + normalized[match.end() :]).strip()
    description = re.sub(r"\s+", " ", description)
    if not description:
        description = default_description

    return ParsedExpense(amount=amount, description=description)
