"""
handlers/guide.py
-----------------
Handles:
  /guide command      → guide topic picker
  menu:guide button   → guide topic picker
  guide:knife         → Knife Skills article (bilingual)
  guide:tips          → Cooking Tips article (bilingual)
  guide:substitutions → Ingredient Substitutions article (bilingual)
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.guide_kb import guide_menu_kb, guide_back_kb
from services.user_service import get_user_lang
from locales import t

router = Router()

# ── Bilingual article content ──────────────────────────────────────────────────
# Each key maps to (title_en, body_en, title_fa, body_fa)

_ARTICLES: dict[str, dict[str, str]] = {
    "knife": {
        "en_title": "🔪 <b>Knife Skills</b>",
        "en_body": (
            "<b>1. The pinch grip</b>\n"
            "Pinch the blade between thumb and index finger just above the handle. "
            "Remaining fingers wrap the handle — far more control than a full grip.\n\n"
            "<b>2. The claw</b>\n"
            "Curl fingertips inward so knuckles guide the blade. "
            "Your fingertips stay safely tucked away.\n\n"
            "<b>3. Let the knife do the work</b>\n"
            "Use the full blade length in a rocking motion. "
            "Apply forward pressure, not just downward. A sharp knife needs little force.\n\n"
            "<b>4. Keep it sharp</b>\n"
            "Hone before each use; sharpen on a whetstone every few months. "
            "A dull knife slips and is far more dangerous.\n\n"
            "<b>5. Essential cuts</b>\n"
            "• <i>Julienne</i> — thin matchstick strips\n"
            "• <i>Brunoise</i> — tiny 3 mm cubes\n"
            "• <i>Chiffonade</i> — fine herb ribbons\n"
            "• <i>Bias cut</i> — diagonal slices for more surface area"
        ),
        "fa_title": "🔪 <b>مهارت‌های کاردزنی</b>",
        "fa_body": (
            "<b>۱. گرفتن صحیح چاقو</b>\n"
            "تیغه را بین شست و اشاره‌انگشت درست بالای دسته بگیرید. "
            "بقیه انگشتان دور دسته باشند — کنترل بسیار بیشتری دارید.\n\n"
            "<b>۲. حالت پنجه</b>\n"
            "نوک انگشتان را به داخل خم کنید تا بند انگشتان راهنما باشند. "
            "نوک انگشتانتان در امنیت کامل است.\n\n"
            "<b>۳. اجازه دهید چاقو کار کند</b>\n"
            "از تمام طول تیغه با حرکت چرخشی استفاده کنید. "
            "فشار به جلو بدهید نه فقط به پایین. چاقوی تیز نیروی کمی لازم دارد.\n\n"
            "<b>۴. همیشه تیز نگه دارید</b>\n"
            "قبل از هر بار استفاده با فولاد تیز کنید؛ چند ماه یکبار با سنگ تیز کنید.\n\n"
            "<b>۵. برش‌های اساسی</b>\n"
            "• <i>ژولیان</i> — نوارهای نازک\n"
            "• <i>برونواز</i> — مکعب‌های ریز ۳ میلیمتری\n"
            "• <i>شیفوناد</i> — نوارهای ظریف سبزی\n"
            "• <i>برش مورب</i> — برش‌های زاویه‌دار با سطح بیشتر"
        ),
    },
    "tips": {
        "en_title": "💡 <b>Cooking Tips</b>",
        "en_body": (
            "<b>1. Mise en place</b>\n"
            "Prep and measure everything before you turn on the heat. "
            "It separates calm cooks from panicked ones.\n\n"
            "<b>2. Salt in layers</b>\n"
            "Season at every stage. Salt builds flavour from the inside. Taste as you go.\n\n"
            "<b>3. Don't crowd the pan</b>\n"
            "Overcrowded ingredients steam instead of sear. Work in batches.\n\n"
            "<b>4. Rest your meat</b>\n"
            "Rest steaks and roasts 5–10 minutes before cutting. Juices redistribute.\n\n"
            "<b>5. Acid brightens everything</b>\n"
            "A squeeze of lemon at the end lifts the entire dish. "
            "If something tastes flat, try acid before adding more salt.\n\n"
            "<b>6. Control your heat</b>\n"
            "High heat for searing, low heat for braises and sauces."
        ),
        "fa_title": "💡 <b>نکات آشپزی</b>",
        "fa_body": (
            "<b>۱. میز آن پلاس</b>\n"
            "قبل از روشن کردن اجاق همه چیز را آماده کنید. "
            "آشپزهای آرام و حرفه‌ای همین کار را می‌کنند.\n\n"
            "<b>۲. نمک در لایه‌ها</b>\n"
            "در هر مرحله طعم‌دار کنید. نمک طعم را از درون می‌سازد.\n\n"
            "<b>۳. تابه را شلوغ نکنید</b>\n"
            "مواد شلوغ بخار می‌شوند نه سرخ. دسته‌ای کار کنید.\n\n"
            "<b>۴. گوشت را استراحت دهید</b>\n"
            "بعد از پخت ۵-۱۰ دقیقه قبل از برش استراحت دهید.\n\n"
            "<b>۵. اسید همه چیز را روشن می‌کند</b>\n"
            "چند قطره آبلیمو آخر کار کل غذا را زنده می‌کند.\n\n"
            "<b>۶. حرارت را کنترل کنید</b>\n"
            "حرارت زیاد برای سرخ‌کردن، حرارت کم برای خورش و سس."
        ),
    },
    "substitutions": {
        "en_title": "🔄 <b>Ingredient Substitutions</b>",
        "en_body": (
            "<b>Dairy</b>\n"
            "• Buttermilk → yoghurt thinned with milk (1:1)\n"
            "• Heavy cream → full-fat coconut milk\n"
            "• Kashk → sour cream or thick Greek yoghurt\n\n"
            "<b>Eggs</b>\n"
            "• 1 egg (binding) → 1 tbsp flaxseed + 3 tbsp water (rest 5 min)\n"
            "• 1 egg (leavening) → 1 tsp baking powder + 1 tbsp apple cider vinegar\n\n"
            "<b>Herbs & Spices</b>\n"
            "• Fresh herbs → ⅓ the amount of dried\n"
            "• Saffron → turmeric + a few drops of rosewater\n"
            "• Dried limes → 2 tbsp lime juice + ½ tsp zest\n\n"
            "<b>Pantry</b>\n"
            "• Barberries → dried cranberries or pomegranate seeds\n"
            "• Tomato paste → 3× the amount of tomato purée, reduced"
        ),
        "fa_title": "🔄 <b>جایگزین مواد اولیه</b>",
        "fa_body": (
            "<b>لبنیات</b>\n"
            "• دوغ → ماست رقیق‌شده با شیر (۱:۱)\n"
            "• خامه سنگین → شیر نارگیل پرچرب\n"
            "• کشک → خامه ترش یا ماست یونانی غلیظ\n\n"
            "<b>تخم‌مرغ</b>\n"
            "• ۱ تخم‌مرغ (چسبنده) → ۱ قاشق بذر کتان + ۳ قاشق آب (۵ دقیقه بگذارید)\n"
            "• ۱ تخم‌مرغ (ورآمدن) → ۱ قاشق بیکینگ پودر + ۱ قاشق سرکه سیب\n\n"
            "<b>سبزی و ادویه</b>\n"
            "• سبزی تازه → یک‌سوم مقدار خشک\n"
            "• زعفران → زردچوبه + چند قطره گلاب\n"
            "• لیمو عمانی → ۲ قاشق آبلیمو + نیم قاشق پوست لیمو\n\n"
            "<b>مواد پایه</b>\n"
            "• زرشک → کرن‌بری خشک یا دانه انار\n"
            "• رب گوجه → ۳ برابر پوره گوجه، کمی بجوشانید تا غلیظ شود"
        ),
    },
}


@router.message(Command("guide"))
async def cmd_guide(message: Message) -> None:
    lang = get_user_lang(message.from_user.id)
    await message.answer(t("guide_title", lang), reply_markup=guide_menu_kb(lang))


@router.callback_query(lambda c: c.data == "menu:guide")
async def cb_guide_menu(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(t("guide_title", lang), reply_markup=guide_menu_kb(lang))
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("guide:"))
async def cb_guide_article(callback: CallbackQuery) -> None:
    topic = callback.data.split(":")[1]
    lang  = get_user_lang(callback.from_user.id)

    if topic not in _ARTICLES:
        await callback.answer(t("guide_not_found", lang), show_alert=True)
        return

    article   = _ARTICLES[topic]
    title_key = f"{lang}_title"
    body_key  = f"{lang}_body"

    title = article.get(title_key, article["en_title"])
    body  = article.get(body_key,  article["en_body"])

    await callback.message.edit_text(
        f"{title}\n{'─' * 30}\n\n{body}",
        reply_markup=guide_back_kb(lang),
    )
    await callback.answer()
