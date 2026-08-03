"""
keyboards/guide_kb.py
---------------------
Keyboards for the Cooking Guide section, fully localized.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import t


def guide_menu_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Top-level guide topic picker."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_guide_knife", lang), callback_data="guide:knife"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_guide_tips",  lang), callback_data="guide:tips"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_guide_subs",  lang), callback_data="guide:substitutions"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


def guide_back_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Back-to-guide + Home buttons shown at the bottom of every article."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_back_to_guide", lang), callback_data="menu:guide"),
        InlineKeyboardButton(text=t("btn_home",           lang), callback_data="menu:home"),
    )
    return builder.as_markup()
