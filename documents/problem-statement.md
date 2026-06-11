# Problem Statement — Family Fork

## The Problem

Planning meals for a household is deceptively hard. Dietary restrictions, nutrition goals, age-appropriate textures, spice tolerances, and cuisine preferences rarely align — and most recipe tools treat these as separate filters on a generic database rather than a coherent personal profile.

The result: families spend 15–20 minutes every evening deciding what to cook, fall back on the same five meals, and rarely discover recipes that actually fit everyone at the table.

There is no tool today that:
- Remembers your household's full dietary profile (restrictions + nutrition goals + spice level + ages + cuisines)
- Surfaces a new, relevant recipe every day without being asked
- Builds a living cookbook over time that grows with your family
- Makes last month's recipes as easy to find as today's
- Generates recipes from whatever is already in the fridge — without assuming you have pantry staples
- Delivers recipes passively by email — no app to open

---

## Who This Is For

**Primary user**: A home cook managing meals for a mixed household — potentially including toddlers, school-age kids, and adults — with varying dietary needs (vegetarian, diabetic-friendly, high-protein, etc.) and a preference for a specific cuisine rotation.

**Secondary concern**: Households where at least one person has a medical or lifestyle-driven dietary constraint (diabetic-friendly, no-carb, sugar-free) where generic recipe suggestions create extra filtering work.

**Also served**: Meat-eating households (chicken OK, seafood OK, any meat OK) who still want structured, cuisine-aware recipe ideas tailored to their profile.

---

## The Solution

**Family Fork** is a personalized, AI-powered recipe generation and cookbook platform. It learns a household's preferences once and continuously delivers tailored recipes — daily at 5 PM or on demand — building a growing, searchable cookbook over time.

Every generated recipe strictly respects all active profile constraints simultaneously: dietary restrictions, preferred cuisines, spice level, serving size, nutrition goals, and age range. Allergen and texture notes are automatically included for households with young children (age ≤ 12).

The app works entirely without an active AI API key by falling back to a curated library of 41 recipes across four cuisines, covering vegetarian, vegan, chicken, seafood, and diabetic-friendly diets. When a valid Anthropic API key is configured, it upgrades to AI-generated recipes via `claude-sonnet-4-6`.

---

## Core User Needs

| Need | How It Is Met |
|---|---|
| Recipes that fit everyone at the table | Profile captures dietary restrictions, age range, spice level, nutrition goals, and cuisines — all enforced at generation time |
| No decision fatigue at dinner time | One new recipe delivered automatically at 5 PM every day |
| Recipes that scale to household size | Ingredient quantities auto-adjusted for 1–10 people |
| Safe meals for young children | Age-aware generation: allergen/texture notes for youngest ≤ 5; child-friendly flavour notes for youngest ≤ 12 |
| Cuisine variety without manual searching | Supports 7 cuisines: Italian, Indian, Mexican, Mediterranean, Chinese, American, European |
| Nutrition goals baked in, not bolted on | Tags like `protein-rich`, `iron-rich`, `sugar-free` applied at generation time |
| Access to past recipes without digging | Full cookbook searchable by tag, ingredient, cuisine, or nutrition value |
| Passive discovery — no app to open | Email notification delivers each new recipe directly to the user |
| Using what's already in the fridge | "What's in the Fridge?" generates a recipe from specified ingredients; no grains assumed unless listed |
| Works for meat-eaters too | Chicken, seafood, and mixed-diet households supported alongside vegetarian/vegan |
| Meals for medically restricted diets | Dedicated diabetic-friendly recipes across all cuisine types |
| Relevant food photos without manual uploads | TheMealDB API fetches real food photos by dish name and cuisine at generation time; falls back to 41 local images |

---

## Pages & Features Built

### Home
- Today's featured recipe in a hero card with food photo, tags, and metadata
- "This Week" strip of recent recipes
- On-demand generation button (async — browser polls for completion, up to 3 minutes)

### Cookbook
- Browsable grid of all saved recipes, grouped by cuisine when unfiltered
- Filter panel: cuisine, dietary restriction, nutrition tag, max spice level, max total time
- Text search across title, description, and ingredients
- Active filter chips showing applied filters with clear options

