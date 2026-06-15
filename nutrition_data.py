"""
Reference nutrition data per 100g of edible portion.

Values are drawn from food-sources.md (which lists per-serving figures) and
standard public nutrition references (USDA FoodData Central, IFCT 2017 for
Indian foods). Where a food is typically eaten cooked (e.g. dal, rice), the
number reflects the raw/dry form unless noted in the "note" field, since
cooked weights vary with water absorption.

Schema for each item:
    name      display name (with Hindi/regional name in parens where useful)
    protein   grams per 100g
    calories  kcal per 100g
    carbs     grams per 100g
    fat       grams per 100g
    fiber     grams per 100g
    note      short string, may be empty
"""


def _row(name, protein, calories, carbs, fat, fiber, note=""):
    return {
        "name": name,
        "protein": protein,
        "calories": calories,
        "carbs": carbs,
        "fat": fat,
        "fiber": fiber,
        "note": note,
    }


CATEGORIES = [
    {
        "key": "millets",
        "label": "Millets",
        "emoji": "🌾",
        "blurb": "Whole-grain millets — gluten-free, mineral-dense. Values are for raw/dry grain.",
        "items": [
            _row("Foxtail Millet (Kangni, कंगनी)",        12.3, 351, 60.9, 4.3,  8.0,  "High iron"),
            _row("Kodo Millet (Kodo, कोदो)",               8.3, 353, 65.9, 1.4,  9.0,  ""),
            _row("Barnyard Millet (Sanwa, सनवा)",          6.2, 307, 65.5, 2.2,  9.8,  "Low GI"),
            _row("Brown Top Millet (Hari Kangni)",        11.5, 340, 71.0, 4.0,  9.0,  ""),
            _row("Little Millet (Kutki, कुटकी)",            7.7, 341, 67.0, 4.7,  7.6,  ""),
            _row("Pearl Millet (Bajra, बाजरा)",            11.0, 378, 67.0, 4.2,  8.5,  "High iron, magnesium"),
            _row("Finger Millet (Ragi, रागी)",              7.3, 336, 72.0, 1.3, 11.0,  "Calcium 344 mg"),
            _row("Sorghum (Jowar, ज्वार)",                 11.0, 339, 72.0, 3.3,  6.7,  ""),
        ],
    },
    {
        "key": "legumes",
        "label": "Legumes & Pulses",
        "emoji": "🫘",
        "blurb": "Dals, beans and chickpeas — values shown for dry/raw form.",
        "items": [
            _row("Chickpea, Kabuli (Chana, चना)",          19.0, 364, 61.0,  6.0, 17.0, "Sattu = 22 g/100 g"),
            _row("Chana Dal (split chickpea)",             22.0, 364, 60.0,  6.0, 12.0, ""),
            _row("Black Chana (Kala chana, काला चना)",     19.0, 350, 60.0,  4.0, 18.0, ""),
            _row("Toor / Arhar Dal (pigeon pea)",          22.0, 343, 63.0,  1.5, 15.0, ""),
            _row("Moong Dal (yellow split mung)",          24.0, 347, 59.0,  1.2, 16.0, ""),
            _row("Whole Moong (green gram)",               24.0, 347, 63.0,  1.2, 16.0, "Sprouted: ≈3 g/100 g (water gain)"),
            _row("Masoor Dal (red lentil)",                25.0, 352, 63.0,  1.1, 11.0, ""),
            _row("Urad Dal (black gram)",                  25.0, 341, 59.0,  1.6, 18.0, ""),
            _row("Rajma (kidney bean)",                    24.0, 333, 60.0,  0.8, 15.0, "High iron"),
            _row("Lobia (black-eyed pea)",                 24.0, 343, 60.0,  2.0, 11.0, ""),
            _row("Horse Gram (Kulthi, कुलथी)",             22.0, 321, 57.0,  0.5,  5.0, "High iron"),
            _row("Soybean (whole, dry)",                   36.0, 446, 30.0, 20.0,  9.0, "Complete protein"),
            _row("Green Peas (fresh)",                      5.4,  81, 14.0,  0.4,  5.7, "≈ 8 g per 160 g serving"),
        ],
    },
    {
        "key": "plant-protein",
        "label": "Plant Protein",
        "emoji": "🌱",
        "blurb": "Concentrated vegetarian protein — tofu, tempeh, gluten, flours.",
        "items": [
            _row("Tofu (firm)",                            17.0, 144,  3.0,  9.0,  2.0, "PDCAAS ≈ 1.0"),
            _row("Tempeh",                                 19.0, 192,  9.0, 11.0,  0.0, "Fermented soy"),
            _row("Soy Chunks / TVP (dry)",                 52.0, 345, 33.0,  0.5, 13.0, "Hydrates 2–3x"),
            _row("Seitan (wheat gluten)",                  75.0, 370, 14.0,  1.9,  0.6, "Not gluten-free"),
            _row("Sattu (roasted chana flour)",            22.0, 413, 60.0,  5.0, 18.0, "≈ 12 g per 50 g serving"),
            _row("Besan (gram flour)",                     22.0, 387, 58.0,  7.0, 11.0, "≈ 8 g per cheela"),
            _row("Edamame (shelled, cooked)",              11.0, 122,  9.0,  5.0,  5.0, ""),
            _row("Quinoa (cooked)",                         4.4, 120, 21.0,  1.9,  2.8, "Complete protein"),
            _row("Masoor-dal Tofu (homemade)",              7.2,  90,  9.0,  0.5,  4.0, "≈ 13 g per 180 g block"),
            _row("Peanut",                                 26.0, 567, 16.0, 49.0,  9.0, "≈ 8 g per 30 g handful"),
        ],
    },
    {
        "key": "dairy-eggs",
        "label": "Dairy & Eggs",
        "emoji": "🥚",
        "blurb": "Complete-protein staples.",
        "items": [
            _row("Paneer (whole-milk)",                    20.0, 265,  1.2, 21.0,  0.0, "Calcium 480 mg"),
            _row("Pumpkin/Watermelon-Seed Paneer",         27.0, 410, 12.0, 33.0,  6.0, "Dairy-free alt"),
            _row("Greek Yogurt (plain, low-fat)",          10.0,  59,  3.6,  0.4,  0.0, ""),
            _row("Curd / Dahi (whole milk)",                3.5,  61,  4.7,  3.3,  0.0, ""),
            _row("Cottage Cheese (low-fat)",               11.0,  72,  3.4,  1.0,  0.0, ""),
            _row("Milk (whole)",                            3.4,  61,  4.8,  3.3,  0.0, "Calcium 113 mg"),
            _row("Whey Protein (concentrate)",             75.0, 400, 10.0,  6.0,  0.0, "Supplement"),
            _row("Egg (whole)",                            13.0, 155,  1.1, 11.0,  0.0, "≈ 6 g per 50 g egg"),
            _row("Egg White",                              11.0,  52,  0.7,  0.2,  0.0, ""),
        ],
    },
    {
        "key": "meat-seafood",
        "label": "Meat & Seafood",
        "emoji": "🍗",
        "blurb": "Animal protein — values for cooked weight unless noted.",
        "items": [
            _row("Chicken Breast (skinless)",              31.0, 165,  0.0,  3.6,  0.0, ""),
            _row("Chicken Thigh (skinless)",               26.0, 209,  0.0, 11.0,  0.0, ""),
            _row("Turkey Breast",                          30.0, 135,  0.0,  1.0,  0.0, ""),
            _row("Lean Beef (sirloin)",                    26.0, 250,  0.0, 15.0,  0.0, "High heme iron, B12"),
            _row("Pork Tenderloin",                        27.0, 143,  0.0,  3.5,  0.0, ""),
            _row("Lamb / Mutton",                          25.0, 294,  0.0, 21.0,  0.0, ""),
            _row("Salmon (Atlantic)",                      25.0, 208,  0.0, 13.0,  0.0, "Omega-3 EPA/DHA"),
            _row("Tuna (canned in water)",                 24.0, 116,  0.0,  1.0,  0.0, ""),
            _row("Tilapia",                                26.0, 129,  0.0,  2.7,  0.0, ""),
            _row("Cod",                                    23.0, 105,  0.0,  0.9,  0.0, "Very lean"),
            _row("Shrimp",                                 24.0,  99,  0.2,  0.3,  0.0, ""),
            _row("Sardines (canned in oil)",               25.0, 208,  0.0, 11.0,  0.0, "Calcium 382 mg"),
        ],
    },
    {
        "key": "nuts-seeds",
        "label": "Nuts & Seeds",
        "emoji": "🥜",
        "blurb": "Calorie-dense — small portions still meaningful for protein and minerals.",
        "items": [
            _row("Almond",                                 21.0, 579, 22.0, 50.0, 13.0, "Calcium 264 mg"),
            _row("Walnut",                                 15.0, 654, 14.0, 65.0,  7.0, "Plant omega-3 (ALA)"),
            _row("Cashew",                                 18.0, 553, 30.0, 44.0,  3.0, ""),
            _row("Pistachio",                              20.0, 560, 28.0, 45.0, 10.0, ""),
            _row("Pumpkin Seed",                           30.0, 559, 11.0, 49.0,  6.0, "Iron 8.8 mg, zinc"),
            _row("Sunflower Seed",                         21.0, 584, 20.0, 51.0,  9.0, ""),
            _row("Watermelon Seed",                        28.0, 557, 15.0, 47.0,  0.0, ""),
            _row("Sesame Seed (Til)",                      18.0, 573, 23.0, 50.0, 12.0, "Calcium 975 mg"),
            _row("Chia Seed",                              17.0, 486, 42.0, 31.0, 34.0, "ALA omega-3"),
            _row("Flax Seed (Alsi)",                       18.0, 534, 29.0, 42.0, 27.0, "ALA omega-3"),
            _row("Hemp Seed (hulled)",                     31.0, 553,  9.0, 49.0,  4.0, "Complete protein"),
        ],
    },
    {
        "key": "grains",
        "label": "Whole Grains",
        "emoji": "🍚",
        "blurb": "Cereals and pseudo-cereals — values for raw/dry grain.",
        "items": [
            _row("Brown Rice",                              8.0, 370, 77.0,  2.7,  3.5, ""),
            _row("White Rice (long-grain)",                 7.0, 365, 80.0,  0.7,  1.3, ""),
            _row("Whole-Wheat Flour (Atta)",               13.0, 340, 72.0,  2.5, 11.0, ""),
            _row("Rolled Oats",                            13.0, 379, 68.0,  7.0, 10.0, "β-glucan fibre"),
            _row("Buckwheat (Kuttu)",                      13.0, 343, 72.0,  3.4, 10.0, "Gluten-free"),
            _row("Amaranth (Rajgira, Chaulai)",            14.0, 371, 65.0,  7.0,  7.0, "Calcium 159 mg"),
            _row("Barley (pearled)",                       12.0, 354, 73.0,  2.3, 17.0, ""),
            _row("Quinoa (dry)",                           14.0, 368, 64.0,  6.1,  7.0, "Complete protein"),
        ],
    },
    {
        "key": "vegetables",
        "label": "Vegetables (notable protein)",
        "emoji": "🥦",
        "blurb": "Raw weights. Most vegetables are low-protein, but these contribute meaningfully.",
        "items": [
            _row("Spinach (Palak)",                         2.9,  23,  3.6,  0.4,  2.2, "Iron 2.7 mg"),
            _row("Broccoli",                                2.8,  34,  7.0,  0.4,  2.6, "Vitamin C 89 mg"),
            _row("Kale",                                    4.3,  49,  9.0,  0.9,  3.6, "Vitamin K, A"),
            _row("Brussels Sprouts",                        3.4,  43,  9.0,  0.3,  3.8, ""),
            _row("Mushroom (button)",                       3.1,  22,  3.3,  0.3,  1.0, "Vitamin D when sun-dried"),
            _row("Sweet Corn",                              3.3,  86, 19.0,  1.2,  2.4, ""),
            _row("Asparagus",                               2.2,  20,  3.9,  0.1,  2.1, ""),
            _row("Artichoke",                               3.3,  47, 11.0,  0.2,  5.4, ""),
        ],
    },
    {
        "key": "fruits",
        "label": "Fruits",
        "emoji": "🍓",
        "blurb": "Carb-leaning but micronutrient-rich; a few are surprisingly protein-positive.",
        "items": [
            _row("Guava",                                   2.6,  68, 14.0,  1.0,  5.4, "Vitamin C 228 mg"),
            _row("Avocado",                                 2.0, 160,  9.0, 15.0,  7.0, "Mono-unsat fat"),
            _row("Banana",                                  1.1,  89, 23.0,  0.3,  2.6, ""),
            _row("Blackberry",                              1.4,  43, 10.0,  0.5,  5.3, ""),
            _row("Raspberry",                               1.2,  52, 12.0,  0.7,  6.5, ""),
            _row("Pomegranate (arils)",                     1.7,  83, 19.0,  1.2,  4.0, ""),
            _row("Orange",                                  0.9,  47, 12.0,  0.1,  2.4, "Vitamin C 53 mg"),
            _row("Apple",                                   0.3,  52, 14.0,  0.2,  2.4, ""),
            _row("Mango",                                   0.8,  60, 15.0,  0.4,  1.6, "Vitamin A"),
        ],
    },
]


def all_categories():
    """Return the full list of categories (used by the /nutrition route)."""
    return CATEGORIES
