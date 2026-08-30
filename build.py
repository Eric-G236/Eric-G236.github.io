"""Generate index.html from data.json.

You normally do not need to run this file directly; the editor calls it after
every save. But you can also run:  py build.py
"""

import html as _html
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "index.html")


CSS = r"""
:root {
  --bg: #fafaf8;
  --text: #1a1a1a;
  --muted: #6b7280;
  --accent: #2563eb;
  --accent-soft: #eef2ff;
  --border: #e5e7eb;
  --card: #ffffff;
  --radius: 12px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
.container { max-width: 960px; margin: 0 auto; padding: 0 20px; }
nav {
  position: sticky; top: 0; z-index: 10;
  background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 58px; gap: 16px; }
.nav-brand { font-weight: 700; color: var(--text); }
.nav-links { display: flex; gap: 18px; list-style: none; margin: 0; padding: 0; flex-wrap: wrap; }
.nav-links a { color: var(--muted); font-size: 0.92rem; }
.nav-links a:hover { color: var(--accent); }
.hero { padding: 54px 0 26px; }
.hero-grid { display: grid; grid-template-columns: 1fr auto; gap: 32px; align-items: center; }
.hero-name { font-size: 2.25rem; margin: 0 0 12px; letter-spacing: -0.4px; }
.role { color: var(--muted); margin-bottom: 3px; }
.hero-contact { color: var(--accent); margin: 14px 0 8px; font-weight: 500; }
.hero-socials { display: flex; gap: 12px; flex-wrap: wrap; }
.photo-placeholder {
  width: 160px; height: 160px; border: 1px dashed var(--border); border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: var(--muted); font-size: 0.9rem; background: var(--card);
}
section { padding: 32px 0 8px; }
.section-title { margin-bottom: 16px; }
.section-title h2 { margin: 0; font-size: 1.35rem; letter-spacing: -0.2px; }
.bio-text { margin: 0 0 12px; }
.news-table { width: 100%; border-collapse: collapse; }
.news-table td { padding: 8px 0; vertical-align: top; border-bottom: 1px solid var(--border); }
.news-table tr:last-child td { border-bottom: none; }
.news-table td:first-child { white-space: nowrap; font-weight: 700; color: var(--accent); padding-right: 18px; }
.item {
  background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 18px 20px; margin-bottom: 14px;
}
.item-head { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 4px; }
.item-title { font-weight: 700; }
.item-date { color: var(--muted); font-size: 0.88rem; white-space: nowrap; }
.item-sub { color: var(--accent); font-weight: 600; font-size: 0.92rem; }
.item-where { color: var(--muted); font-size: 0.9rem; }
.item ul { margin: 8px 0 0; padding-left: 20px; }
.item li { margin-bottom: 5px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.chip { background: var(--accent-soft); color: var(--accent); padding: 4px 11px; border-radius: 999px; font-size: 0.86rem; font-weight: 600; }
.pub { margin-bottom: 18px; }
.pub-title { font-weight: 700; }
.pub-meta { color: var(--muted); font-size: 0.9rem; }
footer { margin-top: 36px; padding: 24px 0 40px; text-align: center; color: var(--muted); border-top: 1px solid var(--border); }
@media (max-width: 680px) {
  .hero-grid { grid-template-columns: 1fr; }
  .item-head { flex-direction: column; gap: 2px; }
  .nav-inner { height: auto; padding: 12px 0; flex-direction: column; align-items: flex-start; }
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
    parts.append(f"<title>{esc(name)}</title>")
    parts.append(f'<meta name="description" content="Personal homepage of {esc(name)}.">')
    parts.append("<style>" + CSS + "</style>")
    parts.append("</head>")
    parts.append("<body>")

    parts.append('<nav><div class="container nav-inner">')
    parts.append(f'<a href="#top" class="nav-brand">{esc(name)}</a>')
    parts.append('<ul class="nav-links">')
    for label, anchor in [
        ("About", "about"),
        ("Research", "research"),
        ("Education", "education"),
        ("Projects", "projects"),
        ("Experience", "experience"),
        ("Awards", "awards"),
        ("Publications", "publications"),
        ("Skills", "skills"),
    ]:
        parts.append(f'<li><a href="#{anchor}">{label}</a></li>')
    parts.append("</ul></div></nav>")

    parts.append('<main id="top">')
    parts.append('<section class="hero container"><div class="hero-grid"><div class="hero-content">')
    parts.append(f'<h1 class="hero-name">{esc(name)}</h1>')
    for role in data.get("roles", []):
        parts.append(f'<div class="role">{esc(role)}</div>')
    email = data.get("email", "")
    parts.append(f'<div class="hero-contact"><a href="mailto:{esc(email)}">{esc(email)}</a></div>')
    parts.append('<div class="hero-socials">')
    github = data.get("github") or ""
    website = data.get("website") or ""
    if github:
        parts.append(f'<a href="{esc(github)}" target="_blank" rel="noopener">GitHub</a>')
    if website:
        parts.append(f'<a href="{esc(website)}" target="_blank" rel="noopener">Personal Website</a>')
    parts.append("</div></div>")

    parts.append('<div class="hero-image"><div class="photo-placeholder">Photo</div></div>')
    parts.append("</div></div></section>")

    parts.append('<section id="about" class="container"><div class="section-title"><h2>About</h2></div>')
    parts.append(f'<p class="bio-text">{esc(data.get("about", ""))}</p>')
    parts.append("</section>")

    parts.append('<section id="research" class="container"><div class="section-title"><h2>Research Interests</h2></div>')
    interests = data.get("interests", [])
    if interests:
        parts.append("<ul>")
        for interest in interests:
            parts.append(f"<li>{esc(interest)}</li>")
        parts.append("</ul>")
    parts.append("</section>")

    parts.append('<section id="education" class="container"><div class="section-title"><h2>Education</h2></div>')
    for item in data.get("education", []):
        parts.append('<div class="item"><div class="item-head">')
        parts.append(f'<span class="item-title">{esc(item.get("title", ""))}</span>')
        parts.append(f'<span class="item-date">{esc(item.get("date", ""))}</span>')
        parts.append("</div>")
        parts.append(f'<div class="item-sub">{esc(item.get("sub", ""))}</div>')
        parts.append(f'<div class="item-where">{esc(item.get("where", ""))}</div>')
        parts.append("</div>")
    parts.append("</section>")

    parts.append('<section id="projects" class="container"><div class="section-title"><h2>Research Projects</h2></div>')
    for item in data.get("projects", []):
        parts.append('<div class="item"><div class="item-title">')
        parts.append(esc(item.get("title", "")))
        parts.append("</div><ul>")
        for bullet in item.get("bullets", []):
            parts.append(f"<li>{esc(bullet)}</li>")
        parts.append("</ul></div>")
    parts.append("</section>")

    parts.append('<section id="experience" class="container"><div class="section-title"><h2>Experience</h2></div>')
    for item in data.get("experience", []):
        parts.append('<div class="item"><div class="item-head">')
        parts.append(f'<span class="item-title">{esc(item.get("title", ""))}</span>')
        parts.append(f'<span class="item-date">{esc(item.get("date", ""))}</span>')
        parts.append("</div>")
        parts.append(f'<div class="item-sub">{esc(item.get("role", ""))}</div><ul>')
        for bullet in item.get("bullets", []):
            parts.append(f"<li>{esc(bullet)}</li>")
        parts.append("</ul></div>")
    parts.append("</section>")

    parts.append('<section id="awards" class="container"><div class="section-title"><h2>Awards &amp; Honors</h2></div><ul>')
    for award in data.get("awards", []):
        parts.append(f"<li>{esc(award)}</li>")
    parts.append("</ul></section>")

    parts.append('<section id="publications" class="container"><div class="section-title"><h2>Publications</h2></div>')
    for pub in data.get("publications", []):
        parts.append(f'<div class="pub"><div class="pub-title">{esc(pub)}</div></div>')
    parts.append("</section>")

    parts.append('<section id="skills" class="container"><div class="section-title"><h2>Skills</h2></div>')
    for skill in data.get("skills", []):
        parts.append(f'<div style="margin-bottom:14px"><strong>{esc(skill.get("name", ""))}</strong><div class="chips">')
        for item in skill.get("items", []):
            parts.append(f'<span class="chip">{esc(item)}</span>')
        parts.append("</div></div>")
    parts.append("</section>")

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
    generated = generate()
    print("Generated:", generated)
