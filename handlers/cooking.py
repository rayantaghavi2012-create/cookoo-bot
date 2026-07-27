"""
handlers/cooking.py
-------------------
Handles the full recipe browsing and step-by-step cooking flow:

  menu:cooking
    → cuisine_category_kb()          (Iranian / Fast Food)
  cuisine:<cuisine>
    → diet_category_kb(cuisine)      (Vegetarian / Non-Vegetarian)
  diet:<cuisine>:<diet>
    → recipe_list_kb(recipes, …)     (list of recipe buttons)
  recipe:<id>
    → format_recipe_card()           (full recipe detail)
  cook:<id>:<step>
    → format_cooking_step()          (one step at a time)
  fav_toggle:<id>
    → toggle_favorite()              (handled inline here for speed)
"""

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.main_menu import main_menu_kb
from keyboards.recipe_kb import (
    cuisine_category_kb,
    diet_category_kb,
    recipe_list_kb,
    recipe_detail_kb,
    cooking_steps_kb,
)
from services.recipe_service import get_recipes_by_category, get_recipe_by_id
from services.favorites_service import is_favorite, toggle_favorite
from utils.formatters import format_recipe_card, format_cooking_step

router = Router()


# ── Step 1 — cuisine picker ────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:cooking")
async def cb_cooking(callback: CallbackQuery) -> None:
    """Show the cuisine category keyboard."""
    await callback.message.edit_text(
        "🍽 <b>Start Cooking</b>\n\nChoose a cuisine:",
        reply_markup=cuisine_category_kb(),
    )
    await callback.answer()


# ── Step 2 — diet picker ───────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("cuisine:"))
async def cb_cuisine(callback: CallbackQuery) -> None:
    """Show the vegetarian / non-vegetarian picker for a cuisine."""
    cuisine = callback.data.split(":")[1]   # 'iranian' | 'fastfood'

    labels = {
        "iranian":  "🇮🇷 <b>Iranian Food</b>",
        "fastfood": "🍔 <b>Fast Food</b>",
    }
    header = labels.get(cuisine, "🍽 <b>Recipes</b>")

    await callback.message.edit_text(
        f"{header}\n\nChoose a diet preference:",
        reply_markup=diet_category_kb(cuisine),
    )
    await callback.answer()


# ── Step 3 — recipe list ───────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("diet:"))
async def cb_diet(callback: CallbackQuery) -> None:
    """Show the list of recipes for the selected cuisine + diet."""
    _, cuisine, diet = callback.data.split(":")   # diet:<cuisine>:<diet>

    recipes = get_recipes_by_category(cuisine, diet)

    diet_label = "🌱 Vegetarian" if diet == "vegetarian" else "🍖 Non-Vegetarian"

    if not recipes:
        await callback.answer("No recipes found for this selection.", show_alert=True)
        return

    await callback.message.edit_text(
        f"{diet_label} — <b>{cuisine.capitalize()} Recipes</b>\n\n"
        "Select a recipe to view:",
        reply_markup=recipe_list_kb(recipes, cuisine, diet),
    )
    await callback.answer()


# ── Step 4 — recipe detail ─────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("recipe:"))
async def cb_recipe_detail(callback: CallbackQuery) -> None:
    """Show the full recipe card with ingredients and action buttons."""
    recipe_id = callback.data.split(":", 1)[1]
    recipe    = get_recipe_by_id(recipe_id)

    if not recipe:
        await callback.answer("Recipe not found.", show_alert=True)
        return

    user_id   = callback.from_user.id
    favorited = is_favorite(user_id, recipe_id)

    await callback.message.edit_text(
        format_recipe_card(recipe),
        reply_markup=recipe_detail_kb(recipe_id, favorited),
    )
    await callback.answer()


# ── Step 5 — step-by-step cooking ─────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("cook:"))
async def cb_cooking_step(callback: CallbackQuery) -> None:
    """
    Display one cooking step at a time.

    callback.data format: cook:<recipe_id>:<step_index>
    """
    parts     = callback.data.split(":")
    recipe_id = parts[1]
    step      = int(parts[2])

    recipe = get_recipe_by_id(recipe_id)

    if not recipe:
        await callback.answer("Recipe not found.", show_alert=True)
        return

    total = len(recipe["steps"])

    # Guard against out-of-range step values
    step = max(0, min(step, total - 1))

    await callback.message.edit_text(
        format_cooking_step(recipe, step),
        reply_markup=cooking_steps_kb(recipe_id, step, total),
    )
    await callback.answer()


# ── Favourite toggle (also reachable from the detail screen) ──────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("fav_toggle:"))
async def cb_fav_toggle(callback: CallbackQuery) -> None:
    """Toggle a recipe in/out of the user's favourites, then refresh the card."""
    recipe_id = callback.data.split(":", 1)[1]
    recipe    = get_recipe_by_id(recipe_id)

    if not recipe:
        await callback.answer("Recipe not found.", show_alert=True)
        return

    user_id   = callback.from_user.id
    now_faved = toggle_favorite(user_id, recipe_id)

    toast = "❤️ Added to Favorites!" if now_faved else "💔 Removed from Favorites."
    await callback.answer(toast, show_alert=False)

    # Refresh the recipe card so the heart button label updates
    await callback.message.edit_text(
        format_recipe_card(recipe),
        reply_markup=recipe_detail_kb(recipe_id, now_faved),
    )
