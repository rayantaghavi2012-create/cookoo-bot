"""
keyboards/settings_kb.py
------------------------
Keyboards for the Settings section.
These are placeholders — the actual logic will be wired up in a later phase.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_menu_kb() -> InlineKeyboardMarkup:
    """Main settings menu."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🌐 Language",       callback_data="settings:language"),
    )
    builder.row(
        InlineKeyboardButton(text="🔔 Notifications",  callback_data="settings:notifications"),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Home",            callback_data="menu:home"),
    )
    return builder.as_markup()


def language_kb() -> InlineKeyboardMarkup:
    """Language selection placeholder."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇬🇧 English",  callback_data="lang:en"),
        InlineKeyboardButton(text="🇮🇷 فارسی",    callback_data="lang:fa"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data="menu:settings"),
        InlineKeyboardButton(text="🏠 Home",  callback_data="menu:home"),
    )
    return builder.as_markup()


def notifications_kb() -> InlineKeyboardMarkup:
    """Notification toggle placeholder."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Enable",  callback_data="notif:on"),
        InlineKeyboardButton(text="❌ Disable", callback_data="notif:off"),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data="menu:settings"),
        InlineKeyboardButton(text="🏠 Home",  callback_data="menu:home"),
    )
    return builder.as_markup()
