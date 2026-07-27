"""
handlers/search.py
------------------
Two-step search flow using FSM:

  1. User taps 🔍 Search  (or sends /search)
       → bot asks for a keyword
       → FSM enters SearchStates.waiting_for_query

  2. User types a keyword
       → service searches the catalogue
       → bot shows matching recipes as inline buttons
       → FSM is cleared
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.search_states import SearchStates
from services.search_service import search_recipes
from utils.formatters import format_search_results
from keyboards.main_menu import back_to_menu_kb

router = Router()


# ── Entry points ──────────────────────────────────────────────────────────────

@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext) -> None:
    """Triggered by /search command."""
    await _ask_for_query(message, state)


@router.callback_query(lambda c: c.data == "menu:search")
async def cb_search(callback: CallbackQuery, state: FSMContext) -> None:
    """Triggered by the 🔍 Search button in the main menu."""
    await callback.answer()
    await _ask_for_query(callback.message, state)


async def _ask_for_query(message: Message, state: FSMContext) -> None:
    """Edit/send the prompt and set the FSM state."""
    await state.set_state(SearchStates.waiting_for_query)
    await message.edit_text(
        "🔍 <b>Search Recipes</b>\n\n"
        "Type a recipe name or ingredient and I'll find it for you.\n\n"
        "<i>Examples: pizza, ghormeh, eggplant, falafel</i>",
        reply_markup=back_to_menu_kb(),
    )


# ── Receive the query ─────────────────────────────────────────────────────────

@router.message(SearchStates.waiting_for_query)
async def handle_search_query(message: Message, state: FSMContext) -> None:
    """Process the user's typed search query and show results."""
    await state.clear()

    query   = message.text.strip() if message.text else ""
    results = search_recipes(query)

    header = format_search_results(results, query)

    # Build a button for each matching recipe
    builder = InlineKeyboardBuilder()
    for recipe in results:
        builder.row(
            InlineKeyboardButton(
                text=f"{recipe['emoji']} {recipe['title']}",
                callback_data=f"recipe:{recipe['id']}",
            )
        )
    builder.row(
        InlineKeyboardButton(text="🔍 Search Again", callback_data="menu:search"),
        InlineKeyboardButton(text="🏠 Home",          callback_data="menu:home"),
    )

    await message.answer(header, reply_markup=builder.as_markup())
