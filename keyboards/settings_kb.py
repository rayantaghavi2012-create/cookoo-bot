"""
keyboards/settings_kb.py
------------------------
Keyboards for the Settings section, fully localized.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import t


def settings_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Main settings menu."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_change_language", lang), callback_data="settings:language"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_notifications",   lang), callback_data="settings:notifications"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


def language_select_settings_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Language picker shown inside Settings → Change Language."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇺🇸 English", callback_data="setlang:en"),
        InlineKeyboardButton(text="🇮🇷 فارسی",   callback_data="setlang:fa"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:settings"),
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


def notifications_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Notification toggle (placeholder)."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_notif_enable",  lang), callback_data="notif:on"),
        InlineKeyboardButton(text=t("btn_notif_disable", lang), callback_data="notif:off"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:settings"),
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()
