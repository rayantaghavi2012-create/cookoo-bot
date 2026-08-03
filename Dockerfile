# ── Stage 1: base ─────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# No system-level C deps needed for aiogram + python-dotenv
# (asyncpg / libpq-dev will be added when PostgreSQL is introduced)

# ── Stage 2: dependencies ─────────────────────────────────────────────────────
FROM base AS deps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 3: final image ──────────────────────────────────────────────────────
FROM deps AS final

COPY . .

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Entry point: run the bot directly from the project root
CMD ["python", "main.py"]
