"""
services/search_service.py
--------------------------
Full-text recipe search over the in-memory catalogue.

Matching strategy (case-insensitive, partial):
  - Recipe title
  - Category / sub-category labels
  - Ingredient names

This is intentionally simple.  When PostgreSQL is introduced, replace
the body of `search_recipes` with a parameterised SQL ILIKE query —
the handler won't need to change at all.
"""

from services.recipe_service import get_all_recipes


def search_recipes(query: str) -> list[dict]:
    """
    Search the recipe catalogue for *query*.

    Args:
        query: Raw text typed by the user.  Leading/trailing whitespace
               is stripped and the comparison is case-insensitive.

    Returns:
        List of matching recipe dicts, ordered as they appear in the
        catalogue.  Empty list if nothing matches or query is blank.
    """
    query = query.strip().lower()

    if not query:
        return []

    results: list[dict] = []

    for recipe in get_all_recipes():
        # Build a single searchable blob for this recipe
        searchable = " ".join([
            recipe.get("title", ""),
            recipe.get("category", ""),
            recipe.get("subcategory", ""),
            " ".join(recipe.get("ingredients", [])),
        ]).lower()

        if query in searchable:
            results.append(recipe)

    return results
