"""
handlers/favorites.py
---------------------
Handles:
  - /favorites command     → show saved recipes
  - menu:favorites button  → show saved recipes
  - fav_remove:<id>        → remove a recipe from favourites inline

The fav_toggle (add/remove from the recipe detail screen) is handled
in cooking.py to keep the recipe card refresh logic together.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.favorites_service import get_favorite_recipes, remove_favorite
from utils.formatters import format_favorites_list

router = Router()


# ── Shared rendering helper ────────────────────────────────────────────────────

async def _show_favorites(target: Message, user_id: int, edit: bool = False) -> None:
    """
    Render the favourites list into *target* (a Message object).

    Args:
        target: The message to edit or reply to.
        user_id: Telegram user ID whose favourites we display.
        edit:    If True, edit the existing message; otherwise send a new one.
    """
    recipes = get_favorite_recipes(user_id)
    header  = format_favorites_list(recipes)

    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        # Each saved recipe gets a view button and a remove button on the same row
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {recipe['title']}",
                callback_data=f"recipe:{recipe['id']}",
            ),
            InlineKeyboardButton(
                text="🗑",
                callback_data=f"fav_remove:{recipe['id']}",
            ),
        )
    builder.row(
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home")
    )

    markup = builder.as_markup()

    if edit:
        await target.edit_text(header, reply_markup=markup)
    else:
        await target.answer(header, reply_markup=markup)


# ── /favorites command ─────────────────────────────────────────────────────────

@router.message(Command("favorites"))
async def cmd_favorites(message: Message) -> None:
    await _show_favorites(message, user_id=message.from_user.id, edit=False)


# ── menu:favorites button ──────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:favorites")
async def cb_favorites(callback: CallbackQuery) -> None:
    await callback.answer()
    await _show_favorites(callback.message, user_id=callback.from_user.id, edit=True)


# ── Inline remove button (🗑) ──────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("fav_remove:"))
async def cb_fav_remove(callback: CallbackQuery) -> None:
    """Remove a recipe from favourites and refresh the list."""
    recipe_id = callback.data.split(":", 1)[1]
    user_id   = callback.from_user.id

    removed = remove_favorite(user_id, recipe_id)

    if removed:
        await callback.answer("💔 Removed from Favorites.", show_alert=False)
    else:
        await callback.answer("Already removed.", show_alert=False)

    # Refresh the favourites list in place
    await _show_favorites(callback.message, user_id=user_id, edit=True)
