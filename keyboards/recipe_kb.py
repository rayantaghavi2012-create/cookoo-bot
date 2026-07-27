"""
keyboards/recipe_kb.py
-----------------------
All keyboards related to recipe browsing:
  - cuisine category picker  (Iranian / Fast Food)
  - diet sub-category picker (Vegetarian / Non-Vegetarian)
  - recipe list
  - recipe detail actions
  - step-by-step navigation
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ── Category & sub-category ───────────────────────────────────────────────────

def cuisine_category_kb() -> InlineKeyboardMarkup:
    """Top-level cuisine picker: Iranian Food or Fast Food."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇮🇷 Iranian Food", callback_data="cuisine:iranian"),
        InlineKeyboardButton(text="🍔 Fast Food",      callback_data="cuisine:fastfood"),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home"),
    )
    return builder.as_markup()


def diet_category_kb(cuisine: str) -> InlineKeyboardMarkup:
    """
    Diet filter for a given cuisine.

    Args:
        cuisine: 'iranian' or 'fastfood' — embedded in callback_data
                 so the handler knows where to route back.
    """
    # Emoji differs slightly between cuisines for personality
    veg_emoji   = "🌱"
    meat_emoji  = "🍖" if cuisine == "iranian" else "🍗"

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f"{veg_emoji} Vegetarian",
            callback_data=f"diet:{cuisine}:vegetarian",
        ),
        InlineKeyboardButton(
            text=f"{meat_emoji} Non-Vegetarian",
            callback_data=f"diet:{cuisine}:non_vegetarian",
        ),
    )
    builder.row(
        InlineKeyboardButton(text="◀️ Back", callback_data="menu:cooking"),
        InlineKeyboardButton(text="🏠 Home",  callback_data="menu:home"),
    )
    return builder.as_markup()


# ── Recipe list ───────────────────────────────────────────────────────────────

def recipe_list_kb(recipes: list[dict], cuisine: str, diet: str) -> InlineKeyboardMarkup:
    """
    Show one button per recipe, then Back and Home.

    Args:
        recipes:  list of recipe dicts from recipes.json.
        cuisine:  used to build the back callback.
        diet:     used to build the back callback.
    """
    builder = InlineKeyboardBuilder()

    for recipe in recipes:
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {recipe['title']}",
                callback_data=f"recipe:{recipe['id']}",
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="◀️ Back",
            callback_data=f"cuisine:{cuisine}",
        ),
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home"),
    )
    return builder.as_markup()


# ── Recipe detail ─────────────────────────────────────────────────────────────

def recipe_detail_kb(recipe_id: str, is_favorite: bool) -> InlineKeyboardMarkup:
    """
    Actions shown below a full recipe card.

    Args:
        recipe_id:   used to build callback strings.
        is_favorite: toggles the heart button label.
    """
    fav_text = "💔 Remove Favorite" if is_favorite else "❤️ Add to Favorites"

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="👨‍🍳 Start Cooking",
            callback_data=f"cook:{recipe_id}:0",   # step index = 0
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=fav_text,
            callback_data=f"fav_toggle:{recipe_id}",
        ),
    )
    builder.row(
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home"),
    )
    return builder.as_markup()


# ── Step-by-step navigation ────────────────────────────────────────────────────

def cooking_steps_kb(recipe_id: str, step: int, total: int) -> InlineKeyboardMarkup:
    """
    Prev / Next / Home navigation for step-by-step cooking mode.

    Args:
        recipe_id: identifies which recipe is being cooked.
        step:      0-based current step index.
        total:     total number of steps in the recipe.
    """
    builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    # Previous — only if not on the first step
    if step > 0:
        buttons.append(
            InlineKeyboardButton(
                text="◀️ Previous",
                callback_data=f"cook:{recipe_id}:{step - 1}",
            )
        )

    # Next — only if not on the last step
    if step < total - 1:
        buttons.append(
            InlineKeyboardButton(
                text="Next ▶️",
                callback_data=f"cook:{recipe_id}:{step + 1}",
            )
        )

    builder.row(*buttons)
    builder.row(
        InlineKeyboardButton(
            text="📋 View Recipe",
            callback_data=f"recipe:{recipe_id}",
        ),
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home"),
    )
    return builder.as_markup()
