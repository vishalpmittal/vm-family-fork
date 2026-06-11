"""Tests for Flask routes — all pages and API endpoints."""
import json
import pytest

from app import app as flask_app
from extensions import db
from models import Recipe, UserProfile


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def profile(app):
    with app.app_context():
        p = UserProfile(
            email="test@example.com",
            dietary_restrictions=["vegetarian"],
            spice_level=3,
            num_people=4,
            age_youngest=5,
            age_oldest=40,
            nutrition_goals=["balanced"],
            cuisines=["indian", "italian"],
            timezone="America/New_York",
        )
        db.session.add(p)
        db.session.commit()
        return p.id


@pytest.fixture
def recipe(app, profile):
    with app.app_context():
        r = Recipe(
            title="Palak Paneer Test",
            description="A test recipe for spinach and paneer.",
            cuisine_tag="indian",
            nutrition_tags=["protein-rich"],
            dietary_tags=["vegetarian"],
            spice_level=3,
            servings=4,
            prep_time_min=10,
            cook_time_min=25,
            ingredients=[{"name": "Spinach", "quantity": "2", "unit": "cups"},
                         {"name": "Paneer", "quantity": "200", "unit": "g"}],
            instructions=["Blanch spinach.", "Add paneer and cook."],
            allergen_notes="",
            image_url="/static/images/palak_paneer.jpg",
            source="on_demand",
        )
        db.session.add(r)
        db.session.commit()
        return r.id


# ═══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class TestHomeRoute:

    def test_redirects_to_profile_when_no_profile(self, client):
        res = client.get("/")
        assert res.status_code == 302
        assert "/profile" in res.headers["Location"]

    def test_home_loads_with_profile(self, client, profile):
        res = client.get("/")
        assert res.status_code == 200
        assert b"Friday Night" in res.data or b"Veggie" in res.data

    def test_home_shows_recipe_when_present(self, client, recipe):
        res = client.get("/")
        assert res.status_code == 200
        assert b"Palak Paneer Test" in res.data


# ═══════════════════════════════════════════════════════════════════════════════
# COOKBOOK PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class TestCookbookRoute:

    def test_cookbook_loads(self, client, profile):
        res = client.get("/cookbook")
        assert res.status_code == 200

    def test_cookbook_shows_recipes(self, client, recipe):
        res = client.get("/cookbook")
        assert b"Palak Paneer Test" in res.data

    def test_cookbook_search_returns_match(self, client, recipe):
        res = client.get("/cookbook?q=spinach")
        assert res.status_code == 200
        assert b"Palak Paneer Test" in res.data

    def test_cookbook_search_no_match(self, client, recipe):
        res = client.get("/cookbook?q=zzznomatch")
        assert res.status_code == 200
        assert b"Palak Paneer Test" not in res.data

    def test_cookbook_cuisine_filter(self, client, recipe):
        res = client.get("/cookbook?cuisine=indian")
        assert res.status_code == 200
        assert b"Palak Paneer Test" in res.data

    def test_cookbook_cuisine_filter_excludes_other(self, client, recipe):
        res = client.get("/cookbook?cuisine=mexican")
        assert res.status_code == 200
        assert b"Palak Paneer Test" not in res.data

    def test_cookbook_diet_filter_match(self, client, recipe):
        res = client.get("/cookbook?diet=vegetarian")
        assert res.status_code == 200
        assert b"Palak Paneer Test" in res.data

    def test_cookbook_diet_filter_no_match(self, client, recipe):
        res = client.get("/cookbook?diet=vegan")
        assert res.status_code == 200
        assert b"Palak Paneer Test" not in res.data

    def test_cookbook_spice_filter(self, client, recipe):
        res = client.get("/cookbook?spice_max=3")
        assert res.status_code == 200
        assert b"Palak Paneer Test" in res.data

    def test_cookbook_spice_filter_excludes_too_hot(self, client, recipe):
        res = client.get("/cookbook?spice_max=2")
        assert res.status_code == 200
        assert b"Palak Paneer Test" not in res.data

    def test_cookbook_time_filter(self, client, recipe):
        # recipe total = 35 min — should appear with max=60
        res = client.get("/cookbook?time_max=60")
        assert b"Palak Paneer Test" in res.data

    def test_cookbook_time_filter_excludes_slow(self, client, recipe):
        # recipe total = 35 min — should not appear with max=20
        res = client.get("/cookbook?time_max=20")
        assert b"Palak Paneer Test" not in res.data


