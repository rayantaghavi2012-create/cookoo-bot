"""
handlers/start.py
-----------------
Handles:
  - /start command  → welcome message + main menu
  - menu:home       → return to main menu from anywhere
  - menu:popular    → popular recipes list
"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.main_menu import main_menu_kb
from keyboards.recipe_kb import recipe_list_kb
from services.recipe_service import get_popular_recipes

router = Router()


# ── /start ────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Greet the user and show the main menu."""
    first_name = message.from_user.first_name or "Chef"
    await message.answer(
        f"👨‍🍳 Welcome to <b>Cookoo Cooking Bot</b>, {first_name}!\n\n"
        "Discover recipes, follow step-by-step cooking guides, "
        "save your favourites, and more.\n\n"
        "What would you like to do?",
        reply_markup=main_menu_kb(),
    )


# ── Home (return to main menu) ─────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:home")
async def cb_home(callback: CallbackQuery) -> None:
    """Edit the current message back to the main menu."""
    await callback.message.edit_text(
        "🏠 <b>Main Menu</b>\n\nWhat would you like to do?",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


# ── Popular Recipes ────────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data == "menu:popular")
async def cb_popular(callback: CallbackQuery) -> None:
    """Show a hand-picked selection of popular recipes."""
    recipes = get_popular_recipes(limit=4)

    if not recipes:
        await callback.answer("No recipes available yet.", show_alert=True)
        return

    # Build the keyboard — no specific cuisine/diet back-navigation needed here
    # so we reuse recipe_list_kb with a generic back target that goes home
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.types import InlineKeyboardButton

    builder = InlineKeyboardBuilder()
    for recipe in recipes:
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {recipe['title']}",
                callback_data=f"recipe:{recipe['id']}",
            )
        )
    builder.row(
        InlineKeyboardButton(text="🏠 Home", callback_data="menu:home")
    )

    await callback.message.edit_text(
        "⭐ <b>Popular Recipes</b>\n\nHere are some crowd favourites:",
        reply_markup=builder.as_markup(),
    )
    await callback.answer()
