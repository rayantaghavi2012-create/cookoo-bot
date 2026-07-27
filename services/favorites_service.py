"""
services/favorites_service.py
------------------------------
Per-user favourites management backed by favorites.json.

Storage schema:
  {
    "<telegram_user_id>": ["recipe_id_1", "recipe_id_2", ...],
    ...
  }

All user IDs are stored as strings because JSON keys are always strings.
"""

import config
from utils.json_storage import read_json, write_json
from services.recipe_service import get_recipe_by_id


def _load() -> dict:
    """Load the full favourites map from disk."""
    return read_json(config.FAVORITES_FILE)


def _save(data: dict) -> None:
    """Persist the favourites map to disk."""
    write_json(config.FAVORITES_FILE, data)


def _key(user_id: int) -> str:
    """Normalise a Telegram user ID to a JSON-safe string key."""
    return str(user_id)


# ── Public API ────────────────────────────────────────────────────────────────

def get_favorite_ids(user_id: int) -> list[str]:
    """
    Return the list of recipe IDs saved by this user.

    Args:
        user_id: Telegram user ID.

    Returns:
        List of recipe ID strings (may be empty).
    """
    data = _load()
    return data.get(_key(user_id), [])


def get_favorite_recipes(user_id: int) -> list[dict]:
    """
    Return the full recipe dicts for every recipe the user has saved.
    Silently skips any IDs that no longer exist in the catalogue.

    Args:
        user_id: Telegram user ID.

    Returns:
        List of recipe dicts.
    """
    ids = get_favorite_ids(user_id)
    recipes = []
    for rid in ids:
        recipe = get_recipe_by_id(rid)
        if recipe:
            recipes.append(recipe)
    return recipes


def is_favorite(user_id: int, recipe_id: str) -> bool:
    """
    Check whether a recipe is in the user's favourites.

    Args:
        user_id:   Telegram user ID.
        recipe_id: Recipe string ID.

    Returns:
        True if the recipe is saved, False otherwise.
    """
    return recipe_id in get_favorite_ids(user_id)


def add_favorite(user_id: int, recipe_id: str) -> bool:
    """
    Add a recipe to the user's favourites.

    Args:
        user_id:   Telegram user ID.
        recipe_id: Recipe string ID.

    Returns:
        True if the recipe was added, False if it was already saved.
    """
    data = _load()
    key  = _key(user_id)

    if key not in data:
        data[key] = []

    if recipe_id in data[key]:
        return False  # Already a favourite — no change

    data[key].append(recipe_id)
    _save(data)
    return True


def remove_favorite(user_id: int, recipe_id: str) -> bool:
    """
    Remove a recipe from the user's favourites.

    Args:
        user_id:   Telegram user ID.
        recipe_id: Recipe string ID.

    Returns:
        True if the recipe was removed, False if it wasn't saved.
    """
    data = _load()
    key  = _key(user_id)

    if key not in data or recipe_id not in data[key]:
        return False  # Nothing to remove

    data[key].remove(recipe_id)
    _save(data)
    return True


def toggle_favorite(user_id: int, recipe_id: str) -> bool:
    """
    Add the recipe if it isn't saved; remove it if it is.

    Args:
        user_id:   Telegram user ID.
        recipe_id: Recipe string ID.

    Returns:
        True  → recipe is now a favourite (was added).
        False → recipe is no longer a favourite (was removed).
    """
    if is_favorite(user_id, recipe_id):
        remove_favorite(user_id, recipe_id)
        return False
    else:
        add_favorite(user_id, recipe_id)
        return True
