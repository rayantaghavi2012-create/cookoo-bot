"""
keyboards/guide_kb.py
---------------------
Keyboards for the Cooking Guide section.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def guide_menu_kb() -> InlineKeyboardMarkup:
    """Top-level guide topic picker."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔪 Knife Skills",             callback_data="guide:knife"),
    )
    builder.row(
        InlineKeyboardButton(text="💡 Cooking Tips",             callback_data="guide:tips"),
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Ingredient Substitutions", callback_data="guide:substitutions"),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home"),
    )
    return builder.as_markup()


def guide_back_kb() -> InlineKeyboardMarkup:
    """Back button used at the bottom of every guide article."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="◀️ Back to Guide", callback_data="menu:guide"),
        InlineKeyboardButton(text="🏠 Home",           callback_data="menu:home"),
    )
    return builder.as_markup()
