"""
handlers/settings.py
--------------------
Handles:
  - menu:settings        → settings main menu
  - settings:language    → language picker (placeholder)
  - settings:notifications → notification toggle (placeholder)
  - lang:<code>          → language selection response
  - notif:<on|off>       → notification toggle response
"""

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.settings_kb import settings_menu_kb, language_kb, notifications_kb

router = Router()


# ── Settings menu ──────────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:settings")
async def cb_settings(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "⚙️ <b>Settings</b>\n\nChoose an option:",
        reply_markup=settings_menu_kb(),
    )
    await callback.answer()


# ── Language ───────────────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "settings:language")
async def cb_language_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🌐 <b>Language</b>\n\n"
        "Select your preferred language.\n"
        "<i>(Multi-language support coming soon)</i>",
        reply_markup=language_kb(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("lang:"))
async def cb_language_select(callback: CallbackQuery) -> None:
    lang = callback.data.split(":")[1]
    names = {"en": "🇬🇧 English", "fa": "🇮🇷 فارسی"}
    selected = names.get(lang, lang)

    await callback.answer(f"Language set to {selected} ✅", show_alert=True)
    # After acknowledging, return to the settings menu
    await callback.message.edit_text(
        "⚙️ <b>Settings</b>\n\nChoose an option:",
        reply_markup=settings_menu_kb(),
    )


# ── Notifications ──────────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "settings:notifications")
async def cb_notifications_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🔔 <b>Notifications</b>\n\n"
        "Would you like to receive daily recipe suggestions?\n"
        "<i>(Notification delivery coming soon)</i>",
        reply_markup=notifications_kb(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("notif:"))
async def cb_notification_toggle(callback: CallbackQuery) -> None:
    state = callback.data.split(":")[1]
    label = "✅ Notifications enabled!" if state == "on" else "❌ Notifications disabled."

    await callback.answer(label, show_alert=True)
    await callback.message.edit_text(
        "⚙️ <b>Settings</b>\n\nChoose an option:",
        reply_markup=settings_menu_kb(),
    )
