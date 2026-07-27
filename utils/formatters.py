"""
utils/formatters.py
-------------------
Pure functions that turn recipe dicts into nicely formatted HTML
strings for Telegram messages.

Keeping formatting logic here means handlers stay clean and any
change to message layout only needs to be made in one place.
"""


def format_recipe_card(recipe: dict) -> str:
    """
    Full recipe card shown when a user taps a recipe from the list.

    Includes all metadata and the full ingredients list.
    Does NOT include steps — those are shown one at a time by
    format_cooking_step().

    Args:
        recipe: A single recipe dict loaded from recipes.json.

    Returns:
        HTML-formatted string ready to send as a Telegram message.
    """
    ingredients = "\n".join(f"  • {ing}" for ing in recipe["ingredients"])

    return (
        f"{recipe['emoji']} <b>{recipe['title']}</b>\n"
        f"{'─' * 30}\n"
        f"⏱ <b>Prep:</b> {recipe['prep_time']}   "
        f"🍳 <b>Cook:</b> {recipe['cook_time']}\n"
        f"📊 <b>Difficulty:</b> {recipe['difficulty']}   "
        f"🍽 <b>Serves:</b> {recipe['servings']}\n"
        f"{'─' * 30}\n"
        f"🛒 <b>Ingredients:</b>\n{ingredients}\n"
        f"{'─' * 30}\n"
        f"👆 Tap <b>Start Cooking</b> to follow the steps one by one."
    )


def format_cooking_step(recipe: dict, step: int) -> str:
    """
    Single step card shown during step-by-step cooking mode.

    Args:
        recipe: Full recipe dict.
        step:   0-based index of the current step.

    Returns:
        HTML-formatted step message.
    """
    total = len(recipe["steps"])
    step_text = recipe["steps"][step]

    return (
        f"{recipe['emoji']} <b>{recipe['title']}</b>\n"
        f"{'─' * 30}\n"
        f"📍 <b>Step {step + 1} of {total}</b>\n\n"
        f"{step_text}"
    )


def format_search_results(recipes: list[dict], query: str) -> str:
    """
    Header message shown above search result buttons.

    Args:
        recipes: List of matching recipe dicts (may be empty).
        query:   The search string typed by the user.

    Returns:
        HTML-formatted string.
    """
    if not recipes:
        return (
            f"😕 No recipes found for <b>\"{query}\"</b>.\n\n"
            "Try a different keyword, like <i>pizza</i>, <i>ghormeh</i>, or <i>kuku</i>."
        )

    count = len(recipes)
    noun  = "recipe" if count == 1 else "recipes"
    return (
        f"🔍 Found <b>{count} {noun}</b> for <b>\"{query}\"</b>:\n\n"
        "Tap a recipe below to view it."
    )


def format_favorites_list(recipes: list[dict]) -> str:
    """
    Header message shown above the favourites inline buttons.

    Args:
        recipes: List of recipe dicts the user has saved.

    Returns:
        HTML-formatted string.
    """
    if not recipes:
        return (
            "❤️ <b>Your Favorites</b>\n\n"
            "You haven't saved any recipes yet.\n"
            "Browse recipes and tap <b>❤️ Add to Favorites</b> to save them here."
        )

    return (
        f"❤️ <b>Your Favorites</b>  ({len(recipes)} saved)\n\n"
        "Tap a recipe to view it:"
    )
