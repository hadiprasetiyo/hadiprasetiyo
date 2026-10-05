"""Generator banner.svg: nama dibangun di grid kontribusi ala GitHub oleh karakter pixel,
lalu karakternya berburu bug tanpa henti.

Ubah NAME / TAGLINE / BUG_LETTERS lalu jalankan: python banner.py
"""
import math
import random

NAME = "HADI PRASETIYO"
TAGLINE = "> FULL-STACK SOFTWARE ENGINEER"
BUG_LETTERS = [8, 1, 9]  # index huruf di NAME tempat bug muncul, urut sesuai diburu

W, H = 1200, 300
PITCH = 12  # jarak antar sel grid
TAG_PITCH = 4  # piksel tagline; 3 piksel tagline = 1 sel grid
SPRITE_PX = 3  # ukuran piksel karakter
SPEED = 300  # kecepatan lari karakter (px/detik)
STEP = 0.1  # durasi satu langkah kaki
HURDLE_T, STOMP_T = 0.34, 0.36  # lama lompat rintangan & lompat injak bug

# skala ungu ala grafik kontribusi GitHub (dark), level 0..4
LEVELS = ["#161b22", "#3c1e70", "#553098", "#8957e5", "#bc8cff"]
NAME_COLOR = "#d2a8ff"
TEXT_COLOR = "#c9d1d9"
BUG_COLOR = "#f85149"  # merah = bug / test gagal
PLUS_COLOR = "#3fb950"  # hijau = +1 kontribusi / test lulus

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
    "1": ".#. ##. .#. .#. .#. .#. ###",
    "+": "..... ..#.. ..#.. ##### ..#.. ..#.. .....",
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

# sprite menghadap kanan, tiap pose digambar utuh
DEV_COLORS = {"B": "#d2a8ff", "b": "#a371f7", "S": "#f2cfa8", "E": "#0d1117",
              "H": "#8957e5", "P": "#6e7681", "W": "#e6edf3"}
DEV_BODY = ["..BBBBB..", ".BBBBBBB.", ".bbbbbbb.", ".SSSSSSS.", ".SSSESES.", ".SSSSSSS.",
            "..HHHHH..", ".HHHHHHH.", ".HHHHHHH.", ".SHHHHHS.", "..PPPPP.."]
DEV_POSES = {"stand": DEV_BODY + ["..PP.PP..", "..WW.WW.."],
             "a": DEV_BODY + [".PP...PP.", ".WW...WW."],
             "b": DEV_BODY + ["...PPP...", "...WWW..."]}

CAT_COLORS = {"#": "#c9d1d9", "E": "#0d1117", "n": "#f2a6b8", "-": "#6e7681"}
CAT_TOP = ["#.....#...#", "#.....#####", "#.....#E#E#", ".#....##n##", "..#########", "..########."]
CAT_POSES = {"stand": CAT_TOP + ["..#.#..#.#."],
             "a": CAT_TOP + [".#..#...#.#"],
             "b": CAT_TOP + ["...#.#.#.#."],
             # tidur meringkuk, ujung ekor digambar terpisah supaya bisa mengibas
             "sleep": ["...........", "......#...#", "......#####", "......#-#-#",
                       "......##n##", "..#########", ".#########."]}

BUG_POSES = {"a": ["#...#", ".###.", "#####", ".###.", "#.#.#"],
             "b": ["#...#", ".###.", ".###.", "#####", ".#.#."]}
ZZZ = ["####", "..#.", ".#..", "####"]


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


def sprite(rows, colors, x=0, y=None, px=SPRITE_PX):
    """Gambar sprite sebagai rect per deretan warna yang sama; default kaki di y=0."""
    y = -len(rows) * px if y is None else y
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            run = 1
            while c + run < len(row) and row[c + run] == row[c]:
                run += 1
            if row[c] in colors:
                out.append(f'<rect x="{x + c * px:g}" y="{y + r * px:g}" width="{run * px}" height="{px}" fill="{colors[row[c]]}"/>')
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


def letter_center(i):
    start = width(NAME[:i]) + 1 if i else 0
    return name_x + (start + len(FONT[NAME[i]].split()[0]) / 2) * PITCH


# --- lintasan: segmen (jenis, t0, t1, x0, x1, tinggi lompat)
dev_w = len(DEV_BODY[0]) * SPRITE_PX
cat_w = len(CAT_TOP[0]) * SPRITE_PX

# rintangan (kiri, kanan, tinggi lompat, inset): celah kata boleh diinjak tepinya, kucing tidak
lit_cols = {col for col, _, _ in pixels(NAME)}
pits, run_start = [], None
for col in range(width(NAME) + 1):
    if col not in lit_cols and run_start is None:
        run_start = col
    elif col in lit_cols and run_start is not None:
        if col - run_start >= 3:  # celah antar huruf cuma 1 kolom, antar kata >= 3
            pits.append((name_x + run_start * PITCH, name_x + col * PITCH, 22, 0.35))
        run_start = None


