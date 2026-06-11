import os
import threading
import uuid
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from sqlalchemy import text

load_dotenv()

from extensions import db
from models import Recipe, UserProfile

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///family_fork.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Add image_url column to existing databases that predate this field
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE recipe ADD COLUMN image_url TEXT"))
            conn.commit()
        except Exception:
            pass


def food_image_url(title, cuisine_tag=""):
    from recipe_generator import recipe_image_url
    return recipe_image_url(title, cuisine_tag)


# ── helpers ───────────────────────────────────────────────────────────────────

def get_profile():
    return UserProfile.query.first()


def recent_recipe_titles(days=7):
    cutoff = datetime.utcnow() - timedelta(days=days)
    recipes = Recipe.query.filter(Recipe.generated_at >= cutoff).all()
    return [r.title for r in recipes]


def _save_recipe(data, source="on_demand"):
    title = data.get("title", "")
    cuisine = data.get("cuisine_tag", "")

    # Return existing record if this title is already in the cookbook
    existing = Recipe.query.filter_by(title=title).first()
    if existing:
        return existing

    image = data.get("image_url") or food_image_url(title, cuisine)
    recipe = Recipe(
        title=title,
        description=data.get("description", ""),
        cuisine_tag=cuisine,
        nutrition_tags=data.get("nutrition_tags", []),
        dietary_tags=data.get("dietary_tags", []),
        spice_level=data.get("spice_level", 1),
        servings=data.get("servings", 4),
        prep_time_min=data.get("prep_time_min", 15),
        cook_time_min=data.get("cook_time_min", 30),
        ingredients=data.get("ingredients", []),
        instructions=data.get("instructions", []),
        allergen_notes=data.get("allergen_notes", ""),
        image_url=image,
        source=source,
    )
    db.session.add(recipe)
    db.session.commit()
    return recipe


def generate_and_notify(source="on_demand"):
    from email_service import send_recipe_email
    from recipe_generator import generate_recipe

    profile = get_profile()
    if not profile:
        return None, "No profile configured"

    try:
        data = generate_recipe(profile, recent_recipe_titles())
        recipe = _save_recipe(data, source)
        if profile.email:
            base_url = os.getenv("BASE_URL", "http://localhost:5000")
            send_recipe_email(recipe.to_dict(), profile.email, base_url)
        return recipe, None
    except Exception as e:
        return None, str(e)


# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    profile = get_profile()
    if not profile:
        return redirect(url_for("profile"))

    today = Recipe.query.order_by(Recipe.generated_at.desc()).first()
    recent = Recipe.query.order_by(Recipe.generated_at.desc()).limit(8).all()
    # exclude today's recipe from the "this week" strip
    week = [r for r in recent if r.id != (today.id if today else None)][:4]

    return render_template("home.html", profile=profile, today=today, week=week)


@app.route("/cookbook")
def cookbook():
    profile = get_profile()
    q = request.args.get("q", "").strip().lower()
    cuisine_filter = request.args.getlist("cuisine")
    diet_filter = request.args.getlist("diet")
    nutrition_filter = request.args.getlist("nutrition")
    spice_max = request.args.get("spice_max", type=int)
    time_max = request.args.get("time_max", type=int)

    query = Recipe.query.order_by(Recipe.generated_at.desc())
    recipes = query.all()

    # text search
    if q:
        def matches(r):
            haystack = (r.title + " " + r.description + " " +
                        " ".join(i["name"] for i in (r.ingredients or []))).lower()
            return q in haystack
        recipes = [r for r in recipes if matches(r)]

    # tag filters
    if cuisine_filter:
        recipes = [r for r in recipes if r.cuisine_tag in cuisine_filter]
    if diet_filter:
        recipes = [r for r in recipes if any(d in (r.dietary_tags or []) for d in diet_filter)]
    if nutrition_filter:
        recipes = [r for r in recipes if any(n in (r.nutrition_tags or []) for n in nutrition_filter)]
    if spice_max:
        recipes = [r for r in recipes if r.spice_level <= spice_max]
    if time_max:
        recipes = [r for r in recipes if (r.prep_time_min + r.cook_time_min) <= time_max]

    # group by cuisine for the default browse view
    by_cuisine = {}
    if not q and not cuisine_filter and not diet_filter and not nutrition_filter:
        for r in recipes:
            by_cuisine.setdefault(r.cuisine_tag or "other", []).append(r)

    active_filters = cuisine_filter + diet_filter + nutrition_filter
    if spice_max and spice_max < 5:
        active_filters.append(f"Spice ≤ {spice_max}")
    if time_max:
        active_filters.append(f"≤ {time_max} min total")

    return render_template(
        "cookbook.html",
        profile=profile,
        recipes=recipes,
        by_cuisine=by_cuisine,
        q=q,
        active_filters=active_filters,
        cuisine_filter=cuisine_filter,
        diet_filter=diet_filter,
        nutrition_filter=nutrition_filter,
        spice_max=spice_max or 5,
        time_max=time_max or 120,
        total=Recipe.query.count(),
    )


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    profile = get_profile()
    return render_template("recipe_detail.html", recipe=recipe, profile=profile)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    p = get_profile()

    if request.method == "POST":
        dietary = request.form.getlist("dietary_restrictions")
        spice = int(request.form.get("spice_level", 3))
        num_people = int(request.form.get("num_people", 4))
        age_youngest = int(request.form.get("age_youngest", 5))
        age_oldest = int(request.form.get("age_oldest", 40))
        nutrition = request.form.getlist("nutrition_goals")
        cuisines = request.form.getlist("cuisines")
        email = request.form.get("email", "").strip()
        timezone = request.form.get("timezone", "America/New_York").strip()

        if p:
            p.dietary_restrictions = dietary
            p.spice_level = spice
            p.num_people = num_people
            p.age_youngest = age_youngest
            p.age_oldest = age_oldest
            p.nutrition_goals = nutrition
            p.cuisines = cuisines
            p.email = email
            p.timezone = timezone
        else:
            p = UserProfile(
                email=email,
                dietary_restrictions=dietary,
                spice_level=spice,
                num_people=num_people,
                age_youngest=age_youngest,
                age_oldest=age_oldest,
                nutrition_goals=nutrition,
                cuisines=cuisines,
                timezone=timezone,
            )
            db.session.add(p)

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("profile.html", profile=p)


