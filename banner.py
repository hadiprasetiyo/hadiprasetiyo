"""Generator banner.svg: nama dibangun di grid kontribusi ala GitHub oleh karakter pixel,
lalu bug datang merusak dan developer + kucingnya memperbaiki, berulang tanpa henti.

Ubah NAME / TAGLINE / BITE / TAG_BITE lalu jalankan: python banner.py
"""
import math
import random

NAME = "HADI PRASETIYO"
TAGLINE = "> FULL-STACK SOFTWARE ENGINEER"
BITE = (5, 6)  # index huruf NAME yang digigit bug; bersebelahan & di kanan celah kata
TAG_BITE = 3  # jumlah huruf terakhir tagline yang dimakan bug kedua

W, H = 1200, 300
PITCH = 12  # jarak antar sel grid
TAG_PITCH = 4  # piksel tagline; 3 piksel tagline = 1 sel grid
SPRITE_PX = 3  # ukuran piksel karakter
SPEED = 300  # kecepatan lari (px/detik)
REPAIR_SPEED = 140  # jalan pelan sambil menambal huruf
STEP = 0.1  # durasi satu langkah kaki
HURDLE_T, STOMP_T, POUNCE_T = 0.34, 0.36, 0.45

# skala ungu ala grafik kontribusi GitHub (dark), level 0..4
LEVELS = ["#161b22", "#3c1e70", "#553098", "#8957e5", "#bc8cff"]
NAME_COLOR = "#d2a8ff"
TEXT_COLOR = "#c9d1d9"
FLASH = "#f3e8ff"
BUG_COLOR = "#f85149"  # merah = bug / test gagal
PLUS_COLOR = "#3fb950"  # hijau = +1 kontribusi / test lulus
ALERT_COLOR = "#d29922"

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
LAPTOP_COLORS = {"#": "#8b949e", "c": NAME_COLOR, "s": LEVELS[1]}
LAPTOP = [[".######.", ".#cscs#.", ".#sccs#.", "########"],
          [".######.", ".#ccsc#.", ".#cssc#.", "########"]]

CAT_COLORS = {"#": "#c9d1d9", "E": "#0d1117", "n": "#f2a6b8", "-": "#6e7681"}
CAT_TOP = ["#.....#...#", "#.....#####", "#.....#E#E#", ".#....##n##", "..#########", "..########."]
CAT_POSES = {"stand": CAT_TOP + ["..#.#..#.#."],
             "a": CAT_TOP + [".#..#...#.#"],
             "b": CAT_TOP + ["...#.#.#.#."],
             # tidur meringkuk, ujung ekor digambar terpisah supaya bisa mengibas
             "sleep": ["...........", "......#...#", "......#####", "......#-#-#",
                       "......##n##", "..#########", ".#########."]}

BUG_A = ["#...#", ".###.", "#####", ".###.", "#.#.#"]
BUG_POSES = {"stand": BUG_A, "a": BUG_A, "b": ["#...#", ".###.", ".###.", "#####", ".#.#."]}
ZZZ = ["####", "..#.", ".#..", "####"]
ALERT = ["#", "#", "#", ".", "#"]

CSS = []  # semua @keyframes dikumpulkan di sini


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


def keyframes(name, points, dur):
    """points: [(detik, deklarasi css)] -> @keyframes dalam persen dari dur."""
    CSS.append(f"@keyframes {name}{{" + "".join(f"{t / dur * 100:.3f}%{{{css}}}" for t, css in points) + "}")
    return name


def visible(name, intervals, dur):
    """Keyframes opacity: tampil hanya di dalam interval [(t0, t1)]; t1 None = terus tampil."""
    points = [(0, "opacity:0")]
    for a, b in intervals:
        points += [(a, "opacity:1")] + ([(b, "opacity:0")] if b is not None else [])
    return keyframes(name, points, dur)


random.seed(7)  # supaya hasil generate selalu sama

