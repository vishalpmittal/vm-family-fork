import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_recipe_email(recipe, recipient_email, base_url="http://localhost:5000"):
    host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    port = int(os.getenv("EMAIL_PORT", 587))
    user = os.getenv("EMAIL_USER", "")
    password = os.getenv("EMAIL_PASSWORD", "")

    if not user or not password:
        print(f"[Email] Skipped — EMAIL_USER/EMAIL_PASSWORD not set. Would have sent '{recipe['title']}' to {recipient_email}")
        return False

    subject = f"🥦 Tonight's Recipe: {recipe['title']}"
    recipe_url = f"{base_url}/recipe/{recipe['id']}"

    cuisine_emoji = {"indian": "🍛", "italian": "🍝", "mexican": "🌮", "mediterranean": "🫒"}.get(
        recipe.get("cuisine_tag", ""), "🍽"
    )

    ingredients_html = "".join(
        f"<li><strong>{i['quantity']} {i['unit']}</strong> {i['name']}</li>"
        for i in (recipe.get("ingredients") or [])
    )
    instructions_html = "".join(
        f"<li style='margin-bottom:8px'>{step}</li>"
        for step in (recipe.get("instructions") or [])
    )
    nutrition_badges = " ".join(
        f"<span style='background:#fff8d6;color:#8a6200;padding:3px 8px;border-radius:99px;font-size:12px;font-weight:600;margin-right:4px'>{t}</span>"
        for t in (recipe.get("nutrition_tags") or [])
    )
    allergen = (
        f"<div style='background:#fff8d6;border-left:4px solid #e86d10;padding:12px 16px;border-radius:6px;margin:16px 0;font-size:13px;color:#7a3800'>"
        f"<strong>⚠ Age Note:</strong> {recipe['allergen_notes']}</div>"
        if recipe.get("allergen_notes")
        else ""
    )

    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#fdf6ec;margin:0;padding:0">
  <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 18px rgba(60,20,0,0.13)">
    <div style="background:linear-gradient(135deg,#7a2200,#c83800,#e86d10,#3a8c1e);padding:32px;color:#fff;text-align:center">
      <div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#f5c842;margin-bottom:8px">Tonight's Recipe</div>
      <h1 style="font-size:26px;font-weight:800;margin:0 0 8px">{cuisine_emoji} {recipe['title']}</h1>
      <p style="font-size:14px;color:#fde0c0;margin:0">{recipe.get('description','')}</p>
    </div>
    <div style="padding:24px">
      <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap">{nutrition_badges}</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px;text-align:center">
        <div style="background:#fdf6ec;border:1px solid #f0d9b8;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#c4a882;font-weight:600;text-transform:uppercase">Prep</div>
          <div style="font-size:16px;font-weight:800">{recipe.get('prep_time_min',0)} <span style="font-size:11px;color:#c4a882">min</span></div>
        </div>
        <div style="background:#fdf6ec;border:1px solid #f0d9b8;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#c4a882;font-weight:600;text-transform:uppercase">Cook</div>
          <div style="font-size:16px;font-weight:800">{recipe.get('cook_time_min',0)} <span style="font-size:11px;color:#c4a882">min</span></div>
        </div>
        <div style="background:#fdf6ec;border:1px solid #f0d9b8;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#c4a882;font-weight:600;text-transform:uppercase">Serves</div>
          <div style="font-size:16px;font-weight:800">{recipe.get('servings',4)}</div>
        </div>
        <div style="background:#fdf6ec;border:1px solid #f0d9b8;border-radius:8px;padding:12px">
          <div style="font-size:10px;color:#c4a882;font-weight:600;text-transform:uppercase">Spice</div>
          <div style="font-size:16px;font-weight:800">{recipe.get('spice_level',1)}/5</div>
        </div>
      </div>
      {allergen}
      <h3 style="color:#e86d10;font-size:15px;border-bottom:2px solid #fff3e6;padding-bottom:8px;margin-bottom:12px">Ingredients</h3>
      <ul style="padding-left:20px;font-size:13px;line-height:2;color:#2a1500">{ingredients_html}</ul>
      <h3 style="color:#e86d10;font-size:15px;border-bottom:2px solid #fff3e6;padding-bottom:8px;margin:20px 0 12px">Instructions</h3>
      <ol style="padding-left:20px;font-size:13px;color:#2a1500">{instructions_html}</ol>
      <div style="text-align:center;margin-top:24px">
        <a href="{recipe_url}" style="background:#e86d10;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px">View Full Recipe →</a>
      </div>
    </div>
    <div style="background:#fdf6ec;text-align:center;padding:16px;font-size:11px;color:#c4a882;border-top:1px solid #f0d9b8">
      Family Fork · Auto-generated daily at 5 PM
    </div>
  </div>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = recipient_email
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(user, password)
            server.sendmail(user, recipient_email, msg.as_string())
        print(f"[Email] Sent '{recipe['title']}' to {recipient_email}")
        return True
    except Exception as e:
        print(f"[Email] Failed: {e}")
        return False