@app.route("/fridge")
def fridge():
    profile = get_profile()
    return render_template("fridge.html", profile=profile)


# ── Background job store ──────────────────────────────────────────────────────

_jobs = {}  # job_id -> {status, recipe, error}


def _run_in_background(job_id, fn):
    def run():
        with app.app_context():
            try:
                result = fn()
                _jobs[job_id] = {"status": "done", **result}
            except Exception as e:
                _jobs[job_id] = {"status": "error", "error": str(e)}
    threading.Thread(target=run, daemon=True).start()


@app.route("/api/job/<job_id>")
def api_job_status(job_id):
    job = _jobs.get(job_id)
    if not job:
        return jsonify({"status": "pending"})
    return jsonify(job)


# ── API endpoints ─────────────────────────────────────────────────────────────

@app.route("/api/generate", methods=["POST"])
def api_generate():
    profile = get_profile()
    if not profile:
        return jsonify({"error": "No profile configured"}), 500

    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "pending"}

    def work():
        recipe, err = generate_and_notify(source="on_demand")
        if err:
            raise RuntimeError(err)
        return {"recipe": recipe.to_dict()}

    _run_in_background(job_id, work)
    return jsonify({"job_id": job_id})


@app.route("/api/fridge-generate", methods=["POST"])
def api_fridge_generate():
    from recipe_generator import generate_from_fridge

    data = request.get_json(silent=True) or {}
    ingredients = [i.strip() for i in data.get("ingredients", []) if i.strip()]
    if not ingredients:
        return jsonify({"error": "Please add at least one ingredient."}), 400

    cuisine        = data.get("cuisine") or None
    sauce          = data.get("sauce") or None
    exclude_titles = data.get("exclude_titles") or []
    profile = get_profile()

    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "pending"}

    def work():
        recipe_data = generate_from_fridge(
            ingredients, profile,
            cuisine=cuisine, sauce=sauce, exclude_titles=exclude_titles
        )
        fridge_match = recipe_data.get("fridge_match", [])
        recipe = _save_recipe(recipe_data, source="fridge")
        result = recipe.to_dict()
        result["fridge_match"] = fridge_match
        return {"recipe": result}

    _run_in_background(job_id, work)
    return jsonify({"job_id": job_id})


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify([])
    recipes = Recipe.query.order_by(Recipe.generated_at.desc()).all()

    def matches(r):
        haystack = (r.title + " " + r.description + " " +
                    " ".join(i["name"] for i in (r.ingredients or []))).lower()
        return q in haystack

    return jsonify([r.to_dict() for r in recipes if matches(r)][:20])


# ── Scheduled daily generation ────────────────────────────────────────────────

def setup_scheduler():
    from apscheduler.schedulers.background import BackgroundScheduler

    scheduler = BackgroundScheduler()

    def daily_job():
        with app.app_context():
            recipe, err = generate_and_notify(source="scheduled")
            if err:
                print(f"[Scheduler] Error: {err}")
            else:
                print(f"[Scheduler] Generated: {recipe.title}")

    scheduler.add_job(daily_job, "cron", hour=17, minute=0, id="daily_recipe")
    scheduler.start()
    return scheduler


# Only run scheduler in the main process (not in Werkzeug reloader subprocess)
if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    _scheduler = setup_scheduler()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=port)