# --- tata letak: grid digeser supaya nama jatuh tepat di sel
name_w = width(NAME) * PITCH
name_x = (W - name_w) // 2
top = (H - 13 * PITCH) // 2  # 7 baris nama + 3 jarak + 3 baris tagline
gx, gy = name_x % PITCH, top % PITCH
cols, rows = (W - gx) // PITCH, (H - gy) // PITCH
name_c0, name_r0 = (name_x - gx) // PITCH, (top - gy) // PITCH
ground = gy + name_r0 * PITCH + 1.5  # lantai 1: sisi atas huruf nama

tag_w = width(TAGLINE) * TAG_PITCH
tag_x = (W - tag_w) // 2
tag_r0 = name_r0 + 10
tag_y = gy + tag_r0 * PITCH + (3 * PITCH - 7 * TAG_PITCH) // 2
floor2 = gy + (tag_r0 + 3) * PITCH - 1.5  # lantai 2: dasar baris terminal tagline
caret_x = tag_x + tag_w + TAG_PITCH
starts, ends, col = [], [], 0
for ch in TAGLINE:
    starts.append(col)
    col += len(FONT[ch].split()[0])
    ends.append(col)
    col += 1


def glyph_center(i):
    return tag_x + (starts[i] + ends[i]) / 2 * TAG_PITCH


def caret_shift(i):
    """Geseran kursor supaya berdiri tepat setelah huruf ke-i tagline."""
    return tag_x + (ends[i] + 1) * TAG_PITCH - caret_x


dev_w = len(DEV_BODY[0]) * SPRITE_PX
cat_w = len(CAT_TOP[0]) * SPRITE_PX
bug_w = len(BUG_A[0]) * SPRITE_PX
cat_bed_x = caret_x + 3 * TAG_PITCH + 14  # kucing tidur di sebelah kursor

# celah antar kata = rintangan yang dilompati (kiri, kanan, tinggi lompat, inset)
lit_cols = {col for col, _, _ in pixels(NAME)}
pits, run_start = [], None
for col in range(width(NAME) + 1):
    if col not in lit_cols and run_start is None:
        run_start = col
    elif col in lit_cols and run_start is not None:
        if col - run_start >= 3:  # celah antar huruf cuma 1 kolom, antar kata >= 3
            pits.append((name_x + run_start * PITCH, name_x + col * PITCH, 22, 0.35))
        run_start = None


class Track:
    """Lintasan satu karakter: segmen (jenis, t0, t1, x0, x1, y0, y1, tinggi lompat / arah)."""

    def __init__(self, x, y, pose="stand", face="r"):
        self.segs, self.t, self.x, self.y = [], 0, x, y
        self.start = (x, y, pose, face)

    def add(self, kind, dur, x=None, y=None, h=0):
        x = self.x if x is None else x
        y = self.y if y is None else y
        self.segs.append((kind, self.t, self.t + dur, self.x, x, self.y, y, h))
        self.t, self.x, self.y = self.t + dur, x, y
        return self

    def until(self, t, kind="rest"):
        return self.add(kind, max(0, t - self.t))

    def rest(self, dur):
        return self.add("rest", dur)

    def sleep(self, dur):
        return self.add("sleep", dur)

    def turn(self, face):
        return self.add("turn", 0, h=face)

    def fall(self, y, dur=0.4):
        return self.add("fall", dur, y=y)

    def walk(self, x, speed=SPEED):
        return self.add("walk", abs(x - self.x) / speed, x)

    def jump(self, x, y=None, h=22, dur=HURDLE_T):
        return self.add("jump", dur, x, y, h)

    def run(self, target, w, obstacles=()):
        """Lari ke target sambil melompati rintangan di antaranya."""
        d = 1 if target >= self.x else -1
        hurdles = []
        for a, b, height, inset in obstacles:
            inset *= w
            take, land = (a - w + inset, b - inset) if d > 0 else (b - inset, a - w + inset)
            if d * (take - self.x) >= 0 and d * (target - land) >= 0:
                hurdles.append((take, land, height))
        for take, land, height in sorted(hurdles, key=lambda h: d * h[0]):
            self.walk(take).jump(land, h=height)
        return self.walk(target)


