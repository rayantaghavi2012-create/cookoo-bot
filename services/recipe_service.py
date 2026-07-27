"""
services/recipe_service.py
--------------------------
All read operations on the recipe catalogue.

This service is the single source of truth for recipe data.
Handlers never read recipes.json directly — they always go through
this module.  When PostgreSQL is added, only this file changes.
"""

import random
from typing import Optional

import config
from utils.json_storage import read_json


def _load_all() -> list[dict]:
    """Load the full recipe list from the JSON file."""
    data = read_json(config.RECIPES_FILE)
    return data.get("recipes", [])


# ── Queries ───────────────────────────────────────────────────────────────────

def get_all_recipes() -> list[dict]:
    """Return every recipe in the catalogue."""
    return _load_all()


def get_recipe_by_id(recipe_id: str) -> Optional[dict]:
    """
    Find and return a single recipe by its unique string id.

    Args:
        recipe_id: e.g. 'ghormeh_sabzi'

    Returns:
        The recipe dict, or None if not found.
    """
    for recipe in _load_all():
        if recipe["id"] == recipe_id:
            return recipe
    return None


def get_recipes_by_category(cuisine: str, diet: str) -> list[dict]:
    """
    Filter recipes by cuisine category and diet sub-category.

    Args:
        cuisine: 'iranian' or 'fastfood'
        diet:    'vegetarian' or 'non_vegetarian'

    Returns:
        List of matching recipe dicts (may be empty).
    """
    return [
        r for r in _load_all()
        if r["category"] == cuisine and r["subcategory"] == diet
    ]


def get_popular_recipes(limit: int = 4) -> list[dict]:
    """
    Return a curated list of popular recipes.

    For now this returns the first *limit* recipes from each cuisine
    as a simple stand-in.  Replace with view-count logic later.

    Args:
        limit: Maximum number of recipes to return.

    Returns:
        List of recipe dicts.
    """
    all_recipes = _load_all()
    # Simple heuristic: pick one from each category until we hit the limit
    seen_ids: set[str] = set()
    result: list[dict] = []

    # Two passes — iranian first, then fastfood — for variety
    for cuisine in ("iranian", "fastfood"):
        for recipe in all_recipes:
            if recipe["category"] == cuisine and recipe["id"] not in seen_ids:
                result.append(recipe)
                seen_ids.add(recipe["id"])
                if len(result) >= limit:
                    return result

    return result


def get_random_recipe() -> Optional[dict]:
    """
    Return a single recipe chosen at random from the full catalogue.

    Returns:
        A recipe dict, or None if the catalogue is empty.
    """
    all_recipes = _load_all()
    if not all_recipes:
        return None
    return random.choice(all_recipes)
