"""Generator gambar pendukung README: judul section, kartu about/stack/proyek, footer (folder assets/).

Ubah ABOUT / STACK / PROJECTS / SECTIONS lalu jalankan: python readme_assets.py
Ikon tech stack diunduh dari skillicons.dev saat generate lalu disematkan, jadi butuh internet.
"""
import base64
import random
import textwrap
import urllib.request
from html import escape
from pathlib import Path

from pixelart import CAT_COLORS, CAT_POSES, pixels, sprite, width

SECTIONS = {"about": "ABOUT", "stack": "TECH STACK", "projects": "FEATURED PROJECTS", "activity": "ACTIVITY"}
ABOUT = {
    "name": "Hadi Prasetiyo",
    "role": "Full-Stack Software Engineer",
    "bio": "I build web applications end to end, from the database schema and REST API to the interface "
           "people actually click on. Most of my work uses Laravel, React and FastAPI, and I care about code "
           "that is simple to read and easy to change.",
    # (ikon, label, isi)
    "facts": [("pin", "LOCATION", "Samarinda, Indonesia"),
              ("cap", "EDUCATION", "Mulawarman University"),
              ("prompt", "CURRENTLY", "Building with Laravel & React"),
              ("sprout", "LEARNING", "Testing · CI/CD · System design")],
}
# (kategori, keterangan, [(id skillicons, label)])
STACK = [
    ("Languages", "The languages I write and think in.",
     [("php", "PHP"), ("js", "JavaScript"), ("python", "Python"), ("java", "Java")]),
    ("Frontend", "Responsive interfaces, from layout to motion.",
     [("html", "HTML"), ("css", "CSS"), ("react", "React"), ("vite", "Vite"), ("tailwind", "Tailwind"), ("bootstrap", "Bootstrap")]),
    ("Backend & Data", "APIs, business logic, and the data behind them.",
     [("laravel", "Laravel"), ("nodejs", "Node.js"), ("express", "Express"), ("fastapi", "FastAPI"), ("mysql", "MySQL"),
      ("postgres", "PostgreSQL")]),
    ("Tools", "How I build, ship, and design.",
     [("git", "Git"), ("github", "GitHub"), ("docker", "Docker"), ("postman", "Postman"), ("figma", "Figma"),
      ("vscode", "VS Code"), ("linux", "Linux")]),
]
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
CARD_W, CARD_H = 420, 170  # kartu grid 2x2; kartu lebar = dua kartu + jarak antar gambar di README
PIXEL_ICONS = {
    "pin": ["..###..", ".#####.", ".##.##.", ".#####.", "..###..", "...#...", "...#..."],
    "cap": ["...#...", ".#####.", "#######", ".#####.", "..###..", "..###..", "......."],
    "prompt": ["#......", ".#.....", "..#....", ".#.....", "#..####", ".......", "......."],
    "sprout": ["##...##", ".##.##.", "..###..", "...#...", "...#...", "..###..", ".#####."],
}
STYLE = f"""<style>
.t{{font:600 19px {UI_FONT};fill:#d2a8ff}}
.h{{font:600 26px {UI_FONT};fill:#e6edf3}}
.r{{font:600 15px {UI_FONT};fill:#bc8cff}}
.d{{font:14px {UI_FONT};fill:#8b949e}}
.c{{font:12px {UI_FONT};fill:#c9d1d9}}
.s{{font:11px {UI_FONT};fill:#8b949e}}
.k{{font:600 11px {UI_FONT};fill:#7d8590;letter-spacing:.08em}}
.v{{font:14px {UI_FONT};fill:#c9d1d9}}
.l{{font:600 12px {UI_FONT};fill:#3fb950}}
.tw{{animation:tw 4s ease-in-out infinite}}
.tw:nth-of-type(2n){{animation-delay:-2s}}
@keyframes tw{{50%{{fill:#bc8cff}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>"""
random.seed(11)


def pixel_text(text, x, y, px, fill):
    return "".join(f'<rect x="{x + c * px}" y="{y + r * px}" width="{px - 1}" height="{px - 1}" fill="{fill}"/>'
                    for c, r, _ in pixels(text))


def cluster(x, y):
    """Ikon 3x3 sel kontribusi; sebagian berkilau pelan."""
    return "".join(f'<rect x="{x + c * 8}" y="{y + r * 8}" width="6" height="6" rx="1" fill="{random.choice(LEVELS[1:])}"'
                   + (' class="tw"' if random.random() < 0.3 else "") + "/>" for r in range(3) for c in range(3))


