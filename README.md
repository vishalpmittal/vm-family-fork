# Family Fork

A personalized, AI-powered recipe generation and digital cookbook platform. Set your household profile once — dietary restrictions, spice level, number of people, age range, nutrition goals, and preferred cuisines — and get a new tailored recipe every day at 5 PM, delivered by email and saved to a growing searchable cookbook.

Works fully without an AI API key using a built-in library of 41 recipes. Upgrades to Claude-generated recipes when a valid Anthropic API key is configured.

---

## Features

- **Daily recipe generation** — new recipe auto-generated at 5 PM, matched to your household profile
- **On-demand generation** — request a recipe any time from the home page; browser waits asynchronously while the recipe is being generated
- **Profile-driven recipes** — every recipe strictly respects dietary restrictions, preferred cuisines, spice level, serving size, nutrition goals, and age range
- **What's in the Fridge?** — generate a recipe from ingredients you already have; choose a sauce style and cuisine; grains never assumed unless listed
- **Persistent cookbook** — every recipe saved, tagged, and searchable; no duplicates
- **Filter & search** — filter by cuisine, dietary restriction, nutrition tag, spice level, and cook time
- **Real food photos** — images fetched from TheMealDB (free, no key required) by matching dish name and cuisine; falls back to 41 local food photos matched by recipe keywords
- **Email delivery** — each new recipe emailed immediately after generation
- **Household profile** — dietary restrictions, spice level, serving size, age range, nutrition goals, cuisine preferences

---

## Recipe Library (41 recipes, no API key needed)

| Cuisine | Count |
|---|---|
| 🍛 Indian | 11 |
| 🍝 Italian | 10 |
| 🌮 Mexican | 10 |
| 🫒 Mediterranean | 10 |

Covers: vegetarian, vegan, chicken, seafood, and diabetic-friendly diets.

---

## Pages

| Page | URL | Description |
|---|---|---|
| Home | `/` | Today's hero recipe + this week's strip + on-demand generate button |
| Cookbook | `/cookbook` | Browse, search, and filter all saved recipes |
| Recipe Detail | `/recipe/<id>` | Full ingredients, instructions, allergen notes, serving scaler |
| What's in the Fridge? | `/fridge` | Ingredient-based recipe generation |
| My Profile | `/profile` | Household preference setup |

---

## Stack

- **Backend**: Flask 3.x, SQLAlchemy + SQLite, APScheduler
- **AI**: Anthropic `claude-sonnet-4-6` (optional — falls back to recipe library or `claude` CLI)
- **Images**: TheMealDB public API (no key required)
- **Frontend**: Jinja2 templates, vanilla JS
- **Port**: 8080

---

## Setup

### 1. Install dependencies

```bash
pip install flask flask-sqlalchemy apscheduler python-dotenv anthropic
```

On corporate networks where PyPI is blocked:
```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
  flask flask-sqlalchemy apscheduler python-dotenv anthropic
```

### 2. Configure environment (optional)

Create a `.env` file in the project root:

```
# Required only for AI-generated recipes (app works without this)
ANTHROPIC_API_KEY=sk-ant-...

# Required only for email delivery
EMAIL_HOST=smtp.example.com
EMAIL_USER=you@example.com
EMAIL_PASS=yourpassword

# Optional
SECRET_KEY=your-secret-key
PORT=8080
BASE_URL=http://localhost:8080
```

If `ANTHROPIC_API_KEY` is absent or invalid, the app uses the built-in recipe library automatically.

### 3. Run

```bash
python3 app.py
```

Open [http://localhost:8080](http://localhost:8080) and complete your household profile to get started.

> **macOS note**: Port 5000 is occupied by AirPlay Receiver. This app runs on 8080 by default.

---

## Profile Options

### Dietary Restrictions

| Tag | Meaning |
|---|---|
| `vegetarian` | No meat or seafood |
| `vegan` | No animal products |
| `chicken` | Chicken allowed |
| `seafood` | Seafood allowed |
| `any meat` | No restrictions |
| `diabetic` | Low glycemic, minimal added sugar |

### Cuisines

`italian` · `indian` · `mexican` · `mediterranean` · `chinese` · `american` · `european`

### Nutrition Goals

`protein-rich` · `iron-rich` · `vitamin-rich` · `no-carb` · `balanced` · `sugar-free`

### Spice Level

`1` very mild → `2` mild → `3` medium → `4` hot → `5` very hot

---

## Project Files

```
app.py                  Flask app, routes, background job runner, APScheduler
recipe_generator.py     41-recipe fallback library, AI generation, fridge logic, image pipeline
models.py               SQLAlchemy models (UserProfile, Recipe)
email_service.py        SMTP email delivery
extensions.py           SQLAlchemy singleton
static/
  css/styles.css        All styles and design tokens
  js/app.js             Generate-button handlers, serving scaler, poll loop
  images/               41 local food photos (.jpg)
templates/
  base.html             Nav, footer, shared layout
  home.html             Homepage
  cookbook.html         Browse + filter view
  recipe_detail.html    Full recipe page
  fridge.html           What's in the Fridge?
  profile.html          Household profile form
wireframe/index.html    Interactive HTML wireframe (5 pages)
design-guide.html       Design system: colours, tokens, components
Recipe-cookbook-prd.md  Product requirements document
problem-statement.md    Problem framing and feature summary
CLAUDE.md               Developer guide: routes, values, architecture
```

---

## License

Personal project — not licensed for redistribution.
