"""Generate index.html from data.json for the personal homepage."""

import html as _html
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "index.html")


CSS = r"""
:root {
  --bg: #fbfaf8;
  --card: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --accent: #0f766e;
  --accent-soft: #e6f2f0;
  --border: #e6e2da;
  --radius: 16px;
  --shadow: 0 10px 30px rgba(31, 41, 55, 0.06);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: var(--text);
  background: var(--bg);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { max-width: 1000px; margin: 0 auto; padding: 0 22px; }
nav {
  position: sticky; top: 0; z-index: 20;
  background: rgba(251, 250, 248, 0.88);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 60px; gap: 16px; }
.brand { font-weight: 700; letter-spacing: -0.2px; color: var(--text); }
.nav-links { display: flex; gap: 20px; flex-wrap: wrap; list-style: none; margin: 0; padding: 0; }
.nav-links a { color: var(--muted); font-size: 0.94rem; }
.nav-links a:hover { color: var(--accent); }
.hero { padding: 64px 0 34px; }
.hero-grid { display: grid; grid-template-columns: 1fr 220px; gap: 36px; align-items: center; }
.hero h1 { font-size: clamp(2.3rem, 6vw, 3.4rem); margin: 0 0 14px; letter-spacing: -1px; }
.hero .roles { color: var(--muted); margin-bottom: 18px; }
.hero .roles div { margin-bottom: 2px; }
.hero-contact { display: flex; flex-wrap: wrap; gap: 14px; font-size: 0.95rem; }
.photo-slot {
  width: 200px; height: 200px; border: 1px dashed var(--border); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: var(--muted); background: var(--card);
}
section { padding: 38px 0 8px; }
.section-head { margin-bottom: 22px; }
.section-head h2 { font-size: 1.65rem; margin: 0; letter-spacing: -0.3px; }
.section-head .lead { color: var(--muted); margin: 8px 0 0; max-width: 760px; }
.intro { font-size: 1.05rem; max-width: 860px; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.card {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 20px 22px; box-shadow: var(--shadow);
}
.card h3 { margin: 0 0 9px; font-size: 1.04rem; letter-spacing: -0.1px; }
.card p { margin: 0; color: var(--muted); font-size: 0.95rem; }
.research-grid { display: grid; grid-template-columns: 1fr; gap: 16px; }
.research-card { padding: 22px 24px; }
.research-card .tag { color: var(--accent); font-size: 0.82rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
.research-card h3 { font-size: 1.18rem; margin: 6px 0 10px; }
.research-card p { color: var(--muted); margin: 0 0 10px; }
.timeline { border-left: 2px solid var(--border); padding-left: 24px; }
.timeline-item { position: relative; margin-bottom: 22px; }
.timeline-item::before { content: ""; position: absolute; left: -31px; top: 7px; width: 10px; height: 10px; border-radius: 50%; background: var(--accent); }
.timeline-date { color: var(--muted); font-size: 0.86rem; }
.timeline-title { font-weight: 700; }
.timeline-sub { color: var(--accent); font-weight: 600; font-size: 0.94rem; }
.timeline-desc { color: var(--muted); font-size: 0.94rem; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
.contact-box {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 28px 26px; text-align: center; box-shadow: var(--shadow);
}
.contact-box h2 { margin-top: 0; }
.contact-box p { color: var(--muted); margin: 8px 0 0; }
footer { margin-top: 50px; padding: 28px 0 44px; text-align: center; color: var(--muted); border-top: 1px solid var(--border); }
@media (max-width: 760px) {
  .hero-grid { grid-template-columns: 1fr; }
  .cards { grid-template-columns: 1fr; }
  .two-col { grid-template-columns: 1fr; }
  .photo-slot { width: 140px; height: 140px; }
}
"""


def esc(value):
    return _html.escape("" if value is None else str(value), quote=True)


