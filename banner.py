"""Generator banner.svg: nama ditulis di grid kontribusi ala GitHub.

Ubah NAME / TAGLINE lalu jalankan: python banner.py
"""
import math
import random

NAME = "HADI PRASETIYO"
TAGLINE = "> FULL-STACK SOFTWARE ENGINEER"

W, H = 1200, 300
PITCH = 12  # jarak antar sel grid
TAG_PITCH = 4  # piksel tagline; 3 piksel tagline = 1 sel grid

# skala ungu ala grafik kontribusi GitHub (dark), level 0..4
LEVELS = ["#161b22", "#3c1e70", "#553098", "#8957e5", "#bc8cff"]
NAME_COLOR = "#d2a8ff"
TEXT_COLOR = "#c9d1d9"

FONT = {
    "A": ".###. #...# #...# ##### #...# #...# #...#",
    "B": "####. #...# #...# ####. #...# #...# ####.",
    "C": ".###. #...# #.... #.... #.... #...# .###.",
    "D": "####. #...# #...# #...# #...# #...# ####.",
    "E": "##### #.... #.... ####. #.... #.... #####",
    "F": "##### #.... #.... ####. #.... #.... #....",
    "G": ".###. #...# #.... #.### #...# #...# .####",
    "H": "#...# #...# #...# ##### #...# #...# #...#",
    "I": "### .#. .#. .#. .#. .#. ###",
    "J": "..## ...# ...# ...# #..# #..# .##.",
    "K": "#...# #..#. #.#.. ##... #.#.. #..#. #...#",
    "L": "#.... #.... #.... #.... #.... #.... #####",
    "M": "#...# ##.## #.#.# #.#.# #...# #...# #...#",
    "N": "#...# #...# ##..# #.#.# #..## #...# #...#",
    "O": ".###. #...# #...# #...# #...# #...# .###.",
    "P": "####. #...# #...# ####. #.... #.... #....",
    "Q": ".###. #...# #...# #...# #.#.# #..#. .##.#",
    "R": "####. #...# #...# ####. #.#.. #..#. #...#",
    "S": ".#### #.... #.... .###. ....# ....# ####.",
    "T": "##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..",
    "U": "#...# #...# #...# #...# #...# #...# .###.",
    "V": "#...# #...# #...# #...# #...# .#.#. ..#..",
    "W": "#...# #...# #...# #.#.# #.#.# ##.## #...#",
    "X": "#...# #...# .#.#. ..#.. .#.#. #...# #...#",
    "Y": "#...# #...# .#.#. ..#.. ..#.. ..#.. ..#..",
    "Z": "##### ....# ...#. ..#.. .#... #.... #####",
    " ": "... ... ... ... ... ... ...",
    ">": "#... .#.. ..#. ...# ..#. .#.. #...",
    "/": "....# ...#. ...#. ..#.. .#... .#... #....",
    "-": "... ... ... ### ... ... ...",
    ".": ". . . . . . #",
    "·": ". . . # . . .",
}
for ch, glyph in FONT.items():
    rows = glyph.split()
    assert len(rows) == 7 and len({len(row) for row in rows}) == 1, f"glyph {ch!r} rusak"


def width(text):
    return sum(len(FONT[ch].split()[0]) + 1 for ch in text) - 1


def pixels(text):
    """(kolom, baris, index huruf) tiap piksel yang menyala."""
    col = 0
    for i, ch in enumerate(text):
        rows = FONT[ch].split()
        for r, row in enumerate(rows):
            for c, bit in enumerate(row):
                if bit == "#":
                    yield col + c, r, i
        col += len(rows[0]) + 1


random.seed(7)  # supaya hasil generate selalu sama

# grid digeser supaya nama jatuh tepat di sel; blok = 7 baris nama + 3 jarak + 3 tagline
name_x = (W - width(NAME) * PITCH) // 2
top = (H - 13 * PITCH) // 2
gx, gy = name_x % PITCH, top % PITCH
cols, rows = (W - gx) // PITCH, (H - gy) // PITCH
name_c0, name_r0 = (name_x - gx) // PITCH, (top - gy) // PITCH


def cell(c, r, extra):
    return f'<rect x="{gx + c * PITCH + 1.5}" y="{gy + r * PITCH + 1.5}" width="9" height="9" rx="2" {extra}/>'


# tagline: prompt ">" langsung tampil, sisanya diketik
tag_w = width(TAGLINE) * TAG_PITCH
tag_x = (W - tag_w) // 2
tag_r0 = name_r0 + 10
tag_y = gy + tag_r0 * PITCH + (3 * PITCH - 7 * TAG_PITCH) // 2
caret_x = tag_x + tag_w + TAG_PITCH
type_start, step = 1.2, 0.045

ends, col = [], 0
for ch in TAGLINE:
    col += len(FONT[ch].split()[0])
    ends.append(col)
    col += 1
caret_dur = type_start + (len(TAGLINE) - 2) * step
frames = [f"0%{{transform:translateX({tag_x + (ends[0] + 1) * TAG_PITCH - caret_x}px)}}"]
for i in range(1, len(TAGLINE)):
    pct = (type_start + (i - 1) * step) / caret_dur * 100
    frames.append(f"{pct:.2f}%{{transform:translateX({tag_x + (ends[i] + 1) * TAG_PITCH - caret_x}px)}}")

