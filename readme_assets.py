"""Generator gambar pendukung README: judul section, kartu proyek, footer (folder assets/).

Ubah SECTIONS / PROJECTS lalu jalankan: python readme_assets.py
"""
import random
import textwrap
from html import escape
from pathlib import Path

from pixelart import CAT_COLORS, CAT_POSES, pixels, sprite, width

SECTIONS = {"about": "ABOUT", "stack": "TECH STACK", "projects": "FEATURED PROJECTS", "activity": "ACTIVITY"}
# (repo, deskripsi, stack, ada demo live?)
PROJECTS = [
    ("portfolio-v2", "Personal portfolio with an animated UI and a secure contact form.",
     ["React", "Vite", "Framer Motion", "Express"], True),
    ("task-tracker", "Task management app with status filtering, a statistics endpoint, and a Docker Compose setup.",
     ["FastAPI", "React", "PostgreSQL", "Docker"], False),
    ("skybarbershop", "Barbershop booking system with queue scheduling, a service catalog, and an admin dashboard.",
     ["Laravel", "PHP"], False),
    ("SneaksAvenue", "E-commerce platform for international sneaker brands, with authentication and product management.",
     ["Laravel 11", "PHP"], False),
]

OUT = Path("assets")
ACCENT = "#8957e5"  # ungu tengah: tetap terbaca di tema terang maupun gelap
LEVELS = ["#161b22", "#3c1e70", "#553098", "#8957e5", "#bc8cff"]
UI_FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
random.seed(11)


def pixel_text(text, x, y, px, fill):
    return "".join(f'<rect x="{x + c * px}" y="{y + r * px}" width="{px - 1}" height="{px - 1}" fill="{fill}"/>'
                    for c, r, _ in pixels(text))


def header(title):
    """Judul section: teks pixel + deretan sel kontribusi yang memudar & berkilau pelan."""
    w, h, px = 900, 32, 4
    text_x = 18
    cells_x = text_x + width(title) * px + 18
    count = (w - cells_x) // 10
    cells = "".join(f'<rect x="{cells_x + i * 10}" y="13" width="6" height="6" rx="1" fill="{ACCENT}" '
                    f'fill-opacity="{0.6 * (1 - i / count) ** 1.3 + 0.06:.2f}" style="animation-delay:{i * 0.04:.2f}s"/>'
                    for i in range(count))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title.title())}">
<style>g rect{{animation:wave 6s ease-in-out infinite}}@keyframes wave{{4%{{fill-opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect x="0" y="2" width="8" height="28" rx="1" fill="{ACCENT}"/>
{pixel_text(title, text_x, 2, px, ACCENT)}
<g>{cells}</g>
</svg>
"""


def project_card(repo, description, stack, live):
    """Kartu proyek gelap senada banner; seluruh kartu ditautkan ke repo di README."""
    w, h = 420, 170
    icon = "".join(f'<rect x="{22 + c * 8}" y="{22 + r * 8}" width="6" height="6" rx="1" fill="{random.choice(LEVELS[1:])}"'
                   + (' class="tw"' if random.random() < 0.3 else "") + "/>" for r in range(3) for c in range(3))
    lines = textwrap.wrap(description, 52)[:3]
    desc = "".join(f'<text class="d" x="22" y="{82 + k * 19}">{escape(line)}</text>' for k, line in enumerate(lines))
    chips, x = [], 22
    for tech in stack:
        chip_w = len(tech) * 6.4 + 18
        chips.append(f'<rect x="{x}" y="{h - 40}" width="{chip_w:.0f}" height="22" rx="11" fill="#161b22" stroke="#30363d"/>'
                     f'<text class="c" x="{x + chip_w / 2:.0f}" y="{h - 25}" text-anchor="middle">{escape(tech)}</text>')
        x += chip_w + 8
    badge = (f'<circle cx="{w - 58}" cy="37" r="4" fill="#3fb950"/><text class="l" x="{w - 22}" y="41" text-anchor="end">Live</text>'
             if live else "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(repo)}: {escape(description)}">
<style>
.t{{font:600 19px {UI_FONT};fill:#d2a8ff}}
.d{{font:14px {UI_FONT};fill:#8b949e}}
.c{{font:12px {UI_FONT};fill:#c9d1d9}}
.l{{font:600 12px {UI_FONT};fill:#3fb950}}
.tw{{animation:tw 4s ease-in-out infinite}}
.tw:nth-of-type(2n){{animation-delay:-2s}}
@keyframes tw{{50%{{fill:#bc8cff}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>
{icon}
<text class="t" x="58" y="43">{escape(repo)}</text>
{badge}
{desc}
{"".join(chips)}
</svg>
"""


def footer():
    """Penutup halaman: kucing dari banner tidur di samping ucapan terima kasih."""
    w, h, px, text_px = 900, 96, 3, 4
    text = "THANKS FOR VISITING"
    cat_w = len(CAT_POSES["sleep"][0]) * px
    group_w = cat_w + 24 + width(text) * text_px
    x0 = (w - group_w) // 2
    floor = 64
    cat_h = len(CAT_POSES["sleep"]) * px
    tail = "".join(f'<rect x="{x0}" y="{floor - cat_h + r * px}" width="{px}" height="{px}" fill="{CAT_COLORS["#"]}" '
                   f'opacity="{1 - k}" style="animation:swap{k} 1.6s step-end infinite"/>' for k, r in enumerate([6, 5]))
    zzz = "".join(f'<g opacity="0" style="animation:zz 3s linear {k}s infinite">'
                  f'{sprite(["###", ".#.", "###"], {"#": "#8b949e"}, x0 + 27, floor - 30, px=2)}</g>' for k in range(3))
    floor_cells = "".join(f'<rect x="{x}" y="{floor + 2}" width="6" height="6" rx="1" fill="{LEVELS[2]}"/>'
                          for x in range(x0 - 40, x0 + group_w + 40, 8))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Thanks for visiting">
<style>
@keyframes swap0{{50%{{opacity:0}}}}
@keyframes swap1{{50%{{opacity:1}}}}
@keyframes zz{{0%{{opacity:0;transform:none}}20%{{opacity:1}}100%{{opacity:0;transform:translate(8px,-18px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs><pattern id="g" width="10" height="10" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="8" height="8" rx="1.5" fill="#161b22"/></pattern>
<linearGradient id="f"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".3" stop-color="#fff"/><stop offset=".7" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="m"><rect width="{w}" height="{h}" fill="url(#f)"/></mask></defs>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="url(#g)" mask="url(#m)" opacity=".7"/>
<g mask="url(#m)">{floor_cells}</g>
{sprite(CAT_POSES["sleep"], CAT_COLORS, x0, floor - cat_h, px=px)}{tail}{zzz}
{pixel_text(text, x0 + cat_w + 24, floor - 7 * text_px, text_px, "#d2a8ff")}
</svg>
"""


OUT.mkdir(exist_ok=True)
for key, title in SECTIONS.items():
    (OUT / f"header-{key}.svg").write_text(header(title), encoding="utf-8")
for project in PROJECTS:
    (OUT / f"project-{project[0].lower()}.svg").write_text(project_card(*project), encoding="utf-8")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8")
print(f"{len(SECTIONS)} judul, {len(PROJECTS)} kartu proyek, 1 footer -> {OUT}/")
