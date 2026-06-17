DEFAULT_CATEGORY = "Other"

CATEGORY_KEYWORDS = {
    "Cafe": {"coffee", "latte", "cafe", "restaurant", "lunch", "dinner", "food"},
    "Transport": {"taxi", "uber", "bus", "metro", "train", "fuel"},
    "Groceries": {"market", "groceries", "milk", "bread", "eggs"},
    "Health": {"pharmacy", "doctor", "medicine"},
    "Entertainment": {"cinema", "movie", "game", "concert"},
}


def match_category(description: str) -> str:
    normalized = description.casefold()
    words = set(normalized.split())

    for category, keywords in CATEGORY_KEYWORDS.items():
        if words & keywords:
            return category

    return DEFAULT_CATEGORY