def run(segs, t, x, target, w, obstacles):
    """Lari dari x ke target sambil melompati rintangan di antaranya; balikan (t, x) akhir."""
    d = 1 if target >= x else -1
    hurdles = []
    for a, b, height, inset in obstacles:
        inset *= w
        take, land = (a - w + inset, b - inset) if d > 0 else (b - inset, a - w + inset)
        if d * (take - x) >= 0 and d * (target - land) >= 0:
            hurdles.append((take, land, height))
    for take, land, height in sorted(hurdles, key=lambda h: d * h[0]):
        segs.append(("walk", t, t + abs(take - x) / SPEED, x, take, 0))
        t = segs[-1][2]
        segs.append(("jump", t, t + HURDLE_T, take, land, height))
        t, x = t + HURDLE_T, land
    segs.append(("walk", t, t + abs(target - x) / SPEED, x, target, 0))
    return segs[-1][2], target


def rest(segs, t, x, dur):
    segs.append(("rest", t, t + dur, x, x, 0))
    return t + dur


def intro(start, x_end, w, celebrate):
    """Jatuh ke huruf pertama lalu lari ke x_end."""
    x0 = name_x - 4
    segs = [("fall", start, start + 0.4, x0, x0, 0)]
    t, x = run(segs, start + 0.4, x0, x_end, w, pits)
    if celebrate:
        segs.append(("jump", t, t + 0.35, x, x, 14))
    else:
        rest(segs, t, x, 0.8)  # berdiri sebentar sebelum tidur
    return segs


def motion(segs, start):
    """Titik (t, x, y) lintasan; jatuh & lompat disampling supaya melengkung."""
    pts = [start]
    for kind, t0, t1, xa, xb, height in segs:
        if kind in ("walk", "rest"):
            pts.append((t1, xb, ground))
            continue
        for k in range(1, 11):
            f = k / 10
            y = -60 + (ground + 60) * f * f if kind == "fall" else ground - 4 * height * f * (1 - f)
            pts.append((t0 + (t1 - t0) * f, xa + (xb - xa) * f, y))
    return pts


def frame_events(segs, first, last):
    """Pergantian pose: a/b saat lari, a saat di udara, stand saat diam."""
    events = [(0, first)]
    for kind, t0, t1, *_ in segs:
        if kind == "walk":
            k = 0
            while t0 + k * STEP < t1:
                events.append((t0 + k * STEP, "ab"[k % 2]))
                k += 1
        else:
            events.append((t0, "stand" if kind == "rest" else "a"))
    events.append((segs[-1][2], last))
    return events


def character(key, poses, colors, w, intro_segs, final_pose, loop=None, extra="", pose_extra=None):
    """SVG + css satu karakter: animasi intro sekali jalan, lalu loop (kalau ada) tanpa henti."""
    pose_extra = pose_extra or {}
    end = intro_segs[-1][2]
    pts = motion(intro_segs, (0, intro_segs[0][3], -60))
    css = [keyframes(f"{key}mv", [(t / end * 100, f"transform:translate({x:.1f}px,{y:.1f}px)") for t, x, y in pts])]
    move = [f"{key}mv {end:.3f}s linear both"]
    events = {"": (frame_events(intro_segs, "a", final_pose), end, "both")}
    if loop:
        loop_dur = loop[-1][2]
        lpts = motion(loop, (0, pts[-1][1], ground))
        css.append(keyframes(f"{key}lp", [(t / loop_dur * 100, f"transform:translate({x:.1f}px,{y:.1f}px)") for t, x, y in lpts]))
        move.append(f"{key}lp {loop_dur:.3f}s linear {LOOP_START:.2f}s infinite")
        events["L"] = (frame_events(loop, "stand", "stand"), loop_dur, f"{LOOP_START:.2f}s infinite")
    groups = []
    for pose, pose_rows in poses.items():
        anims = []
        for suffix, (evs, dur, mode) in events.items():
            css.append(keyframes(f"{key}{pose}{suffix}", [(t / dur * 100, f"opacity:{int(name == pose)}") for t, name in evs]))
            anims.append(f"{key}{pose}{suffix} {dur:.3f}s step-end {mode}")
        groups.append(f'<g opacity="{int(pose == final_pose)}" style="animation:{",".join(anims)}">'
                      f'{sprite(pose_rows, colors)}{pose_extra.get(pose, "")}</g>')
    inner = extra + "".join(groups)
    if loop:
        # balik badan saat lari ke kiri
        facing, last = [(0, "none")], "none"
        for _, t0, _, xa, xb, _ in loop:
            if xb != xa:
                face = "none" if xb > xa else f"matrix(-1,0,0,1,{w},0)"
                if face != last:
                    facing.append((t0, face))
                    last = face
        css.append(keyframes(f"{key}face", [(t / loop_dur * 100, f"transform:{f}") for t, f in facing]))
        inner = f'<g style="animation:{key}face {loop_dur:.3f}s step-end {LOOP_START:.2f}s infinite">{inner}</g>'
    svg = (f'<g style="transform:translate({pts[-1][1]:.1f}px,{pts[-1][2]:.1f}px);animation:{",".join(move)}">'
           f'{inner}</g>')
    return svg, css, end


