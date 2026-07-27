# 🍳 Cookoo — Telegram Cooking Bot

A fully-featured Telegram cooking bot built with **Python 3.12** and **aiogram 3.x**.
Data is stored in JSON files — no database required to get started.

---

## Features

| Feature | Description |
|---|---|
| `/start` | Main menu with inline keyboard |
| Start Cooking | Browse Iranian & Fast Food categories |
| Step-by-step | Navigate recipe steps one at a time |
| 🔍 Search | Search recipes by name |
| ❤️ Favorites | Save / remove favourite recipes (persisted in JSON) |
| 🎲 Random | Get a random recipe instantly |
| 📖 Guide | Quick cooking guides (knife skills, tips, substitutions) |
| ⚙️ Settings | Language & notification placeholders |

---

## Project Structure

```
cookoo-bot/
├── main.py              # Entry point
├── config.py            # Environment variable loader
├── requirements.txt
├── .env.example
│
├── data/
│   ├── recipes.json     # All recipe data
│   └── favorites.json   # Per-user favourites
│
├── handlers/            # One file per feature (aiogram Routers)
│   ├── start.py
│   ├── cooking.py
│   ├── search.py
│   ├── favorites.py
│   ├── random_recipe.py
│   ├── guide.py
│   └── settings.py
│
├── keyboards/           # Inline keyboard builders
│   ├── main_menu.py
│   ├── recipe_kb.py
│   ├── guide_kb.py
│   └── settings_kb.py
│
├── services/            # Business logic, no Telegram knowledge
│   ├── recipe_service.py
│   ├── favorites_service.py
│   └── search_service.py
│
├── states/              # aiogram FSM state groups
│   ├── search_states.py
│   └── recipe_states.py
│
└── utils/
    ├── formatters.py    # Message text builders
    └── json_storage.py  # Generic JSON read/write helper
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd cookoo-bot
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set your **BOT_TOKEN**:

```
BOT_TOKEN=1234567890:ABCDefGhIJKlmNoPQRsTUVwxYZ
```

Get a token from [@BotFather](https://t.me/BotFather) on Telegram.

### 5. Run the bot

```bash
python main.py
```

---

## Extending the Bot

- **Add a recipe** — edit `data/recipes.json` following the existing schema.
- **Add a handler** — create a new file in `handlers/`, define a `router`, and include it in `main.py`.
- **Swap JSON for a real DB** — replace `utils/json_storage.py` and the service layer; handlers stay untouched.

---

## Requirements

- Python 3.12+
- `aiogram==3.13.1`
- `python-dotenv==1.0.1`