# area yang dikosongkan dari dekorasi: nama, tagline, legend
busy = {(c, r) for c in range(name_c0 - 1, name_c0 + width(NAME) + 1) for r in range(name_r0 - 1, name_r0 + 8)}
hole_c0 = (tag_x - gx) // PITCH - 1
hole_c1 = (caret_x + 3 * TAG_PITCH - gx) // PITCH + 1
tag_hole = [(c, r) for c in range(hole_c0, hole_c1 + 1) for r in range(tag_r0, tag_r0 + 3)]
legend_r, legend_c0 = rows - 3, cols - 10
legend_hole = [(c, legend_r) for c in range(legend_c0 - 4, legend_c0 + 9)]
busy.update(tag_hole, legend_hole)

decor = []
for r in range(-1, rows + 1):
    for c in range(-1, cols + 1):
        if (c, r) in busy:
            continue
        x, y = gx + (c + 0.5) * PITCH, gy + (r + 0.5) * PITCH
        d = min(1, math.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2)))
        if random.random() > 0.03 + 0.35 * d * d:  # makin ke pinggir makin rapat
            continue
        if random.random() < 0.35:
            level = random.choice([2, 3, 3, 4])
            dur = random.uniform(3, 7)
            decor.append(cell(c, r, f'fill="{LEVELS[0]}" style="animation:tw{level} {dur:.1f}s ease-in-out {-random.uniform(0, dur):.1f}s infinite"'))
        else:
            level = random.choice([1, 1, 1, 2, 2, 3])
            decor.append(cell(c, r, f'fill="{LEVELS[level]}"'))

name_cells = []
for col, r, _ in pixels(NAME):
    grow = 0.15 + col * 0.014 + random.uniform(0, 0.2)
    shine = 4 + col * 0.012
    name_cells.append(cell(name_c0 + col, name_r0 + r, f'class="n" style="animation-delay:{grow:.2f}s,{shine:.2f}s"'))

tag_groups = {}
for col, r, i in pixels(TAGLINE):
    tag_groups.setdefault(i, []).append(f'<rect x="{tag_x + col * TAG_PITCH}" y="{tag_y + r * TAG_PITCH}" width="3" height="3"/>')
tagline = []
for i, rects in tag_groups.items():
    if i == 0:
        tagline.append(f'<g fill="{NAME_COLOR}">{"".join(rects)}</g>')
    else:
        tagline.append(f'<g class="t" style="animation-delay:{type_start + (i - 1) * step:.3f}s">{"".join(rects)}</g>')

legend_y = gy + legend_r * PITCH
legend = [cell(legend_c0 + k, legend_r, f'fill="{color}"') for k, color in enumerate(LEVELS)]


def hole(cells):
    xs = [c for c, _ in cells]
    ys = [r for _, r in cells]
    return (f'<rect x="{gx + min(xs) * PITCH}" y="{gy + min(ys) * PITCH}" '
            f'width="{(max(xs) - min(xs) + 1) * PITCH}" height="{(max(ys) - min(ys) + 1) * PITCH}" fill="#000"/>')


title = f"{NAME.title()} — {TAGLINE.lstrip('> ').title()}"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
<title>{title}</title>
<style>
.n{{fill:{NAME_COLOR};animation:grow .45s ease-out both,shine 8s ease-in-out infinite}}
.t{{fill:{TEXT_COLOR};animation:show .01s both}}
.caret{{animation:caret {caret_dur:.2f}s step-end both,blink 1s step-end infinite}}
.lg{{font:11px -apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif;fill:#7d8590}}
@keyframes grow{{0%{{fill-opacity:0}}40%{{fill:{LEVELS[2]}}}70%{{fill:{LEVELS[3]}}}}}
@keyframes shine{{3%{{fill:#f3e8ff}}6%{{fill:{NAME_COLOR}}}}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes caret{{{"".join(frames)}}}
{"".join(f"@keyframes tw{k}{{50%{{fill:{LEVELS[k]}}}}}" for k in (2, 3, 4))}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<pattern id="grid" x="{gx}" y="{gy}" width="{PITCH}" height="{PITCH}" patternUnits="userSpaceOnUse"><rect x="1.5" y="1.5" width="9" height="9" rx="2" fill="{LEVELS[0]}"/></pattern>
<filter id="soft" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
<mask id="fade"><rect x="28" y="24" width="{W - 56}" height="{H - 48}" rx="40" fill="#fff" filter="url(#soft)"/>{hole(tag_hole)}{hole(legend_hole)}</mask>
<radialGradient id="glow"><stop offset="0" stop-color="#8957e5" stop-opacity=".22"/><stop offset="1" stop-color="#8957e5" stop-opacity="0"/></radialGradient>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="#0d1117" stroke="#30363d"/>
<g mask="url(#fade)"><rect width="{W}" height="{H}" fill="url(#grid)"/>{"".join(decor)}</g>
<ellipse cx="{W / 2}" cy="{gy + (name_r0 + 3.5) * PITCH}" rx="{W * 0.42}" ry="{H * 0.42}" fill="url(#glow)"/>
{"".join(name_cells)}
{"".join(tagline)}
<rect class="caret" x="{caret_x}" y="{tag_y}" width="{3 * TAG_PITCH}" height="{7 * TAG_PITCH}" fill="{LEVELS[4]}"/>
<text class="lg" x="{gx + legend_c0 * PITCH - 6}" y="{legend_y + 10}" text-anchor="end">Less</text>
{"".join(legend)}
<text class="lg" x="{gx + (legend_c0 + 5) * PITCH + 4}" y="{legend_y + 10}">More</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"banner.svg: {len(svg) // 1024} KB, {len(name_cells)} sel nama, {len(decor)} sel dekorasi")