def card(w, h, label, body):
    """Kartu gelap dasar yang dipakai semua kartu supaya seragam."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}">
{STYLE}
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>
{body}
</svg>
"""


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


def about_card():
    """Kartu lebar: sapaan + bio di kiri, fakta singkat berikon pixel di kanan."""
    w, h = CARD_W * 2 + 8, 224
    bio = "".join(f'<text class="d" x="28" y="{122 + k * 21}">{escape(line)}</text>'
                  for k, line in enumerate(textwrap.wrap(ABOUT["bio"], 62)[:4]))
    facts = ""
    for k, (icon, label, value) in enumerate(ABOUT["facts"]):
        y = 30 + k * 46
        facts += (sprite(PIXEL_ICONS[icon], {"#": "#bc8cff"}, 556, y + 3, px=2)
                  + f'<text class="k" x="580" y="{y + 12}">{label}</text>'
                  + f'<text class="v" x="580" y="{y + 32}">{escape(value)}</text>')
    body = (cluster(28, 30)
            + f'<text class="h" x="64" y="52">Hi, I\'m <tspan fill="#d2a8ff">{escape(ABOUT["name"])}</tspan></text>'
            + f'<text class="r" x="28" y="88">{escape(ABOUT["role"])}</text>'
            + bio
            + f'<rect x="528" y="28" width="1" height="{h - 56}" fill="#21262d"/>'
            + facts)
    return card(w, h, f'{ABOUT["name"]}, {ABOUT["role"]}. {ABOUT["bio"]}', body)


def fetch_icon(name):
    request = urllib.request.Request(f"https://skillicons.dev/icons?i={name}", headers={"User-Agent": "readme-assets"})
    return base64.b64encode(urllib.request.urlopen(request, timeout=30).read()).decode()


def stack_card(category, note, items):
    """Kartu kategori tech stack: ikon disematkan sebagai data URI supaya tidak bergantung layanan luar."""
    slot = 376 / max(len(items), 6)
    icons = "".join(f'<image x="{22 + k * slot:.1f}" y="94" width="36" height="36" href="data:image/svg+xml;base64,{fetch_icon(icon)}"/>'
                    f'<text class="s" x="{40 + k * slot:.1f}" y="{CARD_H - 22}" text-anchor="middle">{escape(label)}</text>'
                    for k, (icon, label) in enumerate(items))
    body = (cluster(22, 22)
            + f'<text class="t" x="58" y="43">{escape(category)}</text>'
            + f'<text class="d" x="22" y="74">{escape(note)}</text>'
            + icons)
    return card(CARD_W, CARD_H, f"{category}: {', '.join(label for _, label in items)}", body)


def project_card(repo, description, stack, live):
    """Kartu proyek; seluruh kartu ditautkan ke repo di README."""
    lines = textwrap.wrap(description, 52)[:3]
    desc = "".join(f'<text class="d" x="22" y="{82 + k * 19}">{escape(line)}</text>' for k, line in enumerate(lines))
    chips, x = [], 22
    for tech in stack:
        chip_w = len(tech) * 6.4 + 18
        chips.append(f'<rect x="{x}" y="{CARD_H - 40}" width="{chip_w:.0f}" height="22" rx="11" fill="#161b22" stroke="#30363d"/>'
                     f'<text class="c" x="{x + chip_w / 2:.0f}" y="{CARD_H - 25}" text-anchor="middle">{escape(tech)}</text>')
        x += chip_w + 8
    badge = (f'<circle cx="{CARD_W - 58}" cy="37" r="4" fill="#3fb950"/>'
             f'<text class="l" x="{CARD_W - 22}" y="41" text-anchor="end">Live</text>' if live else "")
    body = cluster(22, 22) + f'<text class="t" x="58" y="43">{escape(repo)}</text>' + badge + desc + "".join(chips)
    return card(CARD_W, CARD_H, f"{repo}: {description}", body)


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
(OUT / "about.svg").write_text(about_card(), encoding="utf-8")
for category, note, items in STACK:
    (OUT / f"stack-{category.split()[0].lower()}.svg").write_text(stack_card(category, note, items), encoding="utf-8")
for project in PROJECTS:
    (OUT / f"project-{project[0].lower()}.svg").write_text(project_card(*project), encoding="utf-8")
(OUT / "footer.svg").write_text(footer(), encoding="utf-8")
print(f"{len(SECTIONS)} judul, 1 about, {len(STACK)} stack, {len(PROJECTS)} proyek, 1 footer -> {OUT}/")
