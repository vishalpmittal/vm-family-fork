# Family Fork — Demo Script

**Audience**: Stakeholders, product reviewers, or new users  
**Duration**: ~10–12 minutes end-to-end  
**URL**: http://localhost:8080  
**Pre-requisite**: App is running (`python3 app.py`). Profile has NOT been set up yet for a clean first-run demo. (To reset: delete `instance/family_fork.db` and restart.)

---

## Demo Persona

> **Priya** is a home cook managing meals for a family of 4 — two adults and two kids (ages 7 and 40). The family is vegetarian, prefers Indian and Mediterranean food, likes medium spice, and has a goal of eating more protein-rich meals. Every evening, Priya spends 20 minutes figuring out what to cook. She's about to solve that forever.

---

## Scene 1 — First Visit (30 seconds)

**Action**: Open http://localhost:8080

**What you see**: The app redirects immediately to the Profile page.

> *"The first time you open Family Fork, it asks one simple question: who are you cooking for? This is the only form you'll ever fill out — everything else runs automatically from here."*

---

## Scene 2 — Profile Setup (2 minutes)

**Page**: `/profile`

Walk through each section top to bottom.

### Household Details
- **How many people**: Select **4**
- **Youngest eater's age**: Type **7**
- **Oldest eater's age**: Type **40**

> *"We tell the app who's at the table — including the kids. Watch what happens when a 7-year-old is the youngest eater: the app will automatically include age-appropriate texture notes and allergen warnings in every recipe."*

### Food Preferences
- **Dietary Restrictions**: Check **🥬 Vegetarian**
- **Spice Level**: Drag the slider to **3 — Medium**

> *"Drag the spice slider and the label updates live. Spice 3 means medium heat — enough flavour for the adults, not too fiery for a 7-year-old."*

- **Preferred Cuisines**: Check **🍛 Indian** and **🫒 Mediterranean**

> *"Priya's family rotates between Indian and Mediterranean. Every recipe generated will come from one of these two cuisines — never anything outside her list."*

### Nutrition Focus
- Check **💪 Protein-rich** and **⚖️ Balanced**

> *"This is optional, but powerful. The app will now favour high-protein dishes — great for an active family."*

### Daily Recipe Email
- **Email**: Enter `priya@example.com`
- **Timezone**: `America/New_York`

> *"At 5 PM every day, Priya gets an email with a new recipe. No app to open, no decision to make — it just arrives."*

**Action**: Click **✓ Save Profile**

**What you see**: Redirects to the Home page. If recipes already exist, today's recipe hero is displayed. If the cookbook is empty, the welcome screen appears.

---

## Scene 3 — Home Page (1 minute)

**Page**: `/`

**What you see** (if recipes exist):
- A full-width hero card: food photo, recipe title, description, tags (cuisine, dietary, nutrition, spice, servings)
- Date and time stamp on the card
- "This Week's Recipes" strip below — up to 4 recent recipes as cards

> *"This is what Priya sees every day. The hero card is today's recipe — generated automatically at 5 PM, matched exactly to her profile. Indian or Mediterranean. Vegetarian. Medium spice. Scaled for 4 people. Protein-rich where possible."*

> *"Below that, the week's other recipes. Every one of them already passed through the same profile filter — she doesn't need to check a single ingredient."*

**Point out the tags on the hero card**:
- Cuisine chip (e.g. 🍛 Indian)
- Dietary tag (e.g. Vegetarian)
- Nutrition tag (e.g. Protein-rich)
- 🌶 Spice 3/5
- 👥 4 people

---

## Scene 4 — Generate a Recipe On Demand (2 minutes)

**Action**: Scroll to the bottom of the home page → click **⚡ Generate Now**

*(Alternatively, click **Generate Another** in the hero section.)*

**What you see**: All Generate buttons change to **"Generating…"** and become disabled.

> *"The request goes off to Claude in the background. The browser polls every 2 seconds — no page refresh, no spinner page. We just wait here."*

> *(While waiting — typically 20–40 seconds):*  
> *"In the background, the app is sending our full household profile to Claude: vegetarian, Indian or Mediterranean, spice 3, 4 people, protein-rich, ages 7–40. Claude generates a recipe that fits every single one of those constraints simultaneously — not just one or two."*

**What you see on completion**: Browser redirects to the new Recipe Detail page.

> *"And here it is — a brand new recipe, generated just for Priya's family."*

---

## Scene 5 — Recipe Detail (2 minutes)

**Page**: `/recipe/<id>`

**Walk through each section**:

### Hero
- Food photo (fetched from TheMealDB — a real photo of the dish or something very close)
- Title, description, all tag chips

### Stat row
- Prep time / Cook time / Servings / Spice level

> *"Everything at a glance. Priya can see in 3 seconds whether this fits her evening."*

### Serving Scaler
- **Action**: Click **+** and **−** on the serving count

> *"Priya's mother-in-law is coming to visit — now there are 6 people. Click + twice. Every ingredient quantity in the list below adjusts automatically."*

**Point to the ingredients list updating in real time.**