def motion(track):
    """Titik (t, x, y) lintasan; jatuh & lompat disampling supaya melengkung."""
    x, y = track.start[:2]
    pts = [(0, x, y)]
    for kind, t0, t1, xa, xb, ya, yb, h in track.segs:
        if kind not in ("fall", "jump"):
            pts.append((t1, xb, yb))
            continue
        for k in range(1, 11):
            f = k / 10
            y = ya + (yb - ya) * f * f if kind == "fall" else ya + (yb - ya) * f - 4 * h * f * (1 - f)
            pts.append((t0 + (t1 - t0) * f, xa + (xb - xa) * f, y))
    return pts


def poses_of(track):
    """Pergantian pose: a/b saat lari, a saat di udara, stand/sleep saat diam."""
    events = [(0, track.start[2])]
    for kind, t0, t1, *_ in track.segs:
        if kind == "walk":
            k = 0
            while t0 + k * STEP < t1:
                events.append((t0 + k * STEP, "ab"[k % 2]))
                k += 1
        elif kind in ("fall", "jump"):
            events.append((t0, "a"))
        elif kind in ("rest", "sleep"):
            events.append((t0, "stand" if kind == "rest" else "sleep"))
    last = [s[0] for s in track.segs if s[0] != "turn"][-1]
    events.append((track.t, "sleep" if last == "sleep" else "stand"))
    return events


def facings_of(track):
    events = [(0, track.start[3])]
    for kind, t0, _, xa, xb, *_, h in track.segs:
        face = h if kind == "turn" else ("r" if xb > xa else "l") if xb != xa else None
        if face and face != events[-1][1]:
            events.append((t0, face))
    return events


def actor(key, poses, colors, w, phases, base, extra="", pose_extra=None, wrap="", flip=True):
    """Karakter bergerak sesuai phases [(track, timing)]; base = (x, y, pose, hadap) tanpa animasi."""
    pose_extra = pose_extra or {}
    face_css = {"r": "none", "l": f"matrix(-1,0,0,1,{w},0)"}
    move, face, pose_anims = [], [], {pose: [] for pose in poses}
    for p, (track, timing) in enumerate(phases):
        dur = track.t
        name = keyframes(f"{key}m{p}", [(t, f"transform:translate({x:.1f}px,{y:.1f}px)") for t, x, y in motion(track)], dur)
        move.append(f"{name} {dur:.3f}s linear {timing}")
        events = poses_of(track)
        for pose in poses:
            name = keyframes(f"{key}{pose}{p}", [(t, f"opacity:{int(e == pose)}") for t, e in events], dur)
            pose_anims[pose].append(f"{name} {dur:.3f}s step-end {timing}")
        if flip:
            name = keyframes(f"{key}f{p}", [(t, f"transform:{face_css[f]}") for t, f in facings_of(track)], dur)
            face.append(f"{name} {dur:.3f}s step-end {timing}")
    groups = "".join(f'<g opacity="{int(pose == base[2])}" style="animation:{",".join(pose_anims[pose])}">'
                     f'{sprite(rows_, colors)}{pose_extra.get(pose, "")}</g>' for pose, rows_ in poses.items())
    inner = groups + extra  # extra (laptop, kedipan mata) harus di atas badan
    if wrap:
        inner = f"<g {wrap}>{inner}</g>"
    if flip:
        inner = f'<g style="transform:{face_css[base[3]]};animation:{",".join(face)}">{inner}</g>'
    return (f'<g style="transform:translate({base[0]:.1f}px,{base[1]:.1f}px);animation:{",".join(move)}">'
            f"{inner}</g>")


# ================= intro: developer membangun nama, kucing masuk ke baris terminal lalu tidur
dev_rest_x = name_x + name_w - dev_w
dev_intro = (Track(name_x - 4, -60, pose="a").until(0.2).fall(ground)
             .run(dev_rest_x, dev_w, pits).jump(dev_rest_x, h=14, dur=0.35))
dev_done = dev_intro.t
cat_intro = Track(W + 15, floor2, pose="a", face="l").until(1.0).walk(cat_bed_x, 90).turn("r").rest(0.5).sleep(0.01)
cat_done = cat_intro.t
LOOP_START = dev_done + 2.5  # loop mulai setelah tagline selesai diketik

