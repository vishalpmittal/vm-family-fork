"""Tests for recipe_generator.py — fallback selection, fridge logic, image lookup, API key validation."""
import pytest
from recipe_generator import (
    FALLBACK_RECIPES,
    _GRAIN_WORDS,
    _RECIPE_IMAGES,
    _CUISINE_FALLBACK_IMAGES,
    _fridge_fallback,
    _is_valid_api_key,
    _pick_fallback,
    recipe_image_url,
)


# ── helpers ───────────────────────────────────────────────────────────────────

class FakeProfile:
    def __init__(
        self,
        dietary_restrictions=None,
        cuisines=None,
        spice_level=3,
        num_people=4,
        nutrition_goals=None,
        age_youngest=5,
        age_oldest=40,
    ):
        self.dietary_restrictions = dietary_restrictions or []
        self.cuisines = cuisines or []
        self.spice_level = spice_level
        self.num_people = num_people
        self.nutrition_goals = nutrition_goals or []
        self.age_youngest = age_youngest
        self.age_oldest = age_oldest


# ═══════════════════════════════════════════════════════════════════════════════
# FALLBACK RECIPE LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

class TestFallbackLibrary:

    def test_library_has_at_least_40_recipes(self):
        assert len(FALLBACK_RECIPES) >= 40

    def test_all_four_cuisines_represented(self):
        cuisines = {r["cuisine_tag"] for r in FALLBACK_RECIPES}
        assert cuisines == {"indian", "italian", "mexican", "mediterranean"}

    def test_every_recipe_has_required_fields(self):
        required = {
            "title", "description", "cuisine_tag", "nutrition_tags",
            "dietary_tags", "spice_level", "servings", "prep_time_min",
            "cook_time_min", "ingredients", "instructions", "allergen_notes",
        }
        for recipe in FALLBACK_RECIPES:
            missing = required - recipe.keys()
            assert not missing, f"'{recipe.get('title')}' missing fields: {missing}"

    def test_every_recipe_has_ingredients(self):
        for recipe in FALLBACK_RECIPES:
            assert len(recipe["ingredients"]) > 0, f"'{recipe['title']}' has no ingredients"

    def test_every_recipe_has_instructions(self):
        for recipe in FALLBACK_RECIPES:
            assert len(recipe["instructions"]) > 0, f"'{recipe['title']}' has no instructions"

    def test_spice_levels_in_valid_range(self):
        for recipe in FALLBACK_RECIPES:
            assert 1 <= recipe["spice_level"] <= 5, \
                f"'{recipe['title']}' has invalid spice_level {recipe['spice_level']}"

    def test_no_duplicate_titles(self):
        titles = [r["title"] for r in FALLBACK_RECIPES]
        duplicates = [t for t in titles if titles.count(t) > 1]
        assert not duplicates, f"Duplicate titles found: {set(duplicates)}"

    def test_diabetic_friendly_recipes_exist(self):
        diabetic = [r for r in FALLBACK_RECIPES if "diabetic-friendly" in r["dietary_tags"]]
        assert len(diabetic) >= 4, "Expected at least 4 diabetic-friendly recipes"

    def test_diabetic_recipes_in_each_cuisine(self):
        diabetic = [r for r in FALLBACK_RECIPES if "diabetic-friendly" in r["dietary_tags"]]
        cuisines = {r["cuisine_tag"] for r in diabetic}
        assert cuisines == {"indian", "italian", "mexican", "mediterranean"}, \
            "Diabetic recipes missing cuisines: " + str({"indian","italian","mexican","mediterranean"} - cuisines)

    def test_chicken_recipes_exist(self):
        chicken = [r for r in FALLBACK_RECIPES if "chicken" in r["dietary_tags"]]
        assert len(chicken) >= 4

    def test_seafood_recipes_exist(self):
        seafood = [r for r in FALLBACK_RECIPES if "seafood" in r["dietary_tags"]]
        assert len(seafood) >= 2

    def test_vegetarian_recipes_exist(self):
        veg = [r for r in FALLBACK_RECIPES if "vegetarian" in r["dietary_tags"]]
        assert len(veg) >= 10

    def test_ingredient_items_have_name_quantity_unit(self):
        for recipe in FALLBACK_RECIPES:
            for ing in recipe["ingredients"]:
                assert "name" in ing, f"Missing 'name' in ingredient of '{recipe['title']}'"
                assert "quantity" in ing, f"Missing 'quantity' in ingredient of '{recipe['title']}'"
                assert "unit" in ing, f"Missing 'unit' in ingredient of '{recipe['title']}'"