def load_data():
    with open(DATA_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def render(data):
    name = data.get("name", "Homepage")
    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    parts.append(f"<title>{esc(name)} · Personal Homepage</title>")
    parts.append(f'<meta name="description" content="Personal homepage of {esc(name)}.">')
    parts.append("<style>" + CSS + "</style>")
    parts.append("</head>")
    parts.append("<body>")

    parts.append('<nav><div class="wrap nav-inner">')
    parts.append(f'<span class="brand">{esc(name)}</span>')
    parts.append('<ul class="nav-links">')
    for label, anchor in [
        ("News", "news"),
        ("About", "about"),
        ("Research", "research"),
        ("Timeline", "timeline"),
        ("Life", "life"),
        ("Contact", "contact"),
    ]:
        parts.append(f'<li><a href="#{anchor}">{label}</a></li>')
    parts.append("</ul></div></nav>")

    parts.append('<header class="hero wrap"><div class="hero-grid"><div>')
    parts.append(f"<h1>{esc(name)}</h1>")
    parts.append('<div class="roles">')
    for role in data.get("roles", []):
        parts.append(f"<div>{esc(role)}</div>")
    parts.append("</div>")
    parts.append('<div class="hero-contact">')
    email = data.get("email", "")
    parts.append(f'<a href="mailto:{esc(email)}">{esc(email)}</a>')
    github = data.get("github") or ""
    website = data.get("website") or ""
    if github:
        parts.append(f'<a href="{esc(github)}" target="_blank" rel="noopener">GitHub</a>')
    if website:
        parts.append(f'<a href="{esc(website)}" target="_blank" rel="noopener">Homepage</a>')
    parts.append("</div></div>")

    photo = data.get("photo") or ""
    photo_path = os.path.join(BASE_DIR, photo) if photo else ""
    if photo and os.path.isfile(photo_path):
        parts.append(f'<img src="{esc(photo)}" alt="{esc(name)}" style="width:200px;height:200px;border-radius:50%;object-fit:cover;">')
    else:
        parts.append('<div class="photo-slot">Photo</div>')
    parts.append("</div></header>")

    parts.append("<main>")

    news = data.get("news", [])
    if news:
        parts.append('<section id="news" class="wrap"><div class="section-head"><h2>News</h2></div>')
        for item in news:
            parts.append(f'<div class="card"><p style="margin:0">{esc(item)}</p></div>')
        parts.append("</section>")

    parts.append('<section id="about" class="wrap"><div class="section-head"><h2>About</h2></div>')
    parts.append(f'<p class="intro">{esc(data.get("about", ""))}</p>')
    parts.append("</section>")

    research = data.get("research", [])
    if research:
        parts.append('<section id="research" class="wrap"><div class="section-head"><h2>Research</h2><p class="lead">A few problems I have been thinking about and working on.</p></div><div class="research-grid">')
        for item in research:
            parts.append('<div class="card research-card">')
            parts.append(f'<div class="tag">{esc(item.get("tag", ""))}</div>')
            parts.append(f"<h3>{esc(item.get('title', ''))}</h3>")
            for para in item.get("paragraphs", []):
                parts.append(f"<p>{esc(para)}</p>")
            parts.append("</div>")
        parts.append("</div></section>")

    aims = data.get("aims", [])
    if aims:
        parts.append('<section id="aims" class="wrap"><div class="section-head"><h2>What I Care About</h2></div><div class="cards">')
        for item in aims:
            parts.append('<div class="card">')
            parts.append(f"<h3>{esc(item.get('title', ''))}</h3>")
            parts.append(f"<p>{esc(item.get('text', ''))}</p>")
            parts.append("</div>")
        parts.append("</div></section>")

    timeline = data.get("timeline", [])
    if timeline:
        parts.append('<section id="timeline" class="wrap"><div class="section-head"><h2>Timeline</h2></div><div class="timeline">')
        for item in timeline:
            date = item.get("date", "")
            kind = item.get("type", "")
            label = f"{date} · {kind}" if date and kind else (date or kind)
            parts.append('<div class="timeline-item">')
            parts.append(f'<div class="timeline-date">{esc(label)}</div>')
            parts.append(f'<div class="timeline-title">{esc(item.get("title", ""))}</div>')
            sub = item.get("sub", "")
            if sub:
                parts.append(f'<div class="timeline-sub">{esc(sub)}</div>')
            desc = item.get("desc", "")
            if desc:
                parts.append(f'<div class="timeline-desc">{esc(desc)}</div>')
            parts.append("</div>")
        parts.append("</div></section>")

    publications = data.get("publications", [])
    awards = data.get("awards", [])
    if publications or awards:
        parts.append('<section id="publications" class="wrap"><div class="section-head"><h2>Publications &amp; Awards</h2></div><div class="two-col">')
        if publications:
            parts.append('<div class="card"><h3>Publications</h3>')
            for pub in publications:
                parts.append(f"<p>{esc(pub)}</p>")
            parts.append("</div>")
        if awards:
            parts.append('<div class="card"><h3>Awards</h3>')
            for award in awards:
                parts.append(f"<p>{esc(award)}</p>")
            parts.append("</div>")
        parts.append("</div></section>")

    parts.append('<section id="life" class="wrap"><div class="section-head"><h2>Beyond Research</h2><p class="lead">A little more about me.</p></div><div class="card">')
    parts.append(f"<h3>{esc(data.get('life_title', ''))}</h3>")
    parts.append(f'<p style="margin:0">{esc(data.get("life_text", ""))}</p>')
    parts.append("</div></section>")

    parts.append('<section id="contact" class="wrap"><div class="contact-box"><h2>Get in Touch</h2>')
    parts.append(f'<p>Interested in my work or just want to chat? Reach me at <a href="mailto:{esc(email)}">{esc(email)}</a>.</p>')
    parts.append("</div></section>")

    parts.append("</main>")
    parts.append(f"<footer>© 2026 {esc(name)}</footer>")
    parts.append("</body></html>")
    return "\n".join(parts)


def generate():
    data = load_data()
    html = render(data)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(html)
    return OUTPUT_PATH


if __name__ == "__main__":
    print("Generated:", generate())
