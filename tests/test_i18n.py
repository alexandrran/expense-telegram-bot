from decimal import Decimal

from services.i18n import category_title, t
from services.report_service import build_summary


def test_translate_english_message() -> None:
    assert t("en", "category_cafe") == "Cafe"


def test_translate_russian_message() -> None:
    assert t("ru", "category_cafe") == "Кафе"


def test_translate_category_code() -> None:
    assert category_title("ru", "transport") == "Транспорт"


def test_build_russian_summary() -> None:
    summary = build_summary(
        {
            "today": Decimal("250.00"),
            "week": Decimal("1000.00"),
            "month": Decimal("3000.00"),
        },
        "ru",
    )

    assert "Сводка" in summary
    assert "Сегодня: 250.00 ₽" in summary
