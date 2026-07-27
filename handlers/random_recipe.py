"""
handlers/random_recipe.py
--------------------------
Handles:
  - /random command    → show a random recipe
  - menu:random button → show a random recipe
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from services.recipe_service import get_random_recipe
from services.favorites_service import is_favorite
from utils.formatters import format_recipe_card
from keyboards.recipe_kb import recipe_detail_kb

router = Router()


async def _send_random(target: Message, user_id: int, edit: bool = False) -> None:
    """
    Pick a random recipe and render it.

    Args:
        target:  Message to edit or reply to.
        user_id: Used to check favourites status for the toggle button.
        edit:    If True, edit the existing message; otherwise send a new one.
    """
    recipe = get_random_recipe()

    if not recipe:
        text   = "😕 No recipes in the catalogue yet."
        markup = None
    else:
        favorited = is_favorite(user_id, recipe["id"])
        text      = format_recipe_card(recipe)
        markup    = recipe_detail_kb(recipe["id"], favorited)

    if edit:
        await target.edit_text(text, reply_markup=markup)
    else:
        await target.answer(text, reply_markup=markup)


# ── /random command ────────────────────────────────────────────────────────────

@router.message(Command("random"))
async def cmd_random(message: Message) -> None:
    await _send_random(message, user_id=message.from_user.id, edit=False)


# ── menu:random button ─────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:random")
async def cb_random(callback: CallbackQuery) -> None:
    await callback.answer("🎲 Picking a random recipe…")
    await _send_random(callback.message, user_id=callback.from_user.id, edit=True)
