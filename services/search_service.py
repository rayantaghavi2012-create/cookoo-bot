"""
services/search_service.py
--------------------------
Bilingual full-text recipe search.

Searches across English AND Persian fields simultaneously, so a user
typing either language will find the correct recipe.

Matching strategy (case-insensitive, partial match):
  - title_en, title_fa
  - ingredients_en (joined), ingredients_fa (joined)
  - category, subcategory
"""

from services.recipe_service import get_all_recipes


def search_recipes(query: str) -> list[dict]:
    """
    Search the recipe catalogue for *query* in both languages.

    Args:
        query: Raw text from the user (any language).

    Returns:
        List of matching recipe dicts, preserving catalogue order.
        Empty list if query is blank or nothing matches.
    """
    query = query.strip().lower()
    if not query:
        return []

    results: list[dict] = []

    for recipe in get_all_recipes():
        # Build one searchable blob from all text fields in both languages
        searchable = " ".join(filter(None, [
            recipe.get("title_en", ""),
            recipe.get("title_fa", ""),
            recipe.get("category", ""),
            recipe.get("subcategory", ""),
            " ".join(recipe.get("ingredients_en", [])),
            " ".join(recipe.get("ingredients_fa", [])),
        ])).lower()

        if query in searchable:
            results.append(recipe)

    return results
