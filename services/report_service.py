from decimal import Decimal

from services.i18n import t


def build_summary(totals: dict[str, Decimal], language_code: str) -> str:
    return t(
        language_code,
        "summary",
        today=totals["today"],
        week=totals["week"],
        month=totals["month"],
    )
