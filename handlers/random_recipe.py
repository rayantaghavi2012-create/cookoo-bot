"""
handlers/random_recipe.py
--------------------------
Handles:
  /random command    → show a random recipe card
  menu:random button → show a random recipe card
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from services.recipe_service import get_random_recipe
from services.favorites_service import is_favorite
from services.user_service import get_user_lang
from utils.formatters import format_recipe_card
from keyboards.recipe_kb import recipe_detail_kb
from locales import t

router = Router()


async def _send_random(target: Message, user_id: int, lang: str, edit: bool = False) -> None:
    recipe = get_random_recipe()

    if not recipe:
        text   = t("random_empty", lang)
        markup = None
    else:
        favorited = is_favorite(user_id, recipe["id"])
        text      = format_recipe_card(recipe, lang)
        markup    = recipe_detail_kb(recipe["id"], favorited, lang)

    if edit:
        await target.edit_text(text, reply_markup=markup)
    else:
        await target.answer(text, reply_markup=markup)


@router.message(Command("random"))
async def cmd_random(message: Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await _send_random(message, message.from_user.id, lang, edit=False)


@router.callback_query(lambda c: c.data == "menu:random")
async def cb_random(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.answer(t("random_picking", lang))
    await _send_random(callback.message, callback.from_user.id, lang, edit=True)
