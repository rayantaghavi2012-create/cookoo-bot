"""
services/user_service.py
------------------------
Per-user settings management backed by data/users.json.

An in-memory cache avoids reading the JSON file on every single
Telegram update. The cache is updated on every write so it stays
consistent for the lifetime of the process.

Storage schema (users.json):
  {
    "<telegram_user_id>": {
      "lang": "en" | "fa",
      "first_name": "..."
    },
    ...
  }
"""

import config
from utils.json_storage import read_json, write_json

DEFAULT_LANG = "en"

# In-memory cache — populated lazily on first read, updated on every write.
_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is None:
        _cache = read_json(config.USERS_FILE)
        if not isinstance(_cache, dict):
            _cache = {}
    return _cache


def _save(data: dict) -> None:
    global _cache
    _cache = data
    write_json(config.USERS_FILE, data)


def _key(user_id: int) -> str:
    return str(user_id)


# ── Public API ────────────────────────────────────────────────────────────────

def get_user_lang(user_id: int) -> str:
    """
    Return the saved language code for this user.

    Returns DEFAULT_LANG ('en') if the user has never set a language.
    Hot-path: served from in-memory cache, no disk I/O.
    """
    data = _load()
    user = data.get(_key(user_id), {})
    return user.get("lang", DEFAULT_LANG)


def has_selected_language(user_id: int) -> bool:
    """
    Return True if this user has explicitly chosen a language before.

    Used by /start to decide whether to show the language gate.
    """
    data = _load()
    return _key(user_id) in data


def set_user_lang(user_id: int, lang: str, first_name: str = "") -> None:
    """
    Persist the user's language choice to disk and update the cache.

    Args:
        user_id:    Telegram user ID.
        lang:       'en' or 'fa'.
        first_name: Optional display name — stored for diagnostics.
    """
    data = _load()
    key  = _key(user_id)

    if key not in data:
        data[key] = {}

    data[key]["lang"]       = lang
    data[key]["first_name"] = first_name
    _save(data)