# ================= babak 1: bug menggigit nama, developer menginjak lalu menambal
bite_c0 = width(NAME[:BITE[0]]) + 1
bite_c1 = width(NAME[:BITE[-1] + 1]) - 1
bug1_x0 = name_x + bite_c0 * PITCH  # sisi kiri bug saat mendarat
bug1_c1 = name_x + (bite_c1 + 1) * PITCH  # titik tengah bug saat diinjak
drop_t, t_land = 0.6, 0.9

dev = Track(dev_rest_x, ground).until(t_land + 0.8)
stomp_x = bug1_c1 - dev_w / 2
dev.run(stomp_x + 48, dev_w, pits).jump(stomp_x, h=26, dur=STOMP_T)
t_stomp = dev.t
dev.rest(0.25)
repair_t0, repair_x0 = dev.t, dev.x
dev.walk(bug1_x0 - 6, REPAIR_SPEED)
t_repaired = dev.t
dev.rest(0.4).run(dev_rest_x, dev_w, pits)
t_back = dev.t

vb1 = (bug1_c1 - bug_w / 2 - bug1_x0) / (t_stomp - t_land)
bug1 = Track(bug1_x0, -20, pose="a").until(drop_t).fall(ground, 0.3).walk(bug1_c1 - bug_w / 2, vb1)

damage = {}  # (kolom, baris) sel nama -> (detik dimakan, detik ditambal)
for col, r, _ in pixels(NAME):
    if bite_c0 <= col <= bite_c1 and r <= 1:
        t_eat = t_land + (name_x + (col + 1) * PITCH - bug1_x0) / vb1 + r * 0.08  # setelah bug lewat
        if t_eat < t_stomp:
            cx = name_x + (col + 0.5) * PITCH
            damage[col, r] = (t_eat, repair_t0 + max(0, repair_x0 - cx) / REPAIR_SPEED + r * 0.06)

# ================= babak 2: bug memakan ujung tagline, kucing menerkam, developer mengetik ulang
bitten = list(range(len(TAGLINE) - TAG_BITE, len(TAGLINE)))
target_c = glyph_center(bitten[0]) - 6  # titik tengah bug saat diterkam
cat_c = cat_bed_x + cat_w / 2
REACT = 1.2  # kucing masih ngantuk sebelum menerkam
vb2 = (cat_c - target_c) / (REACT + POUNCE_T)
bug2_x0, t2 = W + 10, t_back - 1.0
t_wake = t2 + (bug2_x0 + bug_w / 2 - cat_c) / vb2
t_pounce = t_wake + REACT + POUNCE_T
bug2 = Track(bug2_x0, floor2, pose="a").until(t2).walk(target_c - bug_w / 2, vb2)
glyph_eat = {i: t2 + (bug2_x0 + bug_w / 2 - glyph_center(i)) / vb2 for i in bitten}
glyph_fix = {i: t_pounce + 0.7 + k * 0.25 for k, i in enumerate(bitten)}
typing = (t_pounce + 0.2, glyph_fix[bitten[-1]] + 0.4)

cat = (Track(cat_bed_x, floor2, pose="sleep").until(t_wake, "sleep").rest(REACT)
       .jump(target_c - cat_w / 2, h=26, dur=POUNCE_T).rest(0.6).walk(cat_bed_x, 70).turn("r").rest(0.4))
t_asleep = cat.t
PERIOD = max(t_asleep + 2.5, typing[1] + 2)
cat.until(PERIOD, "sleep")
dev.until(PERIOD)
bug1.until(PERIOD)
bug2.until(PERIOD)
LOOP = f"{LOOP_START:.2f}s infinite"


def loop_anim(name, points, timing="linear"):
    return f"{keyframes(name, points, PERIOD)} {PERIOD:.3f}s {timing} {LOOP}"


