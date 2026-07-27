"""
states/recipe_states.py
-----------------------
FSM state group for the step-by-step cooking flow.

The current step index is stored directly in the callback_data string
(cook:<recipe_id>:<step>), so no FSM state data is needed beyond
tracking that the user IS in cooking mode.  This group is kept here
as a clean extension point if richer per-user state is needed later
(e.g. a timer, a notes field, etc.).
"""

from aiogram.fsm.state import State, StatesGroup


class CookingStates(StatesGroup):
    # User is actively stepping through a recipe
    in_progress = State()
