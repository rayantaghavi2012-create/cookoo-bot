"""
main.py
-------
Entry point for the Cookoo Telegram Cooking Bot.

Registers all routers, sets the bot command menu, and starts
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
    """Register the visible command list shown in the Telegram client."""
    commands = [
        BotCommand(command="start",     description="🏠 Main menu / Language selection"),
        BotCommand(command="search",    description="🔍 Search recipes"),
        BotCommand(command="favorites", description="❤️ My favorites"),
        BotCommand(command="random",    description="🎲 Random recipe"),
        BotCommand(command="guide",     description="📖 Cooking guide"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    logger.info("Starting Cookoo Bot…")

    # ── Bot & Dispatcher ──────────────────────────────────────────────────────
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    # MemoryStorage handles FSM (search state, etc.)
    dp = Dispatcher(storage=MemoryStorage())

    # ── Register routers ──────────────────────────────────────────────────────
    # Order matters: start.py owns setlang: and menu:home callbacks — it must
    # be registered before any handler that also listens to overlapping prefixes.
    dp.include_router(start.router)       # /start, setlang:, menu:home, menu:popular
    dp.include_router(cooking.router)     # menu:cooking, cuisine:, diet:, recipe:, cook:, fav_toggle:
    dp.include_router(search.router)      # /search, menu:search, FSM query handler
    dp.include_router(favorites.router)   # /favorites, menu:favorites, fav_remove:
    dp.include_router(random_recipe.router)  # /random, menu:random
    dp.include_router(guide.router)       # /guide, menu:guide, guide:
    dp.include_router(settings.router)    # menu:settings, settings:, notif:

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