def bug_actor(key, track, t_show, t_squash):
    """Bug yang tampil sejak t_show dan gepeng saat t_squash."""
    flat = "transform:scale(1.5,.3)"
    anim = loop_anim(f"{key}sq", [(0, "opacity:0"), (t_show, "opacity:0"), (t_show + 0.01, "opacity:1;transform:none"),
                                  (t_squash, "opacity:1;transform:none"), (t_squash + 0.06, f"opacity:1;{flat}"),
                                  (t_squash + 0.3, f"opacity:0;{flat}"), (PERIOD, f"opacity:0;{flat}")])
    colors = {"#": BUG_COLOR}
    return actor(key, BUG_POSES, colors, bug_w, [(track, LOOP)], (*track.start[:2], "stand", "r"),
                 wrap=f'opacity="0" style="transform-origin:{bug_w / 2}px 0;animation:{anim}"', flip=False)


def spark(key, cx, cy, t):
    dots = "".join(f'<rect x="{cx + dx - 1.5:g}" y="{cy + dy - 1.5:g}" width="3" height="3" fill="{FLASH}"/>'
                   for dx, dy in [(-20, 0), (20, 0), (-15, -12), (15, -12)])
    anim = loop_anim(key, [(0, "opacity:0"), (t, "opacity:0;transform:scale(.4)"), (t + 0.03, "opacity:1;transform:scale(.6)"),
                           (t + 0.4, "opacity:0;transform:scale(1.8)"), (PERIOD, "opacity:0")])
    return f'<g opacity="0" style="transform-box:fill-box;transform-origin:50% 100%;animation:{anim}">{dots}</g>'


def plus_one(key, cx, y, t):
    rects = "".join(f'<rect x="{cx - 9 + col * 2:g}" y="{y + r * 2:g}" width="2" height="2"/>' for col, r, _ in pixels("+1"))
    anim = loop_anim(key, [(0, "opacity:0"), (t, "opacity:0;transform:none"), (t + 0.05, "opacity:1;transform:none"),
                           (t + 1, "opacity:0;transform:translateY(-18px)"), (PERIOD, "opacity:0")])
    return f'<g opacity="0" fill="{PLUS_COLOR}" style="animation:{anim}">{rects}</g>'


def alert(key, w, h, intervals):
    anim = f"{visible(key, intervals, PERIOD)} {PERIOD:.3f}s step-end {LOOP}"
    return f'<g opacity="0" style="animation:{anim}">{sprite(ALERT, {"#": ALERT_COLOR}, w / 2 - 1.5, -h - 21)}</g>'


# --- developer: mata berkedip, tanda "!", laptop saat mengetik perbaikan
dev_h = len(DEV_POSES["stand"]) * SPRITE_PX
eyes = "".join(f'<rect x="{c * SPRITE_PX}" y="{4 * SPRITE_PX - dev_h}" width="{SPRITE_PX}" height="{SPRITE_PX}" fill="{DEV_COLORS["S"]}"/>'
               for c, bit in enumerate(DEV_BODY[4]) if bit == "E")
laptop_frames = "".join(f'<g opacity="{1 - k}" style="animation:swap{k} .3s step-end infinite">'
                        f'{sprite(rows_, LAPTOP_COLORS, 1.5, (7 - 13) * SPRITE_PX)}</g>' for k, rows_ in enumerate(LAPTOP))
laptop_anim = f"{visible('laptop', [typing], PERIOD)} {PERIOD:.3f}s step-end {LOOP}"
dev_extra = (f'<g opacity="0" style="animation:wink 4.5s step-end infinite">{eyes}</g>'
             + alert("dvalert", dev_w, dev_h, [(t_land + 0.2, t_land + 0.8)]))
dev_svg = actor("dv", DEV_POSES, DEV_COLORS, dev_w, [(dev_intro, "0s both"), (dev, LOOP)], (dev_rest_x, ground, "stand", "r"),
                extra=dev_extra + f'<g opacity="0" style="animation:{laptop_anim}">{laptop_frames}</g>')

# --- kucing: ekor mengibas & "z" melayang saat tidur, "!" saat terbangun
cat_h = len(CAT_POSES["stand"]) * SPRITE_PX
tail_tips = "".join(f'<rect x="0" y="{r * SPRITE_PX - cat_h}" width="{SPRITE_PX}" height="{SPRITE_PX}" fill="{CAT_COLORS["#"]}" '
                    f'opacity="{1 - k}" style="animation:swap{k} 1.6s step-end infinite"/>' for k, r in enumerate([6, 5]))
