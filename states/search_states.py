"""
states/search_states.py
-----------------------
FSM state group for the recipe search flow.

Flow:
  1. User taps 🔍 Search  →  bot asks for a keyword  →  SearchStates.waiting_for_query
  2. User types a keyword  →  handler runs the search  →  FSM cleared
"""

from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    # Waiting for the user to type a search keyword
    waiting_for_query = State()
