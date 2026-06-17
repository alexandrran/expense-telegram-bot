from decimal import Decimal


def build_summary(totals: dict[str, Decimal]) -> str:
    return (
        "Summary\n"
        f"Today: {totals['today']:.2f}\n"
        f"This week: {totals['week']:.2f}\n"
        f"This month: {totals['month']:.2f}"
    )