zzz = "".join(f'<g opacity="0" style="animation:zz 3s linear {k}s infinite">{sprite(ZZZ, {"#": "#8b949e"}, 30, -26, 2)}</g>'
              for k in range(3))
z_intro = f"{visible('zi', [(cat_done, None)], cat_done + 1)} {cat_done + 1:.3f}s step-end both"
z_loop = f"{visible('zl', [(0, t_wake), (t_asleep, PERIOD)], PERIOD)} {PERIOD:.3f}s step-end {LOOP}"
cat_extra = f'<g opacity="0" style="animation:{z_intro},{z_loop}">{zzz}</g>' + alert("ctalert", cat_w, cat_h, [(t_wake, t_wake + 0.7)])
cat_svg = actor("ct", CAT_POSES, CAT_COLORS, cat_w, [(cat_intro, "0s both"), (cat, LOOP)], (cat_bed_x, floor2, "sleep", "r"),
                extra=cat_extra, pose_extra={"sleep": tail_tips})

bugs_svg = bug_actor("b1", bug1, drop_t, t_stomp) + bug_actor("b2", bug2, t2, t_pounce)
effects = (spark("s1", bug1_c1, ground, t_stomp) + plus_one("p1", bug1_x0 - 6 + dev_w / 2, ground - 62, t_repaired)
           + spark("s2", target_c, floor2, t_pounce)
           + plus_one("p2", glyph_center(bitten[1]), tag_y - 22, glyph_fix[bitten[-1]]))


def build_time(cx):
    """Detik saat ujung kaki depan developer mencapai kolom bertitik tengah cx."""
    for kind, t0, t1, xa, xb, *_ in dev_intro.segs:
        if kind == "walk" and xb + dev_w >= cx:
            return t0 + max(0, cx - dev_w - xa) / SPEED
        if kind in ("fall", "jump") and xb + dev_w >= cx:
            return t1
    return dev_done


def cell(c, r, extra):
    return f'<rect x="{gx + c * PITCH + 1.5}" y="{gy + r * PITCH + 1.5}" width="9" height="9" rx="2" {extra}/>'


# --- nama: tumbuh saat diinjak; sel yang digigit bug hilang lalu ditambal
name_cells = []
for k, (col, r, _) in enumerate(pixels(NAME)):
    grow = build_time(name_x + (col + 0.5) * PITCH) + r * 0.025
    shine = dev_done + 1.5 + col * 0.012
    rect = cell(name_c0 + col, name_r0 + r, f'class="n" style="animation-delay:{grow:.2f}s,{shine:.2f}s"')
    if (col, r) not in damage:
        name_cells.append(rect)
        continue
    eat, fix = damage[col, r]
    gone = loop_anim(f"nd{k}", [(0, "opacity:1"), (eat, "opacity:1"), (eat + 0.18, "opacity:0"),
                                (fix, "opacity:0"), (fix + 0.01, "opacity:1"), (PERIOD, "opacity:1")])
    flash = loop_anim(f"nf{k}", [(0, f"opacity:0;fill:{BUG_COLOR}"), (eat - 0.01, f"opacity:0;fill:{BUG_COLOR}"),
                                 (eat, f"opacity:1;fill:{BUG_COLOR}"), (eat + 0.18, f"opacity:0;fill:{BUG_COLOR}"),
                                 (fix, f"opacity:0;fill:{FLASH}"), (fix + 0.01, f"opacity:1;fill:{FLASH}"),
                                 (fix + 0.35, f"opacity:0;fill:{FLASH}"), (PERIOD, "opacity:0")])
    name_cells.append(f'<g style="animation:{gone}">{rect}</g>' + cell(name_c0 + col, name_r0 + r, f'opacity="0" style="animation:{flash}"'))

