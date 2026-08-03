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


def get_popular_recipes(limit: int = 6) -> list[dict]:
    """
    Return a curated selection of popular recipes spread across all cuisines.

    Uses round-robin across the three cuisines so Iranian, Italian, and
    Fast Food are all represented — even when limit is small.

    Args:
        limit: Maximum number of recipes to return.

    Returns:
        List of recipe dicts.
    """
    all_recipes = _load_all()
    cuisines    = ("iranian", "italian", "fastfood")

    # Bucket recipes by cuisine first
    buckets: dict[str, list[dict]] = {c: [] for c in cuisines}
    for recipe in all_recipes:
        cat = recipe.get("category", "")
        if cat in buckets:
            buckets[cat].append(recipe)

    # Round-robin: take one from each cuisine in turns until limit reached
    result: list[dict] = []
    indices = {c: 0 for c in cuisines}

    while len(result) < limit:
        added_any = False
        for cuisine in cuisines:
            if len(result) >= limit:
                break
            idx = indices[cuisine]
            if idx < len(buckets[cuisine]):
                result.append(buckets[cuisine][idx])
                indices[cuisine] = idx + 1
                added_any = True
        if not added_any:
            break  # All buckets exhausted

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