### Instructions
- Numbered steps with orange gradient circles
- Clear, sequential, no ambiguity

### Allergen Notes
- **Point to the allergen_notes section**

> *"Because the youngest eater is 7, the app automatically generated a note here — things like reducing spice for the child, checking that the dish is suitable for their age. This runs automatically for any household with kids under 12."*

---

## Scene 6 — The Cookbook (2 minutes)

**Action**: Click **Cookbook** in the nav

**Page**: `/cookbook`

### Default Browse View
**What you see**: Recipes grouped by cuisine — an Indian row, a Mediterranean row.

> *"Every recipe Priya has ever generated lives here, organised by cuisine. No filing, no tagging — it's all automatic."*

### Search
**Action**: Type `paneer` in the search bar

> *"Full-text search across titles, descriptions, and ingredient lists. If paneer appears anywhere in the recipe — not just the title — it shows up here."*

**Action**: Clear the search.

### Filters
**Action**: Open the filter panel → select **Vegetarian** under Dietary, drag **Spice Max** to **3**

> *"Multi-dimension filters. Cuisine, dietary tag, nutrition tag, spice ceiling, and total cook time — all combinable. The active filter chips appear here so you always know what's applied."*

**Action**: Click **× Vegetarian** chip to remove that filter.

> *"One click to remove a filter. Clear all removes everything at once."*

---

## Scene 7 — What's in the Fridge? (2 minutes)

**Action**: Click **🧊 Fridge** in the nav

**Page**: `/fridge`

> *"It's Thursday evening. Priya hasn't had time to shop. She opens the fridge and sees a few things. Let's see what Family Fork can make from exactly what she has."*

### Step 1 — Add Ingredients
**Action**: Click quick-add chips: **Spinach**, **Paneer**, **Tomatoes**, **Bell Pepper**  
**Action**: Also type `garlic` in the text box and press Enter

> *"Notice: no grains appear in the quick-add list. The app never assumes you have rice, pasta, or naan — if you do, just type it in. Otherwise, the recipe won't require it."*

**What you see**: Counter updates → "5 ingredients added — ready to generate!"

### Step 2 — Sauce
**Action**: Click **🍅 Tomato-based**

> *"Priya knows she has a can of crushed tomatoes. Selecting a sauce base guides the recipe in a direction she can actually execute."*

### Step 3 — Cuisine
**Action**: Click **🍛 Indian**

> *"In the mood for Indian tonight."*

### Generate
**Action**: Click **⚡ Generate Recipe from Fridge**

**What you see**: Button shows "Finding the best recipe…" — polls in the background.

**On completion**: Recipe card appears with:
- Food photo
- Title and description
- Green **✓ matched ingredient** badges showing which fridge items were used
- Prep + cook time, servings, spice level
- **View Full Recipe** and **Try Different** buttons

> *"The green badges show exactly which of Priya's fridge items made it into the recipe. She can see at a glance: yes, I have all of this."*

**Action**: Click **Try Different**

> *"If the first suggestion doesn't appeal, one click generates a completely different recipe from the same ingredients — without repeating the previous result."*

**Action**: Click **View Full Recipe** to open the full detail page.

> *"And this fridge recipe is saved to the cookbook too — tagged with its own source so Priya knows it came from a fridge session."*

---

## Scene 8 — The Email (30 seconds)

> *"The last piece: every time a recipe is generated — whether the daily 5 PM one or an on-demand request — an email lands in Priya's inbox. Full recipe, all ingredients, step-by-step instructions, and a link back to the cookbook entry."*

> *"She can forward it to her husband. She can open it on her phone at the grocery store. She never has to open the app again to get value from it."*

---

## Wrap-up (30 seconds)

> *"That's Family Fork. One profile, set once. A new recipe every day at 5 PM that fits your household exactly — or on demand any time you need it. A growing cookbook that's always searchable. A fridge tool for those evenings when you just need to use what you've got. And email delivery so the app works even when you're not looking at it."*

> *"The whole thing runs locally, no subscription, and works even without an AI API key — it falls back to a library of 41 hand-curated recipes across Indian, Italian, Mexican, and Mediterranean cuisines."*

---

## Quick Reference — Key URLs

| What to demo | URL |
|---|---|
| First-run profile setup | http://localhost:8080/profile |
| Home — today's recipe | http://localhost:8080/ |
| Cookbook — browse & filter | http://localhost:8080/cookbook |
| What's in the Fridge? | http://localhost:8080/fridge |

---

## Demo Tips

- **For a clean first-run**: delete `instance/family_fork.db` and restart the app. You'll land directly on the profile page.
- **If generation takes too long**: the browser polls for up to 3 minutes. Keep talking — the wait is a good moment to explain what Claude is doing in the background.
- **If the AI key is missing**: the app uses the fallback library silently. Generation completes in under 1 second — demo still works perfectly.
- **Fridge demo works best with 3–5 ingredients**: too few gives limited results; too many makes the "I only have what's here" story less compelling.
- **Show the serving scaler on recipe detail**: it's the most visually satisfying interaction in the app.
