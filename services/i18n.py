DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {"en", "ru"}

MESSAGES = {
    "en": {
        "choose_language": "Choose interface language / Выберите язык интерфейса:",
        "language_saved": "Done! Now send expenses like `coffee 250` or `taxi 800`.",
        "start": (
            "Hi! Send an expense like `coffee 250` or `taxi 800`.\n\n"
            "Commands:\n"
            "/summary - totals for today, week, and month\n"
            "/expenses - show and manage recent expenses\n"
            "/undo - delete the latest expense\n"
            "/language - change interface language"
        ),
        "no_expenses": "No expenses yet.",
        "history_title": "Recent expenses:",
        "history_item": "#{expense_id} | {date}\n{amount:.2f} - {description} ({category})",
        "edit_button": "Edit #{expense_id}",
        "delete_button": "Delete #{expense_id}",
        "edit_prompt": "Send the corrected expense, for example `coffee 250`. Use /cancel to stop editing.",
        "edit_cancelled": "Editing cancelled.",
        "expense_updated": "Expense #{expense_id} updated.",
        "expense_deleted": "Expense #{expense_id} deleted.",
        "expense_not_found": "This expense no longer exists.",
        "deleted_expense": "Deleted latest expense: {amount:.2f} - {description}",
        "expense_recorded": "Recorded {amount:.2f}: {description}, category: {category}",
        "summary": (
            "Summary\n"
            "Today: {today:.2f}\n"
            "This week: {week:.2f}\n"
            "This month: {month:.2f}"
        ),
        "default_description": "Expense",
        "expense_example": "Send an expense like `coffee 250`.",
        "expense_amount_missing": "I could not find the amount. Example: `coffee 250`.",
        "expense_amount_invalid": "The amount does not look valid.",
        "expense_amount_positive": "The amount must be greater than zero.",
        "category_cafe": "Cafe",
        "category_transport": "Transport",
        "category_groceries": "Groceries",
        "category_health": "Health",
        "category_entertainment": "Entertainment",
        "category_other": "Other",
    },
    "ru": {
        "choose_language": "Choose interface language / Выберите язык интерфейса:",
        "language_saved": "Готово! Теперь отправьте расход, например: `кофе 250` или `такси 800`.",
        "start": (
            "Привет! Отправьте расход, например: `кофе 250` или `такси 800`.\n\n"
            "Команды:\n"
            "/summary - расходы за день, неделю и месяц\n"
            "/expenses - показать и изменить последние расходы\n"
            "/undo - удалить последний расход\n"
            "/language - изменить язык интерфейса"
        ),
        "no_expenses": "Расходов пока нет.",
        "history_title": "Последние расходы:",
        "history_item": "#{expense_id} | {date}\n{amount:.2f} ₽ - {description} ({category})",
        "edit_button": "Изменить #{expense_id}",
        "delete_button": "Удалить #{expense_id}",
        "edit_prompt": "Отправьте исправленный расход, например `кофе 250`. Для отмены используйте /cancel.",
        "edit_cancelled": "Редактирование отменено.",
        "expense_updated": "Расход #{expense_id} изменён.",
        "expense_deleted": "Расход #{expense_id} удалён.",
        "expense_not_found": "Этот расход больше не существует.",
        "deleted_expense": "Удалил последний расход: {amount:.2f} ₽ - {description}",
        "expense_recorded": "Записал {amount:.2f} ₽: {description}, категория: {category}",
        "summary": (
            "Сводка\n"
            "Сегодня: {today:.2f} ₽\n"
            "За неделю: {week:.2f} ₽\n"
            "За месяц: {month:.2f} ₽"
        ),
        "default_description": "Расход",
        "expense_example": "Отправьте расход, например: `кофе 250`.",
        "expense_amount_missing": "Я не нашел сумму. Пример: `кофе 250`.",
        "expense_amount_invalid": "Сумма выглядит некорректно.",
        "expense_amount_positive": "Сумма должна быть больше нуля.",
        "category_cafe": "Кафе",
        "category_transport": "Транспорт",
        "category_groceries": "Продукты",
        "category_health": "Здоровье",
        "category_entertainment": "Развлечения",
        "category_other": "Другое",
    },
}


def normalize_language(language_code: str | None) -> str:
    if language_code in SUPPORTED_LANGUAGES:
        return language_code
    return DEFAULT_LANGUAGE


def t(language_code: str | None, key: str, **kwargs) -> str:
    language = normalize_language(language_code)
    template = MESSAGES[language].get(key, MESSAGES[DEFAULT_LANGUAGE][key])
    return template.format(**kwargs)


def category_title(language_code: str | None, category_code: str) -> str:
    normalized = category_code.casefold()
    if normalized in {"cafe", "transport", "groceries", "health", "entertainment", "other"}:
        return t(language_code, f"category_{normalized}")

    legacy_codes = {
        "cafe": "cafe",
        "transport": "transport",
        "groceries": "groceries",
        "health": "health",
        "entertainment": "entertainment",
        "other": "other",
    }
    return t(language_code, f"category_{legacy_codes.get(normalized, 'other')}")
