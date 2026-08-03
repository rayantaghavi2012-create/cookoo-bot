"""
handlers/settings.py
--------------------
Handles:
  menu:settings           → settings main menu
  settings:language       → Change Language screen
  settings:notifications  → notification toggle (placeholder)
  notif:<on|off>          → notification toggle response

Note: language change is handled by setlang: in handlers/start.py,
which is shared between the initial gate and settings. This handler
only shows the language picker screen — the actual save happens in start.py.
"""

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.settings_kb import settings_menu_kb, language_select_settings_kb, notifications_kb
from services.user_service import get_user_lang
from locales import t

router = Router()


@router.callback_query(lambda c: c.data == "menu:settings")
async def cb_settings(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t("settings_title", lang), reply_markup=settings_menu_kb(lang))
    await callback.answer()


@router.callback_query(lambda c: c.data == "settings:language")
async def cb_language_menu(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("change_language_title", lang),
        reply_markup=language_select_settings_kb(lang),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "settings:notifications")
async def cb_notifications_menu(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t("notif_title", lang), reply_markup=notifications_kb(lang))
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("notif:"))
async def cb_notification_toggle(callback: CallbackQuery) -> None:
    lang  = get_user_lang(callback.from_user.id)
    state = callback.data.split(":")[1]
    label = t("notif_enabled", lang) if state == "on" else t("notif_disabled", lang)
    await callback.answer(label, show_alert=True)
    await callback.message.edit_text(t("settings_title", lang), reply_markup=settings_menu_kb(lang))
