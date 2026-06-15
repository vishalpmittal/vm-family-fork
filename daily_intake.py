"""
Daily nutrition intake estimator.

Energy needs are computed with the Mifflin–St Jeor equation, the modern default
in clinical and sports-nutrition practice. Macro targets follow the US/Canada
Dietary Reference Intakes (AMDR ranges) and ISSN protein recommendations.
Micronutrient values are RDAs from the NIH Office of Dietary Supplements.

This is an educational reference — not medical advice. Real needs vary with
muscle mass, body composition, climate, pregnancy/lactation, and disease.
"""

from dataclasses import dataclass


ACTIVITY_FACTORS = {
    "sedentary":   (1.2,   "Desk job, little or no exercise"),
    "light":       (1.375, "Light exercise 1–3 days/week"),
    "moderate":    (1.55,  "Moderate exercise 3–5 days/week"),
    "active":      (1.725, "Hard exercise 6–7 days/week"),
    "very_active": (1.9,   "Athlete or physical job + training"),
}


PRESETS = [
    {"key": "avg_male",   "label": "Average adult male",   "sex": "male",   "age": 30, "height": 175, "weight": 75, "activity": "moderate"},
    {"key": "avg_female", "label": "Average adult female", "sex": "female", "age": 30, "height": 162, "weight": 65, "activity": "moderate"},
    {"key": "teen_male",  "label": "Teen male (16)",       "sex": "male",   "age": 16, "height": 172, "weight": 62, "activity": "active"},
    {"key": "teen_female","label": "Teen female (16)",     "sex": "female", "age": 16, "height": 162, "weight": 55, "activity": "active"},
    {"key": "senior_male","label": "Senior male (65)",     "sex": "male",   "age": 65, "height": 173, "weight": 78, "activity": "light"},
    {"key": "senior_female","label": "Senior female (65)", "sex": "female", "age": 65, "height": 160, "weight": 68, "activity": "light"},
]


@dataclass
class Macro:
    name: str
    grams: float
    kcal: float
    pct_of_calories: float
    color: str  # CSS variable to use for the bar


def _bmr_mifflin(sex: str, age: int, height_cm: float, weight_kg: float) -> float:
    """Mifflin–St Jeor resting energy expenditure (kcal/day)."""
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + (5 if sex == "male" else -161)


def _protein_grams(weight_kg: float, activity: str) -> float:
    """Protein recommendation per kg body weight, scaled by activity level."""
    g_per_kg = {
        "sedentary":   0.8,
        "light":       1.0,
        "moderate":    1.4,
        "active":      1.7,
        "very_active": 2.0,
    }.get(activity, 1.0)
    return weight_kg * g_per_kg


def _iron_rda(sex: str, age: int) -> int:
    if sex == "female" and 19 <= age <= 50:
        return 18
    if sex == "female" and 9 <= age <= 13:
        return 8
    if sex == "female" and 14 <= age <= 18:
        return 15
    return 8  # adult male, post-menopausal female


def _calcium_rda(age: int) -> int:
    if age <= 18:
        return 1300
    if age <= 50:
        return 1000
    return 1200


def _vit_d_iu(age: int) -> int:
    return 800 if age > 70 else 600


def _vit_c_rda(sex: str) -> int:
    return 90 if sex == "male" else 75


def _fiber_g(calories: float) -> float:
    """14 g per 1000 kcal (Institute of Medicine)."""
    return round(calories * 14 / 1000)


def _water_litres(sex: str, weight_kg: float) -> float:
    """Adequate Intake from NAS: 3.7 L men, 2.7 L women — capped by ~35 ml/kg
    so very small or very large bodies get a more sensible target."""
    base = 3.7 if sex == "male" else 2.7
    weight_based = weight_kg * 0.035
    return round(max(weight_based, base * 0.85), 1)


def _bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100
    return round(weight_kg / (h_m * h_m), 1)


def _bmi_category(bmi: float) -> tuple[str, str]:
    """Return (label, severity) where severity is one of: low, ok, warn, high."""
    if bmi < 18.5:
        return ("Underweight", "warn")
    if bmi < 25:
        return ("Healthy weight", "ok")
    if bmi < 30:
        return ("Overweight", "warn")
    if bmi < 35:
        return ("Obese (class I)", "high")
    if bmi < 40:
        return ("Obese (class II)", "high")
    return ("Obese (class III)", "high")


def _healthy_weight_range(height_cm: float) -> tuple[int, int]:
    """Weight range that puts BMI between 18.5 and 24.9."""
    h_m = height_cm / 100
    return (round(18.5 * h_m * h_m), round(24.9 * h_m * h_m))


def _fmt_kg(kg: float, unit: str) -> str:
    if unit == "lb":
        return f"{round(kg * 2.20462)} lb"
    return f"{round(kg)} kg"


def _fmt_kg_range(low_kg: float, high_kg: float, unit: str) -> str:
    if unit == "lb":
        return f"{round(low_kg * 2.20462)}–{round(high_kg * 2.20462)} lb"
    return f"{round(low_kg)}–{round(high_kg)} kg"


