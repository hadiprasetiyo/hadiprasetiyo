"""Generator banner.svg: nama dibangun di grid kontribusi ala GitHub oleh karakter pixel.

Ubah NAME / TAGLINE lalu jalankan: python banner.py
"""
import math
import random

NAME = "HADI PRASETIYO"
TAGLINE = "> FULL-STACK SOFTWARE ENGINEER"

W, H = 1200, 300
PITCH = 12  # jarak antar sel grid
TAG_PITCH = 4  # piksel tagline; 3 piksel tagline = 1 sel grid
SPRITE_PX = 3  # ukuran piksel karakter
SPEED = 300  # kecepatan lari karakter (px/detik)
STEP = 0.1  # durasi satu langkah kaki

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

# karakter menghadap kanan; baris kaki dipisah supaya bisa dianimasikan
DEV_COLORS = {"B": "#d2a8ff", "b": "#a371f7", "S": "#f2cfa8", "E": "#0d1117",
              "H": "#8957e5", "P": "#6e7681", "W": "#e6edf3"}
DEV_BODY = ["..BBBBB..", ".BBBBBBB.", ".bbbbbbb.", ".SSSSSSS.", ".SSSESES.", ".SSSSSSS.",
            "..HHHHH..", ".HHHHHHH.", ".HHHHHHH.", ".SHHHHHS.", "..PPPPP.."]
DEV_LEGS = {"stand": ["..PP.PP..", "..WW.WW.."],
            "a": [".PP...PP.", ".WW...WW."],
            "b": ["...PPP...", "...WWW..."]}

CAT_COLORS = {"#": "#c9d1d9", "E": "#0d1117", "n": "#f2a6b8"}
CAT_BODY = ["......#...#", "......#####", "......#E#E#", "......##n##", "..#########", "..########."]
CAT_TAIL = {"up": [(0, 0), (0, 1), (0, 2), (1, 3)], "swish": [(1, 0), (0, 1), (0, 2), (1, 3)]}
CAT_LEGS = {"stand": ["..#.#..#.#."], "a": [".#..#...#.#"], "b": ["...#.#.#.#."]}


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


