"""
handlers/cooking.py
-------------------
Full recipe browsing and step-by-step cooking flow.

Callback chain:
  menu:cooking
    → cuisine_category_kb()        (Iranian / Italian / Fast Food)
  cuisine:<cuisine>
    → diet_category_kb(cuisine)    (Vegetarian / Non-Vegetarian)
  diet:<cuisine>:<diet>
    → recipe_list_kb(recipes, …)   (list of recipe buttons)
  recipe:<id>
    → format_recipe_card()         (full recipe detail)
  cook:<id>:<step>
    → format_cooking_step()        (one step at a time)
  fav_toggle:<id>
    → toggle_favorite()            (inline toggle from detail screen)
"""

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.recipe_kb import (
    cuisine_category_kb,
    diet_category_kb,
    recipe_list_kb,
    recipe_detail_kb,
    cooking_steps_kb,
)
from services.recipe_service import get_recipes_by_category, get_recipe_by_id
from services.favorites_service import is_favorite, toggle_favorite
from services.user_service import get_user_lang
from utils.formatters import format_recipe_card, format_cooking_step, get_steps_count
from locales import t

router = Router()


# ── Step 1 — cuisine picker ────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:cooking")
async def cb_cooking(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("start_cooking_title", lang),
        reply_markup=cuisine_category_kb(lang),
    )
    await callback.answer()


# ── Step 2 — diet picker ───────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("cuisine:"))
async def cb_cuisine(callback: CallbackQuery) -> None:
    cuisine = callback.data.split(":")[1]
    lang    = get_user_lang(callback.from_user.id)

    cuisine_label_key = f"cuisine_{cuisine}"   # e.g. "cuisine_iranian"
    cuisine_label = t(cuisine_label_key, lang)

    await callback.message.edit_text(
        t("diet_title", lang).format(cuisine=cuisine_label),
        reply_markup=diet_category_kb(cuisine, lang),
    )
    await callback.answer()


# ── Step 3 — recipe list ───────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("diet:"))
async def cb_diet(callback: CallbackQuery) -> None:
    _, cuisine, diet = callback.data.split(":")
    lang    = get_user_lang(callback.from_user.id)
    recipes = get_recipes_by_category(cuisine, diet)

    if not recipes:
        await callback.answer(t("no_recipes", lang), show_alert=True)
        return

    cuisine_label = t(f"cuisine_{cuisine}", lang)
    diet_label    = t(f"diet_{diet}", lang)

    await callback.message.edit_text(
        t("recipe_list_title", lang).format(cuisine=cuisine_label, diet=diet_label),
        reply_markup=recipe_list_kb(recipes, cuisine, diet, lang),
    )
    await callback.answer()


# ── Step 4 — recipe detail ─────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("recipe:"))
async def cb_recipe_detail(callback: CallbackQuery) -> None:
    recipe_id = callback.data.split(":", 1)[1]
    lang      = get_user_lang(callback.from_user.id)
    recipe    = get_recipe_by_id(recipe_id)

    if not recipe:
        await callback.answer(t("recipe_not_found", lang), show_alert=True)
        return

    favorited = is_favorite(callback.from_user.id, recipe_id)
    await callback.message.edit_text(
        format_recipe_card(recipe, lang),
        reply_markup=recipe_detail_kb(recipe_id, favorited, lang),
    )
    await callback.answer()


# ── Step 5 — step-by-step cooking ─────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("cook:"))
async def cb_cooking_step(callback: CallbackQuery) -> None:
    parts     = callback.data.split(":")
    recipe_id = parts[1]
    try:
        step = int(parts[2])
    except (IndexError, ValueError):
        step = 0
    lang      = get_user_lang(callback.from_user.id)
    recipe    = get_recipe_by_id(recipe_id)

    if not recipe:
        await callback.answer(t("recipe_not_found", lang), show_alert=True)
        return

    total = get_steps_count(recipe)
    step  = max(0, min(step, total - 1))

    await callback.message.edit_text(
        format_cooking_step(recipe, step, lang),
        reply_markup=cooking_steps_kb(recipe_id, step, total, lang),
    )
    await callback.answer()


# ── Favourite toggle ───────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("fav_toggle:"))
async def cb_fav_toggle(callback: CallbackQuery) -> None:
    recipe_id = callback.data.split(":", 1)[1]
    lang      = get_user_lang(callback.from_user.id)
    recipe    = get_recipe_by_id(recipe_id)

    if not recipe:
        await callback.answer(t("recipe_not_found", lang), show_alert=True)
        return

    now_faved = toggle_favorite(callback.from_user.id, recipe_id)
    toast_key = "added_to_favorites" if now_faved else "removed_from_favorites"
    await callback.answer(t(toast_key, lang), show_alert=False)

    await callback.message.edit_text(
        format_recipe_card(recipe, lang),
        reply_markup=recipe_detail_kb(recipe_id, now_faved, lang),
    )
