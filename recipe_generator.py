import json
import os
import random
import re


FALLBACK_RECIPES = [
    {
        "title": "Palak Paneer with Jeera Rice",
        "description": "Creamy spinach curry with fresh cottage cheese, served with cumin-scented basmati. A classic North Indian comfort dish ready in 35 minutes.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "iron-rich", "vitamin-rich"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Fresh spinach", "quantity": "4", "unit": "cups"},
            {"name": "Paneer, cubed", "quantity": "250", "unit": "g"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tsp"},
            {"name": "Tomatoes, chopped", "quantity": "2", "unit": "medium"},
            {"name": "Cumin seeds", "quantity": "1", "unit": "tsp"},
            {"name": "Garam masala", "quantity": "½", "unit": "tsp"},
            {"name": "Heavy cream", "quantity": "3", "unit": "tbsp"},
            {"name": "Basmati rice", "quantity": "1½", "unit": "cups"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Blanch spinach in boiling water for 2 minutes, transfer to ice water, drain and blend into a smooth purée.",
            "Heat oil over medium heat. Add cumin seeds and let splutter. Add onions and sauté until golden, about 7 minutes.",
            "Add garlic and ginger, sauté 1 minute. Add tomatoes and cook until oil separates, about 5 minutes.",
            "Add spinach purée, garam masala, and salt. Simmer 5 minutes.",
            "Add paneer and cream. Stir gently and simmer 3–4 minutes.",
            "Cook basmati rice with 1:1.75 water and ½ tsp cumin until fluffy.",
            "Serve palak paneer over jeera rice. Garnish with a swirl of cream.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Chana Masala with Bhatura",
        "description": "Robust chickpea curry cooked with tangy tomatoes and aromatic spices. Served with puffy deep-fried bread for a street-food classic.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "iron-rich", "balanced"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Canned chickpeas, drained", "quantity": "2", "unit": "cans (400g each)"},
            {"name": "Onion, finely chopped", "quantity": "2", "unit": "medium"},
            {"name": "Tomatoes, puréed", "quantity": "3", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tbsp"},
            {"name": "Cumin seeds", "quantity": "1", "unit": "tsp"},
            {"name": "Coriander powder", "quantity": "2", "unit": "tsp"},
            {"name": "Chana masala spice blend", "quantity": "2", "unit": "tsp"},
            {"name": "Amchur (dry mango powder)", "quantity": "1", "unit": "tsp"},
            {"name": "Oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh coriander leaves", "quantity": "handful", "unit": ""},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Heat oil, add cumin seeds and let splutter. Add onions and fry until deep golden, about 10 minutes.",
            "Add garlic and ginger, cook 2 minutes. Add tomato purée and cook until oil separates, 8 minutes.",
            "Add coriander powder, chana masala, and amchur. Stir well for 1 minute.",
            "Add chickpeas and ½ cup water. Mash a few chickpeas to thicken the gravy.",
            "Simmer 15 minutes until sauce is thick and coats chickpeas. Season with salt.",
            "Garnish with fresh coriander and a squeeze of lemon. Serve with rice or bread.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Creamy Tuscan White Bean Pasta",
        "description": "Silky pasta tossed with cannellini beans, sun-dried tomatoes, and wilted spinach in a garlicky parmesan cream sauce. Weeknight comfort in 25 minutes.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 5,
        "cook_time_min": 20,
        "ingredients": [
            {"name": "Penne pasta", "quantity": "400", "unit": "g"},
            {"name": "Cannellini beans, drained", "quantity": "1", "unit": "can (400g)"},
            {"name": "Baby spinach", "quantity": "3", "unit": "cups"},
            {"name": "Sun-dried tomatoes in oil, sliced", "quantity": "½", "unit": "cup"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Heavy cream", "quantity": "½", "unit": "cup"},
            {"name": "Parmesan, grated", "quantity": "½", "unit": "cup"},
            {"name": "Olive oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Italian seasoning", "quantity": "1", "unit": "tsp"},
            {"name": "Red chilli flakes", "quantity": "¼", "unit": "tsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Cook pasta in well-salted boiling water until al dente. Reserve 1 cup pasta water before draining.",
            "Heat olive oil over medium heat. Add garlic and chilli flakes, sauté 1 minute until fragrant.",
            "Add sun-dried tomatoes and Italian seasoning, stir 30 seconds.",
            "Add cream and half the parmesan. Stir to combine and bring to a gentle simmer.",
            "Add drained beans and spinach. Toss until spinach wilts, about 2 minutes.",
            "Add cooked pasta and toss. Add pasta water a splash at a time to loosen the sauce.",
            "Serve in warm bowls topped with remaining parmesan and freshly cracked pepper.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Margherita Pizza with Homemade Dough",
        "description": "Classic Neapolitan-style pizza with a blistered hand-stretched base, crushed San Marzano tomatoes, and fresh mozzarella. Simple, perfect, beloved.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["balanced", "vitamin-rich"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "All-purpose flour", "quantity": "500", "unit": "g"},
            {"name": "Instant yeast", "quantity": "7", "unit": "g"},
            {"name": "Warm water", "quantity": "320", "unit": "ml"},
            {"name": "Salt", "quantity": "10", "unit": "g"},
            {"name": "Olive oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Canned whole tomatoes", "quantity": "1", "unit": "can (400g)"},
            {"name": "Fresh mozzarella", "quantity": "300", "unit": "g"},
            {"name": "Fresh basil leaves", "quantity": "handful", "unit": ""},
            {"name": "Garlic clove, halved", "quantity": "1", "unit": "clove"},
            {"name": "Extra-virgin olive oil for finishing", "quantity": "2", "unit": "tbsp"},
        ],
        "instructions": [
            "Mix flour, yeast, and salt. Add warm water and olive oil. Knead 8 minutes until smooth. Rest 1 hour.",
            "Crush canned tomatoes by hand with a pinch of salt. Do not cook.",
            "Preheat oven to maximum temperature (250°C / 480°F) with a baking tray inside for 30 minutes.",
            "Divide dough into 2 balls. Stretch each to a thin round on a floured surface.",
            "Rub pizza base with cut garlic. Spread tomato sauce leaving a 2cm border.",
            "Tear mozzarella over the top. Slide onto the hot tray and bake 10–12 minutes until crust is blistered.",
            "Remove from oven, scatter fresh basil, drizzle extra-virgin olive oil, and serve immediately.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Black Bean Tacos with Mango Salsa",
        "description": "Smoky seasoned black beans in warm corn tortillas, topped with a vibrant fresh mango-jalapeño salsa and cool avocado crema. Ready in 20 minutes.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "vitamin-rich", "balanced"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 10,
        "ingredients": [
            {"name": "Canned black beans, drained", "quantity": "2", "unit": "cans (400g each)"},
            {"name": "Corn tortillas", "quantity": "12", "unit": "small"},
            {"name": "Ripe mango, diced small", "quantity": "1", "unit": "large"},
            {"name": "Red onion, finely diced", "quantity": "½", "unit": "medium"},
            {"name": "Jalapeño, finely chopped", "quantity": "1", "unit": ""},
            {"name": "Lime juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh coriander, chopped", "quantity": "½", "unit": "cup"},
            {"name": "Avocado, mashed", "quantity": "2", "unit": "ripe"},
            {"name": "Cumin powder", "quantity": "1½", "unit": "tsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Garlic powder", "quantity": "½", "unit": "tsp"},
            {"name": "Oil", "quantity": "1", "unit": "tbsp"},
        ],
        "instructions": [
            "Make mango salsa: combine mango, red onion, jalapeño, half the coriander, and 1 tbsp lime juice. Set aside.",
            "Mash avocados with remaining lime juice and a pinch of salt for the crema.",
            "Heat oil in a pan. Add beans, cumin, smoked paprika, garlic powder, and salt. Mash lightly and cook 5 minutes until heated through.",
            "Warm tortillas directly over a gas flame for 30 seconds per side, or in a dry pan.",
            "Assemble tacos: beans first, then mango salsa, a spoonful of avocado crema, and fresh coriander.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Veggie Enchiladas with Red Chile Sauce",
        "description": "Corn tortillas stuffed with roasted sweet potato, black beans, and cheese, smothered in a smoky homemade red chile sauce and baked until bubbling.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["balanced", "protein-rich", "vitamin-rich"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 35,
        "ingredients": [
            {"name": "Corn tortillas", "quantity": "10", "unit": ""},
            {"name": "Sweet potato, diced small", "quantity": "2", "unit": "medium"},
            {"name": "Canned black beans, drained", "quantity": "1", "unit": "can (400g)"},
            {"name": "Canned crushed tomatoes", "quantity": "1", "unit": "can (400g)"},
            {"name": "Chipotle in adobo", "quantity": "2", "unit": "tbsp"},
            {"name": "Garlic cloves", "quantity": "3", "unit": "cloves"},
            {"name": "Cumin powder", "quantity": "2", "unit": "tsp"},
            {"name": "Cheddar cheese, shredded", "quantity": "1½", "unit": "cups"},
            {"name": "Red onion, sliced", "quantity": "1", "unit": "medium"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh coriander and sour cream to serve", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 200°C / 400°F. Toss sweet potato with 1 tbsp oil and salt. Roast 20 minutes until tender.",
            "Blend crushed tomatoes, chipotle, garlic, and cumin into a smooth red sauce. Season with salt.",
            "Mix roasted sweet potato with black beans and half the cheese.",
            "Warm tortillas in a dry pan to make pliable. Fill each with sweet potato mixture, roll, and place seam-down in an oiled baking dish.",
            "Pour red sauce generously over the top. Sprinkle remaining cheese.",
            "Bake 20 minutes until sauce is bubbly and cheese is melted.",
            "Serve topped with sour cream, fresh coriander, and sliced red onion.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Greek Chickpea and Feta Salad Bowl",
        "description": "A hearty Mediterranean bowl of warm roasted chickpeas, crisp cucumber, ripe tomatoes, kalamata olives, and creamy feta drizzled with herby lemon dressing.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "balanced", "vitamin-rich"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Canned chickpeas, drained", "quantity": "2", "unit": "cans (400g each)"},
            {"name": "Feta cheese, crumbled", "quantity": "200", "unit": "g"},
            {"name": "Cherry tomatoes, halved", "quantity": "2", "unit": "cups"},
            {"name": "Cucumber, diced", "quantity": "1", "unit": "large"},
            {"name": "Kalamata olives, pitted", "quantity": "½", "unit": "cup"},
            {"name": "Red onion, thinly sliced", "quantity": "½", "unit": "small"},
            {"name": "Fresh parsley, chopped", "quantity": "½", "unit": "cup"},
            {"name": "Olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Lemon juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Dried oregano", "quantity": "1", "unit": "tsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 220°C / 425°F. Pat chickpeas dry, toss with 2 tbsp olive oil, smoked paprika, and salt.",
            "Roast chickpeas 25 minutes, shaking halfway, until golden and slightly crisp.",
            "Whisk remaining olive oil, lemon juice, oregano, salt, and pepper into a dressing.",
            "Arrange cucumber, tomatoes, olives, and red onion in bowls.",
            "Top with warm roasted chickpeas and crumbled feta.",
            "Drizzle dressing over everything and finish with fresh parsley.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Lemon Herb Orzo with Roasted Vegetables",
        "description": "Tender orzo pasta tossed with roasted zucchini, bell peppers, and cherry tomatoes in a bright lemon-herb dressing. A Mediterranean staple that works hot or cold.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["balanced", "vitamin-rich"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Orzo pasta", "quantity": "350", "unit": "g"},
            {"name": "Zucchini, diced", "quantity": "2", "unit": "medium"},
            {"name": "Red bell pepper, diced", "quantity": "2", "unit": ""},
            {"name": "Cherry tomatoes", "quantity": "1", "unit": "cup"},
            {"name": "Red onion, sliced into wedges", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Lemon juice and zest", "quantity": "1", "unit": "large lemon"},
            {"name": "Fresh basil, torn", "quantity": "½", "unit": "cup"},
            {"name": "Fresh mint, chopped", "quantity": "¼", "unit": "cup"},
            {"name": "Toasted pine nuts", "quantity": "¼", "unit": "cup"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 220°C / 425°F. Toss zucchini, bell pepper, tomatoes, and red onion with 2 tbsp oil, salt, and pepper.",
            "Roast vegetables 25–30 minutes until caramelised at the edges.",
            "Cook orzo in salted boiling water until al dente, about 8 minutes. Drain and rinse with cold water.",
            "Whisk remaining olive oil, lemon juice, lemon zest, and garlic into a bright dressing.",
            "Toss orzo with roasted vegetables and dressing while still warm.",
            "Fold in basil, mint, and pine nuts. Taste and adjust seasoning.",
            "Serve warm or at room temperature.",
        ],
        "allergen_notes": "",
    },
    # ── Indian ──────────────────────────────────────────────────────────────
    {
        "title": "Dal Makhani",
        "description": "Slow-simmered whole black lentils and kidney beans in a velvety tomato-butter gravy. The overnight soak and long cook build deep, smoky richness.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "iron-rich", "balanced"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 50,
        "ingredients": [
            {"name": "Whole black lentils (urad dal)", "quantity": "1", "unit": "cup"},
            {"name": "Red kidney beans (rajma), soaked overnight", "quantity": "¼", "unit": "cup"},
            {"name": "Butter", "quantity": "3", "unit": "tbsp"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tbsp"},
            {"name": "Tomato purée", "quantity": "½", "unit": "cup"},
            {"name": "Heavy cream", "quantity": "4", "unit": "tbsp"},
            {"name": "Kashmiri chilli powder", "quantity": "1", "unit": "tsp"},
            {"name": "Garam masala", "quantity": "½", "unit": "tsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Pressure cook lentils and kidney beans with 3 cups water and salt for 25 minutes until completely soft.",
            "Melt butter in a heavy pan. Fry onions until deep golden, about 10 minutes.",
            "Add garlic and ginger, cook 2 minutes. Add tomato purée and Kashmiri chilli. Cook until oil separates, 8 minutes.",
            "Add cooked lentils and beans to the pan. Mash a few against the side to thicken. Add ½ cup water.",
            "Simmer on low heat for 20 minutes, stirring often. The dal should be thick and creamy.",
            "Stir in cream and garam masala. Simmer 5 more minutes.",
            "Finish with a knob of butter on top. Serve with naan or rice.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Aloo Gobi",
        "description": "Dry-style stir-fried potatoes and cauliflower tossed with turmeric, cumin, and fresh coriander. A simple, satisfying weeknight side that pairs beautifully with dal.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["vitamin-rich", "balanced", "no-carb"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Cauliflower, cut into small florets", "quantity": "1", "unit": "medium head"},
            {"name": "Potatoes, peeled and diced", "quantity": "3", "unit": "medium"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "large"},
            {"name": "Tomato, chopped", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tsp"},
            {"name": "Cumin seeds", "quantity": "1", "unit": "tsp"},
            {"name": "Turmeric powder", "quantity": "½", "unit": "tsp"},
            {"name": "Coriander powder", "quantity": "1", "unit": "tsp"},
            {"name": "Oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh coriander, chopped", "quantity": "handful", "unit": ""},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Heat oil in a wide pan. Add cumin seeds and let splutter.",
            "Add onion and sauté until golden, about 7 minutes. Add garlic and ginger, cook 1 minute.",
            "Add tomato, turmeric, coriander powder, and salt. Cook until tomato softens, 4 minutes.",
            "Add potatoes, stir to coat with spices. Cover and cook on medium-low for 10 minutes.",
            "Add cauliflower florets, toss well. Cover and cook 10–12 minutes, stirring occasionally, until both are tender.",
            "Uncover and cook 2 minutes on high heat to evaporate excess moisture.",
            "Garnish with fresh coriander and a squeeze of lemon. Serve with roti or as a side.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Vegetable Biryani",
        "description": "Fragrant basmati rice layered with spiced vegetables, saffron milk, and crispy fried onions. A festive one-pot showstopper that fills the kitchen with incredible aroma.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["vitamin-rich", "balanced"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 40,
        "ingredients": [
            {"name": "Basmati rice, soaked 30 min", "quantity": "2", "unit": "cups"},
            {"name": "Mixed vegetables (carrot, peas, beans, potato), diced", "quantity": "3", "unit": "cups"},
            {"name": "Onions, thinly sliced", "quantity": "2", "unit": "large"},
            {"name": "Yoghurt", "quantity": "½", "unit": "cup"},
            {"name": "Garlic-ginger paste", "quantity": "2", "unit": "tbsp"},
            {"name": "Whole spices (bay leaf, cardamom, cloves, cinnamon)", "quantity": "1", "unit": "set"},
            {"name": "Biryani masala", "quantity": "2", "unit": "tbsp"},
            {"name": "Saffron strands soaked in 3 tbsp warm milk", "quantity": "pinch", "unit": ""},
            {"name": "Fresh mint leaves", "quantity": "½", "unit": "cup"},
            {"name": "Oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Fry sliced onions in oil until deeply golden and crispy. Set aside half for garnish.",
            "In the same pan, add garlic-ginger paste and whole spices. Cook 1 minute.",
            "Add vegetables, biryani masala, yoghurt, and salt. Toss well and cook 10 minutes until semi-done.",
            "Par-boil soaked rice in salted boiling water until 70% cooked (grains still have a bite). Drain.",
            "Layer rice over vegetables in the pot. Drizzle saffron milk over the rice.",
            "Scatter mint leaves and fried onions on top. Cover tightly with foil and then the lid.",
            "Cook on very low heat (dum) for 20 minutes. Rest 5 minutes, then gently fluff and serve.",
        ],
        "allergen_notes": "",
    },
    # ── Italian ─────────────────────────────────────────────────────────────
    {
        "title": "Mushroom Risotto",
        "description": "Slow-stirred Arborio rice cooked with a mix of earthy mushrooms and finished with parmesan and cold butter. Deeply satisfying and endlessly comforting.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 35,
        "ingredients": [
            {"name": "Arborio rice", "quantity": "320", "unit": "g"},
            {"name": "Mixed mushrooms (button, cremini, shiitake), sliced", "quantity": "400", "unit": "g"},
            {"name": "Vegetable stock, warm", "quantity": "1.2", "unit": "litres"},
            {"name": "Onion, finely diced", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Dry white wine", "quantity": "120", "unit": "ml"},
            {"name": "Parmesan, grated", "quantity": "80", "unit": "g"},
            {"name": "Cold butter", "quantity": "40", "unit": "g"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh thyme leaves", "quantity": "1", "unit": "tsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Heat 2 tbsp oil in a wide pan. Sauté mushrooms on high heat until golden, about 6 minutes. Season and set aside.",
            "In the same pan, heat remaining oil over medium heat. Add onion and cook until soft, 5 minutes. Add garlic and thyme, cook 1 minute.",
            "Add Arborio rice and stir for 2 minutes to toast the grains.",
            "Pour in white wine and stir until fully absorbed.",
            "Add warm stock one ladle at a time, stirring constantly and waiting for each addition to absorb before adding the next. This takes about 20 minutes.",
            "When rice is al dente and creamy, remove from heat. Stir in cold butter and parmesan vigorously.",
            "Fold in three-quarters of the mushrooms. Serve in warm bowls topped with remaining mushrooms.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Minestrone Soup with Crusty Bread",
        "description": "A hearty Italian vegetable soup packed with seasonal vegetables, cannellini beans, and short pasta in a rich tomato broth. A bowl that eats like a meal.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["iron-rich", "vitamin-rich", "balanced"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 35,
        "ingredients": [
            {"name": "Canned chopped tomatoes", "quantity": "1", "unit": "can (400g)"},
            {"name": "Cannellini beans, drained", "quantity": "1", "unit": "can (400g)"},
            {"name": "Ditalini or small pasta", "quantity": "100", "unit": "g"},
            {"name": "Carrot, diced", "quantity": "2", "unit": "medium"},
            {"name": "Celery stalks, diced", "quantity": "2", "unit": ""},
            {"name": "Zucchini, diced", "quantity": "1", "unit": "medium"},
            {"name": "Kale or cavolo nero, roughly chopped", "quantity": "2", "unit": "cups"},
            {"name": "Onion, diced", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Vegetable stock", "quantity": "1.2", "unit": "litres"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Parmesan rind (optional)", "quantity": "1", "unit": "piece"},
            {"name": "Salt, pepper, and fresh basil", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Heat olive oil in a large pot. Sauté onion, carrot, and celery for 8 minutes until softened.",
            "Add garlic and cook 1 minute. Add zucchini and stir for 2 minutes.",
            "Pour in canned tomatoes and stock. Add parmesan rind if using. Bring to a boil.",
            "Reduce heat and simmer 15 minutes. Add beans, kale, and pasta.",
            "Cook 10 more minutes until pasta is tender and kale is wilted.",
            "Remove parmesan rind. Season generously with salt and pepper.",
            "Ladle into bowls, drizzle with extra-virgin olive oil, and serve with crusty bread.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Gnocchi with Sage Brown Butter",
        "description": "Pillowy potato gnocchi tossed in nutty golden brown butter with crispy sage leaves and a blizzard of parmesan. An indulgent 20-minute dinner.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["balanced"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 5,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Fresh or store-bought potato gnocchi", "quantity": "800", "unit": "g"},
            {"name": "Unsalted butter", "quantity": "80", "unit": "g"},
            {"name": "Fresh sage leaves", "quantity": "20", "unit": "leaves"},
            {"name": "Garlic clove, halved", "quantity": "1", "unit": ""},
            {"name": "Parmesan, finely grated", "quantity": "80", "unit": "g"},
            {"name": "Lemon juice", "quantity": "1", "unit": "tbsp"},
            {"name": "Salt and black pepper", "quantity": "to taste", "unit": ""},
            {"name": "Toasted walnuts (optional)", "quantity": "¼", "unit": "cup"},
        ],
        "instructions": [
            "Cook gnocchi in generously salted boiling water until they float plus 30 seconds. Reserve ½ cup pasta water. Drain.",
            "In a large skillet, melt butter over medium heat. Add garlic and sage leaves.",
            "Continue cooking, swirling the pan, until butter turns golden-brown and smells nutty, about 4 minutes. Discard garlic.",
            "Add cooked gnocchi to the butter. Toss and cook 2 minutes until gnocchi are lightly golden.",
            "Remove from heat. Add lemon juice and a splash of pasta water to create a light sauce.",
            "Toss with half the parmesan. Divide among warm bowls.",
            "Top with remaining parmesan, cracked pepper, and walnuts if using.",
        ],
        "allergen_notes": "",
    },
    # ── Mexican ─────────────────────────────────────────────────────────────
    {
        "title": "Vegetarian Burrito Bowl",
        "description": "A colourful build-your-own bowl with cilantro-lime rice, smoky roasted peppers and corn, seasoned black beans, avocado, and tangy pico de gallo.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "balanced", "vitamin-rich"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Long-grain white rice", "quantity": "1½", "unit": "cups"},
            {"name": "Canned black beans, drained", "quantity": "1", "unit": "can (400g)"},
            {"name": "Corn kernels (fresh or frozen)", "quantity": "1", "unit": "cup"},
            {"name": "Bell peppers (mixed colours), sliced", "quantity": "2", "unit": "large"},
            {"name": "Avocados", "quantity": "2", "unit": "ripe"},
            {"name": "Cherry tomatoes, quartered", "quantity": "1", "unit": "cup"},
            {"name": "Red onion, finely diced", "quantity": "½", "unit": "medium"},
            {"name": "Lime juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh coriander, chopped", "quantity": "½", "unit": "cup"},
            {"name": "Cumin powder", "quantity": "1", "unit": "tsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Cook rice. While still warm, toss with half the coriander, juice of 1 lime, and a pinch of salt.",
            "Make pico de gallo: mix tomatoes, red onion, remaining coriander, and 1 tbsp lime juice. Season.",
            "Heat oil in a skillet. Cook peppers and corn on high heat with cumin and smoked paprika until charred at the edges, about 8 minutes.",
            "Warm black beans in a small pan with a pinch of cumin and salt.",
            "Mash avocados with remaining lime juice and salt.",
            "Assemble bowls: cilantro rice base, then beans, roasted peppers and corn, avocado, and pico de gallo on top.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Cheese Quesadillas with Roasted Salsa",
        "description": "Crispy flour tortillas filled with melted cheese and sautéed mushrooms, served with a smoky fire-roasted tomato salsa. Quick, kid-friendly, and endlessly customisable.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 20,
        "ingredients": [
            {"name": "Large flour tortillas", "quantity": "8", "unit": ""},
            {"name": "Cheddar or Monterey Jack cheese, grated", "quantity": "2", "unit": "cups"},
            {"name": "Mushrooms, sliced", "quantity": "300", "unit": "g"},
            {"name": "Red onion, sliced", "quantity": "1", "unit": "small"},
            {"name": "Canned fire-roasted tomatoes", "quantity": "1", "unit": "can (400g)"},
            {"name": "Garlic cloves", "quantity": "2", "unit": "cloves"},
            {"name": "Jalapeño, finely chopped", "quantity": "1", "unit": ""},
            {"name": "Cumin powder", "quantity": "½", "unit": "tsp"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Sour cream and fresh coriander to serve", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Make salsa: blend fire-roasted tomatoes, garlic, jalapeño, cumin, and salt until chunky. Taste and adjust.",
            "Heat 1 tbsp oil in a skillet. Sauté mushrooms and red onion on high until golden, 5 minutes. Season.",
            "Heat a dry non-stick pan or griddle over medium heat.",
            "Place one tortilla in the pan. Scatter cheese on half, then mushroom mixture on top of the cheese. Fold over.",
            "Cook 2–3 minutes per side until golden and cheese is fully melted. Repeat with remaining tortillas.",
            "Cut into wedges and serve immediately with roasted salsa and sour cream.",
        ],
        "allergen_notes": "Contains gluten (flour tortilla) and dairy. Use corn tortillas and vegan cheese to make dairy-free.",
    },
    {
        "title": "Mexican Lentil Soup (Sopa de Lentejas)",
        "description": "Warming red lentil soup simmered with tomatoes, chipotle, and cumin, brightened with a squeeze of lime. A protein-rich bowl ready in 30 minutes.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "iron-rich", "balanced"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Red lentils, rinsed", "quantity": "1½", "unit": "cups"},
            {"name": "Canned chopped tomatoes", "quantity": "1", "unit": "can (400g)"},
            {"name": "Onion, diced", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Chipotle in adobo", "quantity": "1", "unit": "tbsp"},
            {"name": "Cumin powder", "quantity": "1½", "unit": "tsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Vegetable stock", "quantity": "1", "unit": "litre"},
            {"name": "Lime juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh coriander and avocado to serve", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Heat oil in a large pot. Sauté onion until soft, 5 minutes. Add garlic, cumin, and smoked paprika, cook 1 minute.",
            "Add canned tomatoes and chipotle. Cook 3 minutes until slightly reduced.",
            "Add lentils and vegetable stock. Bring to a boil.",
            "Reduce heat and simmer 20 minutes until lentils are completely soft.",
            "Use an immersion blender to blend half the soup for a creamy-yet-chunky texture.",
            "Stir in lime juice. Taste and adjust seasoning.",
            "Serve topped with diced avocado, fresh coriander, and warm tortillas on the side.",
        ],
        "allergen_notes": "",
    },
    # ── Mediterranean ────────────────────────────────────────────────────────
    {
        "title": "Shakshuka",
        "description": "Eggs poached directly in a spiced tomato and pepper sauce, finished with crumbled feta and fresh herbs. A one-pan Mediterranean classic for any meal of the day.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "vitamin-rich", "balanced"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Eggs", "quantity": "8", "unit": "large"},
            {"name": "Canned chopped tomatoes", "quantity": "2", "unit": "cans (400g each)"},
            {"name": "Red and yellow bell peppers, diced", "quantity": "2", "unit": "large"},
            {"name": "Onion, diced", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Feta cheese, crumbled", "quantity": "100", "unit": "g"},
            {"name": "Smoked paprika", "quantity": "1½", "unit": "tsp"},
            {"name": "Cumin powder", "quantity": "1", "unit": "tsp"},
            {"name": "Chilli flakes", "quantity": "¼", "unit": "tsp"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh parsley or coriander", "quantity": "handful", "unit": ""},
            {"name": "Crusty bread to serve", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Heat olive oil in a wide, deep skillet over medium heat. Sauté onion until soft, 5 minutes.",
            "Add bell peppers and cook 5 minutes. Add garlic, smoked paprika, cumin, and chilli flakes. Cook 1 minute until fragrant.",
            "Pour in canned tomatoes. Season with salt. Simmer 10 minutes until sauce thickens.",
            "Use a spoon to make 8 wells in the sauce. Crack an egg into each well.",
            "Cover the pan and cook on low heat for 6–8 minutes until whites are just set but yolks are still runny.",
            "Scatter crumbled feta and fresh herbs over the top.",
            "Serve straight from the pan with crusty bread for scooping.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Falafel Pita with Tahini Sauce",
        "description": "Crispy baked chickpea falafel stuffed into warm pita with shredded cabbage, sliced tomato, and a generous drizzle of creamy garlic tahini.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "iron-rich", "balanced"],
        "dietary_tags": ["vegan", "vegetarian"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Canned chickpeas, drained and patted dry", "quantity": "2", "unit": "cans (400g each)"},
            {"name": "Pita breads", "quantity": "8", "unit": "small"},
            {"name": "Garlic cloves", "quantity": "4", "unit": "cloves"},
            {"name": "Fresh parsley, packed", "quantity": "1", "unit": "cup"},
            {"name": "Fresh coriander, packed", "quantity": "½", "unit": "cup"},
            {"name": "Cumin powder", "quantity": "1½", "unit": "tsp"},
            {"name": "Coriander powder", "quantity": "1", "unit": "tsp"},
            {"name": "Tahini", "quantity": "4", "unit": "tbsp"},
            {"name": "Lemon juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Cabbage, thinly shredded", "quantity": "2", "unit": "cups"},
            {"name": "Tomatoes, sliced", "quantity": "2", "unit": "medium"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 200°C / 400°F. Process chickpeas, garlic, parsley, coriander, cumin, coriander powder, and salt in a food processor until coarse (not smooth).",
            "Roll mixture into 16 small balls, flatten slightly. Arrange on an oiled baking tray. Brush tops with olive oil.",
            "Bake 25 minutes, flipping halfway, until golden and crisp on the outside.",
            "Make tahini sauce: whisk tahini, lemon juice, 1 minced garlic clove, and 3–4 tbsp water until smooth and pourable.",
            "Warm pitas in the oven for 2 minutes. Slice open each pocket.",
            "Fill each pita with shredded cabbage, tomato, and 2 falafel. Drizzle generously with tahini sauce.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Stuffed Bell Peppers with Quinoa and Feta",
        "description": "Vibrant bell peppers filled with herby quinoa, sun-dried tomatoes, olives, and feta, then roasted until tender. A complete, protein-packed Mediterranean meal.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "balanced", "vitamin-rich"],
        "dietary_tags": ["vegetarian"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 35,
        "ingredients": [
            {"name": "Large bell peppers (mixed colours)", "quantity": "4", "unit": ""},
            {"name": "Quinoa, rinsed", "quantity": "1", "unit": "cup"},
            {"name": "Feta cheese, crumbled", "quantity": "150", "unit": "g"},
            {"name": "Sun-dried tomatoes, chopped", "quantity": "½", "unit": "cup"},
            {"name": "Kalamata olives, pitted and halved", "quantity": "½", "unit": "cup"},
            {"name": "Baby spinach", "quantity": "2", "unit": "cups"},
            {"name": "Garlic cloves, minced", "quantity": "2", "unit": "cloves"},
            {"name": "Fresh basil and oregano, chopped", "quantity": "¼", "unit": "cup each"},
            {"name": "Lemon zest", "quantity": "1", "unit": "lemon"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 190°C / 375°F. Cook quinoa in 2 cups salted water for 15 minutes until absorbed. Fluff.",
            "Cut peppers in half lengthways. Remove seeds. Brush with olive oil, season, and roast cut-side down for 15 minutes.",
            "Heat 1 tbsp oil in a pan. Add garlic and spinach, cook until just wilted. Season.",
            "Mix quinoa with wilted spinach, sun-dried tomatoes, olives, herbs, lemon zest, and most of the feta.",
            "Flip pepper halves over. Fill each generously with quinoa mixture. Top with remaining feta.",
            "Return to oven and roast 20 minutes until peppers are tender and filling is lightly golden on top.",
            "Drizzle with extra-virgin olive oil and serve with a green salad.",
        ],
        "allergen_notes": "",
    },

    # ── Indian — Chicken & Seafood ───────────────────────────────────────────
    {
        "title": "Butter Chicken (Murgh Makhani)",
        "description": ""
        " a velvety tomato-cream sauce spiced with garam masala and fenugreek. The definitive Indian restaurant classic, made at home in 40 minutes.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 35,
        "ingredients": [
            {"name": "Chicken thighs, boneless, cubed", "quantity": "700", "unit": "g"},
            {"name": "Canned tomatoes, puréed", "quantity": "400", "unit": "g"},
            {"name": "Heavy cream", "quantity": "½", "unit": "cup"},
            {"name": "Butter", "quantity": "3", "unit": "tbsp"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tbsp"},
            {"name": "Garam masala", "quantity": "2", "unit": "tsp"},
            {"name": "Kashmiri chilli powder", "quantity": "1", "unit": "tsp"},
            {"name": "Dried fenugreek leaves (kasuri methi)", "quantity": "1", "unit": "tsp"},
            {"name": "Plain yoghurt", "quantity": "3", "unit": "tbsp"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Marinate chicken in yoghurt, half the garam masala, Kashmiri chilli, and salt for at least 15 minutes.",
            "Heat oil in a pan over high heat. Sear chicken pieces until golden on all sides, about 6 minutes. Set aside.",
            "In the same pan, melt butter. Sauté onion until golden, 7 minutes. Add garlic and ginger, cook 2 minutes.",
            "Add tomato purée and remaining garam masala. Cook on medium until oil separates, about 8 minutes.",
            "Add cream and seared chicken. Stir and simmer on low for 10 minutes until chicken is cooked through.",
            "Crush kasuri methi between your palms and stir in. Simmer 2 more minutes.",
            "Serve with basmati rice or naan. Swirl extra cream on top if desired.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Chicken Tikka Masala",
        "description": "Charred tandoori-style chicken in a bold, aromatic masala sauce. This beloved dish balances smoky chicken with a rich, spiced tomato gravy.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Chicken breast, cubed", "quantity": "700", "unit": "g"},
            {"name": "Plain yoghurt", "quantity": "½", "unit": "cup"},
            {"name": "Lemon juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Tikka masala paste", "quantity": "3", "unit": "tbsp"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tbsp"},
            {"name": "Canned chopped tomatoes", "quantity": "400", "unit": "g"},
            {"name": "Heavy cream", "quantity": "¼", "unit": "cup"},
            {"name": "Garam masala", "quantity": "1", "unit": "tsp"},
            {"name": "Oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh coriander to garnish", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Mix chicken with yoghurt, lemon juice, 1 tbsp tikka paste, and salt. Marinate 30 minutes (or overnight).",
            "Grill or pan-fry chicken on high heat until charred at edges and cooked through, about 8 minutes. Set aside.",
            "Heat oil, sauté onion until golden. Add garlic and ginger, cook 1 minute.",
            "Add remaining tikka paste and cook 1 minute. Add tomatoes and simmer 10 minutes until thickened.",
            "Blend sauce until smooth if desired. Return to pan, add cream and garam masala.",
            "Add grilled chicken to the sauce. Simmer 5 minutes to marry flavours.",
            "Garnish with coriander and a drizzle of cream. Serve with naan or rice.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Goan Prawn Curry",
        "description": "Plump prawns in a fiery coconut milk and tamarind gravy with whole spices. A coastal Indian classic with bold, tangy depth — ready in just 25 minutes.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["seafood"],
        "spice_level": 4,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 20,
        "ingredients": [
            {"name": "Large prawns, peeled and deveined", "quantity": "500", "unit": "g"},
            {"name": "Coconut milk", "quantity": "400", "unit": "ml"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "medium"},
            {"name": "Tomato, chopped", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tsp"},
            {"name": "Tamarind paste", "quantity": "1", "unit": "tbsp"},
            {"name": "Goan curry powder or masala", "quantity": "2", "unit": "tbsp"},
            {"name": "Turmeric powder", "quantity": "½", "unit": "tsp"},
            {"name": "Green chillies, slit", "quantity": "2", "unit": ""},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Heat oil in a pan. Sauté onion until golden, about 6 minutes.",
            "Add garlic, ginger, and green chillies. Cook 1 minute.",
            "Add tomato, curry powder, and turmeric. Cook 4 minutes until oil separates.",
            "Pour in coconut milk and add tamarind paste. Stir and bring to a gentle simmer.",
            "Add prawns and cook just until they turn pink and curl, about 4 minutes. Do not overcook.",
            "Taste and adjust salt and tamarind. The gravy should be tangy and coconutty.",
            "Serve immediately with steamed rice.",
        ],
        "allergen_notes": "Contains shellfish. Avoid if allergic to prawns or crustaceans.",
    },

    # ── Italian — Chicken & Seafood ──────────────────────────────────────────
    {
        "title": "Chicken Piccata",
        "description": "Thin-pounded chicken cutlets pan-fried golden then finished in a bright lemon-caper-butter sauce. An Italian trattoria favourite that takes under 25 minutes.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Chicken breasts, halved and pounded thin", "quantity": "4", "unit": ""},
            {"name": "All-purpose flour for dredging", "quantity": "½", "unit": "cup"},
            {"name": "Butter", "quantity": "4", "unit": "tbsp"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Dry white wine", "quantity": "120", "unit": "ml"},
            {"name": "Chicken stock", "quantity": "120", "unit": "ml"},
            {"name": "Lemon juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Capers, drained", "quantity": "3", "unit": "tbsp"},
            {"name": "Fresh parsley, chopped", "quantity": "¼", "unit": "cup"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Season chicken with salt and pepper. Dredge in flour, shaking off excess.",
            "Heat olive oil and 2 tbsp butter in a large skillet over medium-high heat.",
            "Cook chicken 3–4 minutes per side until golden. Transfer to a plate.",
            "Add garlic to the pan and cook 30 seconds. Pour in wine and scrape up any browned bits.",
            "Add stock and lemon juice. Simmer 3 minutes until slightly reduced.",
            "Stir in capers and remaining butter. Return chicken to pan and coat in the sauce.",
            "Garnish with fresh parsley and lemon slices. Serve with pasta or roasted vegetables.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Shrimp Scampi with Linguine",
        "description": "Juicy garlic-butter shrimp tossed with al dente linguine, white wine, and a squeeze of lemon. A restaurant-quality Italian classic ready in 20 minutes.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["seafood"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 5,
        "cook_time_min": 20,
        "ingredients": [
            {"name": "Large shrimp, peeled and deveined", "quantity": "500", "unit": "g"},
            {"name": "Linguine pasta", "quantity": "400", "unit": "g"},
            {"name": "Butter", "quantity": "4", "unit": "tbsp"},
            {"name": "Olive oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Garlic cloves, thinly sliced", "quantity": "6", "unit": "cloves"},
            {"name": "Dry white wine", "quantity": "½", "unit": "cup"},
            {"name": "Lemon juice and zest", "quantity": "1", "unit": "lemon"},
            {"name": "Red chilli flakes", "quantity": "¼", "unit": "tsp"},
            {"name": "Fresh parsley, chopped", "quantity": "½", "unit": "cup"},
            {"name": "Parmesan, grated", "quantity": "¼", "unit": "cup"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Cook linguine in salted boiling water until al dente. Reserve 1 cup pasta water. Drain.",
            "Heat butter and olive oil in a large skillet over medium heat. Add garlic and chilli flakes, cook 1 minute.",
            "Add shrimp in a single layer. Cook 2 minutes per side until pink. Remove shrimp.",
            "Add white wine to the pan, scrape up any bits. Simmer 2 minutes.",
            "Add pasta and a splash of pasta water. Toss to coat. Return shrimp.",
            "Add lemon juice, zest, and parsley. Toss everything together.",
            "Serve in warm bowls with parmesan and extra parsley.",
        ],
        "allergen_notes": "Contains shellfish. Avoid if allergic to shrimp.",
    },
    {
        "title": "Chicken Parmigiana",
        "description": "Crispy breaded chicken topped with marinara, melted mozzarella, and fresh basil, baked until bubbling. The ultimate Italian-American comfort dish.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Chicken breasts, halved and pounded", "quantity": "4", "unit": ""},
            {"name": "Breadcrumbs", "quantity": "1", "unit": "cup"},
            {"name": "Parmesan, grated", "quantity": "½", "unit": "cup"},
            {"name": "Eggs, beaten", "quantity": "2", "unit": ""},
            {"name": "Marinara sauce", "quantity": "1½", "unit": "cups"},
            {"name": "Fresh mozzarella, sliced", "quantity": "200", "unit": "g"},
            {"name": "Fresh basil leaves", "quantity": "handful", "unit": ""},
            {"name": "Italian seasoning", "quantity": "1", "unit": "tsp"},
            {"name": "Olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 200°C / 400°F. Mix breadcrumbs with half the parmesan and Italian seasoning.",
            "Season chicken, dip in egg, then coat in breadcrumb mixture.",
            "Heat olive oil in an oven-safe skillet. Fry chicken 3 minutes per side until golden.",
            "Spoon marinara sauce over each piece. Top with mozzarella and remaining parmesan.",
            "Transfer to oven and bake 15–18 minutes until cheese is melted and bubbling.",
            "Rest 2 minutes. Top with fresh basil before serving.",
            "Serve with spaghetti or a green salad.",
        ],
        "allergen_notes": "",
    },

    # ── Mexican — Chicken & Seafood ──────────────────────────────────────────
    {
        "title": "Sizzling Chicken Fajitas",
        "description": "Juicy lime-marinated chicken strips with caramelised peppers and onions, served sizzling in warm flour tortillas with all the toppings.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "balanced", "vitamin-rich"],
        "dietary_tags": ["chicken"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Chicken breast, sliced into strips", "quantity": "600", "unit": "g"},
            {"name": "Flour tortillas", "quantity": "8", "unit": "large"},
            {"name": "Bell peppers (red, yellow, green), sliced", "quantity": "3", "unit": ""},
            {"name": "Onion, sliced", "quantity": "1", "unit": "large"},
            {"name": "Lime juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Cumin powder", "quantity": "1½", "unit": "tsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Chilli powder", "quantity": "½", "unit": "tsp"},
            {"name": "Oil", "quantity": "3", "unit": "tbsp"},
            {"name": "Sour cream, guacamole, salsa to serve", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Marinate chicken strips in lime juice, garlic, cumin, smoked paprika, chilli powder, and salt for 10 minutes.",
            "Heat a cast-iron skillet or heavy pan over very high heat until smoking.",
            "Cook chicken strips in a single layer, 3–4 minutes per side without stirring, for maximum char. Set aside.",
            "In the same pan, cook peppers and onion on high heat 4–5 minutes until charred at the edges.",
            "Return chicken to the pan, toss everything together for 1 minute.",
            "Warm tortillas directly over a flame or in a dry pan.",
            "Serve straight from the sizzling pan with sour cream, guacamole, and salsa.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Chipotle Shrimp Tacos",
        "description": "Smoky chipotle-spiced shrimp in crunchy corn tortillas with a cooling avocado crema and crunchy slaw. A fiesta of textures in every bite.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["seafood"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 10,
        "ingredients": [
            {"name": "Large shrimp, peeled and deveined", "quantity": "500", "unit": "g"},
            {"name": "Corn tortillas", "quantity": "12", "unit": "small"},
            {"name": "Chipotle in adobo, minced", "quantity": "2", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "2", "unit": "cloves"},
            {"name": "Lime juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Avocados", "quantity": "2", "unit": "ripe"},
            {"name": "Red cabbage, shredded", "quantity": "2", "unit": "cups"},
            {"name": "Sour cream", "quantity": "½", "unit": "cup"},
            {"name": "Cumin powder", "quantity": "1", "unit": "tsp"},
            {"name": "Fresh coriander", "quantity": "handful", "unit": ""},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
        ],
        "instructions": [
            "Toss shrimp with chipotle, garlic, cumin, 1 tbsp lime juice, and salt.",
            "Make avocado crema: blend avocado, sour cream, remaining lime juice, and a pinch of salt until smooth.",
            "Dress cabbage slaw with a squeeze of lime and pinch of salt.",
            "Heat oil in a skillet over high heat. Cook shrimp 2 minutes per side until pink and slightly charred.",
            "Warm corn tortillas in a dry pan.",
            "Assemble tacos: slaw first, then 3–4 shrimp, a drizzle of avocado crema, and fresh coriander.",
        ],
        "allergen_notes": "Contains shellfish.",
    },
    {
        "title": "Chicken Enchiladas Verde",
        "description": "Shredded chicken enchiladas smothered in a tangy roasted tomatillo verde sauce and baked with melted cheese. Comforting, bold, and deeply satisfying.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Chicken breasts, cooked and shredded", "quantity": "500", "unit": "g"},
            {"name": "Corn or flour tortillas", "quantity": "10", "unit": ""},
            {"name": "Tomatillos, husked", "quantity": "500", "unit": "g"},
            {"name": "Jalapeños", "quantity": "2", "unit": ""},
            {"name": "Onion", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves", "quantity": "3", "unit": "cloves"},
            {"name": "Fresh coriander", "quantity": "½", "unit": "cup"},
            {"name": "Sour cream", "quantity": "½", "unit": "cup"},
            {"name": "Monterey Jack cheese, shredded", "quantity": "2", "unit": "cups"},
            {"name": "Chicken stock", "quantity": "½", "unit": "cup"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
        ],
        "instructions": [
            "Preheat oven to 200°C / 400°F. Roast tomatillos, jalapeños, onion, and garlic on a tray for 20 minutes.",
            "Blend roasted vegetables with coriander, sour cream, and stock into a smooth verde sauce. Season.",
            "Mix shredded chicken with ½ cup verde sauce and half the cheese.",
            "Warm tortillas to make pliable. Fill each with chicken mixture, roll, and place seam-down in an oiled baking dish.",
            "Pour remaining verde sauce over the top. Sprinkle with remaining cheese.",
            "Bake 20 minutes until sauce is bubbly and cheese is golden.",
            "Serve with sour cream, sliced avocado, and extra coriander.",
        ],
        "allergen_notes": "",
    },

    # ── Mediterranean — Chicken & Seafood ────────────────────────────────────
    {
        "title": "Lemon Herb Roast Chicken Thighs",
        "description": "Juicy chicken thighs marinated in lemon, garlic, and fresh herbs, roasted until the skin is irresistibly crispy. A simple Mediterranean weeknight hero.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 35,
        "ingredients": [
            {"name": "Chicken thighs, bone-in skin-on", "quantity": "8", "unit": ""},
            {"name": "Lemon juice and zest", "quantity": "2", "unit": "lemons"},
            {"name": "Garlic cloves, minced", "quantity": "5", "unit": "cloves"},
            {"name": "Fresh rosemary, chopped", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh thyme leaves", "quantity": "1", "unit": "tbsp"},
            {"name": "Olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Dijon mustard", "quantity": "1", "unit": "tbsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Cherry tomatoes", "quantity": "1", "unit": "cup"},
            {"name": "Kalamata olives", "quantity": "½", "unit": "cup"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Mix lemon juice, zest, garlic, rosemary, thyme, olive oil, mustard, and paprika into a marinade.",
            "Score chicken thighs and coat generously. Marinate at least 30 minutes.",
            "Preheat oven to 220°C / 425°F.",
            "Place chicken skin-side up in a roasting tray. Scatter cherry tomatoes and olives around.",
            "Roast 35 minutes until skin is golden and crispy, basting once halfway through.",
            "Rest 5 minutes. Spoon pan juices over the chicken before serving.",
            "Serve with roasted potatoes or a simple Greek salad.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Garlic Butter Shrimp with Orzo",
        "description": "Pan-seared shrimp in rich garlic butter tossed with orzo, sun-dried tomatoes, and fresh spinach. A complete one-pan Mediterranean dinner in 25 minutes.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["seafood"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 5,
        "cook_time_min": 20,
        "ingredients": [
            {"name": "Large shrimp, peeled and deveined", "quantity": "500", "unit": "g"},
            {"name": "Orzo pasta", "quantity": "300", "unit": "g"},
            {"name": "Butter", "quantity": "4", "unit": "tbsp"},
            {"name": "Olive oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "5", "unit": "cloves"},
            {"name": "Sun-dried tomatoes, chopped", "quantity": "⅓", "unit": "cup"},
            {"name": "Baby spinach", "quantity": "2", "unit": "cups"},
            {"name": "Lemon juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh parsley, chopped", "quantity": "¼", "unit": "cup"},
            {"name": "Red chilli flakes", "quantity": "¼", "unit": "tsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Cook orzo in salted boiling water until al dente. Reserve ½ cup water, drain.",
            "Heat olive oil in a wide pan over high heat. Sear shrimp 2 minutes per side. Set aside.",
            "Reduce heat to medium. Add butter and garlic, cook 1 minute.",
            "Add sun-dried tomatoes and chilli flakes, stir 30 seconds.",
            "Add cooked orzo and a splash of pasta water. Toss.",
            "Add spinach and toss until wilted. Return shrimp and add lemon juice.",
            "Serve in warm bowls scattered with fresh parsley.",
        ],
        "allergen_notes": "Contains shellfish.",
    },
    {
        "title": "Chicken Souvlaki with Tzatziki",
        "description": "Greek-marinated chicken skewers grilled until charred and juicy, served in warm pitas with cool homemade tzatziki and crisp salad. A Mediterranean street-food favourite.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "balanced"],
        "dietary_tags": ["chicken"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Chicken breast, cubed", "quantity": "600", "unit": "g"},
            {"name": "Pita breads", "quantity": "8", "unit": ""},
            {"name": "Olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Lemon juice", "quantity": "3", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Dried oregano", "quantity": "1½", "unit": "tsp"},
            {"name": "Greek yoghurt", "quantity": "1", "unit": "cup"},
            {"name": "Cucumber, grated and squeezed dry", "quantity": "½", "unit": ""},
            {"name": "Fresh dill, chopped", "quantity": "2", "unit": "tbsp"},
            {"name": "Tomatoes, sliced", "quantity": "2", "unit": ""},
            {"name": "Red onion, thinly sliced", "quantity": "½", "unit": ""},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Marinate chicken with olive oil, lemon juice, garlic, oregano, salt, and pepper for at least 15 minutes.",
            "Make tzatziki: mix yoghurt with grated cucumber, dill, 1 minced garlic clove, and a squeeze of lemon. Season.",
            "Thread chicken onto skewers. Grill or pan-fry on high heat, turning every 2 minutes, until charred and cooked through — about 10 minutes.",
            "Warm pita breads.",
            "Assemble: spread tzatziki inside each pita, add chicken pieces, tomato, and red onion.",
            "Drizzle with a little extra olive oil and serve immediately.",
        ],
        "allergen_notes": "",
    },

    # ── Indian — Diabetic-friendly ───────────────────────────────────────────
    {
        "title": "Methi Dal (Fenugreek Lentil Curry)",
        "description": "Red lentils slow-simmered with fresh fenugreek leaves, turmeric, and a tempered mustard-garlic tarka. Fenugreek naturally helps regulate blood sugar — deeply nourishing and low-GI.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "iron-rich", "sugar-free"],
        "dietary_tags": ["vegan", "vegetarian", "diabetic-friendly"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Red lentils (masoor dal), rinsed", "quantity": "1", "unit": "cup"},
            {"name": "Fresh fenugreek leaves (methi), chopped", "quantity": "1½", "unit": "cups"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "medium"},
            {"name": "Tomato, chopped", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tsp"},
            {"name": "Turmeric powder", "quantity": "½", "unit": "tsp"},
            {"name": "Cumin seeds", "quantity": "1", "unit": "tsp"},
            {"name": "Mustard seeds", "quantity": "½", "unit": "tsp"},
            {"name": "Dry red chilli", "quantity": "1", "unit": ""},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Pressure cook lentils with turmeric and 2 cups water for 3 whistles until soft. Mash lightly.",
            "Heat oil in a pan. Add mustard seeds and cumin seeds. Let splutter.",
            "Add dry red chilli, then onion. Cook until golden, 7 minutes.",
            "Add garlic and ginger, cook 1 minute. Add tomato and cook until soft, 4 minutes.",
            "Add fenugreek leaves and stir. Cook 3 minutes until wilted.",
            "Pour cooked dal into the pan. Add ½ cup water to adjust consistency. Simmer 8 minutes.",
            "Season with salt. Serve with roti or cauliflower rice for a diabetic-friendly meal.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Egg Bhurji (Indian Spiced Scrambled Eggs)",
        "description": "Fluffy scrambled eggs cooked with onion, tomato, green chilli, and turmeric. High-protein, zero carb, and ready in 10 minutes — a perfect diabetic-friendly Indian breakfast or light dinner.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "sugar-free", "no-carb"],
        "dietary_tags": ["vegetarian", "diabetic-friendly"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 5,
        "cook_time_min": 10,
        "ingredients": [
            {"name": "Eggs", "quantity": "8", "unit": "large"},
            {"name": "Onion, finely chopped", "quantity": "1", "unit": "medium"},
            {"name": "Tomato, finely chopped", "quantity": "1", "unit": "medium"},
            {"name": "Green chilli, finely chopped", "quantity": "1", "unit": ""},
            {"name": "Garlic cloves, minced", "quantity": "2", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "½", "unit": "tsp"},
            {"name": "Turmeric powder", "quantity": "¼", "unit": "tsp"},
            {"name": "Cumin seeds", "quantity": "½", "unit": "tsp"},
            {"name": "Fresh coriander, chopped", "quantity": "3", "unit": "tbsp"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt and black pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Beat eggs with a pinch of salt and pepper. Set aside.",
            "Heat oil in a non-stick pan. Add cumin seeds and let splutter.",
            "Add onion and cook until soft and translucent, about 3 minutes.",
            "Add garlic, ginger, and green chilli. Cook 1 minute.",
            "Add tomato and turmeric. Cook 2 minutes until tomato softens.",
            "Pour in beaten eggs. Stir continuously with a spatula over medium heat until just set.",
            "Remove from heat (eggs continue cooking). Garnish with fresh coriander and serve immediately.",
        ],
        "allergen_notes": "Contains eggs.",
    },
    {
        "title": "Tandoori Spiced Chicken with Cucumber Raita",
        "description": "Yoghurt-marinated chicken grilled with smoky tandoori spices, served with a cooling cucumber raita. High protein, zero grains — an ideal diabetic-friendly Indian main course.",
        "cuisine_tag": "indian",
        "nutrition_tags": ["protein-rich", "sugar-free", "balanced"],
        "dietary_tags": ["chicken", "diabetic-friendly"],
        "spice_level": 3,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Chicken thighs, boneless, scored", "quantity": "700", "unit": "g"},
            {"name": "Plain yoghurt", "quantity": "½", "unit": "cup"},
            {"name": "Tandoori masala powder", "quantity": "2", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Ginger, grated", "quantity": "1", "unit": "tbsp"},
            {"name": "Lemon juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Kashmiri chilli powder", "quantity": "1", "unit": "tsp"},
            {"name": "Cucumber, grated and squeezed", "quantity": "1", "unit": "medium"},
            {"name": "Mint leaves, chopped", "quantity": "2", "unit": "tbsp"},
            {"name": "Greek yoghurt for raita", "quantity": "1", "unit": "cup"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Mix yoghurt, tandoori masala, garlic, ginger, lemon juice, Kashmiri chilli, and salt into a marinade.",
            "Coat chicken deeply in the marinade, ensuring it gets into the scored cuts. Marinate 30 minutes minimum.",
            "Make raita: mix Greek yoghurt with grated cucumber, mint, and a pinch of salt. Refrigerate.",
            "Heat a grill pan or oven grill to high. Brush with oil.",
            "Grill chicken 6–7 minutes per side until charred and cooked through.",
            "Rest 5 minutes before slicing.",
            "Serve with raita, sliced onions, and lemon wedges. Skip the bread for a low-carb meal.",
        ],
        "allergen_notes": "",
    },

    # ── Italian — Diabetic-friendly ──────────────────────────────────────────
    {
        "title": "Zucchini Noodles with Basil Pesto and Cherry Tomatoes",
        "description": "Spiralised zucchini tossed in vibrant homemade basil pesto with burst cherry tomatoes and pine nuts. All the flavour of pasta with a fraction of the carbs — ready in 15 minutes.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["vitamin-rich", "sugar-free", "no-carb"],
        "dietary_tags": ["vegetarian", "diabetic-friendly"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 5,
        "ingredients": [
            {"name": "Zucchini, spiralised or peeled into ribbons", "quantity": "4", "unit": "large"},
            {"name": "Cherry tomatoes, halved", "quantity": "1½", "unit": "cups"},
            {"name": "Fresh basil leaves, packed", "quantity": "2", "unit": "cups"},
            {"name": "Garlic cloves", "quantity": "2", "unit": "cloves"},
            {"name": "Pine nuts, toasted", "quantity": "¼", "unit": "cup"},
            {"name": "Parmesan, grated", "quantity": "⅓", "unit": "cup"},
            {"name": "Extra-virgin olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Lemon juice", "quantity": "1", "unit": "tbsp"},
            {"name": "Salt and black pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Make pesto: blend basil, garlic, pine nuts, parmesan, lemon juice, and olive oil until smooth. Season.",
            "Salt zucchini noodles and let sit 5 minutes. Pat dry with a kitchen towel to remove moisture.",
            "Heat a wide pan over high heat. Add cherry tomatoes and cook 2 minutes until beginning to blister.",
            "Add zucchini noodles and toss 1–2 minutes — just enough to warm through, not to soften.",
            "Remove from heat. Add pesto and toss quickly.",
            "Serve immediately topped with extra parmesan, pine nuts, and fresh basil.",
        ],
        "allergen_notes": "Contains tree nuts (pine nuts) and dairy.",
    },
    {
        "title": "Oven-Baked Salmon with Mediterranean Vegetables",
        "description": "Omega-3 rich salmon fillets baked with courgette, cherry tomatoes, olives, and herbs in one tray. Naturally low-carb, anti-inflammatory, and deeply satisfying.",
        "cuisine_tag": "italian",
        "nutrition_tags": ["protein-rich", "sugar-free", "balanced"],
        "dietary_tags": ["seafood", "diabetic-friendly"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Salmon fillets", "quantity": "4", "unit": "150g each"},
            {"name": "Zucchini, sliced into rounds", "quantity": "2", "unit": "medium"},
            {"name": "Cherry tomatoes", "quantity": "1½", "unit": "cups"},
            {"name": "Red onion, sliced into wedges", "quantity": "1", "unit": "medium"},
            {"name": "Kalamata olives, pitted", "quantity": "½", "unit": "cup"},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Extra-virgin olive oil", "quantity": "4", "unit": "tbsp"},
            {"name": "Lemon juice and zest", "quantity": "1", "unit": "lemon"},
            {"name": "Fresh thyme and rosemary", "quantity": "1", "unit": "tbsp each"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Preheat oven to 200°C / 400°F.",
            "Toss zucchini, tomatoes, red onion, and olives with half the olive oil, garlic, thyme, rosemary, salt, and pepper.",
            "Spread vegetables on a large baking tray. Roast 15 minutes.",
            "Nestle salmon fillets among the vegetables. Drizzle with remaining olive oil and lemon juice.",
            "Return to oven and bake 10–12 minutes until salmon is just cooked through and flakes easily.",
            "Finish with lemon zest and fresh herbs. Serve straight from the tray.",
        ],
        "allergen_notes": "Contains fish.",
    },

    # ── Mexican — Diabetic-friendly ──────────────────────────────────────────
    {
        "title": "Chicken Lettuce Wrap Tacos",
        "description": "Spiced ground chicken and black beans served in crisp iceberg lettuce cups with pico de gallo and avocado. All the taco flavour with zero tortilla carbs.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "sugar-free", "balanced"],
        "dietary_tags": ["chicken", "diabetic-friendly"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Ground chicken", "quantity": "500", "unit": "g"},
            {"name": "Iceberg lettuce heads", "quantity": "2", "unit": ""},
            {"name": "Black beans, drained", "quantity": "1", "unit": "can (400g)"},
            {"name": "Cherry tomatoes, diced", "quantity": "1", "unit": "cup"},
            {"name": "Avocado, diced", "quantity": "1", "unit": "ripe"},
            {"name": "Red onion, finely diced", "quantity": "½", "unit": ""},
            {"name": "Garlic cloves, minced", "quantity": "3", "unit": "cloves"},
            {"name": "Cumin powder", "quantity": "1½", "unit": "tsp"},
            {"name": "Chilli powder", "quantity": "½", "unit": "tsp"},
            {"name": "Lime juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh coriander", "quantity": "handful", "unit": ""},
            {"name": "Oil", "quantity": "1", "unit": "tbsp"},
        ],
        "instructions": [
            "Carefully separate lettuce leaves to form cups. Refrigerate until serving.",
            "Make pico de gallo: combine tomatoes, red onion, half the coriander, and 1 tbsp lime juice.",
            "Heat oil in a pan. Cook ground chicken, breaking it up, until browned, 6 minutes.",
            "Add garlic, cumin, and chilli powder. Cook 1 minute. Add black beans and stir.",
            "Simmer 3 minutes. Season with salt and remaining lime juice.",
            "Fill each lettuce cup with the chicken mixture. Top with pico de gallo and diced avocado.",
            "Scatter remaining coriander and serve immediately.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Mexican Black Bean and Vegetable Soup",
        "description": "A hearty low-GI soup of black beans, roasted peppers, and warming spices. High in fibre and plant protein, this comforting bowl keeps blood sugar steady for hours.",
        "cuisine_tag": "mexican",
        "nutrition_tags": ["protein-rich", "iron-rich", "sugar-free"],
        "dietary_tags": ["vegan", "vegetarian", "diabetic-friendly"],
        "spice_level": 2,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Black beans, drained", "quantity": "2", "unit": "cans (400g each)"},
            {"name": "Canned fire-roasted tomatoes", "quantity": "1", "unit": "can (400g)"},
            {"name": "Vegetable stock", "quantity": "1", "unit": "litre"},
            {"name": "Bell peppers (red and green), diced", "quantity": "2", "unit": ""},
            {"name": "Onion, diced", "quantity": "1", "unit": "large"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Cumin powder", "quantity": "2", "unit": "tsp"},
            {"name": "Smoked paprika", "quantity": "1", "unit": "tsp"},
            {"name": "Chipotle in adobo", "quantity": "1", "unit": "tbsp"},
            {"name": "Lime juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Fresh coriander and avocado to serve", "quantity": "", "unit": ""},
        ],
        "instructions": [
            "Heat oil in a large pot. Sauté onion until soft, 5 minutes.",
            "Add garlic, bell peppers, cumin, and smoked paprika. Cook 3 minutes.",
            "Add fire-roasted tomatoes, chipotle, black beans, and stock. Stir well.",
            "Bring to a boil then reduce heat. Simmer 20 minutes.",
            "Use an immersion blender to blend a quarter of the soup for a creamy-chunky texture.",
            "Stir in lime juice. Taste and adjust seasoning.",
            "Serve topped with diced avocado and fresh coriander.",
        ],
        "allergen_notes": "",
    },

    # ── Mediterranean — Diabetic-friendly ────────────────────────────────────
    {
        "title": "Greek Salad with Grilled Chicken",
        "description": "Herb-marinated grilled chicken served over a classic Greek salad of cucumber, tomato, olives, and feta with lemon-oregano dressing. A protein-rich, near-zero-carb Mediterranean plate.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "vitamin-rich", "sugar-free"],
        "dietary_tags": ["chicken", "diabetic-friendly"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Chicken breasts", "quantity": "4", "unit": ""},
            {"name": "Cucumber, diced", "quantity": "1", "unit": "large"},
            {"name": "Cherry tomatoes, halved", "quantity": "2", "unit": "cups"},
            {"name": "Kalamata olives", "quantity": "½", "unit": "cup"},
            {"name": "Feta cheese, cubed", "quantity": "150", "unit": "g"},
            {"name": "Red onion, thinly sliced", "quantity": "½", "unit": ""},
            {"name": "Dried oregano", "quantity": "2", "unit": "tsp"},
            {"name": "Lemon juice", "quantity": "4", "unit": "tbsp"},
            {"name": "Extra-virgin olive oil", "quantity": "5", "unit": "tbsp"},
            {"name": "Garlic cloves, minced", "quantity": "2", "unit": "cloves"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Marinate chicken in 2 tbsp olive oil, 2 tbsp lemon juice, garlic, 1 tsp oregano, salt, and pepper for 10 minutes.",
            "Grill chicken on high heat 6 minutes per side until golden and cooked through. Rest 3 minutes, then slice.",
            "Make dressing: whisk remaining olive oil, lemon juice, oregano, salt, and pepper.",
            "Combine cucumber, tomatoes, olives, red onion, and feta in a large bowl.",
            "Drizzle dressing over the salad and toss gently.",
            "Arrange salad on plates and top with sliced grilled chicken.",
        ],
        "allergen_notes": "",
    },
    {
        "title": "Red Lentil and Spinach Soup",
        "description": "A warming Mediterranean soup of red lentils and spinach simmered with cumin, coriander, and lemon. Naturally thick, low-GI, and full of soluble fibre that steadies blood sugar.",
        "cuisine_tag": "mediterranean",
        "nutrition_tags": ["protein-rich", "iron-rich", "sugar-free"],
        "dietary_tags": ["vegan", "vegetarian", "diabetic-friendly"],
        "spice_level": 1,
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 30,
        "ingredients": [
            {"name": "Red lentils, rinsed", "quantity": "1½", "unit": "cups"},
            {"name": "Baby spinach", "quantity": "3", "unit": "cups"},
            {"name": "Onion, diced", "quantity": "1", "unit": "large"},
            {"name": "Carrot, diced", "quantity": "1", "unit": "medium"},
            {"name": "Garlic cloves, minced", "quantity": "4", "unit": "cloves"},
            {"name": "Cumin powder", "quantity": "1½", "unit": "tsp"},
            {"name": "Coriander powder", "quantity": "1", "unit": "tsp"},
            {"name": "Turmeric", "quantity": "¼", "unit": "tsp"},
            {"name": "Vegetable stock", "quantity": "1.2", "unit": "litres"},
            {"name": "Lemon juice", "quantity": "2", "unit": "tbsp"},
            {"name": "Olive oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Salt and pepper", "quantity": "to taste", "unit": ""},
        ],
        "instructions": [
            "Heat olive oil. Sauté onion and carrot until soft, 7 minutes.",
            "Add garlic, cumin, coriander, and turmeric. Stir 1 minute.",
            "Add lentils and stock. Bring to a boil, then simmer 20 minutes until lentils are completely soft.",
            "Use an immersion blender to blend half the soup for a creamy texture.",
            "Add spinach and stir until wilted, about 2 minutes.",
            "Stir in lemon juice. Season with salt and pepper.",
            "Serve with a drizzle of olive oil and warm whole-grain bread if desired.",
        ],
        "allergen_notes": "",
    },
]


_RECIPE_IMAGES = {
    # Indian
    "Palak Paneer with Jeera Rice":             "/static/images/palak_paneer.jpg",
    "Chana Masala with Bhatura":                "/static/images/chana_masala.jpg",
    "Dal Makhani":                              "/static/images/dal_makhani.jpg",
    "Aloo Gobi":                                "/static/images/aloo_gobi.jpg",
    "Vegetable Biryani":                        "/static/images/biryani.jpg",
    # Italian
    "Creamy Tuscan White Bean Pasta":           "/static/images/tuscan_pasta.jpg",
    "Margherita Pizza with Homemade Dough":     "/static/images/pizza.jpg",
    "Mushroom Risotto":                         "/static/images/risotto.jpg",
    "Minestrone Soup with Crusty Bread":        "/static/images/minestrone.jpg",
    "Gnocchi with Sage Brown Butter":           "/static/images/gnocchi.jpg",
    # Mexican
    "Black Bean Tacos with Mango Salsa":        "/static/images/tacos.jpg",
    "Veggie Enchiladas with Red Chile Sauce":   "/static/images/enchiladas.jpg",
    "Vegetarian Burrito Bowl":                  "/static/images/burrito_bowl.jpg",
    "Cheese Quesadillas with Roasted Salsa":    "/static/images/quesadillas.jpg",
    "Mexican Lentil Soup (Sopa de Lentejas)":   "/static/images/mexican_soup.jpg",
    # Mediterranean — vegetarian
    "Greek Chickpea and Feta Salad Bowl":       "/static/images/greek_salad.jpg",
    "Lemon Herb Orzo with Roasted Vegetables":  "/static/images/orzo.jpg",
    "Shakshuka":                                "/static/images/shakshuka.jpg",
    "Falafel Pita with Tahini Sauce":           "/static/images/falafel.jpg",
    "Stuffed Bell Peppers with Quinoa and Feta":"/static/images/stuffed_peppers.jpg",
    # Indian — chicken & seafood
    "Butter Chicken (Murgh Makhani)":           "/static/images/butter_chicken.jpg",
    "Chicken Tikka Masala":                     "/static/images/chicken_tikka.jpg",
    "Goan Prawn Curry":                         "/static/images/goan_prawn_curry.jpg",
    # Italian — chicken & seafood
    "Chicken Piccata":                          "/static/images/chicken_piccata.jpg",
    "Shrimp Scampi with Linguine":              "/static/images/shrimp_scampi.jpg",
    "Chicken Parmigiana":                       "/static/images/chicken_parmigiana.jpg",
    # Mexican — chicken & seafood
    "Sizzling Chicken Fajitas":                 "/static/images/chicken_fajitas.jpg",
    "Chipotle Shrimp Tacos":                    "/static/images/shrimp_tacos.jpg",
    "Chicken Enchiladas Verde":                 "/static/images/chicken_enchiladas.jpg",
    # Mediterranean — chicken & seafood
    "Lemon Herb Roast Chicken Thighs":          "/static/images/lemon_herb_chicken.jpg",
    "Garlic Butter Shrimp with Orzo":           "/static/images/garlic_shrimp_orzo.jpg",
    "Chicken Souvlaki with Tzatziki":           "/static/images/chicken_souvlaki.jpg",
    # Indian — diabetic-friendly
    "Methi Dal (Fenugreek Lentil Curry)":       "/static/images/methi_dal.jpg",
    "Egg Bhurji (Indian Spiced Scrambled Eggs)":"/static/images/egg_bhurji.jpg",
    "Tandoori Spiced Chicken with Cucumber Raita":"/static/images/tandoori_chicken.jpg",
    # Italian — diabetic-friendly
    "Zucchini Noodles with Basil Pesto and Cherry Tomatoes":"/static/images/zucchini_noodles.jpg",
    "Oven-Baked Salmon with Mediterranean Vegetables":"/static/images/baked_salmon.jpg",
    # Mexican — diabetic-friendly
    "Chicken Lettuce Wrap Tacos":               "/static/images/lettuce_wraps.jpg",
    "Mexican Black Bean and Vegetable Soup":    "/static/images/black_bean_soup.jpg",
    # Mediterranean — diabetic-friendly
    "Greek Salad with Grilled Chicken":         "/static/images/greek_chicken.jpg",
    "Red Lentil and Spinach Soup":              "/static/images/lentil_soup.jpg",
}

_CUISINE_FALLBACK_IMAGES = {
    "indian":        "/static/images/chana_masala.jpg",
    "italian":       "/static/images/tuscan_pasta.jpg",
    "mexican":       "/static/images/tacos.jpg",
    "mediterranean": "/static/images/greek_salad.jpg",
}


def recipe_image_url(title, cuisine_tag=""):
    if title in _RECIPE_IMAGES:
        return _RECIPE_IMAGES[title]
    return _CUISINE_FALLBACK_IMAGES.get(cuisine_tag, "/static/images/biryani.jpg")


def _try_themealdb(title, cuisine_tag):
    """Search TheMealDB for a matching meal image (free public API, no key required)."""
    import urllib.request
    import urllib.parse

    # 1. Search by full title
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={urllib.parse.quote(title)}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    if data.get("meals"):
        return data["meals"][0]["strMealThumb"]

    # 2. Search by key words from the title (skip short/common words)
    stop = {"with", "and", "the", "a", "an", "in", "on", "of", "for", "from",
            "style", "over", "spiced", "herb", "roasted", "baked", "grilled"}
    words = [w for w in re.sub(r"[^a-z\s]", "", title.lower()).split()
             if w not in stop and len(w) > 3]
    for word in words[:4]:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={urllib.parse.quote(word)}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data.get("meals"):
            return data["meals"][0]["strMealThumb"]

    # 3. Fall back to a random meal from the cuisine area
    area_map = {
        "indian": "Indian", "italian": "Italian", "mexican": "Mexican",
        "mediterranean": "Greek", "american": "American",
        "chinese": "Chinese", "european": "British",
    }
    area = area_map.get((cuisine_tag or "").lower())
    if area:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?a={area}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data.get("meals"):
            meal = random.choice(data["meals"][:10])
            return meal["strMealThumb"]

    return None


def _download_and_save_image(title, cuisine_tag=""):
    """Fetch a food photo and save to static/images/. Falls back to local images."""
    import urllib.request

    safe_name = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
    filename = f"{safe_name}.jpg"
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")
    save_path = os.path.join(images_dir, filename)

    if os.path.exists(save_path):
        return f"/static/images/{filename}"

    # Try TheMealDB first (best match quality, free, no key required)
    try:
        img_url = _try_themealdb(title, cuisine_tag)
        if img_url:
            with urllib.request.urlopen(img_url, timeout=15) as img_resp:
                with open(save_path, "wb") as f:
                    f.write(img_resp.read())
            return f"/static/images/{filename}"
    except Exception:
        pass

    # Fall back to the best matching local image
    return _try_local_food_image(title, cuisine_tag) or recipe_image_url(title, cuisine_tag)


def _try_unsplash_public_api(title, cuisine_tag):
    """Try Unsplash public API (no key required, but rate limited to ~50 requests/hour)"""
    import urllib.request
    import urllib.parse

    # Extract key food terms from title for better search results
    food_keywords = [
        "chicken", "beef", "pork", "fish", "salmon", "shrimp", "pasta", "rice", "bread",
        "soup", "salad", "curry", "stew", "pizza", "burger", "sandwich", "tacos",
        "noodles", "sushi", "cake", "pie", "cookies", "pancakes", "waffles",
        "vegetables", "fruit", "cheese", "butter", "cream", "milk", "eggs",
        "potatoes", "tomatoes", "onions", "garlic", "herbs", "spices"
    ]

    # Clean title and find food-related words
    clean_title = re.sub(r'[^\w\s]', '', title.lower())
    title_words = clean_title.split()
    food_words = [word for word in title_words if word in food_keywords]

    # Build a more specific food-focused query
    if food_words:
        # Use the found food words plus cuisine and "food"
        query_parts = food_words[:3] + [cuisine_tag, "food", "dish", "meal"]
    else:
        # Fallback to cuisine + common food terms
        query_parts = [cuisine_tag, "food", "dish", "recipe", "meal", "cooking"]

    query = urllib.parse.quote(" ".join(query_parts))
    api_url = f"https://api.unsplash.com/search/photos?query={query}&orientation=landscape&per_page=1&content_filter=high"

    req = urllib.request.Request(api_url, headers={"User-Agent": "FridayNightVeggieWins/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    if data.get("results") and len(data["results"]) > 0:
        return data["results"][0]["urls"]["regular"]
    return None


def _try_lorem_picsum(title, cuisine_tag):
    """Try Lorem Picsum for generic food images (no key required)"""
    import urllib.request

    # Use multiple seeds based on title and cuisine for variety
    base_seed = hash(title + (cuisine_tag or "")) % 1000

    # Try a few different seeds to get better food-like images
    seeds_to_try = [base_seed, (base_seed + 100) % 1000, (base_seed + 200) % 1000]

    for seed in seeds_to_try:
        # Use consistent dimensions for food photos (landscape)
        img_url = f"https://picsum.photos/seed/food_{seed}/800/600"
        # Test if URL is accessible (Lorem Picsum should always work)
        try:
            req = urllib.request.Request(img_url, method='HEAD')
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return img_url
        except:
            continue

    # Fallback to a basic Lorem Picsum image
    return f"https://picsum.photos/800/600?random={base_seed}"


def _try_foodish_api(title, cuisine_tag):
    """Try Foodish API for food images (free, no key required)"""
    import urllib.request
    import json
    import re

    # Foodish has categories: biryani, burger, butter-chicken, dessert, dosa, idli, pizza, rice, samosa, tacos
    # Map cuisine types and ingredients to Foodish categories more accurately
    cuisine_mapping = {
        'indian': ['biryani', 'butter-chicken', 'dosa', 'samosa'],
        'italian': ['pizza'],  # Foodish only has pizza for Italian
        'mexican': ['tacos'],
        'american': ['burger'],
        'mediterranean': ['dosa'],  # closest available
        'chinese': ['rice'],
    }

    # Check for specific ingredients in title - be more specific
    title_lower = title.lower()
    ingredient_mapping = {
        'chicken tikka': ['butter-chicken'],
        'butter chicken': ['butter-chicken'],
        'biryani': ['biryani'],
        'dosa': ['dosa'],
        'samosa': ['samosa'],
        'pizza': ['pizza'],
        'tacos': ['tacos'],
        'burger': ['burger'],
        'rice': ['rice'],
        'pasta': [],  # No pasta in Foodish, let local images handle this
        'spaghetti': [],  # No spaghetti in Foodish
        'curry': ['butter-chicken'],
        'masala': ['butter-chicken'],
    }

    # Try ingredient-specific first (only for exact matches)
    for ingredient, categories in ingredient_mapping.items():
        if ingredient in title_lower and categories:  # Only if we have categories
            for category in categories:
                try:
                    api_url = f"https://foodish-api.com/api/images/{category}"
                    with urllib.request.urlopen(api_url, timeout=10) as resp:
                        data = json.loads(resp.read().decode())
                        if data.get('image'):
                            return data['image']
                except:
                    continue

    # Fall back to cuisine mapping ONLY for specific cuisines that have good matches
    # Don't use generic Italian -> pizza fallback since it gives wrong images
    if cuisine_tag == 'indian':
        categories = ['biryani', 'butter-chicken']  # Only use these for Indian
        for category in categories:
            try:
                api_url = f"https://foodish-api.com/api/images/{category}"
                with urllib.request.urlopen(api_url, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    if data.get('image'):
                        return data['image']
            except:
                continue

    return None  # Let local images handle other cuisines


def _try_local_food_image(title, cuisine_tag):
    """Try to find a relevant local food image based on title keywords"""
    import os
    import re

    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")

    # Clean title for matching
    clean_title = re.sub(r"[^a-z0-9\s]", "", title.lower())

    # Keywords to look for in local image filenames - more specific mappings
    food_keywords = {
        'chicken tikka': ['chicken_tikka'],
        'butter chicken': ['butter_chicken'],
        'biryani': ['biryani'],
        'dosa': ['dosa'],
        'samosa': ['samosa'],
        'pizza': ['margherita_pizza'],
        'pasta': ['pasta_primavera', 'pasta_puttanesca', 'chicken_parmigiana'],
        'spaghetti': ['pasta_primavera', 'chicken_parmigiana'],
        'carbonara': ['pasta_puttanesca'],
        'tacos': ['fish_tacos', 'chicken_enchiladas'],
        'burger': ['veggie_burger'],
        'rice': ['biryani', 'cauliflower_rice'],
        'soup': ['black_bean_soup', 'minestrone', 'lentil_soup', 'mexican_soup'],
        'noodle': ['zucchini_noodles', 'chicken_and_vegetable_chow_mein'],
        'chow mein': ['chicken_and_vegetable_chow_mein'],
        'salad': ['greek_salad', 'quinoa_salad'],
        'pancakes': ['blueberry_pancakes'],
        'indian': ['biryani', 'chana_masala', 'butter_chicken', 'chicken_tikka'],
        'italian': ['margherita_pizza', 'chicken_parmigiana', 'pasta_primavera'],
        'mexican': ['chicken_enchiladas', 'burrito_bowl'],
        'american': ['veggie_burger', 'mac_and_cheese'],
    }

    # Check for direct title matches first - more specific
    title_words = clean_title.split()
    title_phrase = ' '.join(title_words[:3])  # Check first 3 words as phrase
    
    # Check for exact phrase matches
    if title_phrase in food_keywords:
        candidates = food_keywords[title_phrase]
        for candidate in candidates:
            candidate_file = f"{candidate}.jpg"
            if os.path.exists(os.path.join(images_dir, candidate_file)):
                return f"/static/images/{candidate_file}"
    
    # Check individual words
    for word in title_words:
        if word in food_keywords:
            candidates = food_keywords[word]
            for candidate in candidates:
                candidate_file = f"{candidate}.jpg"
                if os.path.exists(os.path.join(images_dir, candidate_file)):
                    return f"/static/images/{candidate_file}"

    # Check cuisine-based matches
    if cuisine_tag in food_keywords:
        candidates = food_keywords[cuisine_tag]
        for candidate in candidates:
            candidate_file = f"{candidate}.jpg"
            if os.path.exists(os.path.join(images_dir, candidate_file)):
                return f"/static/images/{candidate_file}"

    # Fallback to a generic food image
    fallback_options = ['chana_masala.jpg', 'chicken_parmigiana.jpg', 'burrito_bowl.jpg', 'greek_salad.jpg']
    for fallback in fallback_options:
        if os.path.exists(os.path.join(images_dir, fallback)):
            return f"/static/images/{fallback}"

    return None


def _is_valid_api_key(key):
    return bool(key and key.startswith("sk-ant") and len(key) > 20)


def _call_claude_cli(prompt):
    """Call the claude CLI in non-interactive mode. No API key required.
    ANTHROPIC_API_KEY is stripped from the subprocess env so the CLI uses
    its own session auth rather than the (possibly placeholder) env key.
    """
    import subprocess
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )
    if result.returncode != 0:
        msg = result.stderr.strip() or result.stdout.strip() or "claude CLI returned non-zero exit code"
        raise RuntimeError(msg)
    return result.stdout.strip()


def _pick_fallback(profile, recent_titles=None):
    cuisines = profile.cuisines if profile.cuisines else []
    dietary = set(profile.dietary_restrictions or [])
    exclude = set(recent_titles or [])

    candidates = [r for r in FALLBACK_RECIPES if not cuisines or r["cuisine_tag"] in cuisines]
    if not candidates:
        candidates = list(FALLBACK_RECIPES)

    if dietary:
        matching = [r for r in candidates if set(r["dietary_tags"]) & dietary]
        if matching:
            candidates = matching

    # Filter out recipes seen in the last 7 days; if all are excluded fall back to full set
    fresh = [r for r in candidates if r["title"] not in exclude]
    if fresh:
        candidates = fresh

    recipe = dict(random.choice(candidates))
    recipe["servings"] = profile.num_people
    recipe["spice_level"] = min(profile.spice_level, recipe["spice_level"] + 1)
    recipe["image_url"] = _download_and_save_image(recipe["title"], recipe.get("cuisine_tag", ""))
    return recipe


_GRAIN_WORDS = {"rice", "pasta", "bread", "naan", "roti", "tortilla", "orzo",
                "gnocchi", "couscous", "quinoa", "flour", "oats", "noodle", "basmati",
                "arborio", "pita", "bhatura", "biryani", "jeera rice"}

_SAUCE_KEYWORDS = {
    "tomato":    ["tomato", "passata", "marinara", "salsa", "crushed tomato"],
    "coconut":   ["coconut milk", "coconut cream"],
    "cream":     ["cream", "butter", "bechamel", "heavy cream"],
    "olive-oil": ["olive oil"],
    "broth":     ["broth", "stock", "vegetable stock"],
    "yogurt":    ["yogurt", "curd", "raita"],
    "dry":       [],  # no sauce — penalise saucy recipes
}


def generate_from_fridge(ingredients, profile=None, cuisine=None, sauce=None, exclude_titles=None):
    api_key = os.getenv("ANTHROPIC_API_KEY")

    fridge_list = ", ".join(ingredients)
    dietary  = ", ".join(profile.dietary_restrictions) if profile and profile.dietary_restrictions else "none"
    spice    = profile.spice_level if profile else 3
    servings = profile.num_people if profile else 4

    cuisine_line = f"- Cuisine style: {cuisine}" if cuisine else "- Cuisine style: any (choose the best fit)"
    sauce_line   = f"- Sauce / cooking base: {sauce}" if sauce else ""
    grain_note   = ("IMPORTANT: Do NOT include any grains (rice, pasta, bread, naan, tortilla, etc.) "
                    "unless they appear explicitly in the fridge ingredient list above.")

    prompt = f"""You are a creative home chef. The user has these ingredients in their fridge:
{fridge_list}

Constraints:
- Dietary restrictions: {dietary}
{cuisine_line}
{sauce_line}
- Spice level: {spice}/5
- Servings: {servings}

{grain_note}
You may add up to 5 pantry staples (salt, basic dried spices, oil) but do NOT require fresh produce, proteins, or dairy beyond what is listed.

Return ONLY a valid JSON object:
{{
  "title": "Recipe Name",
  "description": "2-3 sentences mentioning the key fridge ingredients",
  "cuisine_tag": "indian|italian|mexican|mediterranean",
  "nutrition_tags": ["protein-rich"|"iron-rich"|"vitamin-rich"|"balanced"|"sugar-free"|"no-carb"],
  "dietary_tags": ["vegetarian"|"vegan"|"chicken"|"seafood"|"diabetic-friendly"],
  "spice_level": {spice},
  "servings": {servings},
  "prep_time_min": 10,
  "cook_time_min": 25,
  "ingredients": [{{"name": "...", "quantity": "...", "unit": "..."}}],
  "instructions": ["Step 1...", "Step 2..."],
  "allergen_notes": "",
  "fridge_match": ["fridge ingredients actually used"]
}}"""

    try:
        if _is_valid_api_key(api_key):
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            text = message.content[0].text.strip()
        else:
            text = _call_claude_cli(prompt)

        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            text = m.group(0)

        data = json.loads(text)
        data["image_url"] = _download_and_save_image(data.get("title", ""), data.get("cuisine_tag", ""))
        return data

    except Exception:
        return _fridge_fallback(ingredients, profile, cuisine=cuisine, sauce=sauce, exclude_titles=exclude_titles)


def _fridge_fallback(ingredients, profile=None, cuisine=None, sauce=None, exclude_titles=None):
    fridge_set = set(i.lower() for i in ingredients)
    has_grains = any(word in fridge_set for word in _GRAIN_WORDS)
    excluded = set(exclude_titles or [])

    def score(recipe):
        recipe_text = " ".join(ing["name"].lower() for ing in recipe.get("ingredients", []))

        match_score = sum(
            1 for item in fridge_set
            if any(word in recipe_text for word in item.lower().split())
        )

        if not has_grains and any(g in recipe_text for g in _GRAIN_WORDS):
            match_score -= 3

        if cuisine and recipe.get("cuisine_tag") == cuisine:
            match_score += 5

        if sauce and sauce in _SAUCE_KEYWORDS:
            sauce_words = _SAUCE_KEYWORDS[sauce]
            if sauce == "dry":
                if not any(w in recipe_text for ws in _SAUCE_KEYWORDS.values() if ws for w in ws):
                    match_score += 3
            elif any(w in recipe_text for w in sauce_words):
                match_score += 3

        return match_score

    # Hard-filter by cuisine if selected
    candidates = FALLBACK_RECIPES
    if cuisine:
        filtered = [r for r in candidates if r.get("cuisine_tag") == cuisine]
        if filtered:
            candidates = filtered

    # Score all candidates
    scored = sorted(candidates, key=score, reverse=True)

    # Exclude already-seen titles; if all excluded, reset to full scored list
    fresh = [r for r in scored if r["title"] not in excluded]
    pool = fresh if fresh else scored

    # Pick randomly from the top-scoring tier (within 2 points of the best)
    top = score(pool[0])
    top_tier = [r for r in pool if score(r) >= top - 2]
    best = dict(random.choice(top_tier))

    if profile:
        best["servings"] = profile.num_people
        best["spice_level"] = min(profile.spice_level, best["spice_level"] + 1)

    matched = [i for i in ingredients
               if any(i.lower() in ing["name"].lower() for ing in best.get("ingredients", []))]
    best["fridge_match"] = matched if matched else []
    best["image_url"] = _download_and_save_image(best["title"], best.get("cuisine_tag", ""))
    return best


def generate_recipe(profile, recent_titles=None):
    api_key = os.getenv("ANTHROPIC_API_KEY")

    dietary_list = profile.dietary_restrictions or []
    cuisine_list = profile.cuisines or []
    nutrition_list = profile.nutrition_goals or []

    dietary = ", ".join(dietary_list) if dietary_list else "none specified"
    cuisines = ", ".join(cuisine_list) if cuisine_list else "any"
    nutrition = ", ".join(nutrition_list) if nutrition_list else "balanced"
    recent = ", ".join(recent_titles) if recent_titles else "none"

    cuisine_tag_example = cuisine_list[0] if cuisine_list else "italian"
    dietary_tag_example = json.dumps(dietary_list) if dietary_list else '["none"]'
    nutrition_tag_example = json.dumps(nutrition_list[:3]) if nutrition_list else '["balanced"]'

    age_note = ""
    if profile.age_youngest:
        if profile.age_youngest <= 5:
            age_note = (
                f"\nIMPORTANT: Youngest eater is {profile.age_youngest} years old. "
                "Avoid choking hazards. Include allergen warnings and age-appropriate texture notes in allergen_notes."
            )
        elif profile.age_youngest <= 12:
            age_note = (
                f"\nIMPORTANT: Youngest eater is {profile.age_youngest} years old. "
                "Keep flavours approachable for children; note any strong spices or allergens."
            )

    prompt = f"""You are a professional chef. Generate a recipe as a JSON object that strictly follows this household profile.

HOUSEHOLD PROFILE (you MUST respect every constraint below):
- Dietary restrictions: {dietary} — the recipe MUST comply with ALL of these restrictions
- Preferred cuisines: {cuisines} — pick ONE cuisine from this exact list
- Spice level: {profile.spice_level}/5 (1=very mild, 5=very hot) — match this exactly
- Servings: {profile.num_people} — scale ALL ingredient quantities for exactly {profile.num_people} people
- Nutrition goals: {nutrition} — the recipe should address these goals
- Age range: {profile.age_youngest}–{profile.age_oldest} years{age_note}

RECENTLY GENERATED — do NOT repeat these titles:
{recent}

Return ONLY a valid JSON object, no extra text, no markdown fences:
{{
  "title": "Recipe Name",
  "description": "2-3 sentence appealing description",
  "cuisine_tag": "{cuisine_tag_example}",
  "nutrition_tags": {nutrition_tag_example},
  "dietary_tags": {dietary_tag_example},
  "spice_level": {profile.spice_level},
  "servings": {profile.num_people},
  "prep_time_min": 10,
  "cook_time_min": 25,
  "ingredients": [{{"name": "...", "quantity": "...", "unit": "..."}}],
  "instructions": ["Step 1: ...", "Step 2: ..."],
  "allergen_notes": "list any allergens or age-related notes here"
}}"""

    try:
        if _is_valid_api_key(api_key):
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            text = message.content[0].text.strip()
        else:
            text = _call_claude_cli(prompt)

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)

        data = json.loads(text)
        data["image_url"] = _download_and_save_image(data.get("title", ""), data.get("cuisine_tag", ""))
        return data

    except Exception:
        return _pick_fallback(profile, recent_titles=recent_titles)