def _fmt_cm(cm: float, unit: str) -> str:
    if unit == "ft":
        total_in = cm / 2.54
        ft = int(total_in // 12)
        inches = round(total_in - ft * 12)
        return f"{ft}′{inches}″"
    return f"{round(cm)} cm"


def _devine_ideal_weight(sex: str, height_cm: float) -> int:
    """Devine (1974) formula — widely used in clinical drug dosing.
    Men:   50.0 kg + 2.3 kg per inch over 5 ft (152.4 cm)
    Women: 45.5 kg + 2.3 kg per inch over 5 ft
    """
    inches_over_5ft = max(0, (height_cm - 152.4) / 2.54)
    base = 50.0 if sex == "male" else 45.5
    return round(base + 2.3 * inches_over_5ft)


def _recommendations(*, sex, age, weight_kg, bmi, bmi_label, ideal_low, ideal_high,
                     tdee, protein_g, activity, weight_unit="kg") -> list[str]:
    """Generate plain-English, individualized bullets the user can act on."""
    bullets = []
    range_str = _fmt_kg_range(ideal_low, ideal_high, weight_unit)
    # Loss/gain pace expressed in the user's unit (0.5 kg/week ≈ 1 lb/week).
    pace_str = "1 lb/week" if weight_unit == "lb" else "0.5 kg/week"

    # Weight-status guidance
    if bmi < 18.5:
        bullets.append(
            f"BMI {bmi} is below the healthy range ({range_str}). "
            f"To reach the lower bound, aim for a ~300–500 kcal/day surplus over your "
            f"TDEE ({tdee} kcal). Calorie-dense additions: nut butters, paneer, "
            f"full-fat dairy, dried fruit, ghee."
        )
    elif bmi < 25:
        bullets.append(
            f"BMI {bmi} is in the healthy range ({range_str}). "
            f"Maintain ~{tdee} kcal/day and focus on food quality, not quantity."
        )
    elif bmi < 30:
        loss_target_kcal = tdee - 500
        gap_str = _fmt_kg(weight_kg - ideal_high, weight_unit)
        bullets.append(
            f"BMI {bmi} is above the healthy range ({range_str}) by ~{gap_str}. "
            f"For sustainable loss of ~{pace_str}, eat ~{loss_target_kcal} kcal/day "
            f"and keep protein at {protein_g} g to preserve muscle."
        )
    else:
        loss_target_kcal = max(tdee - 750, round(tdee * 0.7))
        bullets.append(
            f"BMI {bmi} ({bmi_label}). A ~750 kcal/day deficit (~{loss_target_kcal} kcal target) "
            f"with high protein ({protein_g} g) and a walk daily is a safe starting point. "
            f"Consider a check-in with a clinician for any underlying drivers."
        )

    # Protein practicality
    eggs = round(protein_g / 6)
    chicken_g = round(protein_g / 0.31)
    dal_servings = round(protein_g / 18)
    bullets.append(
        f"Hit your {protein_g} g protein target with combos like: {eggs} eggs + {dal_servings} "
        f"bowls of cooked dal, or ~{chicken_g} g chicken breast + 200 g paneer/tofu, "
        f"or 2 scoops whey + dal + nuts."
    )

    # Fiber/whole foods
    bullets.append(
        "Anchor each meal in a whole grain (millet, oats, brown rice) and a pulse or dal — "
        "this single rule covers fiber, complex carbs, and most of the iron/magnesium gaps."
    )

    # Activity-specific note
    if activity in ("active", "very_active"):
        bullets.append(
            "Around training: 20–40 g protein + carbs within 1–2 hours of finishing. "
            "Sodium and water intake should rise on long or hot sessions."
        )
    elif activity == "sedentary":
        bullets.append(
            "Adding even a 30-minute daily walk shifts you to 'light' activity (+10 % TDEE) "
            "and meaningfully improves insulin sensitivity."
        )

    # Age-specific note
    if age >= 65:
        bullets.append(
            "After 60, protein needs trend up (~1.2 g/kg) to fight sarcopenia. "
            "Vitamin D + calcium + resistance training together protect bone density."
        )
    elif age <= 18:
        bullets.append(
            "Growing bodies need higher calcium (1300 mg) and don't benefit from calorie "
            "restriction — focus on food quality, not deficits."
        )

    return bullets


def compute_intake(sex: str, age: int, height_cm: float, weight_kg: float, activity: str,
                   *, height_unit: str = "cm", weight_unit: str = "kg") -> dict:
    """Return a fully-populated intake dictionary ready for the template."""
    activity = activity if activity in ACTIVITY_FACTORS else "moderate"
    height_unit = height_unit if height_unit in ("cm", "ft") else "cm"
    weight_unit = weight_unit if weight_unit in ("kg", "lb") else "kg"
    factor, factor_blurb = ACTIVITY_FACTORS[activity]

    bmr = _bmr_mifflin(sex, age, height_cm, weight_kg)
    tdee = bmr * factor

    protein_g = _protein_grams(weight_kg, activity)
    protein_kcal = protein_g * 4

    # Fat at 30% of calories (mid-AMDR), carbs fill the remainder.
    fat_kcal = tdee * 0.30
    fat_g = fat_kcal / 9
    carbs_kcal = tdee - protein_kcal - fat_kcal
    carbs_g = max(carbs_kcal, 0) / 4

    macros = [
        Macro("Protein", round(protein_g),       round(protein_kcal),
              round(protein_kcal / tdee * 100, 1), "var(--green)"),
        Macro("Carbs",   round(max(carbs_g, 0)), round(max(carbs_kcal, 0)),
              round(max(carbs_kcal, 0) / tdee * 100, 1), "var(--orange)"),
        Macro("Fat",     round(fat_g),           round(fat_kcal),
              round(fat_kcal / tdee * 100, 1), "var(--yellow)"),
    ]

    fiber_g = _fiber_g(tdee)
    water_l = _water_litres(sex, weight_kg)

    micros = [
        {"name": "Iron",       "amount": _iron_rda(sex, age), "unit": "mg",
         "why": "Oxygen transport. Plant iron pairs well with vitamin C."},
        {"name": "Calcium",    "amount": _calcium_rda(age),   "unit": "mg",
         "why": "Bone density, muscle contraction."},
        {"name": "Vitamin D",  "amount": _vit_d_iu(age),      "unit": "IU",
         "why": "Calcium absorption. Sunlight is the cheapest source."},
        {"name": "Vitamin C",  "amount": _vit_c_rda(sex),     "unit": "mg",
         "why": "Antioxidant, collagen, iron absorption."},
        {"name": "Vitamin B12","amount": 2.4,                 "unit": "µg",
         "why": "Nerve & red-cell formation. Vegans need a supplement."},
        {"name": "Magnesium",  "amount": 420 if sex == "male" else 320, "unit": "mg",
         "why": "Muscle, nerve, sleep quality."},
        {"name": "Potassium",  "amount": 3400 if sex == "male" else 2600, "unit": "mg",
         "why": "Blood pressure, fluid balance."},
        {"name": "Zinc",       "amount": 11 if sex == "male" else 8, "unit": "mg",
         "why": "Immune function, wound healing."},
        {"name": "Sodium (limit)", "amount": 2300, "unit": "mg",
         "why": "Upper limit — most adults exceed this."},
        {"name": "Added sugar (limit)", "amount": 50 if sex == "male" else 25, "unit": "g",
         "why": "AHA cap. Natural sugars in fruit don't count."},
    ]

    bmi = _bmi(weight_kg, height_cm)
    bmi_label, bmi_severity = _bmi_category(bmi)
    ideal_low, ideal_high = _healthy_weight_range(height_cm)
    devine = _devine_ideal_weight(sex, height_cm)
    # Marker position on a 15–40 BMI scale, clamped to 0–100 for CSS width.
    bmi_marker_pct = max(0, min(100, (bmi - 15) / (40 - 15) * 100))

    recommendations = _recommendations(
        sex=sex, age=age, weight_kg=weight_kg, bmi=bmi, bmi_label=bmi_label,
        ideal_low=ideal_low, ideal_high=ideal_high, tdee=round(tdee),
        protein_g=round(protein_g), activity=activity, weight_unit=weight_unit,
    )

    return {
        "inputs": {
            "sex": sex, "age": age, "height_cm": height_cm,
            "weight_kg": weight_kg, "activity": activity,
            "activity_blurb": factor_blurb, "activity_factor": factor,
        },
        "energy": {
            "bmr": round(bmr),
            "tdee": round(tdee),
            "calories": round(tdee),
        },
        "body": {
            "bmi": bmi,
            "bmi_label": bmi_label,
            "bmi_severity": bmi_severity,
            "bmi_marker_pct": round(bmi_marker_pct, 1),
            "ideal_low": ideal_low,
            "ideal_high": ideal_high,
            "devine": devine,
            "delta_to_range": (
                round(ideal_low - weight_kg) if weight_kg < ideal_low
                else round(weight_kg - ideal_high) if weight_kg > ideal_high
                else 0
            ),
            # Pre-formatted display strings in the user's chosen units.
            "weight_display":     _fmt_kg(weight_kg, weight_unit),
            "height_display":     _fmt_cm(height_cm, height_unit),
            "ideal_range_display": _fmt_kg_range(ideal_low, ideal_high, weight_unit),
            "devine_display":     _fmt_kg(devine, weight_unit),
            "delta_display": _fmt_kg(
                abs(ideal_low - weight_kg) if weight_kg < ideal_low
                else abs(weight_kg - ideal_high) if weight_kg > ideal_high
                else 0,
                weight_unit,
            ),
        },
        "macros": macros,
        "fiber_g": fiber_g,
        "water_l": water_l,
        "micros": micros,
        "recommendations": recommendations,
    }
