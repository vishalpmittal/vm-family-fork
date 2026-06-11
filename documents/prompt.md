# Family Fork — Product Prompts

This file documents the prompts used to build the application from a product manager's perspective — describing user problems, desired outcomes, and acceptance criteria at each stage. Prompts are organized chronologically from initial concept through all features and documentation.

---

## Phase 1 — Core Product

### 1.1 Define the Product Vision

> I want to build a web app called **Family Fork** that solves a real household problem: families spend 15–20 minutes every evening deciding what to cook, fall back on the same meals, and can never find a recipe tool that actually remembers their household's full dietary profile.
>
> The app should:
> - Let a household set their preferences once (dietary restrictions, spice tolerance, family size, ages, nutrition goals, cuisine preferences) and never ask again
> - Automatically deliver a new, tailored recipe every day at 5 PM
> - Allow on-demand recipe generation at any time
> - Build a permanent, searchable cookbook of every recipe ever generated
> - Send the recipe by email so the user never has to open the app to receive value
>
> Use AI (Anthropic Claude) to generate the recipes. The app should be web-based with a warm, food-inspired visual design. Start with a clean scaffold — I'll describe each page next.

### 1.2 Household Profile — Set Preferences Once

> **User problem**: Every time a user opens a recipe app, they have to re-filter for their dietary needs. This app should remember everything about their household so they never filter again.
>
> Build a profile setup page where users configure their household once. It needs:
>
> **Dietary restrictions** (multi-select, all that apply):
> Vegetarian · Vegan · Chicken OK · Seafood OK · Any Meat OK · Diabetic-friendly
>
> **Spice level**: A slider from 1 (very mild) to 5 (very hot) — the whole household eats together, so this is the household max
>
> **Who's eating**: Number of people (1–10) and the age of the youngest and oldest eater — recipes should be safe for the youngest and satisfying for adults
>
> **Nutrition goals** (multi-select): Protein-rich · Iron-rich · Vitamin-rich · No-carb · Balanced · Sugar-free
>
> **Cuisine preferences** (multi-select): Indian · Italian · Mexican · Mediterranean
>
> **Email + timezone**: Where to send the daily recipe and when "5 PM" means
>
> The profile should persist across sessions. If no profile exists when the user visits the app, redirect them here first. Once saved, redirect to the home page.
>
> **Acceptance criteria**: A first-time user can complete the profile in under 2 minutes. All selections are remembered if the user revisits the page to edit them.

### 1.3 Home Page — Today's Recipe at a Glance

> **User problem**: The user wants to know what they're cooking tonight at a glance — without searching, filtering, or making any decisions.
>
> Build a home page that shows:
> - **Today's recipe hero**: the most recently generated recipe displayed prominently with its title, a short description, all its tags (cuisine, dietary, nutrition, spice level), prep + cook time, and serving count. Include a "View Full Recipe" button.
> - **This Week's Recipes**: a horizontal strip of the 4 most recent recipes as cards (photo, title, tags, time)
> - **On-demand strip**: a clearly visible section at the bottom — "Need a recipe right now?" with a generate button for users who want inspiration outside the 5 PM schedule
>
> If the user hasn't set up their profile yet, redirect them to profile setup.
>
> **Acceptance criteria**: A user who opens the app after 5 PM sees today's recipe immediately — no clicks required. The generate button is clearly visible for on-demand use.

### 1.4 Cookbook — Browse and Find Past Recipes

> **User problem**: After 30 days, a user has 30+ recipes. Finding last month's Indian vegetarian recipe that the kids loved should take under 10 seconds — not a scroll through an unsorted list.
>
> Build a cookbook page with two ways to find recipes:
>
> **Browse mode** (default, no filters applied): recipes grouped in rows by cuisine — one row for Indian, one for Italian, etc. Familiar and easy to scan.
>
> **Filter + search mode**: when the user applies any filter or types in the search box, switch to a flat filtered grid. Filters should include:
> - Cuisine (checkboxes)
> - Dietary restrictions (checkboxes)
> - Nutrition tags (checkboxes)
> - Maximum spice level (slider)
> - Maximum total cook time (slider)
>
> Active filters should be visible as removable pills above the results so the user always knows what's applied. "Clear all" removes everything at once.
>
> The search box should match against recipe title, description, and ingredients — so searching "spinach" finds any recipe that uses spinach.
>
> **Acceptance criteria**: A user can find any past recipe in under 10 seconds using either search or filters. Applied filters are visible and easy to remove one at a time.