### Recipe Detail
- Hero food photo with full recipe metadata (prep time, cook time, servings, spice level)
- Ingredients list with quantities and units; interactive serving scaler
- Step-by-step instructions with numbered circles
- Allergen/age notes section

### My Profile
- One-time setup for dietary restrictions, spice level, household size, age range, nutrition goals, preferred cuisines, email, and timezone
- Profile persists across sessions; editable at any time via nav

### What's in the Fridge?
- 3-step ingredient-based recipe generation
- Step 1: Add fresh ingredients via text input or quick-add chips (Vegetables, Proteins & Dairy, Aromatics — grains never assumed)
- Step 2: Optional sauce/cooking base selector (Tomato, Coconut Milk, Cream, Olive Oil, Broth, Yogurt, Dry)
- Step 3: Optional cuisine style selector
- "Try Different Recipe" generates a new result without repeating already-seen titles
- Matched ingredient badges show which fridge items the recipe uses

---

## Recipe Library

- **41 curated fallback recipes** across Italian, Indian, Mexican, and Mediterranean cuisines
- Covers: vegetarian, vegan, chicken, seafood, diabetic-friendly dietary categories
- Each recipe carries cuisine, nutrition, and dietary tags
- Smart profile-matching: cuisine and dietary filters applied when selecting from the fallback library
- All recipes have local food photos in `static/images/`

---

## Image Pipeline

Food photos are resolved in this order for each generated recipe:
1. Exact title match in the local `_RECIPE_IMAGES` dictionary
2. TheMealDB API — searched by full dish title, then key words, then cuisine area (free, no key required)
3. Local keyword-matched image from `static/images/`
4. Cuisine-based generic fallback from local images

---

## Design Direction

The UI uses a food-inspired warm palette — spiced browns in the navigation, cream page backgrounds, and four semantic accent colours (orange for actions, yellow for nutrition, red for spice, green for dietary/success). Recipe cards use real food photography with emoji fallbacks.

The combined layout: an editorial homepage spotlighting today's recipe, a full browsable cookbook with live filters, and a fridge tool for ingredient-driven cooking — all in a consistent warm visual system.

See `design-guide.html` for the full design token reference and component library.

---

## Key Features (Built)

1. **Household preference profile** — set dietary restrictions, spice level, number of people, age range, nutrition goals, and preferred cuisines once; all constraints enforced at generation time.
2. **Daily recipe generation** — one new recipe generated automatically at 5 PM, matched to the full profile.
3. **On-demand generation** — request a new recipe at any time from the home page; async with 3-minute browser poll.
4. **What's in the Fridge?** — ingredient-based recipe generation with sauce and cuisine controls, grain-free by default.
5. **Persistent cookbook** — every generated recipe is saved, tagged, and never lost; deduplication prevents repeat entries.
6. **Tag system** — each recipe carries cuisine, nutrition, and dietary tags applied at generation time.
7. **Search & filters** — full-text and tag-based search plus multi-dimension filter panel across the cookbook.
8. **Real food photos** — TheMealDB API fetches dish-matched photos at generation time; 41 local images as fallback.
9. **Email delivery** — each new recipe is emailed to the user immediately after generation.
10. **AI-optional** — runs fully with a curated fallback library when no Anthropic API key is configured; upgrades to Claude-generated recipes when a valid key is present.

---

## Success Looks Like

- A user can set up their household profile in under 2 minutes.
- Every daily recipe requires zero manual filtering to be suitable for the household.
- After 30 days, the user has a searchable cookbook of 30+ tailored recipes.
- Finding a past recipe takes under 10 seconds via search or tag browsing.
- The user never has to open the app to receive a new recipe — email is sufficient.
- A user with only a few fridge ingredients can generate a usable dinner recipe in under 60 seconds.

---

## Out of Scope (v1)

- Grocery list generation or shopping cart integration
- Multi-user / multi-household profiles
- Social sharing or community recipe submission
- Video or step-by-step guided cooking mode
- Calorie counting or detailed macro tracking
- Recipe rating or feedback loop
- Mobile native app (iOS / Android)