# --- intro: developer membangun nama, kucing menyusul lalu tidur
dev_rest_x = name_x + name_w - dev_w
cat_rest_x = dev_rest_x - 46
dev_intro = intro(0.2, dev_rest_x, dev_w, celebrate=True)
cat_intro = intro(0.75, cat_rest_x, cat_w, celebrate=False)
dev_done = dev_intro[-1][2]
cat_done = cat_intro[-1][2]
LOOP_START = dev_done + 2.5  # mulai berburu setelah tagline selesai diketik

# --- loop: bug muncul satu per satu, diburu & diinjak, lalu kembali ke huruf terakhir
obstacles = pits + [(cat_rest_x + 3, cat_rest_x + cat_w - 3, 30, -3 / dev_w)]
dev_loop, bugs = [], []
t, x = rest(dev_loop, 0, dev_rest_x, 1.4), dev_rest_x
spawn = 0.5
for letter in BUG_LETTERS:
    bug_x = letter_center(letter)
    target = bug_x - dev_w / 2
    d = 1 if target > x else -1
    t, x = run(dev_loop, t, x, target - d * 48, dev_w, obstacles)
    dev_loop.append(("jump", t, t + STOMP_T, x, target, 26))
    t, x = t + STOMP_T, target
    bugs.append((bug_x, spawn, t))
    spawn = t + 0.1
    t = rest(dev_loop, t, x, 0.35)
t, x = run(dev_loop, t, x, dev_rest_x, dev_w, obstacles)
t = rest(dev_loop, t, x, 0.5)
dev_loop.append(("jump", t, t + 0.35, x, x, 14))
t = rest(dev_loop, t + 0.35, x, 2.5)
period = t


def bug_parts(i, bug_x, spawn, kill):
    """Bug merayap, gepeng saat diinjak, lalu percikan & '+1' hijau melayang."""
    pct = lambda s: s / period * 100
    hidden, alive, flat = "opacity:0;transform:translateY(-10px)", "opacity:1;transform:none", "transform:scale(1.5,.3)"
    css = [keyframes(f"bug{i}", [(0, hidden), (pct(spawn), hidden), (pct(spawn + 0.2), alive), (pct(kill), alive),
                                 (pct(kill + 0.06), f"opacity:1;{flat}"), (pct(kill + 0.3), f"opacity:0;{flat}"),
                                 (100, f"opacity:0;{flat}")]),
           keyframes(f"plus{i}", [(0, "opacity:0"), (pct(kill), "opacity:0;transform:none"),
                                  (pct(kill + 0.05), "opacity:1;transform:none"),
                                  (pct(kill + 1), "opacity:0;transform:translateY(-18px)"), (100, "opacity:0")]),
           keyframes(f"spark{i}", [(0, "opacity:0"), (pct(kill), "opacity:0;transform:scale(.4)"),
                                   (pct(kill + 0.03), "opacity:1;transform:scale(.6)"),
                                   (pct(kill + 0.4), "opacity:0;transform:scale(1.8)"), (100, "opacity:0")])]
    timing = f"{period:.3f}s linear {LOOP_START:.2f}s infinite"
    legs = "".join(f'<g opacity="{1 - k}" style="animation:leg{k} .3s step-end infinite">'
                   f'{sprite(rows_, {"#": BUG_COLOR}, bug_x - 7.5, ground - 15)}</g>'
                   for k, rows_ in enumerate(BUG_POSES.values()))
    bug = (f'<g opacity="0" style="transform-box:fill-box;transform-origin:50% 100%;animation:bug{i} {timing}">'
           f'<g style="animation:crawl 1.6s ease-in-out infinite alternate">{legs}</g></g>')
    spark_dots = "".join(f'<rect x="{bug_x + dx - 1.5:g}" y="{ground - 8 + dy - 1.5:g}" width="3" height="3" fill="#f3e8ff"/>'
                         for dx, dy in [(-20, 0), (20, 0), (-15, -12), (15, -12)])
    spark = (f'<g opacity="0" style="transform-box:fill-box;transform-origin:50% 100%;animation:spark{i} {timing}">'
             f'{spark_dots}</g>')
    plus_rects = "".join(f'<rect x="{bug_x - 9 + col * 2}" y="{ground - 62 + r * 2:g}" width="2" height="2"/>'
                         for col, r, _ in pixels("+1"))
    plus = f'<g opacity="0" fill="{PLUS_COLOR}" style="animation:plus{i} {timing}">{plus_rects}</g>'
    return bug, spark + plus, css


