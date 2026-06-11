# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Family Fork is a Flask app that generates personalized recipes from a single household `UserProfile` (dietary restrictions, spice level, serving count, age range, nutrition goals, cuisines) and saves every result to a persistent SQLite cookbook. A new recipe is auto-generated daily at 5 PM via APScheduler and emailed; recipes can also be requested on-demand or from a list of fridge ingredients.

---

## Commands

```bash
# Run the dev server (port 8080, debug + reloader on)
python3 app.py

# Install deps
pip install -r requirements.txt

# Run the full test suite
pytest

# Run a single test file / test
pytest tests/test_routes.py
pytest tests/test_recipe_generator.py::test_pick_fallback_respects_dietary
```

There is no separate lint/format step configured.

---

## Architecture

The non-obvious pieces that span multiple files:

### Three-tier recipe generation fallback chain

`recipe_generator.generate_recipe()` and `generate_from_fridge()` both try, in order:

1. **Anthropic SDK** with `model="claude-sonnet-4-6"` — only if `ANTHROPIC_API_KEY` passes `_is_valid_api_key()`.
2. **`claude` CLI subprocess** (`_call_claude_cli`) — invoked as `claude -p <prompt>`. **Note:** this call deliberately strips `ANTHROPIC_API_KEY` from the subprocess env so the CLI uses its own auth, not the (presumed invalid) key.
3. **Built-in 41-recipe library** (`FALLBACK_RECIPES` + `_pick_fallback` / `_fridge_fallback`) — pure-Python selection that respects profile constraints.

The app is designed to work end-to-end with zero API keys. When editing generation, preserve this no-key path.

### Async job pattern (in-memory, single-process)

`POST /api/generate` and `POST /api/fridge-generate` do **not** block. They:
1. Allocate a `job_id`, store `{"status": "pending"}` in the module-level `_jobs` dict in `app.py`,
2. Start a daemon `threading.Thread` that runs the generator inside `app.app_context()`,
3. Return `{"job_id": ...}` immediately. The browser polls `GET /api/job/<id>` every 2 s (see `static/js/app.js`).

Consequences to remember when changing this:
- Job state lives only in process memory — it does not survive restarts and will not work behind multiple workers (gunicorn `-w >1`, etc.).
- Background work must re-enter `app.app_context()` to use SQLAlchemy.

### APScheduler daily job

`setup_scheduler()` registers a cron job at `hour=17, minute=0` (server-local time, not per-user — `UserProfile.timezone` is stored but not honored by the scheduler). It is guarded by `if os.environ.get("WERKZEUG_RUN_MAIN") != "true"` so the Werkzeug reloader doesn't schedule it twice. Any production deployment should disable the reloader or this guard will silently skip scheduling in the worker.

### Schema migrations

There is no migration framework. `app.py` runs `db.create_all()` then attempts an inline `ALTER TABLE recipe ADD COLUMN image_url TEXT` wrapped in a broad `try/except` to upgrade pre-existing databases. Adding new columns to existing models requires a similar ad-hoc `ALTER` statement here.

### Recipe deduplication

`_save_recipe()` returns the existing record (no update) if a row with the same `title` already exists. The daily job and on-demand path both go through this, so duplicate-title results are silently dropped rather than overwritten.

### Image resolution pipeline

`recipe_image_url()` in `recipe_generator.py` resolves recipe images in this priority order:
1. `_RECIPE_IMAGES` exact-title lookup → local `static/images/*.jpg`
2. TheMealDB public API (no key) — full title, then key words, then cuisine area; downloaded result is cached to `static/images/`
3. `_try_local_food_image` keyword scan over local images
4. `_CUISINE_FALLBACK_IMAGES` cuisine-level default

### Single-profile assumption

The app treats `UserProfile.query.first()` as "the" profile — there is no notion of multiple users. Routes redirect to `/profile` when no profile exists.

---

## Routes

| Method | Path | Description |
|---|---|---|
| GET | `/` | Home — today's hero recipe + recent strip |
| GET | `/cookbook` | Browse + filter (cuisine, diet, nutrition, spice_max, time_max, text `q`) |
| GET | `/recipe/<id>` | Full recipe detail |
| GET/POST | `/profile` | View/update the single household profile |
| GET | `/fridge` | Fridge-based generator UI |
| POST | `/api/generate` | Start async on-demand generation → `{job_id}` |
| POST | `/api/fridge-generate` | Start async fridge generation → `{job_id}` |
| GET | `/api/job/<id>` | Poll job status: `pending` / `done` / `error` |
| GET | `/api/search?q=` | JSON search across title, description, ingredients (≤20 results) |

---

## Domain values (used by the AI prompt and fallback selection)

These are the canonical option sets the generator and UI expect. If you add or rename one, update both `recipe_generator.py` (prompt + scoring) and the `profile.html` form.

- **Dietary restrictions**: `vegetarian`, `vegan`, `chicken`, `seafood`, `any meat`, `diabetic`
- **Spice level**: `1` very mild → `5` very hot
- **Number of people**: `1`–`10` (all ingredient quantities are scaled to match)
- **Age of eaters**: `2`–`10+`. Youngest ≤ 5 ⇒ allergen + choking-hazard notes required. Youngest ≤ 12 ⇒ child-friendly flavour notes required.
- **Nutrition tags**: `protein-rich`, `iron-rich`, `vitamin-rich`, `no-carb`, `balanced`, `sugar-free`
- **Cuisines**: `italian`, `indian`, `mexican`, `mediterranean`, `chinese`, `american`, `european`

Every saved `Recipe` is tagged with cuisine, nutrition values, and dietary compatibility, all of which back the cookbook filters.

---

## Key files

```
app.py                  Flask app, routes, in-memory job store, APScheduler, inline schema migration
recipe_generator.py     41-recipe fallback library, AI prompt, fridge logic, 3-tier generation chain, image pipeline
models.py               UserProfile, Recipe (JSON columns for tags/ingredients/instructions)
extensions.py           SQLAlchemy singleton (separate file to avoid circular imports)
email_service.py        SMTP delivery — silently no-ops when EMAIL_USER/EMAIL_PASSWORD unset
static/                 css/, js/app.js (poll loop + serving scaler), images/
templates/              Jinja2 templates (base, home, cookbook, recipe_detail, fridge, profile)
tests/                  pytest — in-memory SQLite via fixtures that reconfigure the real Flask app
instance/family_fork.db SQLite database (auto-created)
```

---

## Environment variables

| Variable | Required | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | No | If absent/invalid, falls through to `claude` CLI then to fallback library |
| `EMAIL_HOST` | No | SMTP host (defaults to `smtp.gmail.com`) |
| `EMAIL_PORT` | No | SMTP port (defaults to `587`, STARTTLS) |
| `EMAIL_USER` | No | If unset, email send is a no-op (prints + returns `False`) |
| `EMAIL_PASSWORD` | No | Password for `EMAIL_USER` |
| `SECRET_KEY` | No | Flask session secret (defaults to a dev value) |
| `PORT` | No | Server port (defaults to `8080` — macOS port 5000 is taken by AirPlay) |
| `BASE_URL` | No | Public base URL used for the "View Full Recipe" link in emails |

The repo's README mentions `EMAIL_PASS`, but the code (`email_service.py`) actually reads `EMAIL_PASSWORD` and `EMAIL_PORT` — use those names in `.env`.
