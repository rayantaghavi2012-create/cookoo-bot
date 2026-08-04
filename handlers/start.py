"""
handlers/start.py
-----------------
Handles:
  /start         → language gate (first time) or main menu (returning user)
  setlang:<code> → save language choice, show main menu
  menu:home      → return to main menu in the user's language
  menu:popular   → popular recipes list
"""

import logging
from html import escape

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.main_menu import language_select_kb, main_menu_kb
from services.user_service import get_user_lang, has_selected_language, set_user_lang
from services.recipe_service import get_popular_recipes
from utils.formatters import get_recipe_title
from locales import t

router = Router()
logger = logging.getLogger(__name__)


def _welcome_text(lang: str, first_name: str) -> str:
    """Render the HTML welcome message safely for Telegram."""
    return t("welcome", lang).format(name=escape(first_name))


# ── /start ─────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user_id    = message.from_user.id
    first_name = message.from_user.first_name or ""

    if not has_selected_language(user_id):
        # First visit — show language selection screen
        await message.answer(
            t("choose_language", "en"),   # bilingual prompt, always in EN
            reply_markup=language_select_kb(),
        )
    else:
        lang = get_user_lang(user_id)
        await message.answer(
            _welcome_text(lang, first_name),
            reply_markup=main_menu_kb(lang),
        )


# ── Language selection (from /start gate OR settings) ─────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("setlang:"))
async def cb_set_language(callback: CallbackQuery) -> None:
    lang       = callback.data.split(":", 1)[1]   # 'en' or 'fa'
    user_id    = callback.from_user.id

    if lang not in {"en", "fa"}:
        logger.warning("Rejected unsupported language callback: user_id=%s lang=%r", user_id, lang)
        await callback.answer()
        return

    try:
        set_user_lang(user_id, lang, callback.from_user.first_name or "")
        saved_lang = get_user_lang(user_id)
        menu_markup = main_menu_kb(saved_lang)

        logger.info(
            "Language selected: user_id=%s lang=%s message_id=%s keyboard=%s",
            user_id,
            saved_lang,
            callback.message.message_id,
            menu_markup.inline_keyboard,
        )
        await callback.message.answer(
            t("main_menu_title", saved_lang),
            reply_markup=menu_markup,
        )
        logger.info("Main menu sent: user_id=%s lang=%s", user_id, saved_lang)
    except TelegramAPIError:
        logger.exception("Telegram API failure while opening main menu: user_id=%s lang=%s", user_id, lang)
        raise
    except Exception:
        logger.exception("Failed to change language: user_id=%s lang=%s", user_id, lang)
        raise
    finally:
        # Always clear Telegram's callback progress indicator, even if sending fails.
        try:
            await callback.answer(t("language_set", lang), show_alert=False)
        except TelegramAPIError:
            logger.exception("Telegram API failure while answering callback: user_id=%s lang=%s", user_id, lang)


# ── Home (return to main menu) ─────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:home")
async def cb_home(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("main_menu_title", lang),
        reply_markup=main_menu_kb(lang),
    )
    await callback.answer()


# ── Popular Recipes ────────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:popular")
async def cb_popular(callback: CallbackQuery) -> None:
    lang    = get_user_lang(callback.from_user.id)
    recipes = get_popular_recipes(limit=6)

    if not recipes:
        await callback.answer(t("popular_empty", lang), show_alert=True)
        return

    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {get_recipe_title(recipe, lang)}",
                callback_data=f"recipe:{recipe['id']}",
            )
        )
    builder.row(InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"))

    await callback.message.edit_text(
        t("popular_title", lang),
        reply_markup=builder.as_markup(),
    )
    await callback.answer()