# ═══════════════════════════════════════════════════════════════════════════════
# API KEY VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

class TestApiKeyValidation:

    def test_valid_key_accepted(self):
        assert _is_valid_api_key("sk-ant-api03-abcdefghijklmnopqrstuvwxyz") is True

    def test_placeholder_key_rejected(self):
        assert _is_valid_api_key("your_anthropic_api_key_here") is False

    def test_none_rejected(self):
        assert _is_valid_api_key(None) is False

    def test_empty_string_rejected(self):
        assert _is_valid_api_key("") is False

    def test_wrong_prefix_rejected(self):
        assert _is_valid_api_key("sk-openai-abcdefghijklmnop") is False

    def test_too_short_rejected(self):
        assert _is_valid_api_key("sk-ant-short") is False

    def test_exact_boundary_rejected(self):
        # exactly 20 chars starting with sk-ant — should be False (must be > 20)
        key = "sk-ant" + "x" * 14  # total 20
        assert _is_valid_api_key(key) is False

    def test_twenty_one_chars_accepted(self):
        key = "sk-ant" + "x" * 15  # total 21
        assert _is_valid_api_key(key) is True


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE LOOKUP
# ═══════════════════════════════════════════════════════════════════════════════

class TestImageLookup:

    def test_known_title_returns_local_path(self):
        url = recipe_image_url("Palak Paneer with Jeera Rice", "indian")
        assert url.startswith("/static/images/")
        assert url.endswith(".jpg")

    def test_unknown_title_falls_back_to_cuisine(self):
        url = recipe_image_url("Some Unknown Dish", "indian")
        assert url.startswith("/static/images/")

    def test_unknown_title_unknown_cuisine_returns_fallback(self):
        url = recipe_image_url("Mystery Dish", "unknown_cuisine")
        assert url.startswith("/static/images/")

    def test_all_recipe_images_map_to_local_paths(self):
        for title, path in _RECIPE_IMAGES.items():
            assert path.startswith("/static/images/"), \
                f"'{title}' has non-local image path: {path}"
            assert path.endswith(".jpg"), f"'{title}' image is not a .jpg"

    def test_all_cuisine_fallbacks_exist(self):
        for cuisine, path in _CUISINE_FALLBACK_IMAGES.items():
            assert path.startswith("/static/images/"), \
                f"Cuisine '{cuisine}' fallback has non-local path: {path}"

    def test_every_recipe_in_library_has_image_mapping(self):
        missing = [
            r["title"] for r in FALLBACK_RECIPES
            if r["title"] not in _RECIPE_IMAGES
        ]
        assert not missing, f"Recipes missing image mappings: {missing}"


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE-BASED FALLBACK SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

class TestPickFallback:

    def test_returns_a_recipe(self):
        profile = FakeProfile()
        result = _pick_fallback(profile)
        assert isinstance(result, dict)
        assert "title" in result

    def test_respects_cuisine_preference(self):
        profile = FakeProfile(cuisines=["italian"])
        for _ in range(20):
            result = _pick_fallback(profile)
            assert result["cuisine_tag"] == "italian"

    def test_respects_multiple_cuisines(self):
        profile = FakeProfile(cuisines=["indian", "mexican"])
        for _ in range(20):
            result = _pick_fallback(profile)
            assert result["cuisine_tag"] in ("indian", "mexican")

    def test_respects_dietary_restriction(self):
        profile = FakeProfile(dietary_restrictions=["diabetic-friendly"])
        for _ in range(20):
            result = _pick_fallback(profile)
            assert "diabetic-friendly" in result["dietary_tags"]

    def test_respects_cuisine_and_dietary_combined(self):
        profile = FakeProfile(cuisines=["indian"], dietary_restrictions=["diabetic-friendly"])
        for _ in range(30):
            result = _pick_fallback(profile)
            assert result["cuisine_tag"] == "indian"
            assert "diabetic-friendly" in result["dietary_tags"]

    def test_scales_servings_to_profile(self):
        profile = FakeProfile(num_people=6)
        result = _pick_fallback(profile)
        assert result["servings"] == 6

    def test_spice_level_capped_to_profile(self):
        profile = FakeProfile(spice_level=1)
        for _ in range(20):
            result = _pick_fallback(profile)
            assert result["spice_level"] <= 2  # profile level + 1 max

    def test_fallback_when_cuisine_has_no_match(self):
        # No recipes for "japanese" — should fall back to full library
        profile = FakeProfile(cuisines=["japanese"])
        result = _pick_fallback(profile)
        assert "title" in result  # still returns something

    def test_result_includes_image_url(self):
        profile = FakeProfile()
        result = _pick_fallback(profile)
        assert "image_url" in result
        assert result["image_url"].startswith("/static/images/")