### 1.5 Recipe Detail — Everything Needed to Cook

> **User problem**: Once a user finds a recipe they want to make, they need everything in one place — no scrolling back and forth, no guessing quantities.
>
> Build a recipe detail page that shows:
> - A food photo (or a visual placeholder if none is available)
> - Recipe title and all its tags as chips
> - At-a-glance stats: prep time, cook time, servings, spice level
> - Complete ingredients list with names and exact quantities
> - Step-by-step instructions, clearly numbered
> - An allergen/age note if relevant — e.g. "Youngest eater is 3 years old: cut paneer into small soft cubes, reduce whole spices"
> - A back button to return to the cookbook
>
> **Acceptance criteria**: A user can open this page on their phone in the kitchen and follow the recipe from start to finish without needing to reference anything else.

### 1.6 Daily Recipe Generation — The Core Value Delivery

> **User problem**: Deciding what to cook every day is exhausting. The app's core promise is that it handles this decision automatically.
>
> The app should use AI (Anthropic Claude) to generate a recipe every day at 5 PM that:
> - Matches all of the user's active profile constraints simultaneously (dietary, spice, nutrition, cuisine)
> - Scales ingredient quantities to the household's configured serving count
> - Includes allergen and texture guidance when the youngest eater is under 5 years old
> - Avoids repeating any recipe generated in the past 30 days
> - Is saved to the cookbook automatically
> - Triggers an email notification immediately after generation
>
> **Acceptance criteria**: The 5 PM recipe arrives in the user's inbox and appears at the top of the home page — no user action required. Every generated recipe complies with all profile constraints.

### 1.7 Email Delivery — Value Without Opening the App

> **User problem**: The user's phone is in the kitchen. They don't want to open a browser — they want the recipe to arrive in their inbox so they can read it directly.
>
> After every recipe generation (daily at 5 PM or on-demand), send an email to the user's configured address containing:
> - Recipe title and short description
> - All tags (cuisine, dietary, nutrition, spice)
> - Full ingredient list with quantities
> - Step-by-step instructions
> - A link to view the full recipe in the cookbook
>
> **Acceptance criteria**: The user receives the email within 5 minutes of generation and can follow the recipe entirely from email without opening the app.

---

## Phase 2 — Unblocking the Build

### 2.1 Corporate Network Blocking Package Downloads

> We're trying to set up the app on a work laptop but pip can't download packages — our company network uses OpenDNS which blocks the Python Package Index (PyPI). We need to install Flask, the database library, the scheduler, the environment variable handler, and the Anthropic SDK. What's the workaround?

### 2.2 App Not Loading — Port Conflict on Mac

> When I try to open the app in the browser, I get a "401 Unauthorized" error immediately — before I've done anything. I'm on a Mac. The app seems to be starting but something is intercepting the request before it reaches our code. How do I fix this so the app is accessible normally?

### 2.3 App Must Work Without an AI API Key

> Our company doesn't provide access to Anthropic API keys, so the app can't rely on AI generation to function. However, the app should still deliver its full user experience — daily recipes, on-demand generation, cookbook, email — just using a built-in recipe library as the source instead of the AI.
>
> **Requirements:**
> - The app should detect automatically whether a valid API key is present and fall back to the built-in library if not — no configuration or mode-switching required from the user
> - The fallback library needs enough recipes to cover all 4 cuisines (Indian, Italian, Mexican, Mediterranean) and all dietary types
> - The fallback selection must still respect the user's profile — a user who selected Indian cuisine and vegetarian should only see Indian vegetarian recipes
> - The user experience should be identical regardless of whether recipes come from AI or the library
>
> **Acceptance criteria**: The app runs end-to-end — profile, home page, daily generation, cookbook — with no API key configured. The user cannot tell the difference from the UI.

---

## Phase 3 — Fixing What's Broken

### 3.1 Cookbook Filters Don't Work

> **User-reported issue**: When I check a filter in the cookbook's left panel (e.g. "Vegetarian" or "Indian"), nothing happens. The checkbox appears to be clickable but the recipe list doesn't change.
>
> **Expected behavior**: Selecting any filter should immediately update the recipe list to show only matching recipes, and the selected filter should appear as a pill in the active filter strip above the results.
>
> Investigate why the filter checkboxes aren't triggering a results update and fix it. The filter state should also survive a page refresh — if a user applies filters and then navigates back, the filters should still be applied.
>
> **Acceptance criteria**: A user can check "Vegetarian" and immediately see only vegetarian recipes. Multiple filters stack (e.g. "Vegetarian" + "Indian" shows only Indian vegetarian recipes). Applied filters are visible as removable pills.

