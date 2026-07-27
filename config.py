"""
config.py
---------
Loads environment variables and exposes them as typed settings.
All secrets are read from the .env file — never hard-coded.
"""

import os
from dotenv import load_dotenv

# Load variables from .env into the process environment
load_dotenv()


def _require(key: str) -> str:
    """Return an env variable or raise a clear error if it is missing."""
    value = os.getenv(key)
    if not value:
        raise RuntimeError(
            f"Required environment variable '{key}' is not set.\n"
            "Copy .env.example to .env and fill in the value."
        )
    return value


# ── Bot ───────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = _require("BOT_TOKEN")

# ── Data storage ──────────────────────────────────────────────────────────────
# Paths to the JSON files used as temporary data storage
DATA_DIR: str = os.path.join(os.path.dirname(__file__), "data")
RECIPES_FILE: str = os.path.join(DATA_DIR, "recipes.json")
FAVORITES_FILE: str = os.path.join(DATA_DIR, "favorites.json")
