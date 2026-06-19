from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

DEFAULT_COMMANDS = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="language", description="Change interface language"),
    BotCommand(command="summary", description="Show expense summary"),
    BotCommand(command="expenses", description="Show and manage recent expenses"),
    BotCommand(command="undo", description="Delete the latest expense"),
]

RU_COMMANDS = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="language", description="Изменить язык"),
    BotCommand(command="summary", description="Показать сводку расходов"),
    BotCommand(command="expenses", description="Показать последние расходы"),
    BotCommand(command="undo", description="Удалить последний расход"),
]


def commands_for_language(language_code: str | None) -> list[BotCommand]:
    if language_code == "ru":
        return RU_COMMANDS
    return DEFAULT_COMMANDS


async def setup_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(DEFAULT_COMMANDS)
    await bot.set_my_commands(RU_COMMANDS, language_code="ru")


async def setup_chat_commands(bot: Bot, chat_id: int, language_code: str | None) -> None:
    await bot.set_my_commands(
        commands_for_language(language_code),
        scope=BotCommandScopeChat(chat_id=chat_id),
    )