---

## Phase 4 — Growing the Recipe Library

### 4.1 The Library Is Too Small — Users Need More Variety

> **User problem**: With only 8 recipes in the fallback library, users will start seeing the same recipes within days. A household checking the app daily needs at least a month of variety before recipes repeat.
>
> Expand the recipe library to at least 20 recipes, adding more options across all 4 cuisines. Prioritize vegetarian and vegan options since those are the most common dietary restrictions. Each recipe should feel like something a real home cook would actually make on a Friday night — not exotic or overly complex.
>
> Add to the library:
> - Indian: Chana Masala, Dal Makhani, Aloo Gobi, Vegetable Biryani
> - Italian: Tuscan White Bean Pasta, Margherita Pizza, Mushroom Risotto, Minestrone Soup, Gnocchi with Pesto
> - Mexican: Black Bean Tacos, Enchiladas, Veggie Burrito Bowl, Quesadillas, Tortilla Soup
> - Mediterranean: Greek Salad, Lemon Herb Orzo, Shakshuka, Falafel with Tzatziki, Stuffed Bell Peppers
>
> **Acceptance criteria**: A household that uses the app daily with no API key will see a different recipe every day for at least 3 weeks before any repetition.

### 4.2 The App Is Too Vegetarian-Focused — Add Chicken and Seafood

> **User feedback**: Households that eat chicken or seafood have very few recipe options. The app currently skews heavily vegetarian even when the user's profile says "Chicken OK" or "Seafood OK".
>
> Add chicken and seafood recipes to the library so those users get relevant options:
> - Indian: Butter Chicken, Chicken Tikka Masala, Goan Prawn Curry
> - Italian: Chicken Piccata, Shrimp Scampi, Chicken Parmigiana
> - Mexican: Chicken Fajitas, Shrimp Tacos, Chicken Enchiladas
> - Mediterranean: Lemon Herb Chicken, Garlic Shrimp Orzo, Chicken Souvlaki
>
> These recipes should only appear for users who have selected "Chicken OK" or "Seafood OK" in their profile — they should never surface for vegetarian or vegan users.
>
> **Acceptance criteria**: A user with "Chicken OK" selected gets chicken recipes when browsing. A vegetarian user never sees a recipe containing chicken or seafood.

### 4.3 No Recipes for Diabetic Users

> **User problem**: The diabetic-friendly filter exists in the profile setup, but selecting it doesn't change anything — there are no diabetic-friendly tagged recipes in the library. This is a broken promise to a user who specifically set that restriction.
>
> Add diabetic-friendly recipes across all 4 cuisines. These recipes must use low-glycemic ingredients, avoid added sugars, avoid refined carbs, and be genuinely appropriate for a diabetic diet — not just vaguely "healthy". Aim for 2–3 options per cuisine.
>
> - Indian: Methi Dal (Fenugreek Lentil Curry), Egg Bhurji, Tandoori Spiced Chicken with Cucumber Raita
> - Italian: Zucchini Noodles with Basil Pesto, Oven-Baked Salmon with Mediterranean Vegetables
> - Mexican: Chicken Lettuce Wrap Tacos, Mexican Black Bean and Vegetable Soup
> - Mediterranean: Greek Salad with Grilled Chicken, Red Lentil and Spinach Soup
>
> **Acceptance criteria**: A user with "Diabetic-friendly" selected in their profile only receives recipes appropriate for a diabetic diet. The diabetic filter in the cookbook returns results.

---

## Phase 5 — Visual Identity

### 5.1 Recipe Cards Have No Photos — The App Feels Unfinished

> **User problem**: Every recipe card shows a blank placeholder where a food photo should be. For a food app, visual presentation is part of the product — users form an appetite from seeing the dish before committing to cook it.
>
> Add a real food photo to every recipe in the library. The photos should:
> - Be actual photos of the dish (not generic food stock images)
> - Load quickly (serve from the app itself, not a slow external CDN)
> - Have a graceful fallback (a cuisine emoji) if the image fails to load for any reason
> - Automatically be assigned to any new recipe based on its title or cuisine
>
> **Acceptance criteria**: Every recipe card shows a real photo of the dish on the home page, cookbook, and recipe detail page. If a photo can't load, the card shows an appropriate emoji instead of a broken image icon.

