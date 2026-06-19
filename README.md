# Expense Telegram Bot

Telegram bot for personal expense tracking. The bot lets a user choose English or Russian interface language, add expenses with natural messages like `coffee 250` or `кофе 250`, manage recent records, and view a short summary.

## Features

- Add an expense from a plain text message.
- Auto-detect basic categories by keywords.
- Choose English or Russian interface language.
- View the 10 most recent expenses.
- Edit or delete a selected expense with inline buttons.
- View totals for today, this week, and this month.
- Delete the latest expense.
- Store data in SQLite through SQLAlchemy async ORM.

## Tech Stack

- Python 3.11+
- aiogram 3
- SQLAlchemy 2
- SQLite
- pytest

## Quick Start

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Copy `.env.example` to `.env` and set `BOT_TOKEN`.
4. Run the bot:

```bash
python -m bot.main
```

5. Run tests:

```bash
pytest
```

## Commands

- `/start` - show greeting and usage examples.
- `/language` - change interface language.
- `/expenses` - show, edit, or delete recent expenses.
- `/summary` - show totals for today, week, and month.
- `/undo` - delete the last expense.

## Example

```text
User: coffee 250
Bot: Recorded 250.00: coffee, category: Cafe
```

```text
User: кофе 250
Bot: Записал 250.00 ₽: кофе, категория: Кафе
```
