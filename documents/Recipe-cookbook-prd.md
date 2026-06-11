# Product Requirements Document
## Family Fork

| Field | Value |
|---|---|
| Author | Poorva Mittal |
| Status | Shipped — v1 MVP |
| Version | 1.1 |
| Last Updated | 2026-04-24 |
| Target Release | v1 (MVP) — Shipped |

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
9. [System Architecture Overview](#9-system-architecture-overview)
10. [Data Model](#10-data-model)
11. [Out of Scope](#11-out-of-scope)
12. [Risks & Mitigations](#12-risks--mitigations)
13. [Open Questions](#13-open-questions)

---

## 1. Executive Summary

**Family Fork** is a personalized, AI-powered recipe generation and digital cookbook platform. Users set their household profile once — dietary restrictions, nutrition goals, spice tolerance, age range, number of people, and preferred cuisines — and the system delivers a new, tailored recipe every day at 5 PM, builds a growing searchable cookbook, and notifies the user by email.

The product removes the daily decision tax of meal planning without requiring users to actively engage with the app. A dedicated "What's in the Fridge?" feature lets users generate a recipe from whatever ingredients they already have, without assuming pantry items like grains or fresh produce. The app runs fully without an AI API key using a curated fallback library of 41 recipes, upgrading to Claude-generated recipes when a valid key is present.

---

## 2. Problem Statement

Families spend 15–20 minutes every evening deciding what to cook, fall back on the same meals repeatedly, and struggle to find recipe tools that holistically reflect their household's dietary profile. No existing tool:

- Holds a full household preference profile (restrictions + nutrition + spice + age + cuisine)
- Proactively surfaces a new relevant recipe every day
- Builds a living cookbook that grows and remains searchable over time
- Delivers recipes passively without requiring the user to open an app
- Generates recipes from what's actually in the fridge, without assuming ingredients

See `problem-statement.md` for the full problem framing.

---

## 3. Goals & Success Metrics

### Product Goals

| Goal | Description |
|---|---|
| Reduce decision fatigue | Eliminate the daily "what do I cook?" question for the household |
| Build a personal cookbook | Accumulate a growing, tagged, searchable library of household-relevant recipes |
| Passive delivery | User receives value (a recipe) without opening the app |
| Inclusivity | Every recipe is safe and appropriate for every member of the household — including diabetic, chicken, seafood, and mixed-diet households |
| Fridge-first cooking | Enable ingredient-led recipe generation with no pantry assumptions |

### Success Metrics (MVP)

| Metric | Target | Status |
|---|---|---|
| Profile setup completion time | ≤ 2 minutes | Met |
| Recipe relevance (manual audit) | ≥ 90% of generated recipes match all active profile constraints | Met |
| Daily email delivery success rate | ≥ 99% | Dependent on SMTP config |
| Time to find a past recipe via search | ≤ 10 seconds | Met |
| Cookbook size after 30 days of use | ≥ 30 recipes | Met (41 in fallback library) |
| On-demand recipe generation latency | ≤ 15 seconds (API); < 1 second (fallback) | Met |
| Fridge recipe generation | Works with 1+ ingredient, no pantry assumptions | Met |

---

## 4. User Personas

### Persona A — The Household Manager
> **"I need dinner sorted before 6 PM and I can't Google options every night."**

- **Age**: 28–45
- **Context**: Cooking for 2–6 people including children, managing at least one dietary restriction
- **Goal**: A reliable daily suggestion that requires no extra filtering
- **Pain point**: Generic recipe apps require manual filtering every single time; nothing remembers the family's needs

### Persona B — The Health-Conscious Cook
> **"I want high-protein, low-carb meals but I don't want to read macros every time."**

- **Age**: 25–50
- **Context**: Individual or couple with specific nutrition goals (diabetic-friendly, sugar-free, protein-rich)
- **Goal**: Recipes that fit their health goals without manual verification
- **Pain point**: Nutrition filters on recipe sites are unreliable or require paid tiers

### Persona C — The Curious Explorer
> **"I want to try new cuisines but I'm not sure where to start."**

- **Age**: 20–40
- **Context**: Single or small household, enjoys variety, wants to rotate across cuisines
- **Goal**: Be introduced to new cuisines within safe dietary guardrails
- **Pain point**: Too many choices; no trusted curator that knows their preferences

### Persona D — The Fridge Cook
> **"I have spinach, paneer, and a few tomatoes — what can I make right now?"**

- **Age**: Any
- **Context**: Doesn't want to shop; wants to use what's already on hand
- **Goal**: A recipe that uses their actual fridge contents, not a pantry shopping list
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
| US-06 | As a user, I want to choose preferred cuisines so that recipe variety matches my taste | P1 | Done |
| US-07 | As a user, I want to edit my profile at any time so that changes in household needs are reflected immediately | P1 | Done |

### Recipe Generation

| ID | Story | Priority | Status |
|---|---|---|---|
| US-08 | As a user, I want to receive a new recipe every day at 5 PM so that I don't have to plan dinner myself | P0 | Done |
| US-09 | As a user, I want to request a recipe on demand so that I can get inspiration outside the daily cadence | P0 | Done |
| US-10 | As a user, I want every generated recipe to respect all my active profile constraints simultaneously | P0 | Done |
| US-11 | As a user, I want the recipe to include ingredients, quantities (scaled to my household size), and step-by-step instructions | P0 | Done |
| US-12 | As a user, I want each recipe to display its cuisine type, nutrition tags, and dietary compatibility clearly | P1 | Done |
| US-13 | As a user, I want the daily recipe to feel fresh and not repeat recent suggestions | P1 | Done |

### Cookbook

| ID | Story | Priority | Status |
|---|---|---|---|
| US-14 | As a user, I want every generated recipe automatically saved to my cookbook so I never lose it | P0 | Done |
| US-15 | As a user, I want to browse my cookbook organized by cuisine and nutrition tags | P1 | Done |
| US-16 | As a user, I want to search my cookbook by ingredient, cuisine, tag, or free text | P0 | Done |
| US-17 | As a user, I want each recipe card to show key metadata (cuisine, nutrition tags, date added, servings) at a glance | P1 | Done |

### Notifications

| ID | Story | Priority | Status |
|---|---|---|---|
| US-18 | As a user, I want to receive an email with the full recipe when a new one is generated so I don't need to open the app | P0 | Done |
| US-19 | As a user, I want the email to include a link back to the full cookbook entry | P2 | Done |

### Fridge Feature

| ID | Story | Priority | Status |
|---|---|---|---|
| US-20 | As a user, I want to enter the ingredients I have on hand and get a recipe that only uses those items | P1 | Done |
| US-21 | As a user, I want to optionally specify a sauce type or cooking style so the recipe fits what I want to make | P1 | Done |
| US-22 | As a user, I want to optionally narrow the cuisine style so the fridge recipe matches my mood | P1 | Done |
| US-23 | As a user, I want to see which of my fridge ingredients were used in the generated recipe | P1 | Done |
| US-24 | As a user, I want to click "Try Different Recipe" to get a new suggestion without repeating the previous result | P1 | Done |

---

## 6. Functional Requirements

### FR-1: Household Profile

| Req ID | Requirement |
|---|---|
| FR-1.1 | The system shall allow the user to configure dietary restrictions: `vegetarian`, `vegan`, `chicken`, `seafood`, `any-meat`, `diabetic-friendly` (multi-select) |
| FR-1.2 | The system shall allow the user to set a spice level from 1 (very mild) to 5 (very hot) |
| FR-1.3 | The system shall allow the user to set the number of people from 1 to 10 |
| FR-1.4 | The system shall allow the user to specify the youngest and oldest eater's age (range: 2 years to 10+) |
| FR-1.5 | The system shall allow the user to select nutrition requirements: `protein-rich`, `iron-rich`, `vitamin-rich`, `no-carb`, `balanced`, `sugar-free` (multi-select) |
| FR-1.6 | The system shall allow the user to select preferred cuisines: `italian`, `indian`, `mexican`, `mediterranean` (multi-select) |
| FR-1.7 | The system shall persist profile settings across sessions |
| FR-1.8 | The system shall allow the user to edit any profile field at any time; changes apply to the next generated recipe |
| FR-1.9 | The system shall allow the user to set their email address and timezone for daily delivery |

### FR-2: Recipe Generation

| Req ID | Requirement |
|---|---|
| FR-2.1 | The system shall automatically generate one recipe daily at 5 PM per the user's configured timezone |
| FR-2.2 | The system shall generate a recipe on demand when the user requests it |
| FR-2.3 | Every generated recipe shall comply with all active profile constraints simultaneously |
| FR-2.4 | The system shall scale ingredient quantities to the configured number of people |
| FR-2.5 | The system shall include allergen and texture notes when the youngest eater is under 5 years old |
| FR-2.6 | Each recipe shall include: title, description, cuisine tag, nutrition tags, dietary tags, ingredient list (with quantities), step-by-step instructions, estimated prep and cook time, serving count, and spice level |
| FR-2.7 | The system shall avoid repeating a recipe generated in the prior 30 days |
| FR-2.8 | When no valid AI API key is configured, the system shall fall back to the curated recipe library and apply the same profile-matching constraints |

### FR-3: Cookbook

| Req ID | Requirement |
|---|---|
| FR-3.1 | Every generated recipe shall be automatically saved to the cookbook |
| FR-3.2 | Each cookbook entry shall carry tags for: cuisine, nutrition values, and dietary compatibility |
| FR-3.3 | The cookbook shall be searchable by: free text (title, ingredients, description), cuisine tag, nutrition tag, dietary tag |
| FR-3.4 | The cookbook shall display recipes in reverse chronological order by default |
| FR-3.5 | The cookbook shall support browsing by cuisine category in the default (unfiltered) view |
| FR-3.6 | Each recipe card shall display: food photo (with emoji fallback), title, cuisine tag, key nutrition/diet tags, prep+cook time, and spice level |
| FR-3.7 | The filter panel shall support: cuisine, dietary restriction, nutrition tag, maximum spice level, and maximum total cook time |
| FR-3.8 | The system shall not create duplicate cookbook entries for the same recipe title |

### FR-4: Email Notification

| Req ID | Requirement |
|---|---|
| FR-4.1 | The system shall send an email to the configured user address each time a recipe is generated (daily or on demand) |
| FR-4.2 | The email shall include the full recipe: title, ingredients, instructions, and all tags |
| FR-4.3 | The email shall include a link to the recipe's cookbook entry |
| FR-4.4 | Email delivery shall occur within 5 minutes of recipe generation |

### FR-5: What's in the Fridge?

| Req ID | Requirement |
|---|---|
| FR-5.1 | The system shall allow the user to enter a list of fresh ingredients they have on hand |
| FR-5.2 | The generated recipe shall use only the specified ingredients plus up to 5 pantry staples (salt, dried spices, oil) |
| FR-5.3 | The system shall never assume grains (rice, pasta, bread, naan, tortillas, etc.) unless the user explicitly adds them to their ingredient list |
| FR-5.4 | The user may optionally select a sauce/cooking base: tomato, coconut milk, cream/butter, olive oil, broth, yogurt, or dry |
| FR-5.5 | The user may optionally select a cuisine style to narrow the recipe suggestion |
| FR-5.6 | The result shall display which of the user's listed ingredients were used in the recipe (matched ingredient badges) |
| FR-5.7 | The user shall be able to click "Try Different Recipe" to generate a new result without repeating previously shown recipes for the same ingredient set |
| FR-5.8 | The fridge-generated recipe shall be saved to the cookbook with `source = "fridge"` |

---

## 7. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | On-demand recipe generation completes in ≤ 15 seconds (AI) or ≤ 1 second (fallback library) |
| **Performance** | Cookbook search returns results in ≤ 2 seconds for a library up to 500 recipes |
| **Reliability** | Daily scheduled generation succeeds ≥ 99% of the time |
| **Reliability** | Email delivery success rate ≥ 99% (when SMTP is configured) |
| **Reliability** | App must function fully without an AI API key using the fallback recipe library |
| **Scalability** | Cookbook supports up to 1,000 stored recipes without degraded search performance |
| **Security** | User profile and email address are stored locally; no third-party sharing |
| **Availability** | System uptime ≥ 99.5% (excluding planned maintenance) |

---

## 8. UX & Design Requirements

### Layout Principles

**Homepage / Daily View**
- Hero section featuring today's generated recipe with a food photo (local static image), recipe title, and key tag chips
- "This Week's Recipes" strip showing the 4 most recent recipes as a horizontal card row
- On-demand generation CTA strip: "Need a recipe right now? ⚡ Generate Now"

**Cookbook / Browse View**
- Horizontal category rows by cuisine when no filters applied (default view)
- Persistent search bar at the top; left filter panel with collapsible groups
- Filters: Cuisine, Dietary Restrictions, Nutrition, Spice Level (range slider), Total Cook Time (range slider)
- Active filter pills strip showing applied filters with individual remove buttons and "Clear all"
- Each recipe card: food photo with emoji fallback, title, tag chips, time metadata, spice dots

**Recipe Detail View**
- Full-width food hero image (local static file with emoji fallback)
- Title, all tag chips
- Stat cards: Prep time, Cook time, Servings, Spice level
- Ingredients list with quantities and units
- Step-by-step instructions with numbered orange-gradient circles
- Allergen/age notes box when youngest eater is under 5

**Profile Setup**
- Single-page form: dietary restrictions, spice slider, household size + age range, nutrition goals, cuisines, email, timezone
- Multi-select chips for dietary, nutrition, and cuisine fields
- Orange-red gradient bubble showing live spice value

**What's in the Fridge?**
- 3-step progressive form on a single page
- Step 1: Text input + categorized quick-add chips (Vegetables / Proteins & Dairy / Aromatics & Extras — no grain chips shown)
- Step 2: Single-select sauce/cooking base chips (7 options) — deselectable
- Step 3: Single-select cuisine chips (4 options) — deselectable
- Generate button enabled only when ≥ 1 ingredient added
- Result card: food photo + matched ingredient badges (green) + "Try Different Recipe" button

### Visual Design
- Warm food-inspired palette: orange (#e86d10) for CTAs, red (#c8301a) for spice/alerts, yellow (#e8a800) for nutrition, green (#3a8c1e) for dietary/success
- Page background: #fdf6ec (warm cream); cards: #ffffff; borders: #f0d9b8
- All food photos served from local `static/images/` directory; emoji fallback if image fails to load
- See `design-guide.html` for full token reference and component library

### Responsive Design
- Mobile-first; card grid collapses to single-column on screens < 480px
- Filter panel collapses on mobile (accessible via toggle)
- Email template is responsive and readable on mobile email clients

---

## 9. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Frontend (Jinja2 Templates + Vanilla JS)        │
│  Home · Cookbook · Recipe Detail · Profile · Fridge         │
└────────────────────────┬────────────────────────────────────┘
                         │ Flask routes
┌────────────────────────▼────────────────────────────────────┐
│                    Flask Backend (app.py)                    │
│  /api/generate · /api/fridge-generate · /api/search         │
│  APScheduler (5 PM cron) · Email Service                    │
└───────┬───────────────────────┬───────────────┬─────────────┘
        │                       │               │
┌───────▼──────────┐  ┌─────────▼──────┐  ┌────▼────────────┐
│  AI / Claude API │  │  SQLite DB     │  │  Email (SMTP)   │
│  claude-sonnet   │  │  (SQLAlchemy)  │  │  (email_service)│
│  Falls back to   │  │  UserProfile   │  └─────────────────┘
│  41-recipe lib   │  │  Recipe        │
└──────────────────┘  └────────────────┘
```

**Key components:**
- **`app.py`** — Flask routes, scheduler setup, request handling
- **`recipe_generator.py`** — Claude API calls, 41-recipe fallback library, fridge scoring logic, image lookup
- **`models.py`** — SQLAlchemy models: `UserProfile`, `Recipe`
- **`email_service.py`** — SMTP email sending
- **`static/images/`** — Local food photos (no CDN dependency)
- **Scheduler** — APScheduler fires daily at 17:00; skipped in Werkzeug reloader subprocess
- **Port** — 8080 (5000 occupied by macOS AirPlay Receiver)

---

## 10. Data Model

### `UserProfile`
```
id                  Integer (auto-increment PK)
email               String
dietary_restrictions JSON    // e.g. ["vegetarian", "diabetic-friendly"]
spice_level         Integer  // 1–5
num_people          Integer  // 1–10
age_youngest        Integer  // years
age_oldest          Integer  // years
nutrition_goals     JSON     // e.g. ["protein-rich", "sugar-free"]
cuisines            JSON     // e.g. ["indian", "italian"]
timezone            String   // e.g. "America/New_York"
```

### `Recipe`
```
id                  Integer (auto-increment PK)
title               String   (unique — deduplication enforced on insert)
description         String
cuisine_tag         String   // "italian" | "indian" | "mexican" | "mediterranean"
nutrition_tags      JSON     // ["protein-rich", "iron-rich"]
dietary_tags        JSON     // ["vegetarian", "diabetic-friendly"]
spice_level         Integer  // 1–5
servings            Integer
prep_time_min       Integer
cook_time_min       Integer
ingredients         JSON     // [{name, quantity, unit}]
instructions        JSON     // ordered string array
allergen_notes      String
image_url           String   // "/static/images/{name}.jpg" or ""
generated_at        DateTime
source              String   // "scheduled" | "on_demand" | "fridge"
```

### Search
- In-process Python filtering over `Recipe.query.all()`
- Text search: title + description + ingredient names (lowercased substring match)
- Tag filters: exact match on `cuisine_tag`, `dietary_tags`, `nutrition_tags`
- Range filters: `spice_level ≤ max`, `prep_time_min + cook_time_min ≤ max`

---

## 11. Out of Scope

The following are explicitly deferred to future versions:

| Feature | Rationale |
|---|---|
| Grocery list / shopping cart integration | Significant supply-chain complexity; v2 candidate |
| Multi-user / multi-household profiles | Auth complexity out of scope for MVP |
| Social sharing or community recipe submission | Different product surface; no current user signal |
| Video or guided cooking mode | High content production cost |
| Detailed calorie / macro tracking | Requires nutritional database integration |
| Mobile native app (iOS / Android) | Web-first for MVP; native app based on adoption |
| Recipe rating or feedback loop | v2 — improves generation quality over time |
| Serving adjuster that rescales quantities in real time | UX enhancement; quantities currently static post-generation |

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM generates a recipe that violates a dietary constraint | Medium | High | Validate every output against profile constraints before saving; fallback to library on failure |
| Daily cron job fails silently | Low | Medium | APScheduler logs to stdout; scheduler only starts in main Werkzeug process (not reloader subprocess) |
| Email delivery failure | Low | Medium | SMTP failures are caught and logged; recipe still saved and accessible in cookbook |
| Recipe repetition within 30-day window | Medium | Low | Recent titles passed to generator as exclusion list; fridge mode tracks seen titles per session |
| LLM API key not available (corporate policy, cost) | High | Low | Full fallback library of 41 recipes covers all dietary types and cuisines without API dependency |
| Corporate network blocking PyPI | Medium | Medium | Use Alibaba mirror (`mirrors.aliyun.com`) for pip install |
| Port 5000 conflict (macOS AirPlay Receiver) | High on Mac | Low | App runs on port 8080 by default |
| Duplicate cookbook entries from repeated generation | Low | Low | `_save_recipe()` checks for existing title before insert |
| Fridge mode assuming grains user doesn't have | Medium | Medium | `_GRAIN_WORDS` set penalizes grain-heavy recipes unless user added those grains to ingredient list |

---

## 13. Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| OQ-1 | Which LLM provider and model will be used? | Engineering | **Resolved**: Anthropic `claude-sonnet-4-6`; fallback to 41-recipe library when key absent |
| OQ-2 | What is the image strategy? | Design | **Resolved**: Local static files from Unsplash (downloaded at setup); emoji fallback |
| OQ-3 | Should 5 PM trigger be per-user timezone or global? | Product | **Resolved**: Per-user timezone via APScheduler; UTC fallback if timezone not set |
| OQ-4 | What email provider? | Engineering | **Resolved**: SMTP via `email_service.py`; configurable via ENV vars |
| OQ-5 | Should users be able to delete or archive recipes? | Product | **Open**: Currently no delete UI; v2 candidate |
| OQ-6 | Max cuisines/nutrition tags — are all combinations valid? | Product | **Resolved**: All combinations valid; no constraint on selection count |
| OQ-7 | Should fridge-generated recipes appear in the main cookbook? | Product | **Resolved**: Yes — saved with `source = "fridge"` tag, visible in cookbook |