### 5.2 Broken Images Are Causing Page Errors

> **User-reported issue**: After adding recipe images, the app is throwing a template rendering error on multiple pages. The error appears to be caused by how the fallback emoji is being inserted into the page template. The app is currently broken for all users.
>
> Fix this immediately — the page must render without errors, and the image fallback behavior (show emoji when photo fails to load) must still work correctly.
>
> **Acceptance criteria**: All pages load without errors. Recipe cards show the food photo when available, and the cuisine emoji when the photo fails to load — no broken image icons.

### 5.3 Wrong Photo for Palak Paneer

> **User feedback**: The Palak Paneer recipe is showing a photo of what looks like jeera rice on a plain background — not the creamy green spinach curry the dish actually is. This is misleading and makes the recipe look unappetizing.
>
> Find and use a correct, appetizing photo of Palak Paneer — the dish should show a creamy green spinach gravy with visible paneer cubes — and update it in the app.
>
> **Acceptance criteria**: The Palak Paneer recipe displays an accurate, appetizing photo of the dish.

---

## Phase 6 — What's in the Fridge?

### 6.1 New Feature: Cook from What You Already Have

> **User problem**: Sometimes users don't want a recipe based on their preferences — they want to use what's already in the fridge before it goes bad. No current app does this without assuming you also have a fully stocked pantry.
>
> Build a new "What's in the Fridge?" page. The user experience should be:
>
> 1. **Add your ingredients**: User types in what they have (spinach, paneer, tomatoes) or picks from quick-add chips organized by category — Vegetables, Proteins & Dairy, Aromatics. **Do not suggest grains** (rice, pasta, bread, naan) as quick-add options — those are pantry items, not fridge items, and users shouldn't be nudged to assume they have them.
>
> 2. **Pick a sauce style** (optional): If the user wants a specific cooking style — tomato-based, coconut milk, cream, olive oil, broth, yogurt, or dry — they can select it. Leave blank to let the app decide.
>
> 3. **Pick a cuisine** (optional): Narrow to a specific style (Indian, Italian, Mexican, Mediterranean) or leave blank for any.
>
> 4. **Generate**: One button that's disabled until at least 1 ingredient is added. When clicked, shows a recipe card with the dish name, description, which of the user's ingredients are used (highlighted with ✓ badges), and time/serving info.
>
> 5. **Try again**: "Try Different Recipe" generates a new suggestion — different from the previous result.
>
> **Acceptance criteria**: A user with 3 random fridge items gets a plausible recipe that uses those items. The recipe never requires grains the user didn't add. Each click of "Try Different Recipe" returns a different dish.

### 6.2 Fridge Recipes Should Be Saved to the Cookbook

> Any recipe generated from the Fridge page should be saved to the user's cookbook automatically, just like daily and on-demand recipes. It should be tagged to indicate it came from the fridge so the user can tell them apart.
>
> **Acceptance criteria**: After using the Fridge feature, the generated recipe appears in the cookbook. The recipe is identifiable as fridge-sourced if the user looks for it.

### 6.3 Fridge Mode Must Never Assume Pantry Items

> **User problem**: The current fridge generation is suggesting recipes that require rice or pasta that the user never said they had. The whole point of this feature is to use only what's available — assuming pantry staples defeats the purpose.
>
> The fridge recipe generator must never include grains (rice, pasta, bread, naan, tortilla, couscous, orzo, gnocchi, etc.) in a recipe unless the user explicitly added that grain to their ingredient list. Minor pantry staples like salt, dried spices, and oil are fine to assume.
>
> **Acceptance criteria**: A user who adds only "spinach, paneer, tomatoes" gets a recipe that doesn't require rice, pasta, or bread. If they add "basmati rice" to the list, a rice-based recipe is acceptable.

### 6.4 "Try Different Recipe" Returns the Same Recipe Every Time

> **User-reported issue**: Clicking "Try Different Recipe" on the Fridge page generates the same recipe again. The user expects a different suggestion each time.
>
> Fix this so each click produces a genuinely different recipe. The app should remember which recipes it's already shown the user for the current ingredient set and not repeat them. When the user changes their ingredients, the history should reset so they get fresh suggestions.
>
> **Acceptance criteria**: Clicking "Try Different Recipe" 3 times in a row produces 3 different recipes. Changing the ingredient list resets the history.

---

## Phase 7 — Data Quality

