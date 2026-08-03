"""
locales/__init__.py
-------------------
Provides a single get_text(key, lang) helper that the rest of the
codebase uses to retrieve translated strings.

Usage:
    from locales import t
    t("welcome", "en")   # → "👨‍🍳 Welcome to Cookoo!"
    t("welcome", "fa")   # → "👨‍🍳 به کوکو خوش آمدید!"
"""

from locales.en import STRINGS as EN
from locales.fa import STRINGS as FA

_BUNDLES: dict[str, dict[str, str]] = {
    "en": EN,
    "fa": FA,
}


def t(key: str, lang: str) -> str:
    """
    Return the translated string for *key* in *lang*.

    Falls back to English if the key is missing in the requested locale.
    Falls back to the raw key if it doesn't exist in either locale.
    """
    bundle = _BUNDLES.get(lang, EN)
    return bundle.get(key) or EN.get(key) or key
