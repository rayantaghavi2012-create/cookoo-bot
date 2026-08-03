"""
config.py
---------
Loads environment variables and exposes them as typed settings.
All secrets are read from the .env file — never hard-coded.

Deployment notes (Railway)
--------------------------
- BOT_TOKEN must be set as an environment variable in the Railway
  service dashboard under Variables.  Do NOT commit the .env file.
- load_dotenv() is a no-op on Railway because Railway injects
  environment variables directly into the process — this is correct
  behaviour and requires no changes.
- DATA_DIR points to the data/ folder inside the container image.
  recipes.json is read-only and is always present (committed to the
  repo).  favorites.json is writable at runtime but lives on Railway's
  ephemeral filesystem: it resets on every redeploy.  This is
  acceptable for the current JSON-backed phase.  When PostgreSQL is
  introduced, favorites_service.py is the only file that changes.
"""

import os
from dotenv import load_dotenv

# Load variables from .env into the process environment.
# On Railway this is a no-op — env vars are already in the environment.
load_dotenv()


def _require(key: str) -> str:
    """Return an env variable or raise a clear error if it is missing."""
    value = os.getenv(key)
    if not value:
        raise RuntimeError(
            f"Required environment variable '{key}' is not set.\n"
            "Local: copy .env.example to .env and fill in the value.\n"
            "Railway: add the variable in the service Variables tab."
        )
    return value


# ── Bot ───────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = _require("BOT_TOKEN")

# ── Data storage ──────────────────────────────────────────────────────────────
# Absolute paths to the JSON files used as temporary data storage.
# __file__ resolves correctly both locally and inside the Railway container.
DATA_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RECIPES_FILE: str = os.path.join(DATA_DIR, "recipes.json")

# NOTE: favorites.json is written at runtime.  On Railway's ephemeral
# filesystem this file resets on each redeploy.  Favourites saved by
# users will persist for the lifetime of the running container only.
FAVORITES_FILE: str = os.path.join(DATA_DIR, "favorites.json")