# ═══════════════════════════════════════════════════════════════════════════════
# RECIPE DETAIL PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class TestRecipeDetailRoute:

    def test_recipe_detail_loads(self, client, recipe):
        res = client.get(f"/recipe/{recipe}")
        assert res.status_code == 200
        assert b"Palak Paneer Test" in res.data

    def test_recipe_detail_shows_ingredients(self, client, recipe):
        res = client.get(f"/recipe/{recipe}")
        assert b"Spinach" in res.data

    def test_recipe_detail_shows_instructions(self, client, recipe):
        res = client.get(f"/recipe/{recipe}")
        assert b"Blanch spinach" in res.data

    def test_recipe_detail_404_for_missing(self, client, profile):
        res = client.get("/recipe/99999")
        assert res.status_code == 404


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class TestProfileRoute:

    def test_profile_page_loads_empty(self, client):
        res = client.get("/profile")
        assert res.status_code == 200

    def test_profile_page_loads_with_existing_profile(self, client, profile):
        res = client.get("/profile")
        assert res.status_code == 200

    def test_profile_post_creates_profile(self, client, app):
        with app.app_context():
            assert UserProfile.query.count() == 0
        res = client.post("/profile", data={
            "dietary_restrictions": ["vegetarian"],
            "spice_level": "3",
            "num_people": "4",
            "age_youngest": "5",
            "age_oldest": "40",
            "nutrition_goals": ["balanced"],
            "cuisines": ["indian"],
            "email": "newuser@example.com",
            "timezone": "America/New_York",
        })
        assert res.status_code == 302  # redirect to home
        with app.app_context():
            assert UserProfile.query.count() == 1
            p = UserProfile.query.first()
            assert p.email == "newuser@example.com"
            assert p.num_people == 4

    def test_profile_post_updates_existing(self, client, app, profile):
        res = client.post("/profile", data={
            "dietary_restrictions": ["vegan"],
            "spice_level": "1",
            "num_people": "2",
            "age_youngest": "3",
            "age_oldest": "35",
            "nutrition_goals": ["protein-rich"],
            "cuisines": ["italian"],
            "email": "updated@example.com",
            "timezone": "America/Chicago",
        })
        assert res.status_code == 302
        with app.app_context():
            assert UserProfile.query.count() == 1  # no duplicate created
            p = UserProfile.query.first()
            assert p.email == "updated@example.com"
            assert p.spice_level == 1


# ═══════════════════════════════════════════════════════════════════════════════
# FRIDGE PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class TestFridgeRoute:

    def test_fridge_page_loads(self, client, profile):
        res = client.get("/fridge")
        assert res.status_code == 200
        assert b"Fridge" in res.data or b"fridge" in res.data


# ═══════════════════════════════════════════════════════════════════════════════
# API — /api/generate
# ═══════════════════════════════════════════════════════════════════════════════

class TestApiGenerate:

    def test_generate_returns_recipe(self, client, profile):
        res = client.post("/api/generate")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "recipe" in data
        assert "title" in data["recipe"]

    def test_generate_saves_to_cookbook(self, client, app, profile):
        with app.app_context():
            count_before = Recipe.query.count()
        client.post("/api/generate")
        with app.app_context():
            assert Recipe.query.count() == count_before + 1

    def test_generate_no_profile_returns_error(self, client):
        res = client.post("/api/generate")
        assert res.status_code == 500
        data = json.loads(res.data)
        assert "error" in data

    def test_generate_no_duplicates_on_repeat(self, client, app, profile):
        # Generating twice should not create duplicate entries for the same title
        res1 = client.post("/api/generate")
        title = json.loads(res1.data)["recipe"]["title"]
        res2 = client.post("/api/generate")
        with app.app_context():
            count = Recipe.query.filter_by(title=title).count()
            assert count == 1


