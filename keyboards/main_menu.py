"""
keyboards/main_menu.py
----------------------
Main menu inline keyboard shown after /start.
Each button carries a callback_data string that the handlers listen for.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb() -> InlineKeyboardMarkup:
    """Return the root inline keyboard with all top-level features."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="🍽 Start Cooking",    callback_data="menu:cooking"),
        InlineKeyboardButton(text="🔍 Search",            callback_data="menu:search"),
    )
    builder.row(
        InlineKeyboardButton(text="⭐ Popular Recipes",  callback_data="menu:popular"),
        InlineKeyboardButton(text="❤️ Favorites",         callback_data="menu:favorites"),
    )
    builder.row(
        InlineKeyboardButton(text="🎲 Random Recipe",    callback_data="menu:random"),
        InlineKeyboardButton(text="📖 Cooking Guide",    callback_data="menu:guide"),
    )
    builder.row(
        InlineKeyboardButton(text="⚙️ Settings",          callback_data="menu:settings"),
    )

    return builder.as_markup()


def back_to_menu_kb() -> InlineKeyboardMarkup:
    """Single 'Back to Menu' button — reused across many screens."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home")
    )
    return builder.as_markup()