# --- tagline: prompt ">" langsung tampil, sisanya diketik; huruf yang dimakan bug diketik ulang
type_start, step = dev_done + 0.1, 0.045
caret_dur = type_start + (len(TAGLINE) - 2) * step
caret_intro = [(0, f"transform:translateX({caret_shift(0)}px)")]
caret_intro += [(type_start + (i - 1) * step, f"transform:translateX({caret_shift(i)}px)") for i in range(1, len(TAGLINE))]
caret_loop = [(0, "transform:none"), (t_pounce + 0.5, f"transform:translateX({caret_shift(bitten[0] - 1)}px)")]
caret_loop += [(glyph_fix[i], f"transform:translateX({caret_shift(i)}px)") for i in bitten]
caret_anim = (f"{keyframes('caret', caret_intro, caret_dur)} {caret_dur:.2f}s step-end both,blink 1s step-end infinite,"
              + loop_anim("caretfix", caret_loop, "step-end"))

tag_groups = {}
for col, r, i in pixels(TAGLINE):
    tag_groups.setdefault(i, []).append(f'<rect x="{tag_x + col * TAG_PITCH}" y="{tag_y + r * TAG_PITCH}" width="3" height="3"/>')
tagline = []
for i, rects in tag_groups.items():
    if i == 0:
        tagline.append(f'<g fill="{NAME_COLOR}">{"".join(rects)}</g>')
        continue
    group = f'<g class="t" style="animation-delay:{type_start + (i - 1) * step:.3f}s">{"".join(rects)}</g>'
    if i in bitten:
        eat, fix = glyph_eat[i], glyph_fix[i]
        gone = loop_anim(f"gd{i}", [(0, "opacity:1"), (eat, "opacity:1"), (eat + 0.15, "opacity:0"),
                                    (fix - 0.01, "opacity:0"), (fix, "opacity:1"), (PERIOD, "opacity:1")])
        red = loop_anim(f"gr{i}", [(0, "opacity:0"), (eat - 0.01, "opacity:0"), (eat, "opacity:1"), (eat + 0.2, "opacity:0"), (PERIOD, "opacity:0")])
        group = f'<g style="animation:{gone}">{group}</g><g opacity="0" fill="{BUG_COLOR}" style="animation:{red}">{"".join(rects)}</g>'
    tagline.append(group)

# --- latar: grid kontribusi; dikosongkan di jalur karakter, baris terminal, legend
busy = {(c, r) for c in range(name_c0 - 1, name_c0 + width(NAME) + 1) for r in range(name_r0 - 5, name_r0 + 8)}
hole_c0 = (tag_x - gx) // PITCH - 1
hole_c1 = (cat_bed_x + cat_w - gx) // PITCH + 1
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
.lg{{font:11px -apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif;fill:#7d8590}}
@keyframes grow{{0%{{fill-opacity:0;fill:{LEVELS[3]}}}25%{{fill-opacity:1;fill:{FLASH}}}}}
@keyframes shine{{3%{{fill:{FLASH}}}6%{{fill:{NAME_COLOR}}}}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes wink{{0%{{opacity:0}}96%{{opacity:1}}}}
@keyframes swap0{{50%{{opacity:0}}}}
@keyframes swap1{{50%{{opacity:1}}}}
@keyframes zz{{0%{{opacity:0;transform:none}}20%{{opacity:1}}100%{{opacity:0;transform:translate(10px,-24px)}}}}
{"".join(f"@keyframes tw{k}{{50%{{fill:{LEVELS[k]}}}}}" for k in (2, 3, 4))}
{"".join(CSS)}
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
{"".join(tagline)}
<rect x="{caret_x}" y="{tag_y}" width="{3 * TAG_PITCH}" height="{7 * TAG_PITCH}" fill="{LEVELS[4]}" style="animation:{caret_anim}"/>
<g clip-path="url(#card)">{bugs_svg}{cat_svg}{dev_svg}{effects}</g>
<text class="lg" x="{gx + legend_c0 * PITCH - 6}" y="{legend_y + 10}" text-anchor="end">Less</text>
{"".join(legend)}
<text class="lg" x="{gx + (legend_c0 + 5) * PITCH + 4}" y="{legend_y + 10}">More</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"banner.svg: {len(svg) // 1024} KB, nama jadi di detik {dev_done:.1f}, "
      f"loop mulai detik {LOOP_START:.1f}, satu putaran {PERIOD:.1f} detik")