# ═══════════════════════════════════════════════════════════════════════════════
# API — /api/fridge-generate
# ═══════════════════════════════════════════════════════════════════════════════

class TestApiFridgeGenerate:

    def test_fridge_generate_returns_recipe(self, client, profile):
        res = client.post(
            "/api/fridge-generate",
            json={"ingredients": ["spinach", "paneer", "tomato"]},
            content_type="application/json",
        )
        assert res.status_code == 200
        data = json.loads(res.data)
        assert "recipe" in data
        assert "title" in data["recipe"]

    def test_fridge_generate_returns_fridge_match(self, client, profile):
        res = client.post(
            "/api/fridge-generate",
            json={"ingredients": ["spinach", "paneer", "tomato"]},
            content_type="application/json",
        )
        data = json.loads(res.data)
        assert "fridge_match" in data["recipe"]
        assert isinstance(data["recipe"]["fridge_match"], list)

    def test_fridge_generate_empty_ingredients_returns_400(self, client, profile):
        res = client.post(
            "/api/fridge-generate",
            json={"ingredients": []},
            content_type="application/json",
        )
        assert res.status_code == 400
        data = json.loads(res.data)
        assert "error" in data

    def test_fridge_generate_no_ingredients_key_returns_400(self, client, profile):
        res = client.post(
            "/api/fridge-generate",
            json={},
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_fridge_generate_saves_with_fridge_source(self, client, app, profile):
        client.post(
            "/api/fridge-generate",
            json={"ingredients": ["tomato", "cheese"]},
            content_type="application/json",
        )
        with app.app_context():
            fridge_recipes = Recipe.query.filter_by(source="fridge").all()
            assert len(fridge_recipes) >= 1

    def test_fridge_generate_respects_cuisine(self, client, profile):
        res = client.post(
            "/api/fridge-generate",
            json={"ingredients": ["tomato", "garlic"], "cuisine": "italian"},
            content_type="application/json",
        )
        data = json.loads(res.data)
        assert data["recipe"]["cuisine_tag"] == "italian"

    def test_fridge_generate_exclude_titles(self, client, profile):
        res1 = client.post(
            "/api/fridge-generate",
            json={"ingredients": ["spinach", "paneer", "tomato"]},
            content_type="application/json",
        )
        title1 = json.loads(res1.data)["recipe"]["title"]
        # Second request excludes first result
        res2 = client.post(
            "/api/fridge-generate",
            json={"ingredients": ["spinach", "paneer", "tomato"], "exclude_titles": [title1]},
            content_type="application/json",
        )
        title2 = json.loads(res2.data)["recipe"]["title"]
        # If library has >1 candidate, titles should differ
        if len(FALLBACK_RECIPES) > 1:
            assert title2 != title1


# ═══════════════════════════════════════════════════════════════════════════════
# API — /api/search
# ═══════════════════════════════════════════════════════════════════════════════

class TestApiSearch:

    def test_search_returns_list(self, client, recipe):
        res = client.get("/api/search?q=palak")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert isinstance(data, list)

    def test_search_finds_by_title(self, client, recipe):
        res = client.get("/api/search?q=palak")
        data = json.loads(res.data)
        assert any("Palak Paneer" in r["title"] for r in data)

    def test_search_finds_by_ingredient(self, client, recipe):
        res = client.get("/api/search?q=spinach")
        data = json.loads(res.data)
        assert any("Palak Paneer" in r["title"] for r in data)

    def test_search_empty_query_returns_empty(self, client, recipe):
        res = client.get("/api/search?q=")
        data = json.loads(res.data)
        assert data == []

    def test_search_no_match_returns_empty(self, client, recipe):
        res = client.get("/api/search?q=zzznomatch")
        data = json.loads(res.data)
        assert data == []

    def test_search_missing_q_returns_empty(self, client, recipe):
        res = client.get("/api/search")
        data = json.loads(res.data)
        assert data == []


# ── import needed for exclude test ────────────────────────────────────────────
from recipe_generator import FALLBACK_RECIPES