def sprite(rows, colors, top_row):
    """Gambar sprite sebagai rect per deretan warna yang sama; kaki karakter di y=0."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            run = 1
            while c + run < len(row) and row[c + run] == row[c]:
                run += 1
            if row[c] in colors:
                out.append(f'<rect x="{c * SPRITE_PX}" y="{(top_row + r) * SPRITE_PX}" '
                           f'width="{run * SPRITE_PX}" height="{SPRITE_PX}" fill="{colors[row[c]]}"/>')
            c += run
    return "".join(out)


def keyframes(name, points):
    """points: [(persen, deklarasi css)] -> @keyframes."""
    return f"@keyframes {name}{{" + "".join(f"{p:.3f}%{{{css}}}" for p, css in points) + "}"


random.seed(7)  # supaya hasil generate selalu sama

# grid digeser supaya nama jatuh tepat di sel; blok = 7 baris nama + 3 jarak + 3 tagline
name_w = width(NAME) * PITCH
name_x = (W - name_w) // 2
top = (H - 13 * PITCH) // 2
gx, gy = name_x % PITCH, top % PITCH
cols, rows = (W - gx) // PITCH, (H - gy) // PITCH
name_c0, name_r0 = (name_x - gx) // PITCH, (top - gy) // PITCH
ground = gy + name_r0 * PITCH + 1.5  # sisi atas huruf = lantai tempat karakter berlari


def cell(c, r, extra):
    return f'<rect x="{gx + c * PITCH + 1.5}" y="{gy + r * PITCH + 1.5}" width="9" height="9" rx="2" {extra}/>'


# --- lintasan karakter: jatuh -> lari -> lompati celah kata -> lompat selebrasi
lit_cols = {col for col, _, _ in pixels(NAME)}
gaps, run_start = [], None
for col in range(width(NAME) + 1):
    if col not in lit_cols and run_start is None:
        run_start = col
    elif col in lit_cols and run_start is not None:
        if col - run_start >= 3:  # celah antar huruf cuma 1 kolom, antar kata >= 3
            gaps.append((name_x + run_start * PITCH, name_x + col * PITCH))
        run_start = None


def path(start, x0, x_end, sprite_w, celebrate):
    """Segmen gerak (jenis, t0, t1, x0, x1, tinggi) sebuah karakter."""
    segs, t, x = [], start, x0
    segs.append(("fall", t, t + 0.4, x, x, 0))
    t += 0.4
    hops = [(left - 0.6 * sprite_w, right - 0.3 * sprite_w) for left, right in gaps if left < x_end]
    for takeoff, land in hops + [(x_end, None)]:
        segs.append(("walk", t, t + (takeoff - x) / SPEED, x, takeoff, 0))
        t, x = segs[-1][2], takeoff
        if land is None:
            break
        segs.append(("jump", t, t + 0.42, x, land, 22))
        t, x = t + 0.42, land
    if celebrate:
        segs.append(("jump", t, t + 0.35, x, x, 14))
    return segs


def motion(segs):
    """Titik (t, x, y) lintasan; jatuh & lompat disampling supaya melengkung."""
    pts = [(0, segs[0][3], -60)]
    for kind, t0, t1, xa, xb, height in segs:
        if kind == "walk":
            pts.append((t1, xb, ground))
            continue
        for k in range(1, 11):
            f = k / 10
            y = -60 + (ground + 60) * f * f if kind == "fall" else ground - 4 * height * f * (1 - f)
            pts.append((t0 + (t1 - t0) * f, xa + (xb - xa) * f, y))
    return pts


def frame_events(segs):
    """Pergantian frame kaki: a/b saat lari, a saat di udara, stand di akhir."""
    events = [(0, "a")]
    for kind, t0, t1, *_ in segs:
        if kind == "walk":
            k = 0
            while t0 + k * STEP < t1:
                events.append((t0 + k * STEP, "ab"[k % 2]))
                k += 1
        else:
            events.append((t0, "a"))
    events.append((segs[-1][2], "stand"))
    return events


def character(key, segs, body, legs, colors, extra=""):
    """SVG + css untuk satu karakter yang bergerak sesuai segs."""
    end = segs[-1][2]
    pts = motion(segs)
    css = [keyframes(f"{key}mv", [(t / end * 100, f"transform:translate({x:.1f}px,{y:.1f}px)") for t, x, y in pts])]
    events = frame_events(segs)
    frames = []
    for leg, leg_rows in legs.items():
        steps = [(t / end * 100, f"opacity:{int(name == leg)}") for t, name in events]
        css.append(keyframes(f"{key}{leg}", steps))
        frames.append(f'<g opacity="{int(leg == "stand")}" style="animation:{key}{leg} {end:.3f}s step-end both">'
                      f'{sprite(leg_rows, colors, -len(leg_rows))}</g>')
    final_x, final_y = pts[-1][1], pts[-1][2]
    svg = (f'<g style="transform:translate({final_x:.1f}px,{final_y:.1f}px);animation:{key}mv {end:.3f}s linear both">'
           f'{extra}{sprite(body, colors, -len(body) - len(next(iter(legs.values()))))}{"".join(frames)}</g>')
    return svg, css, end


dev_w = len(DEV_BODY[0]) * SPRITE_PX
cat_w = len(CAT_BODY[0]) * SPRITE_PX
x_start = name_x - 4
dev_end_x = name_x + name_w - dev_w
dev_segs = path(0.2, x_start, dev_end_x, dev_w, celebrate=True)
cat_segs = path(0.75, x_start, dev_end_x - 46, cat_w, celebrate=False)

# mata berkedip & ekor kucing mengibas, dipasang di dalam grup karakter
dev_h = (len(DEV_BODY) + 2) * SPRITE_PX
eyes = "".join(f'<rect x="{c * SPRITE_PX}" y="{4 * SPRITE_PX - dev_h}" width="{SPRITE_PX}" height="{SPRITE_PX}" fill="{DEV_COLORS["S"]}"/>'
               for c, bit in enumerate(DEV_BODY[4]) if bit == "E")
dev_extra = f'<g opacity="0" style="animation:wink 4.5s step-end infinite">{eyes}</g>'
cat_h = (len(CAT_BODY) + 1) * SPRITE_PX
tails = []
for k, (pose, cells_) in enumerate(CAT_TAIL.items()):
    rects = "".join(f'<rect x="{c * SPRITE_PX}" y="{r * SPRITE_PX - cat_h}" width="{SPRITE_PX}" height="{SPRITE_PX}" fill="{CAT_COLORS["#"]}"/>'
                    for c, r in cells_)
    tails.append(f'<g opacity="{1 - k}" style="animation:tail{k} 1.4s step-end infinite">{rects}</g>')

dev_svg, dev_css, dev_done = character("dv", dev_segs, DEV_BODY, DEV_LEGS, DEV_COLORS, dev_extra)
cat_svg, cat_css, _ = character("ct", cat_segs, CAT_BODY, CAT_LEGS, CAT_COLORS, "".join(tails))


def build_time(cx):
    """Detik saat ujung kaki depan karakter mencapai kolom bertitik tengah cx."""
    front = dev_w
    for kind, t0, t1, xa, xb, _ in dev_segs:
        if kind == "walk" and xb + front >= cx:
            return t0 + max(0, cx - front - xa) / SPEED
        if kind != "walk" and xb + front >= cx:
            return t1
    return dev_done


# tagline: prompt ">" langsung tampil, sisanya diketik setelah nama selesai dibangun
tag_w = width(TAGLINE) * TAG_PITCH
tag_x = (W - tag_w) // 2
tag_r0 = name_r0 + 10
tag_y = gy + tag_r0 * PITCH + (3 * PITCH - 7 * TAG_PITCH) // 2
caret_x = tag_x + tag_w + TAG_PITCH
type_start, step = dev_done + 0.1, 0.045

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

# area yang dikosongkan dari dekorasi: nama + jalur lari di atasnya, tagline, legend
busy = {(c, r) for c in range(name_c0 - 1, name_c0 + width(NAME) + 1) for r in range(name_r0 - 4, name_r0 + 8)}
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

# kolom nama tumbuh dari atas ke bawah tepat saat diinjak karakter
name_cells = []
for col, r, _ in pixels(NAME):
    grow = build_time(name_x + (col + 0.5) * PITCH) + r * 0.025
    shine = dev_done + 1.5 + col * 0.012
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
.n{{fill:{NAME_COLOR};animation:grow .5s ease-out both,shine 8s ease-in-out infinite}}
.t{{fill:{TEXT_COLOR};animation:show .01s both}}
.caret{{animation:caret {caret_dur:.2f}s step-end both,blink 1s step-end infinite}}
.hop{{animation:hop 7s ease-in-out {dev_done + 3:.2f}s infinite}}
.lg{{font:11px -apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif;fill:#7d8590}}
@keyframes grow{{0%{{fill-opacity:0;fill:{LEVELS[3]}}}25%{{fill-opacity:1;fill:#f3e8ff}}}}
@keyframes shine{{3%{{fill:#f3e8ff}}6%{{fill:{NAME_COLOR}}}}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes wink{{0%{{opacity:0}}96%{{opacity:1}}}}
@keyframes tail0{{50%{{opacity:0}}}}
@keyframes tail1{{50%{{opacity:1}}}}
@keyframes hop{{0%,6%,100%{{transform:translateY(0)}}3%{{transform:translateY(-12px)}}}}
@keyframes caret{{{"".join(frames)}}}
{"".join(f"@keyframes tw{k}{{50%{{fill:{LEVELS[k]}}}}}" for k in (2, 3, 4))}
{"".join(dev_css + cat_css)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<pattern id="grid" x="{gx}" y="{gy}" width="{PITCH}" height="{PITCH}" patternUnits="userSpaceOnUse"><rect x="1.5" y="1.5" width="9" height="9" rx="2" fill="{LEVELS[0]}"/></pattern>
<filter id="soft" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
<mask id="fade"><rect x="28" y="24" width="{W - 56}" height="{H - 48}" rx="40" fill="#fff" filter="url(#soft)"/>{hole(tag_hole)}{hole(legend_hole)}</mask>
<radialGradient id="glow"><stop offset="0" stop-color="#8957e5" stop-opacity=".22"/><stop offset="1" stop-color="#8957e5" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="#0d1117" stroke="#30363d"/>
<g mask="url(#fade)"><rect width="{W}" height="{H}" fill="url(#grid)"/>{"".join(decor)}</g>
<ellipse cx="{W / 2}" cy="{gy + (name_r0 + 3.5) * PITCH}" rx="{W * 0.42}" ry="{H * 0.42}" fill="url(#glow)"/>
{"".join(name_cells)}
<g clip-path="url(#card)">{cat_svg}<g class="hop">{dev_svg}</g></g>
{"".join(tagline)}
<rect class="caret" x="{caret_x}" y="{tag_y}" width="{3 * TAG_PITCH}" height="{7 * TAG_PITCH}" fill="{LEVELS[4]}"/>
<text class="lg" x="{gx + legend_c0 * PITCH - 6}" y="{legend_y + 10}" text-anchor="end">Less</text>
{"".join(legend)}
<text class="lg" x="{gx + (legend_c0 + 5) * PITCH + 4}" y="{legend_y + 10}">More</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"banner.svg: {len(svg) // 1024} KB, nama selesai dibangun di detik {dev_done:.1f}")
