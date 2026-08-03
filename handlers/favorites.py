"""
handlers/favorites.py
---------------------
Handles:
  /favorites command    → show saved recipes
  menu:favorites button → show saved recipes
  fav_remove:<id>       → remove from favourites and refresh list
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.favorites_service import get_favorite_recipes, remove_favorite
from services.user_service import get_user_lang
from utils.formatters import format_favorites_list, get_recipe_title
from locales import t

router = Router()


async def _show_favorites(target: Message, user_id: int, lang: str, edit: bool = False) -> None:
    recipes = get_favorite_recipes(user_id)
    header  = format_favorites_list(recipes, lang)

    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {get_recipe_title(recipe, lang)}",
                callback_data=f"recipe:{recipe['id']}",
            ),
            InlineKeyboardButton(
                text="🗑",
                callback_data=f"fav_remove:{recipe['id']}",
            ),
        )
    builder.row(InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"))

    markup = builder.as_markup()
    if edit:
        await target.edit_text(header, reply_markup=markup)
    else:
        await target.answer(header, reply_markup=markup)


@router.message(Command("favorites"))
async def cmd_favorites(message: Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await _show_favorites(message, message.from_user.id, lang, edit=False)


@router.callback_query(lambda c: c.data == "menu:favorites")
async def cb_favorites(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.answer()
    await _show_favorites(callback.message, callback.from_user.id, lang, edit=True)


@router.callback_query(lambda c: c.data and c.data.startswith("fav_remove:"))
async def cb_fav_remove(callback: CallbackQuery) -> None:
    recipe_id = callback.data.split(":", 1)[1]
    user_id   = callback.from_user.id
    lang      = get_user_lang(user_id)

    removed = remove_favorite(user_id, recipe_id)
    await callback.answer(
        t("fav_removed", lang) if removed else t("fav_already_removed", lang),
        show_alert=False,
    )
    await _show_favorites(callback.message, user_id, lang, edit=True)
