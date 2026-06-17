from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re


class ExpenseParseError(ValueError):
    pass


@dataclass(frozen=True)
class ParsedExpense:
    amount: Decimal
    description: str


AMOUNT_PATTERN = re.compile(r"(?<!\w)(\d+(?:[.,]\d{1,2})?)(?!\w)")


def parse_expense(text: str) -> ParsedExpense:
    normalized = text.strip()
    if not normalized:
        raise ExpenseParseError("Send an expense like `coffee 250`.")

    match = AMOUNT_PATTERN.search(normalized)
    if match is None:
        raise ExpenseParseError("I could not find the amount. Example: `coffee 250`.")

    raw_amount = match.group(1).replace(",", ".")
    try:
        amount = Decimal(raw_amount).quantize(Decimal("0.01"))
    except InvalidOperation as exc:
        raise ExpenseParseError("The amount does not look valid.") from exc

    if amount <= 0:
        raise ExpenseParseError("The amount must be greater than zero.")

    description = (normalized[: match.start()] + normalized[match.end() :]).strip()
    description = re.sub(r"\s+", " ", description)
    if not description:
        description = "Expense"

    return ParsedExpense(amount=amount, description=description)
