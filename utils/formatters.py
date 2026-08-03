"""
utils/formatters.py
-------------------
Language-aware message formatters.

Every public function accepts a `lang` parameter ('en' or 'fa') and
returns HTML text in the correct language.  Handlers never build
message strings themselves — they always call these helpers.
"""

from locales import t


def _title(recipe: dict, lang: str) -> str:
    """Return the recipe title in the requested language."""
    return recipe.get(f"title_{lang}") or recipe.get("title_en", "")


def _ingredients(recipe: dict, lang: str) -> list[str]:
    return recipe.get(f"ingredients_{lang}") or recipe.get("ingredients_en", [])


def _steps(recipe: dict, lang: str) -> list[str]:
    return recipe.get(f"steps_{lang}") or recipe.get("steps_en", [])


def _field(recipe: dict, key: str, lang: str) -> str:
    """Return a bilingual scalar field, falling back to English."""
    return recipe.get(f"{key}_{lang}") or recipe.get(f"{key}_en", "")


# ── Public formatters ─────────────────────────────────────────────────────────

def format_recipe_card(recipe: dict, lang: str = "en") -> str:
    """
    Full recipe card: metadata + ingredients list.

    Shown when a user taps a recipe title.
    Step-by-step view is handled by format_cooking_step().
    """
    title       = _title(recipe, lang)
    prep        = _field(recipe, "prep_time", lang)
    cook        = _field(recipe, "cook_time", lang)
    difficulty  = _field(recipe, "difficulty", lang)
    ingredients = _ingredients(recipe, lang)

    ing_lines = "\n".join(f"  • {ing}" for ing in ingredients)

    return (
        f"{recipe['emoji']} <b>{title}</b>\n"
        f"{'─' * 30}\n"
        f"{t('recipe_prep', lang)} {prep}   "
        f"{t('recipe_cook', lang)} {cook}\n"
        f"{t('recipe_difficulty', lang)} {difficulty}   "
        f"{t('recipe_serves', lang)} {recipe.get('servings', '—')}\n"
        f"{t('recipe_calories', lang)} {recipe.get('calories', '—')} kcal\n"
        f"{'─' * 30}\n"
        f"{t('recipe_ingredients', lang)}\n{ing_lines}\n"
        f"{'─' * 30}\n"
        f"{t('recipe_start_prompt', lang)}"
    )


def format_cooking_step(recipe: dict, step: int, lang: str = "en") -> str:
    """
    Single step card for step-by-step cooking mode.

    Args:
        recipe: Full recipe dict.
        step:   0-based step index.
        lang:   'en' or 'fa'.
    """
    steps = _steps(recipe, lang)
    total = len(steps)
    step  = max(0, min(step, total - 1))

    step_text = steps[step]
    title     = _title(recipe, lang)

    step_label = t("step_label", lang).format(current=step + 1, total=total)

    return (
        f"{recipe['emoji']} <b>{title}</b>\n"
        f"{'─' * 30}\n"
        f"{step_label}\n\n"
        f"{step_text}"
    )


def format_search_results(recipes: list[dict], query: str, lang: str = "en") -> str:
    """
    Header shown above search-result buttons.
    """
    if not recipes:
        return t("search_empty", lang).format(query=query)

    count = len(recipes)
    noun  = t("search_recipe", lang) if count == 1 else t("search_recipes", lang)
    return t("search_found", lang).format(count=count, noun=noun, query=query)


def format_favorites_list(recipes: list[dict], lang: str = "en") -> str:
    """
    Header shown above the favourites inline buttons.
    """
    if not recipes:
        return t("favorites_empty", lang)

    return t("favorites_count", lang).format(count=len(recipes))


def get_recipe_title(recipe: dict, lang: str = "en") -> str:
    """
    Convenience helper — returns just the display title.
    Used by keyboards that show recipe buttons.
    """
    return _title(recipe, lang)


def get_steps_count(recipe: dict) -> int:
    """Return the total number of steps (language-agnostic)."""
    return len(recipe.get("steps_en", []))
