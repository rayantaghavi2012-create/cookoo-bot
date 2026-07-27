"""
main.py
-------
Entry point for the Cookoo Telegram Cooking Bot.

Registers all routers, sets the bot commands menu, and starts
long-polling. All configuration is loaded from the .env file.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import config
from handlers import (
    start,
    cooking,
    search,
    favorites,
    random_recipe,
    guide,
    settings,
)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot) -> None:
    """Register the visible command menu shown in the Telegram client."""
    commands = [
        BotCommand(command="start", description="🏠 Main menu"),
        BotCommand(command="search", description="🔍 Search recipes"),
        BotCommand(command="favorites", description="❤️ My favorites"),
        BotCommand(command="random", description="🎲 Random recipe"),
        BotCommand(command="guide", description="📖 Cooking guide"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    logger.info("Starting Cookoo Bot…")

    # ── Bot & Dispatcher ──────────────────────────────────────────────────────
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # MemoryStorage is fine for FSM while we don't have Redis yet.
    dp = Dispatcher(storage=MemoryStorage())

    # ── Register routers (order matters for overlapping filters) ──────────────
    dp.include_router(start.router)
    dp.include_router(cooking.router)
    dp.include_router(search.router)
    dp.include_router(favorites.router)
    dp.include_router(random_recipe.router)
    dp.include_router(guide.router)
    dp.include_router(settings.router)

    # ── Bot command menu ──────────────────────────────────────────────────────
    await set_bot_commands(bot)

    # ── Start polling ─────────────────────────────────────────────────────────
    logger.info("Bot is running. Press Ctrl+C to stop.")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
