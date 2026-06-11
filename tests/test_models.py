"""Tests for SQLAlchemy models — UserProfile and Recipe."""
import pytest
from datetime import datetime

from app import app as flask_app
from extensions import db
from models import Recipe, UserProfile


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


# ═══════════════════════════════════════════════════════════════════════════════
# UserProfile MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class TestUserProfileModel:

    def test_create_profile_with_defaults(self, app):
        with app.app_context():
            p = UserProfile(email="test@example.com")
            db.session.add(p)
            db.session.commit()
            saved = UserProfile.query.first()
            assert saved.email == "test@example.com"
            assert saved.spice_level == 3
            assert saved.num_people == 4

    def test_create_profile_full(self, app):
        with app.app_context():
            p = UserProfile(
                email="hello@example.com",
                dietary_restrictions=["vegetarian", "diabetic-friendly"],
                spice_level=2,
                num_people=3,
                age_youngest=6,
                age_oldest=45,
                nutrition_goals=["protein-rich", "balanced"],
                cuisines=["indian", "mediterranean"],
                timezone="America/Chicago",
            )
            db.session.add(p)
            db.session.commit()
            saved = UserProfile.query.first()
            assert saved.dietary_restrictions == ["vegetarian", "diabetic-friendly"]
            assert saved.cuisines == ["indian", "mediterranean"]
            assert saved.timezone == "America/Chicago"

    def test_to_dict_returns_all_keys(self, app):
        with app.app_context():
            p = UserProfile(email="a@b.com")
            db.session.add(p)
            db.session.commit()
            d = p.to_dict()
            for key in ["id", "email", "dietary_restrictions", "spice_level",
                        "num_people", "age_youngest", "age_oldest",
                        "nutrition_goals", "cuisines", "timezone"]:
                assert key in d, f"Key '{key}' missing from UserProfile.to_dict()"

    def test_to_dict_empty_json_fields_return_lists(self, app):
        with app.app_context():
            p = UserProfile(email="a@b.com")
            db.session.add(p)
            db.session.commit()
            d = p.to_dict()
            assert isinstance(d["dietary_restrictions"], list)
            assert isinstance(d["nutrition_goals"], list)
            assert isinstance(d["cuisines"], list)

    def test_profile_update(self, app):
        with app.app_context():
            p = UserProfile(email="old@example.com", spice_level=1)
            db.session.add(p)
            db.session.commit()
            p.email = "new@example.com"
            p.spice_level = 4
            db.session.commit()
            saved = UserProfile.query.first()
            assert saved.email == "new@example.com"
            assert saved.spice_level == 4


# ═══════════════════════════════════════════════════════════════════════════════
# Recipe MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class TestRecipeModel:

    def _sample_recipe(self, **kwargs):
        defaults = dict(
            title="Test Palak Paneer",
            description="A test recipe",
            cuisine_tag="indian",
            nutrition_tags=["protein-rich"],
            dietary_tags=["vegetarian"],
            spice_level=2,
            servings=4,
            prep_time_min=10,
            cook_time_min=25,
            ingredients=[{"name": "Spinach", "quantity": "2", "unit": "cups"}],
            instructions=["Step 1", "Step 2"],
            allergen_notes="",
            image_url="/static/images/palak_paneer.jpg",
            source="on_demand",
        )
        defaults.update(kwargs)
        return Recipe(**defaults)

    def test_create_recipe(self, app):
        with app.app_context():
            r = self._sample_recipe()
            db.session.add(r)
            db.session.commit()
            saved = Recipe.query.first()
            assert saved.title == "Test Palak Paneer"
            assert saved.cuisine_tag == "indian"

    def test_to_dict_returns_all_keys(self, app):
        with app.app_context():
            r = self._sample_recipe()
            db.session.add(r)
            db.session.commit()
            d = r.to_dict()
            for key in ["id", "title", "description", "cuisine_tag", "nutrition_tags",
                        "dietary_tags", "spice_level", "servings", "prep_time_min",
                        "cook_time_min", "ingredients", "instructions",
                        "allergen_notes", "image_url", "generated_at", "source"]:
                assert key in d, f"Key '{key}' missing from Recipe.to_dict()"

    def test_to_dict_json_fields_are_lists(self, app):
        with app.app_context():
            r = self._sample_recipe()
            db.session.add(r)
            db.session.commit()
            d = r.to_dict()
            assert isinstance(d["nutrition_tags"], list)
            assert isinstance(d["dietary_tags"], list)
            assert isinstance(d["ingredients"], list)
            assert isinstance(d["instructions"], list)

    def test_to_dict_null_image_returns_empty_string(self, app):
        with app.app_context():
            r = self._sample_recipe(image_url=None)
            db.session.add(r)
            db.session.commit()
            assert r.to_dict()["image_url"] == ""

    def test_to_dict_generated_at_is_formatted_string(self, app):
        with app.app_context():
            r = self._sample_recipe()
            db.session.add(r)
            db.session.commit()
            d = r.to_dict()
            assert isinstance(d["generated_at"], str)
            assert len(d["generated_at"]) > 0

    def test_source_defaults_to_on_demand(self, app):
        with app.app_context():
            r = Recipe(title="Quick Recipe")
            db.session.add(r)
            db.session.commit()
            assert r.source == "on_demand"

    def test_source_can_be_fridge(self, app):
        with app.app_context():
            r = self._sample_recipe(source="fridge")
            db.session.add(r)
            db.session.commit()
            assert Recipe.query.first().source == "fridge"

    def test_multiple_recipes_stored(self, app):
        with app.app_context():
            db.session.add(self._sample_recipe(title="Recipe One"))
            db.session.add(self._sample_recipe(title="Recipe Two"))
            db.session.commit()
            assert Recipe.query.count() == 2
