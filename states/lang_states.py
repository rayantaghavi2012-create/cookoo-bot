"""
states/lang_states.py
---------------------
FSM state group for the initial language selection screen.

Flow:
  /start (no saved lang)  →  LangStates.choosing  →  user taps a button
  lang:<code> callback    →  language saved        →  FSM cleared → main menu
"""

from aiogram.fsm.state import State, StatesGroup


class LangStates(StatesGroup):
    # Waiting for the user to tap a language button
    choosing = State()
