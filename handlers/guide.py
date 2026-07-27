"""
handlers/guide.py
-----------------
Handles:
  - /guide command     → show guide topic picker
  - menu:guide button  → show guide topic picker
  - guide:knife        → Knife Skills article
  - guide:tips         → Cooking Tips article
  - guide:substitutions → Ingredient Substitutions article
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.guide_kb import guide_menu_kb, guide_back_kb

router = Router()

# ── Article content ────────────────────────────────────────────────────────────

ARTICLES: dict[str, tuple[str, str]] = {
    "knife": (
        "🔪 <b>Knife Skills</b>",
        (
            "<b>1. The pinch grip</b>\n"
            "Grip the blade between your thumb and the side of your index finger, "
            "just above the handle. Your remaining fingers wrap around the handle. "
            "This gives you far more control than a full-handle grip.\n\n"

            "<b>2. The claw</b>\n"
            "Curl the fingertips of your guiding hand inward so your knuckles lead. "
            "The flat side of the blade rests against your knuckles as you slice — "
            "your fingertips are safely tucked away.\n\n"

            "<b>3. Let the knife do the work</b>\n"
            "Use the full length of the blade in a smooth rocking motion. "
            "Apply forward pressure as you push down, not just downward pressure. "
            "A sharp knife needs very little force.\n\n"

            "<b>4. Keep your knife sharp</b>\n"
            "A dull knife is more dangerous than a sharp one — it slips. "
            "Hone your blade with a steel before each use and sharpen it on a whetstone "
            "every few months.\n\n"

            "<b>5. Basic cuts to learn first</b>\n"
            "• <i>Julienne</i> — thin matchstick strips (great for stir-fries)\n"
            "• <i>Brunoise</i> — tiny 3 mm cubes (for soups, sauces)\n"
            "• <i>Chiffonade</i> — fine herb ribbons (stack leaves, roll, slice)\n"
            "• <i>Bias cut</i> — diagonal slices that increase surface area"
        ),
    ),
    "tips": (
        "💡 <b>Cooking Tips</b>",
        (
            "<b>1. Mise en place</b>\n"
            "Prep and measure every ingredient before you turn on the heat. "
            "French for 'everything in its place' — it is the single habit that "
            "separates calm cooks from panicked ones.\n\n"

            "<b>2. Salt in layers</b>\n"
            "Season at every stage, not just at the end. Salt draws out moisture and "
            "builds flavour from the inside. Taste as you go.\n\n"

            "<b>3. Don't crowd the pan</b>\n"
            "Overcrowded ingredients steam instead of sear. Work in batches and leave "
            "space between pieces for the Maillard reaction to happen.\n\n"

            "<b>4. Rest your meat</b>\n"
            "After cooking, rest steaks, chops, and roasts for 5–10 minutes before "
            "cutting. The juices redistribute and the meat stays moist.\n\n"

            "<b>5. Acid brightens everything</b>\n"
            "A squeeze of lemon or a splash of vinegar at the end of cooking lifts "
            "the entire dish. If something tastes flat, try acid before adding more salt.\n\n"

            "<b>6. Control your heat</b>\n"
            "High heat for searing and caramelising. Low heat for slow braises and "
            "emulsified sauces. The right heat at the right time is the foundation of cooking."
        ),
    ),
    "substitutions": (
        "🔄 <b>Ingredient Substitutions</b>",
        (
            "Ran out of something? Here are reliable swaps:\n\n"

            "<b>Dairy</b>\n"
            "• Buttermilk → plain yoghurt thinned with milk (1:1)\n"
            "• Heavy cream → full-fat coconut milk (in sauces & soups)\n"
            "• Kashk → sour cream or thick Greek yoghurt\n\n"

            "<b>Eggs</b>\n"
            "• 1 egg (binding) → 1 tbsp ground flaxseed + 3 tbsp water (rest 5 min)\n"
            "• 1 egg (leavening) → 1 tsp baking powder + 1 tbsp apple cider vinegar\n\n"

            "<b>Herbs & spices</b>\n"
            "• Fresh herbs → use ⅓ the amount of dried\n"
            "• Saffron → a pinch of turmeric + a few drops of rosewater\n"
            "• Fresh fenugreek → dried fenugreek leaves (use half the quantity)\n\n"

            "<b>Pantry</b>\n"
            "• Dried limes (limoo amani) → 2 tbsp lime juice + ½ tsp lime zest\n"
            "• Tomato paste → 3× the amount of tomato purée, reduced\n"
            "• Barberries (zereshk) → dried cranberries or pomegranate seeds\n\n"

            "<b>Flours</b>\n"
            "• All-purpose flour → 50/50 mix of bread flour and cake flour\n"
            "• Breadcrumbs → crushed crackers or panko in equal amounts"
        ),
    ),
}


# ── Entry points ───────────────────────────────────────────────────────────────

@router.message(Command("guide"))
async def cmd_guide(message: Message) -> None:
    """Triggered by /guide command — sends a new message."""
    await message.answer(
        "📖 <b>Cooking Guide</b>\n\nChoose a topic:",
        reply_markup=guide_menu_kb(),
    )


@router.callback_query(lambda c: c.data == "menu:guide")
async def cb_guide_menu(callback: CallbackQuery) -> None:
    """Triggered by the 📖 Guide button or the Back button inside a guide article."""
    await callback.message.edit_text(
        "📖 <b>Cooking Guide</b>\n\nChoose a topic:",
        reply_markup=guide_menu_kb(),
    )
    await callback.answer()


# ── Article display ────────────────────────────────────────────────────────────

@router.callback_query(lambda c: c.data and c.data.startswith("guide:"))
async def cb_guide_article(callback: CallbackQuery) -> None:
    """Display the selected guide article."""
    topic = callback.data.split(":")[1]   # 'knife' | 'tips' | 'substitutions'

    if topic not in ARTICLES:
        await callback.answer("Article not found.", show_alert=True)
        return

    title, body = ARTICLES[topic]

    await callback.message.edit_text(
        f"{title}\n{'─' * 30}\n\n{body}",
        reply_markup=guide_back_kb(),
    )
    await callback.answer()
