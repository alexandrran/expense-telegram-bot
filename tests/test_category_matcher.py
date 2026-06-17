from services.category_matcher import match_category


def test_match_category_english_keyword() -> None:
    assert match_category("coffee") == "cafe"


def test_match_category_russian_keyword() -> None:
    assert match_category("такси") == "transport"


def test_match_category_unknown_keyword() -> None:
    assert match_category("notebook") == "other"
