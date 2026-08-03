"""
locales/en.py
-------------
All English UI strings for the Cookoo Bot.
Keys are snake_case identifiers shared between locales.
"""

STRINGS: dict[str, str] = {

    # ── Language selection ────────────────────────────────────────────────────
    "choose_language":      "🌐 <b>Welcome!</b>\n\nPlease choose your language:",
    "lang_btn_en":          "🇺🇸 English",
    "lang_btn_fa":          "🇮🇷 فارسی",
    "language_set":         "🇺🇸 Language set to English!",

    # ── Welcome / home ────────────────────────────────────────────────────────
    "welcome":              "👨‍🍳 Welcome to <b>Cookoo Cooking Bot</b>, {name}!\n\n"
                            "Discover recipes, follow step-by-step guides,\n"
                            "save your favourites, and more.\n\n"
                            "What would you like to do?",
    "main_menu_title":      "🏠 <b>Main Menu</b>\n\nWhat would you like to do?",

    # ── Main menu buttons ─────────────────────────────────────────────────────
    "btn_cooking":          "🍽 Start Cooking",
    "btn_search":           "🔍 Search",
    "btn_popular":          "⭐ Popular Recipes",
    "btn_favorites":        "❤️ Favorites",
    "btn_random":           "🎲 Random Recipe",
    "btn_guide":            "📖 Cooking Guide",
    "btn_settings":         "⚙️ Settings",
    "btn_home":             "🏠 Home",
    "btn_back":             "◀️ Back",

    # ── Cooking / categories ──────────────────────────────────────────────────
    "start_cooking_title":  "🍽 <b>Start Cooking</b>\n\nChoose a cuisine:",
    "btn_iranian":          "🇮🇷 Iranian Food",
    "btn_italian":          "🍕 Italian Food",
    "btn_fastfood":         "🍔 Fast Food",
    "btn_vegetarian":       "🌱 Vegetarian",
    "btn_non_vegetarian":   "🍖 Non-Vegetarian",
    "diet_title":           "{cuisine}\n\nChoose a diet preference:",
    "recipe_list_title":    "{diet} — <b>{cuisine} Recipes</b>\n\nSelect a recipe to view:",
    "no_recipes":           "No recipes found for this selection.",

    # ── Cuisine labels (for display) ──────────────────────────────────────────
    "cuisine_iranian":      "🇮🇷 <b>Iranian Food</b>",
    "cuisine_italian":      "🍕 <b>Italian Food</b>",
    "cuisine_fastfood":     "🍔 <b>Fast Food</b>",
    "diet_vegetarian":      "🌱 Vegetarian",
    "diet_non_vegetarian":  "🍖 Non-Vegetarian",

    # ── Recipe detail ─────────────────────────────────────────────────────────
    "recipe_prep":          "⏱ <b>Prep:</b>",
    "recipe_cook":          "🍳 <b>Cook:</b>",
    "recipe_difficulty":    "📊 <b>Difficulty:</b>",
    "recipe_serves":        "🍽 <b>Serves:</b>",
    "recipe_calories":      "🔥 <b>Calories:</b>",
    "recipe_ingredients":   "🛒 <b>Ingredients:</b>",
    "recipe_start_prompt":  "👆 Tap <b>Start Cooking</b> to follow the steps one by one.",
    "btn_start_cooking":    "👨‍🍳 Start Cooking",
    "btn_add_favorite":     "❤️ Add to Favorites",
    "btn_remove_favorite":  "💔 Remove Favorite",
    "btn_view_recipe":      "📋 View Recipe",
    "recipe_not_found":     "Recipe not found.",
    "added_to_favorites":   "❤️ Added to Favorites!",
    "removed_from_favorites": "💔 Removed from Favorites.",

    # ── Cooking steps ─────────────────────────────────────────────────────────
    "step_label":           "📍 <b>Step {current} of {total}</b>",
    "btn_previous":         "◀️ Previous",
    "btn_next":             "Next ▶️",

    # ── Popular ───────────────────────────────────────────────────────────────
    "popular_title":        "⭐ <b>Popular Recipes</b>\n\nHere are some crowd favourites:",
    "popular_empty":        "No recipes available yet.",

    # ── Search ────────────────────────────────────────────────────────────────
    "search_prompt":        "🔍 <b>Search Recipes</b>\n\n"
                            "Type a recipe name or ingredient in <b>English or Persian</b>.\n\n"
                            "<i>Examples: pizza, ghormeh, pasta, کوکو</i>",
    "search_found":         "🔍 Found <b>{count} {noun}</b> for <b>\"{query}\"</b>:\n\n"
                            "Tap a recipe below to view it.",
    "search_recipe":        "recipe",
    "search_recipes":       "recipes",
    "search_empty":         "😕 No recipes found for <b>\"{query}\"</b>.\n\n"
                            "Try a different keyword.",
    "btn_search_again":     "🔍 Search Again",

    # ── Favorites ─────────────────────────────────────────────────────────────
    "favorites_title":      "❤️ <b>Your Favorites</b>",
    "favorites_count":      "❤️ <b>Your Favorites</b>  ({count} saved)\n\nTap a recipe to view it:",
    "favorites_empty":      "❤️ <b>Your Favorites</b>\n\n"
                            "You haven't saved any recipes yet.\n"
                            "Browse recipes and tap <b>❤️ Add to Favorites</b> to save them here.",
    "fav_removed":          "💔 Removed from Favorites.",
    "fav_already_removed":  "Already removed.",

    # ── Random ────────────────────────────────────────────────────────────────
    "random_picking":       "🎲 Picking a random recipe…",
    "random_empty":         "😕 No recipes in the catalogue yet.",

    # ── Guide ─────────────────────────────────────────────────────────────────
    "guide_title":          "📖 <b>Cooking Guide</b>\n\nChoose a topic:",
    "btn_guide_knife":      "🔪 Knife Skills",
    "btn_guide_tips":       "💡 Cooking Tips",
    "btn_guide_subs":       "🔄 Ingredient Substitutions",
    "btn_back_to_guide":    "◀️ Back to Guide",
    "guide_not_found":      "Article not found.",

    # ── Settings ──────────────────────────────────────────────────────────────
    "settings_title":       "⚙️ <b>Settings</b>\n\nChoose an option:",
    "btn_change_language":  "🌐 Change Language",
    "btn_notifications":    "🔔 Notifications",
    "change_language_title":"🌐 <b>Change Language</b>\n\nSelect your preferred language:",
    "notif_title":          "🔔 <b>Notifications</b>\n\n"
                            "Would you like to receive daily recipe suggestions?\n"
                            "<i>(Notification delivery coming soon)</i>",
    "btn_notif_enable":     "✅ Enable",
    "btn_notif_disable":    "❌ Disable",
    "notif_enabled":        "✅ Notifications enabled!",
    "notif_disabled":       "❌ Notifications disabled.",
}