### 7.1 The Cookbook Has Duplicate Entries

> **User-reported issue**: The cookbook is showing the same recipe multiple times — for example, "Palak Paneer with Jeera Rice" appears 5 times. This makes the cookbook cluttered and confusing.
>
> Fix this in two ways:
> 1. **Clean up existing duplicates**: For any recipe that appears more than once, keep the original (first-added) entry and remove the rest
> 2. **Prevent future duplicates**: Before saving any new recipe, check if a recipe with the same title already exists. If it does, don't create a new entry
>
> **Acceptance criteria**: Each recipe title appears exactly once in the cookbook. Generating an on-demand recipe that was already generated before doesn't create a second copy.

---

## Phase 8 — Documentation

### 8.1 Update the Problem Statement

> The `problem-statement.md` was written before the product was built, as a vision document. Now that the product is shipped, update it to reflect what was actually built and delivered — including the Fridge feature, chicken/seafood/diabetic support, and the AI-optional fallback system. Add a clear "Features Built" section so a new reader understands exactly what the product does today.

### 8.2 Update the Design Guide

> The design guide (`design-guide.html`) was created before the Fridge page existed. Update it to v1.1 to document the new visual components that were introduced with the Fridge feature — specifically the ingredient chips, the single-select option chips (for sauce and cuisine), and the result card with matched ingredient badges. Also update the navigation component demo to show the actual 5-link nav (including 🧊 Fridge) that's in the live product.

### 8.3 Update the Developer Guide

> The `CLAUDE.md` developer guide has outdated information — wrong dietary restriction values, missing routes, no mention of the Fridge feature, and no explanation of the fallback recipe system. Update it to accurately reflect the shipped product so a developer picking this up for the first time can understand how it actually works.

### 8.4 Update the PRD

> `Recipe-cookbook-prd.md` is still marked as Draft and reflects the pre-build plan. Update it to v1.1 Shipped, capturing:
> - What was actually built vs. what was planned
> - The Fridge feature (new user stories, functional requirements, and persona)
> - Constraints discovered during build (no API key, corporate network, port conflict)
> - Open questions that were resolved during development
> - Data model as implemented (not as originally designed)

### 8.5 Update the Wireframe

> The wireframe (`wireframe/index.html`) covers 4 pages but the shipped product has 5. Add the Fridge page as a fully interactive wireframe view so the complete product can be demo'd from the wireframe. The Fridge wireframe should show the 3-step flow, the result card with matched ingredient badges, and have working chip interactions. Update the nav and footer to reflect 5 pages.

### 8.6 Write the README

> The `README.md` is currently just the project name — one line. Write a complete README that serves two audiences: a developer who wants to run the app, and a stakeholder who wants to understand what the product does. Cover the product overview, all features, the recipe library, setup instructions (including the corporate network workaround), and the full file structure.

---

## PM Prompting Principles

Lessons from building this product with an AI coding assistant:

**Lead with the user problem, not the solution.**
> Instead of "add a seenTitles array to the fridge page JS", say "users report clicking Try Different Recipe returns the same recipe. Fix this so each click returns a different suggestion and the history resets when ingredients change."
> The AI picks the right implementation. You describe the broken behavior and the expected outcome.

**Write acceptance criteria, not code specs.**
> Instead of "filter checkboxes should submit filter-form-panel", say "selecting a filter should immediately update the recipe list. Applied filters should be visible as removable pills."
> Acceptance criteria give the AI the success bar to hit — and it often finds a better path to get there.

**Name the persona and the problem, not the button.**
> Instead of "add a generate button that calls /api/generate", say "users who want a recipe outside the 5 PM schedule need a clearly visible way to trigger generation from the home page."
> Context about who and why produces better UX decisions.

**Describe the edge case from the user's perspective.**
> Instead of "handle the case where no API key is present", say "the app must work for users who don't have an Anthropic API key due to company policy — they should get the same experience as API users."
> The user constraint frames the fallback requirement more precisely than the technical framing.

**State what the feature must NOT do.**
> "Do NOT suggest grains as quick-add options on the Fridge page — users shouldn't be nudged to assume they have pantry staples."
> Negative constraints are often more important than positive ones and easier for an AI to miss without explicit instruction.

**Describe the "broken state" clearly when reporting bugs.**
> "I expect to see filtered results when I check Vegetarian, but the recipe list doesn't change at all" is more useful than "the filter doesn't work."
> The observed symptom helps the AI diagnose root cause faster.
