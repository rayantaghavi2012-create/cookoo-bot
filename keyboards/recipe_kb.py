"""
keyboards/recipe_kb.py
-----------------------
All keyboards for recipe browsing, detail view, and step-by-step cooking.
Every function accepts a `lang` parameter so labels are always localized.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales import t
from utils.formatters import get_recipe_title


# ── Category pickers ──────────────────────────────────────────────────────────

def cuisine_category_kb(lang: str = "en") -> InlineKeyboardMarkup:
    """Top-level cuisine picker: Iranian / Italian / Fast Food."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_iranian",  lang), callback_data="cuisine:iranian"),
        InlineKeyboardButton(text=t("btn_italian",  lang), callback_data="cuisine:italian"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_fastfood", lang), callback_data="cuisine:fastfood"),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


def diet_category_kb(cuisine: str, lang: str = "en") -> InlineKeyboardMarkup:
    """Vegetarian / Non-Vegetarian picker for a given cuisine."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=t("btn_vegetarian",     lang),
            callback_data=f"diet:{cuisine}:vegetarian",
        ),
        InlineKeyboardButton(
            text=t("btn_non_vegetarian", lang),
            callback_data=f"diet:{cuisine}:non_vegetarian",
        ),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:cooking"),
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


# ── Recipe list ───────────────────────────────────────────────────────────────

def recipe_list_kb(
    recipes: list[dict],
    cuisine: str,
    diet: str,
    lang: str = "en",
) -> InlineKeyboardMarkup:
    """One button per recipe plus Back / Home."""
    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {get_recipe_title(recipe, lang)}",
                callback_data=f"recipe:{recipe['id']}",
            )
        )
    builder.row(
        InlineKeyboardButton(
            text=t("btn_back", lang),
            callback_data=f"cuisine:{cuisine}",
        ),
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


# ── Recipe detail ─────────────────────────────────────────────────────────────

def recipe_detail_kb(
    recipe_id: str,
    is_favorite: bool,
    lang: str = "en",
) -> InlineKeyboardMarkup:
    """Start Cooking + Favorite toggle + Home."""
    fav_key = "btn_remove_favorite" if is_favorite else "btn_add_favorite"
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=t("btn_start_cooking", lang),
            callback_data=f"cook:{recipe_id}:0",
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=t(fav_key, lang),
            callback_data=f"fav_toggle:{recipe_id}",
        ),
    )
    builder.row(
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()


# ── Step-by-step navigation ────────────────────────────────────────────────────

def cooking_steps_kb(
    recipe_id: str,
    step: int,
    total: int,
    lang: str = "en",
) -> InlineKeyboardMarkup:
    """Previous / Next / View Recipe / Home for step-by-step cooking."""
    builder  = InlineKeyboardBuilder()
    nav_btns: list[InlineKeyboardButton] = []

    if step > 0:
        nav_btns.append(InlineKeyboardButton(
            text=t("btn_previous", lang),
            callback_data=f"cook:{recipe_id}:{step - 1}",
        ))
    if step < total - 1:
        nav_btns.append(InlineKeyboardButton(
            text=t("btn_next", lang),
            callback_data=f"cook:{recipe_id}:{step + 1}",
        ))

    if nav_btns:
        builder.row(*nav_btns)

    builder.row(
        InlineKeyboardButton(
            text=t("btn_view_recipe", lang),
            callback_data=f"recipe:{recipe_id}",
        ),
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="menu:home"),
    )
    return builder.as_markup()
