"""
keyboards/main_menu.py
----------------------
Main menu and language-selection keyboards.
All button labels are resolved through the localization system.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import t


def language_select_kb() -> InlineKeyboardMarkup:
    """
    Shown on first /start — user must pick a language before
    seeing anything else.  Uses hardcoded strings because the
    user hasn't chosen a language yet.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇮🇷 فارسی",   callback_data="setlang:fa"),
        InlineKeyboardButton(text="🇺🇸 English",  callback_data="setlang:en"),
    )
    return builder.as_markup()


def main_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Return the root inline keyboard with all top-level feature buttons."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_cooking",  lang), callback_data="menu:cooking"),
        InlineKeyboardButton(text=t("btn_search",   lang), callback_data="menu:search"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_popular",  lang), callback_data="menu:popular"),
        InlineKeyboardButton(text=t("btn_favorites",lang), callback_data="menu:favorites"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_random",   lang), callback_data="menu:random"),
        InlineKeyboardButton(text=t("btn_guide",    lang), callback_data="menu:guide"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_settings", lang), callback_data="menu:settings"),
    )
    return builder.as_markup()


def back_to_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Single Home button reused across many screens."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home")
    )
    return builder.as_markup()
