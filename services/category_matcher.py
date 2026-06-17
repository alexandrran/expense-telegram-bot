DEFAULT_CATEGORY = "other"

CATEGORY_KEYWORDS = {
    "cafe": {
        "coffee",
        "latte",
        "cafe",
        "restaurant",
        "lunch",
        "dinner",
        "food",
        "кофе",
        "латте",
        "кафе",
        "ресторан",
        "обед",
        "ужин",
        "еда",
    },
    "transport": {
        "taxi",
        "uber",
        "bus",
        "metro",
        "train",
        "fuel",
        "такси",
        "автобус",
        "метро",
        "поезд",
        "бензин",
    },
    "groceries": {
        "market",
        "groceries",
        "milk",
        "bread",
        "eggs",
        "магазин",
        "продукты",
        "молоко",
        "хлеб",
        "яйца",
    },
    "health": {"pharmacy", "doctor", "medicine", "аптека", "врач", "лекарства"},
    "entertainment": {
        "cinema",
        "movie",
        "game",
        "concert",
        "кино",
        "фильм",
        "игра",
        "концерт",
    },
}


def match_category(description: str) -> str:
    normalized = description.casefold()
    words = set(normalized.split())

    for category, keywords in CATEGORY_KEYWORDS.items():
        if words & keywords:
            return category

    return DEFAULT_CATEGORY