# mata berkedip, ekor kucing mengibas saat tidur, "z" melayang
dev_h = len(DEV_POSES["stand"]) * SPRITE_PX
eyes = "".join(f'<rect x="{c * SPRITE_PX}" y="{4 * SPRITE_PX - dev_h}" width="{SPRITE_PX}" height="{SPRITE_PX}" fill="{DEV_COLORS["S"]}"/>'
               for c, bit in enumerate(DEV_BODY[4]) if bit == "E")
dev_extra = f'<g opacity="0" style="animation:wink 4.5s step-end infinite">{eyes}</g>'
tail_tips = "".join(f'<rect x="0" y="{r * SPRITE_PX - 7 * SPRITE_PX}" width="{SPRITE_PX}" height="{SPRITE_PX}" fill="{CAT_COLORS["#"]}" '
                    f'opacity="{1 - k}" style="animation:tail{k} 1.6s step-end infinite"/>'
                    for k, r in enumerate([6, 5]))

dev_svg, dev_css, _ = character("dv", DEV_POSES, DEV_COLORS, dev_w, dev_intro, "stand", dev_loop, dev_extra)
cat_svg, cat_css, _ = character("ct", CAT_POSES, CAT_COLORS, cat_w, cat_intro, "sleep", pose_extra={"sleep": tail_tips})

zzz = "".join(f'<g opacity="0" style="animation:zz 3s linear {cat_done + k:.2f}s infinite">'
              f'{sprite(ZZZ, {"#": "#8b949e"}, cat_rest_x + 30, ground - 30, 2)}</g>' for k in range(3))

bug_svg, effects, bug_css = [], [], []
for i, (bug_x, spawn, kill) in enumerate(bugs):
    part, effect, part_css = bug_parts(i, bug_x, spawn, kill)
    bug_svg.append(part)
    effects.append(effect)
    bug_css += part_css


def build_time(cx):
    """Detik saat ujung kaki depan developer mencapai kolom bertitik tengah cx."""
    for kind, t0, t1, xa, xb, _ in dev_intro:
        if kind == "walk" and xb + dev_w >= cx:
            return t0 + max(0, cx - dev_w - xa) / SPEED
        if kind != "walk" and xb + dev_w >= cx:
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
busy = {(c, r) for c in range(name_c0 - 1, name_c0 + width(NAME) + 1) for r in range(name_r0 - 5, name_r0 + 8)}
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
.lg{{font:11px -apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif;fill:#7d8590}}
@keyframes grow{{0%{{fill-opacity:0;fill:{LEVELS[3]}}}25%{{fill-opacity:1;fill:#f3e8ff}}}}
@keyframes shine{{3%{{fill:#f3e8ff}}6%{{fill:{NAME_COLOR}}}}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes wink{{0%{{opacity:0}}96%{{opacity:1}}}}
@keyframes tail0{{50%{{opacity:0}}}}
@keyframes tail1{{50%{{opacity:1}}}}
@keyframes leg0{{50%{{opacity:0}}}}
@keyframes leg1{{50%{{opacity:1}}}}
@keyframes crawl{{from{{transform:translateX(-5px)}}to{{transform:translateX(5px)}}}}
@keyframes zz{{0%{{opacity:0;transform:none}}20%{{opacity:1}}100%{{opacity:0;transform:translate(10px,-24px)}}}}
@keyframes caret{{{"".join(frames)}}}
{"".join(f"@keyframes tw{k}{{50%{{fill:{LEVELS[k]}}}}}" for k in (2, 3, 4))}
{"".join(dev_css + cat_css + bug_css)}
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
<g clip-path="url(#card)">{"".join(bug_svg)}{cat_svg}{zzz}{dev_svg}{"".join(effects)}</g>
{"".join(tagline)}
<rect class="caret" x="{caret_x}" y="{tag_y}" width="{3 * TAG_PITCH}" height="{7 * TAG_PITCH}" fill="{LEVELS[4]}"/>
<text class="lg" x="{gx + legend_c0 * PITCH - 6}" y="{legend_y + 10}" text-anchor="end">Less</text>
{"".join(legend)}
<text class="lg" x="{gx + (legend_c0 + 5) * PITCH + 4}" y="{legend_y + 10}">More</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"banner.svg: {len(svg) // 1024} KB, nama jadi di detik {dev_done:.1f}, "
      f"berburu bug mulai detik {LOOP_START:.1f}, satu putaran {period:.1f} detik")
