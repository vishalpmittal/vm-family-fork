# Product Requirements Document
## Family Fork

| Field | Value |
|---|---|
| Author | Poorva Mittal |
| Status | Shipped — v1 MVP |
| Version | 1.2 |
| Last Updated | 2026-04-29 |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Metrics](#3-goals--success-metrics)
4. [User Personas](#4-user-personas)
5. [User Stories](#5-user-stories)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [UX & Design Requirements](#8-ux--design-requirements)
9. [System Architecture](#9-system-architecture)
10. [Data Model](#10-data-model)
11. [Out of Scope](#11-out-of-scope)
12. [Risks & Mitigations](#12-risks--mitigations)
13. [Open Questions](#13-open-questions)

---

## 1. Executive Summary

**Family Fork** is a personalized, AI-powered recipe generation and digital cookbook platform. Users configure their household profile once — dietary restrictions, nutrition goals, spice tolerance, age range, number of people, and preferred cuisines — and the system delivers a new tailored recipe every day at 5 PM, builds a growing searchable cookbook, and notifies the user by email.

The product eliminates the daily meal-planning decision without requiring users to actively engage with the app. A "What's in the Fridge?" feature generates a recipe from whatever ingredients the user already has, without assuming pantry items like grains or fresh produce.

Every generated recipe strictly enforces all active profile constraints simultaneously. The app runs fully without an AI API key using a curated fallback library of 41 recipes, upgrading to `claude-sonnet-4-6`-generated recipes when a valid Anthropic key is present. Real food photos are sourced automatically from the TheMealDB public API (free, no key required), with 41 local images as a fallback.

---

## 2. Problem Statement

Families spend 15–20 minutes every evening deciding what to cook, fall back on the same meals repeatedly, and struggle to find recipe tools that holistically reflect their household's dietary profile. No existing tool:

- Holds a complete household preference profile (restrictions + nutrition + spice + age + cuisine)
- Proactively surfaces a new relevant recipe every day without being asked
- Builds a living cookbook that grows and stays searchable over time
- Delivers recipes passively without requiring the user to open an app
- Generates recipes from what's actually in the fridge, without assuming ingredients

See `problem-statement.md` for full problem framing and persona detail.

---

## 3. Goals & Success Metrics

### Product Goals

| Goal | Description |
|---|---|
| Reduce decision fatigue | Eliminate the daily "what do I cook?" question |
| Build a personal cookbook | Accumulate a growing, tagged, searchable library of household-relevant recipes |
| Passive delivery | User receives value (a recipe) without opening the app |
| Full constraint compliance | Every recipe is safe and appropriate for every household member |
| Fridge-first cooking | Enable ingredient-led recipe generation with no pantry assumptions |

### Success Metrics

| Metric | Target | Status |
|---|---|---|
| Profile setup time | ≤ 2 minutes | Met |
| Recipe constraint compliance | 100% of profile constraints enforced in prompt and validated before save | Met |
| Daily email delivery | ≥ 99% success rate (when SMTP configured) | Dependent on SMTP config |
| Time to find a past recipe | ≤ 10 seconds via search or filter | Met |
| Cookbook after 30 days | ≥ 30 recipes | Met (41 in fallback library) |
| On-demand generation latency | ≤ 60 seconds (AI); < 1 second (fallback) | Met |
| Food photo relevance | Photo matches dish or cuisine for every recipe | Met via TheMealDB |
| Fridge recipe generation | Works with 1+ ingredient; no grain assumptions | Met |

---

## 4. User Personas

### Persona A — The Household Manager
> *"I need dinner sorted before 6 PM and I can't Google options every night."*

- **Context**: Cooking for 2–6 people including children, managing at least one dietary restriction
- **Goal**: A reliable daily suggestion that requires no extra filtering
- **Pain point**: Generic apps require manual filtering every single time; nothing remembers the family's full needs

### Persona B — The Health-Conscious Cook
> *"I want high-protein, low-carb meals but I don't want to read macros every time."*

- **Context**: Individual or couple with specific nutrition goals (diabetic-friendly, sugar-free, protein-rich)
- **Goal**: Recipes that fit their health goals without manual verification
- **Pain point**: Nutrition filters on recipe sites are unreliable or locked behind paid tiers

### Persona C — The Cuisine Explorer
> *"I want to try new cuisines but I'm not sure where to start."*

- **Context**: Small household, enjoys variety, wants to rotate across cuisines (Indian, Mediterranean, Chinese, etc.)
- **Goal**: Be introduced to new cuisines within safe dietary guardrails
- **Pain point**: Too many choices; no trusted curator that knows their preferences

### Persona D — The Fridge Cook
> *"I have spinach, paneer, and a few tomatoes — what can I make right now?"*

- **Context**: Doesn't want to shop; wants to use what's already on hand
- **Goal**: A recipe that uses actual fridge contents, not a pantry shopping list
- **Pain point**: Most recipe tools suggest dishes requiring ingredients they don't have

---

## 5. User Stories

### Profile Setup

| ID | Story | Priority | Status |
|---|---|---|---|
| US-01 | As a user, I want to set my dietary restrictions so that every recipe is safe for my household | P0 | Done |
| US-02 | As a user, I want to set a spice level so that recipes match my household's heat tolerance | P0 | Done |
| US-03 | As a user, I want to specify the number of people so that ingredient quantities are correctly scaled | P0 | Done |
| US-04 | As a user, I want to enter the age range of eaters so that recipes are age-appropriate and allergen-aware | P0 | Done |
| US-05 | As a user, I want to select nutrition requirements so that recipes align with my health goals | P0 | Done |
| US-06 | As a user, I want to choose preferred cuisines from a list of 7 so that variety matches my taste | P1 | Done |
| US-07 | As a user, I want to edit my profile at any time so that changes in household needs are reflected in the next recipe | P1 | Done |

### Recipe Generation

| ID | Story | Priority | Status |
|---|---|---|---|
| US-08 | As a user, I want to receive a new recipe every day at 5 PM so that I don't have to plan dinner myself | P0 | Done |
| US-09 | As a user, I want to request a recipe on demand so that I can get inspiration outside the daily cadence | P0 | Done |
| US-10 | As a user, I want every generated recipe to respect all my active profile constraints simultaneously | P0 | Done |
| US-11 | As a user, I want the recipe to include ingredients scaled to my household size and step-by-step instructions | P0 | Done |
| US-12 | As a user, I want each recipe to display its cuisine, nutrition tags, and dietary compatibility clearly | P1 | Done |
| US-13 | As a user, I want the daily recipe to feel fresh and not repeat recent suggestions | P1 | Done |
| US-14 | As a user with young children, I want recipes to include age-appropriate notes and allergen warnings | P1 | Done |

### Cookbook

| ID | Story | Priority | Status |
|---|---|---|---|
| US-15 | As a user, I want every generated recipe automatically saved to my cookbook so I never lose it | P0 | Done |
| US-16 | As a user, I want to browse my cookbook organized by cuisine | P1 | Done |
| US-17 | As a user, I want to search my cookbook by ingredient, cuisine, tag, or free text | P0 | Done |
| US-18 | As a user, I want each recipe card to show key metadata at a glance (cuisine, tags, time, servings) | P1 | Done |
| US-19 | As a user, I want to filter the cookbook by cuisine, dietary restriction, nutrition tag, spice level, and cook time | P1 | Done |

### Notifications

| ID | Story | Priority | Status |
|---|---|---|---|
| US-20 | As a user, I want to receive an email with the full recipe when a new one is generated so I don't need to open the app | P0 | Done |
| US-21 | As a user, I want the email to include a link back to the full cookbook entry | P2 | Done |

### Fridge Feature

| ID | Story | Priority | Status |
|---|---|---|---|
| US-22 | As a user, I want to enter the ingredients I have on hand and get a recipe that only uses those items | P1 | Done |
| US-23 | As a user, I want to optionally specify a sauce type so the recipe fits what I want to make | P1 | Done |
| US-24 | As a user, I want to optionally narrow by cuisine style | P1 | Done |
| US-25 | As a user, I want to see which of my fridge ingredients were actually used in the recipe | P1 | Done |
| US-26 | As a user, I want to click "Try Different Recipe" to get a new result without repeating the previous one | P1 | Done |

---

## 6. Functional Requirements

### FR-1: Household Profile

| Req ID | Requirement |
|---|---|
| FR-1.1 | The system shall allow the user to configure dietary restrictions: `vegetarian`, `vegan`, `chicken`, `seafood`, `any-meat`, `diabetic` (multi-select) |
| FR-1.2 | The system shall allow the user to set a spice level from 1 (very mild) to 5 (very hot) |
| FR-1.3 | The system shall allow the user to set the number of people from 1 to 10 |
| FR-1.4 | The system shall allow the user to specify the youngest and oldest eater's age |
| FR-1.5 | The system shall allow the user to select nutrition goals: `protein-rich`, `iron-rich`, `vitamin-rich`, `no-carb`, `balanced`, `sugar-free` (multi-select) |
| FR-1.6 | The system shall allow the user to select preferred cuisines from: `italian`, `indian`, `mexican`, `mediterranean`, `chinese`, `american`, `european` (multi-select) |
| FR-1.7 | The system shall persist profile settings across sessions |
| FR-1.8 | The system shall allow the user to edit any profile field at any time; changes apply to the next generated recipe |
| FR-1.9 | The system shall allow the user to set their email address and timezone |

### FR-2: Recipe Generation

| Req ID | Requirement |
|---|---|
| FR-2.1 | The system shall automatically generate one recipe daily at 5 PM |
| FR-2.2 | The system shall generate a recipe on demand when the user requests it from the home page |
| FR-2.3 | Every generated recipe shall comply with all active profile constraints simultaneously: dietary restrictions, cuisines, spice level, serving size, nutrition goals, and age range |
| FR-2.4 | The system shall scale ingredient quantities to the configured number of people |
| FR-2.5 | The system shall include allergen and texture notes when the youngest eater is ≤ 5 years old |
| FR-2.6 | The system shall include child-friendly flavour guidance when the youngest eater is ≤ 12 years old |
| FR-2.7 | Each recipe shall include: title, description, cuisine tag, nutrition tags, dietary tags, ingredients (name, quantity, unit), step-by-step instructions, prep time, cook time, serving count, spice level, and allergen notes |
| FR-2.8 | The system shall avoid repeating a recipe generated in the prior 7 days |
| FR-2.9 | On-demand generation shall be handled asynchronously; the browser polls for status every 2 seconds for up to 3 minutes |
| FR-2.10 | When no valid AI API key is configured, the system shall fall back to the curated recipe library and apply the same profile-matching constraints |

### FR-3: Cookbook

| Req ID | Requirement |
|---|---|
| FR-3.1 | Every generated recipe shall be automatically saved to the cookbook |
| FR-3.2 | Each cookbook entry shall carry tags for cuisine, nutrition values, and dietary compatibility |
| FR-3.3 | The cookbook shall be searchable by: free text (title, description, ingredients), cuisine tag, nutrition tag, dietary tag |
| FR-3.4 | The cookbook shall display recipes in reverse chronological order by default |
| FR-3.5 | The cookbook shall support browsing by cuisine category in the default (unfiltered) view |
| FR-3.6 | Each recipe card shall display: food photo (with emoji fallback), title, cuisine, key tags, prep+cook time, and spice level |
| FR-3.7 | The filter panel shall support: cuisine, dietary restriction, nutrition tag, maximum spice level, and maximum total cook time |
| FR-3.8 | The system shall not create duplicate cookbook entries for the same recipe title |

### FR-4: Food Photos

| Req ID | Requirement |
|---|---|
| FR-4.1 | The system shall resolve a food photo for every recipe at generation time |
| FR-4.2 | Photo resolution order: (1) exact title match in local dictionary → (2) TheMealDB API by dish name/keywords/cuisine → (3) local keyword-matched image → (4) cuisine-based generic fallback |
| FR-4.3 | Downloaded images shall be cached to `static/images/` and reused on subsequent requests |
| FR-4.4 | The UI shall display an emoji fallback if no image file is available |

### FR-5: Email Notification

| Req ID | Requirement |
|---|---|
| FR-5.1 | The system shall send an email to the configured user address each time a recipe is generated (daily or on demand) |
| FR-5.2 | The email shall include the full recipe: title, ingredients, instructions, and all tags |
| FR-5.3 | The email shall include a link to the recipe's cookbook entry |
| FR-5.4 | Email delivery shall occur immediately after recipe generation |

### FR-6: What's in the Fridge?

| Req ID | Requirement |
|---|---|
| FR-6.1 | The system shall allow the user to enter a list of fresh ingredients |
| FR-6.2 | The generated recipe shall use only the specified ingredients plus up to 5 pantry staples (salt, basic spices, oil) |
| FR-6.3 | The system shall never assume grains (rice, pasta, bread, naan, tortillas, etc.) unless explicitly listed by the user |
| FR-6.4 | The user may optionally select a sauce/cooking base: tomato, coconut milk, cream/butter, olive oil, broth, yogurt, or dry |
| FR-6.5 | The user may optionally select a cuisine style |
| FR-6.6 | The result shall display which of the user's listed ingredients were used (matched ingredient badges) |
| FR-6.7 | The user shall be able to request a different recipe without repeating previously shown results for the same ingredient set |
| FR-6.8 | Fridge-generated recipes shall be saved to the cookbook with `source = "fridge"` |

---

## 7. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | On-demand AI generation completes in ≤ 60 seconds; fallback library in ≤ 1 second |
| **Performance** | Cookbook search returns results in ≤ 2 seconds for up to 500 recipes |
| **Performance** | TheMealDB image fetch completes in ≤ 15 seconds; failure falls back to local image immediately |
| **Reliability** | Daily scheduled generation succeeds ≥ 99% of the time |
| **Reliability** | App functions fully without an AI API key using the fallback recipe library |
| **Reliability** | Email delivery failures are caught, logged, and do not block recipe saving |
| **Scalability** | Cookbook supports up to 1,000 stored recipes without degraded search performance |
| **Security** | User profile and email address are stored locally in SQLite; no third-party data sharing |
| **Compatibility** | App runs on macOS and Linux; defaults to port 8080 to avoid macOS AirPlay conflict on 5000 |

---

## 8. UX & Design Requirements

### Homepage
- Hero section: today's recipe with food photo, title, description, tag chips, prep/cook time, servings
- "This Week" strip: 4 most recent recipes as a horizontal card row
- On-demand CTA: "Need a recipe right now? ⚡ Generate Now"
- Buttons disable and show "Generating…" while a job is in progress

### Cookbook
- Default view: horizontal cuisine rows (grouped)
- Filtered view: flat grid ordered by date
- Persistent search bar; left filter panel with collapsible groups
- Active filter chips with individual remove and "Clear all"
- Recipe cards: food photo, title, tags, time, spice level

### Recipe Detail
- Full-width hero image with emoji fallback
- Stat row: prep time, cook time, servings, spice level
- Interactive serving scaler — adjusts ingredient quantities in real time
- Numbered instruction steps with orange gradient circles
- Allergen/age notes box when relevant

### My Profile
- Single-page form: dietary restrictions, spice slider, household size, age range, nutrition goals, cuisines, email, timezone
- Multi-select chips for categorical fields
- Accessible via "My Profile" in main nav

### What's in the Fridge?
- 3-step progressive form on a single page
- Step 1: text input + quick-add chips by food category (no grain chips)
- Step 2: optional sauce/base selector (deselectable)
- Step 3: optional cuisine selector (deselectable)
- Generate button enabled only when ≥ 1 ingredient entered
- Result: food photo + matched ingredient badges + "Try Different Recipe"

### Visual Design
- Warm food palette: orange `#e86d10` (CTAs), red `#c8301a` (spice), yellow `#e8a800` (nutrition), green `#3a8c1e` (dietary/success)
- Background `#fdf6ec` (warm cream), cards `#ffffff`, borders `#f0d9b8`
- Nav: spiced brown with logo and main links; no redundant Settings button
- See `design-guide.html` for full token reference and component library

### Responsive Design
- Mobile-first; card grid collapses to single column on screens < 480px
- Filter panel collapses on mobile
- Email template readable on mobile email clients

---

## 9. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│             Frontend (Jinja2 Templates + Vanilla JS)          │
│  Home · Cookbook · Recipe Detail · Profile · Fridge          │
└───────────────────────┬──────────────────────────────────────┘
                        │ HTTP / Flask routes
┌───────────────────────▼──────────────────────────────────────┐
│                   Flask Backend (app.py)                      │
│  /api/generate · /api/fridge-generate · /api/job/<id>        │
│  /api/search · APScheduler (5 PM cron) · Background threads  │
└──────┬────────────────────────┬──────────────┬───────────────┘
       │                        │              │
┌──────▼──────────┐  ┌──────────▼──────┐  ┌───▼─────────────┐
│  AI / Claude    │  │  SQLite DB      │  │  SMTP Email     │
│  claude-sonnet  │  │  (SQLAlchemy)   │  │  email_service  │
│  Falls back to  │  │  UserProfile    │  └─────────────────┘
│  41-recipe lib  │  │  Recipe         │
└──────┬──────────┘  └─────────────────┘
       │
┌──────▼──────────┐
│  TheMealDB API  │
│  (food photos)  │
│  No key needed  │
└─────────────────┘
```

### Key Components

| File | Responsibility |
|---|---|
| `app.py` | Flask routes, background job runner (`_jobs` dict + threading), APScheduler (5 PM cron) |
| `recipe_generator.py` | AI prompt builder, 41-recipe fallback library, fridge scoring, image pipeline (TheMealDB → local) |
| `models.py` | SQLAlchemy models: `UserProfile`, `Recipe` |
| `email_service.py` | SMTP email composition and delivery |
| `extensions.py` | SQLAlchemy `db` singleton |
| `static/js/app.js` | Generate-button handlers, async poll loop, interactive serving scaler |
| `static/css/styles.css` | Design tokens, layout, components |

### Async Generation Flow

```
Browser clicks "Generate"
  → POST /api/generate
  → Returns job_id immediately
  → Background thread calls Claude / fallback library
  → Browser polls GET /api/job/<id> every 2 seconds
  → On status=done → redirect to /recipe/<id>
  → Poll timeout: 90 attempts × 2s = 3 minutes
```

---

## 10. Data Model

### `UserProfile`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `email` | String | For email delivery |
| `dietary_restrictions` | JSON | `["vegetarian", "diabetic"]` |
| `spice_level` | Integer | 1–5 |
| `num_people` | Integer | 1–10 |
| `age_youngest` | Integer | Years |
| `age_oldest` | Integer | Years |
| `nutrition_goals` | JSON | `["protein-rich", "sugar-free"]` |
| `cuisines` | JSON | `["indian", "italian"]` |
| `timezone` | String | e.g. `"America/New_York"` |

### `Recipe`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `title` | String | Unique — deduplication enforced on insert |
| `description` | Text | |
| `cuisine_tag` | String | One of 7 supported cuisines |
| `nutrition_tags` | JSON | `["protein-rich", "iron-rich"]` |
| `dietary_tags` | JSON | `["vegetarian", "diabetic-friendly"]` |
| `spice_level` | Integer | 1–5 |
| `servings` | Integer | |
| `prep_time_min` | Integer | |
| `cook_time_min` | Integer | |
| `ingredients` | JSON | `[{name, quantity, unit}]` |
| `instructions` | JSON | Ordered string array |
| `allergen_notes` | Text | |
| `image_url` | String | `/static/images/{name}.jpg` or `""` |
| `generated_at` | DateTime | UTC |
| `source` | String | `"scheduled"` \| `"on_demand"` \| `"fridge"` |

### Search Implementation
- In-process Python filtering over `Recipe.query.all()`
- Text: lowercased substring match across title + description + ingredient names
- Tag filters: exact match on `cuisine_tag`, list intersection on `dietary_tags` / `nutrition_tags`
- Range filters: `spice_level ≤ max`, `prep_time_min + cook_time_min ≤ max`

---

## 11. Out of Scope

| Feature | Rationale |
|---|---|
| Grocery list / shopping cart | Supply-chain complexity; v2 candidate |
| Multi-user / multi-household profiles | Auth complexity out of scope for MVP |
| Social sharing or community recipes | Different product surface |
| Video or guided cooking mode | High content cost |
| Calorie / macro tracking | Requires nutritional database integration |
| Mobile native app | Web-first for MVP |
| Recipe rating or feedback loop | v2 — improves generation quality over time |
| Recipe deletion or archiving | No current user signal; v2 candidate |

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM generates a recipe violating a dietary constraint | Low (post-fix) | High | All constraints now injected directly into prompt JSON schema; fallback to library on parse failure |
| Daily cron job fails silently | Low | Medium | APScheduler logs to stdout; only starts in main Werkzeug process (not reloader subprocess) |
| Email delivery failure | Low | Medium | SMTP failures caught and logged; recipe still saved and accessible in cookbook |
| Recipe repetition | Medium | Low | Recent titles (7-day window) passed to generator as exclusion list; fridge mode tracks seen titles per session |
| AI API key unavailable | High | Low | Full 41-recipe fallback library covers all dietary types and cuisines |
| TheMealDB API unavailable | Low | Low | Falls back to local keyword-matched images immediately on any exception |
| On-demand generation timeout (browser side) | Low (post-fix) | Medium | Poll timeout increased to 3 minutes (90 × 2s); was 18 seconds before fix |
| Duplicate cookbook entries | Low | Low | `_save_recipe()` checks for existing title before insert |
| Fridge mode assuming grains user doesn't have | Medium | Medium | `_GRAIN_WORDS` set penalises grain-heavy recipes unless user listed them as ingredients |
| Port 5000 conflict on macOS | High on Mac | Low | App runs on port 8080 by default |

---

## 13. Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| OQ-1 | Which LLM model? | Engineering | **Resolved**: `claude-sonnet-4-6`; fallback to 41-recipe library when key absent |
| OQ-2 | Image strategy? | Design | **Resolved**: TheMealDB API (free, no key) → local keyword match → cuisine fallback |
| OQ-3 | Per-user timezone or global for 5 PM trigger? | Product | **Resolved**: Per-user timezone via APScheduler |
| OQ-4 | Email provider? | Engineering | **Resolved**: SMTP via `email_service.py`; configurable via ENV vars |
| OQ-5 | Should users be able to delete or archive recipes? | Product | **Open**: No delete UI in v1; v2 candidate |
| OQ-6 | Should fridge-generated recipes appear in the main cookbook? | Product | **Resolved**: Yes — saved with `source = "fridge"`, visible in cookbook |
| OQ-7 | How long should the browser poll for on-demand generation? | Engineering | **Resolved**: 3 minutes (90 × 2s); covers AI generation latency with margin |
| OQ-8 | Should all 7 cuisines appear in the fallback library, or only the original 4? | Product | **Open**: Fallback library currently covers Italian, Indian, Mexican, Mediterranean only; Chinese, American, European require AI key |
