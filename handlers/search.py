"""
handlers/search.py
------------------
Two-step FSM search flow:

  1. User taps 🔍 Search (or sends /search)
       → bot asks for a keyword (in user's language)
       → FSM enters SearchStates.waiting_for_query

  2. User types a keyword (either EN or FA)
       → service searches both language fields
       → bot shows matching recipes
       → FSM cleared
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.search_states import SearchStates
from services.search_service import search_recipes
from services.user_service import get_user_lang
from utils.formatters import format_search_results, get_recipe_title
from keyboards.main_menu import back_to_menu_kb
from locales import t

router = Router()


async def _ask_for_query(message: Message, state: FSMContext, lang: str) -> None:
    await state.set_state(SearchStates.waiting_for_query)
    await message.edit_text(
        t("search_prompt", lang),
        reply_markup=back_to_menu_kb(lang),
    )


@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext) -> None:
    lang = get_user_lang(message.from_user.id)
    # /search is a new message, not a callback — send instead of edit
    await state.set_state(SearchStates.waiting_for_query)
    await message.answer(
        t("search_prompt", lang),
        reply_markup=back_to_menu_kb(lang),
    )


@router.callback_query(lambda c: c.data == "menu:search")
async def cb_search(callback: CallbackQuery, state: FSMContext) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.answer()
    await _ask_for_query(callback.message, state, lang)


@router.message(SearchStates.waiting_for_query)
async def handle_search_query(message: Message, state: FSMContext) -> None:
    await state.clear()
    lang    = get_user_lang(message.from_user.id)
    query   = message.text.strip() if message.text else ""
    results = search_recipes(query)
    header  = format_search_results(results, query, lang)

    builder = InlineKeyboardBuilder()
    for recipe in results:
        builder.row(InlineKeyboardButton(
            text=f"{recipe['emoji']} {get_recipe_title(recipe, lang)}",
            callback_data=f"recipe:{recipe['id']}",
        ))
    builder.row(
        InlineKeyboardButton(text=t("btn_search_again", lang), callback_data="menu:search"),
        InlineKeyboardButton(text=t("btn_home",         lang), callback_data="menu:home"),
    )
    await message.answer(header, reply_markup=builder.as_markup())