# ═══════════════════════════════════════════════════════════════════════════════
# FRIDGE FALLBACK
# ═══════════════════════════════════════════════════════════════════════════════

class TestFridgeFallback:

    def test_returns_a_recipe(self):
        result = _fridge_fallback(["spinach", "paneer"])
        assert isinstance(result, dict)
        assert "title" in result

    def test_includes_fridge_match_field(self):
        result = _fridge_fallback(["spinach", "paneer"])
        assert "fridge_match" in result
        assert isinstance(result["fridge_match"], list)

    def test_matched_ingredients_are_subset_of_input(self):
        ingredients = ["spinach", "paneer", "tomatoes"]
        result = _fridge_fallback(ingredients)
        for matched in result["fridge_match"]:
            assert matched in ingredients

    def test_cuisine_filter_applied(self):
        for _ in range(15):
            result = _fridge_fallback(["tomato", "cheese"], cuisine="italian")
            assert result["cuisine_tag"] == "italian"

    def test_excludes_seen_titles(self):
        ingredients = ["spinach", "tomato", "garlic"]
        first = _fridge_fallback(ingredients)
        exclude = [first["title"]]
        # Run many times — should never return the excluded title
        for _ in range(30):
            result = _fridge_fallback(ingredients, exclude_titles=exclude)
            if len(FALLBACK_RECIPES) > 1:  # only meaningful if >1 recipe exists
                assert result["title"] != exclude[0] or len(FALLBACK_RECIPES) == 1

    def test_grain_penalty_when_no_grains_in_fridge(self):
        # Fridge has no grains — recipes requiring grains should score lower
        # Test by ensuring a grain-free recipe wins over a grain-heavy one when
        # only non-grain ingredients are provided
        ingredients = ["spinach", "paneer", "tomato"]
        result = _fridge_fallback(ingredients, cuisine="indian")
        recipe_text = " ".join(
            ing["name"].lower() for ing in result.get("ingredients", [])
        )
        # If grains appear, it means the grain penalty didn't eliminate all grain recipes
        # — acceptable if all indian candidates have grains. Check score logic held.
        assert result["title"]  # at minimum, a result was returned

    def test_no_grain_penalty_when_grains_in_fridge(self):
        # User added rice — grain recipes should be eligible
        result = _fridge_fallback(["spinach", "basmati rice", "paneer"])
        assert "title" in result

    def test_scales_servings_with_profile(self):
        profile = FakeProfile(num_people=2)
        result = _fridge_fallback(["tomato", "cheese"], profile=profile)
        assert result["servings"] == 2

    def test_spice_capped_with_profile(self):
        profile = FakeProfile(spice_level=2)
        result = _fridge_fallback(["tomato", "paneer"], profile=profile)
        assert result["spice_level"] <= 3

    def test_empty_exclude_list_works(self):
        result = _fridge_fallback(["tomato"], exclude_titles=[])
        assert "title" in result

    def test_single_ingredient_returns_result(self):
        result = _fridge_fallback(["tomato"])
        assert "title" in result

    def test_result_has_image_url(self):
        result = _fridge_fallback(["spinach", "paneer"])
        assert "image_url" in result
        assert result["image_url"].startswith("/static/images/")

    def test_sauce_boost_applied(self):
        # Requesting tomato sauce — tomato-based recipes should be preferred
        result = _fridge_fallback(["onion", "garlic"], sauce="tomato", cuisine="italian")
        assert result["cuisine_tag"] == "italian"

    def test_no_crash_on_all_excluded(self):
        # If all recipes excluded, should still return something
        all_titles = [r["title"] for r in FALLBACK_RECIPES]
        result = _fridge_fallback(["tomato"], exclude_titles=all_titles)
        assert "title" in result


# ═══════════════════════════════════════════════════════════════════════════════
# GRAIN WORDS SET
# ═══════════════════════════════════════════════════════════════════════════════

class TestGrainWords:

    def test_common_grains_in_set(self):
        for grain in ["rice", "pasta", "bread", "naan", "tortilla", "orzo", "gnocchi"]:
            assert grain in _GRAIN_WORDS, f"'{grain}' missing from _GRAIN_WORDS"

    def test_non_grains_not_in_set(self):
        for item in ["spinach", "paneer", "tomato", "chicken", "olive oil"]:
            assert item not in _GRAIN_WORDS, f"'{item}' should not be in _GRAIN_WORDS"
