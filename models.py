from datetime import datetime
from extensions import db


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, default="")
    dietary_restrictions = db.Column(db.JSON, default=list)
    spice_level = db.Column(db.Integer, default=3)
    num_people = db.Column(db.Integer, default=4)
    age_youngest = db.Column(db.Integer, default=5)
    age_oldest = db.Column(db.Integer, default=40)
    nutrition_goals = db.Column(db.JSON, default=list)
    cuisines = db.Column(db.JSON, default=list)
    timezone = db.Column(db.String(50), default="America/New_York")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "dietary_restrictions": self.dietary_restrictions or [],
            "spice_level": self.spice_level,
            "num_people": self.num_people,
            "age_youngest": self.age_youngest,
            "age_oldest": self.age_oldest,
            "nutrition_goals": self.nutrition_goals or [],
            "cuisines": self.cuisines or [],
            "timezone": self.timezone,
        }


class Recipe(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    cuisine_tag = db.Column(db.String(50), default="")
    nutrition_tags = db.Column(db.JSON, default=list)
    dietary_tags = db.Column(db.JSON, default=list)
    spice_level = db.Column(db.Integer, default=1)
    servings = db.Column(db.Integer, default=4)
    prep_time_min = db.Column(db.Integer, default=15)
    cook_time_min = db.Column(db.Integer, default=30)
    ingredients = db.Column(db.JSON, default=list)   # [{name, quantity, unit}]
    instructions = db.Column(db.JSON, default=list)  # ["Step 1...", ...]
    allergen_notes = db.Column(db.Text, default="")
    image_url = db.Column(db.String(500), nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(20), default="on_demand")  # 'scheduled' | 'on_demand'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "cuisine_tag": self.cuisine_tag,
            "nutrition_tags": self.nutrition_tags or [],
            "dietary_tags": self.dietary_tags or [],
            "spice_level": self.spice_level,
            "servings": self.servings,
            "prep_time_min": self.prep_time_min,
            "cook_time_min": self.cook_time_min,
            "ingredients": self.ingredients or [],
            "instructions": self.instructions or [],
            "allergen_notes": self.allergen_notes,
            "image_url": self.image_url or "",
            "generated_at": self.generated_at.strftime("%b %d, %Y") if self.generated_at else "",
            "source": self.source,
        }
