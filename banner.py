"""Generator banner.svg: ruang kerja developer pixel di samping nama di grid kontribusi GitHub.

Developer mengetik dan piksel dari monitornya membangun nama; bug keluar dari layar merusak
nama, kucing menangkapnya, developer menambal. Lalu kucing duduk di keyboard dan mengacaukan
tagline. Berulang tanpa henti. Ubah NAME / TAGLINE / BITE lalu jalankan: python banner.py
"""
import math
import random
from functools import partial

import pixelart
from pixelart import CAT_COLORS, CAT_POSES, CAT_TOP, FONT, pixels, width

NAME = "HADI PRASETIYO"
TAGLINE = "> FULL-STACK SOFTWARE ENGINEER"
BITE = (9, 10)  # index huruf NAME yang digerogoti bug (bersebelahan)
GARBLE = [i for i, ch in enumerate(TAGLINE) if ch != " "][14:18]  # huruf tagline yang diacak kucing

W, H = 1200, 300
PITCH, CELL = 10, 8  # grid kontribusi: jarak & ukuran sel
TAG_PITCH = 4  # piksel tagline
PX = 4  # ukuran piksel karakter & perabot
SPEED = 300  # kecepatan lari kucing (px/detik)
STEP = 0.1  # durasi satu langkah kaki
FLY_T = 0.65  # lama piksel terbang dari layar ke nama

LEVELS = ["#161b22", "#3c1e70", "#553098", "#8957e5", "#bc8cff"]  # level kontribusi, versi ungu
NAME_COLOR = "#d2a8ff"
TEXT_COLOR = "#c9d1d9"
FLASH = "#f3e8ff"
BUG_COLOR = "#f85149"  # merah = bug
PLUS_COLOR = "#3fb950"  # hijau = +1 / beres
ALERT_COLOR = "#d29922"
HEART_COLOR = "#f778ba"
sprite = partial(pixelart.sprite, px=PX)

# ---------------------------------------------------------------- sprite (menghadap kanan)
DEV_COLORS = {"B": "#d2a8ff", "b": "#a371f7", "S": "#f2cfa8", "E": "#0d1117",
              "H": "#8957e5", "P": "#6e7681", "W": "#e6edf3"}
WALK_BODY = ["..BBBBB..", ".BBBBBBB.", ".bbbbbbb.", ".SSSSSSS.", ".SSSESES.", ".SSSSSSS.",
             "..HHHHH..", ".HHHHHHH.", ".HHHHHHH.", ".SHHHHHS.", "..PPPPP.."]
SIT_HEAD = ["...BBBBB.....", "..BBBBBBB....", "..bbbbbbb....", "..SSSSSSS....", "..SSSSESE....", "..SSSSSSS...."]
SIT_LEGS = ["..PPPPPPPPP..", "..PPPPPPPPP..", ".........PP..", ".........PP..", ".........WWW."]
DEV_POSES = {
    "stand": WALK_BODY + ["..PP.PP..", "..WW.WW.."],
    "a": WALK_BODY + [".PP...PP.", ".WW...WW."],
    "b": WALK_BODY + ["...PPP...", "...WWW..."],
    "sit_a": SIT_HEAD + ["...HHHHH.....", "..HHHHHHHHSS.", "..HHHHHHH....", "..HHHHHHH...."] + SIT_LEGS,
    "sit_b": SIT_HEAD + ["...HHHHH.....", "..HHHHHHH....", "..HHHHHHHHSS.", "..HHHHHHH...."] + SIT_LEGS,
}
TYPING = ["sit_a", "sit_b"]
CHAIR = ["CC", "CC", "CC", "CC", "CC", "CC", "CC", "CC", "CCCCCCCCC", ".C.....C.", ".C.....C."]  # sejajar baris 4..14 pose duduk

BUG_COLORS = {"#": BUG_COLOR, "w": "#c9d1d9"}
BUG_WALK = ["#...#", ".###.", "#####", ".###.", "#.#.#"]
BUG_POSES = {"stand": BUG_WALK, "a": BUG_WALK, "b": ["#...#", ".###.", ".###.", "#####", ".#.#."],
             "fa": (["ww...ww", ".w###w.", "..###..", ".#####.", "..###.."], -1),  # sayap naik
             "fb": ([".......", "ww###ww", "..###..", ".#####.", "..###.."], -1)}  # sayap turun
ZZZ = ["####", "..#.", ".#..", "####"]
ALERT = ["#", "#", "#", ".", "#"]
HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
CHECK = ["......#", ".....##", "#...##.", "##.##..", ".###...", "..#...."]
CROSS = ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"]
MUG = ["MMMM.", "MMMMM", "MMMMM", "MMMM."]

CSS = []  # semua @keyframes dikumpulkan di sini



def keyframes(name, points, dur):
    """points: [(detik, deklarasi css)] -> @keyframes dalam persen dari dur."""
    CSS.append(f"@keyframes {name}{{" + "".join(f"{min(t, dur) / dur * 100:.3f}%{{{css}}}" for t, css in points) + "}")
    return name


def opacity_points(intervals):
    """Tampil hanya di dalam interval [(t0, t1)]; t1 None = terus tampil."""
    points = [(0, "opacity:0")]
    for a, b in intervals:
        points += [(a, "opacity:1")] + ([(b, "opacity:0")] if b is not None else [])
    return points


def alternate(t0, t1, poses, rate):
    """Pose bergantian tiap `rate` detik, mis. tangan mengetik."""
    out, k = [], 0
    while t0 + k * rate < t1:
        out.append((t0 + k * rate, poses[k % len(poses)]))
        k += 1
    return out


random.seed(7)  # supaya hasil generate selalu sama

# ---------------------------------------------------------------- tata letak
name_w = width(NAME) * PITCH
SCENE_W = 50 * PX  # lebar meja kerja
name_x = (W - name_w - 50 - SCENE_W) // 2 // PITCH * PITCH
floor = 170  # lantai: dasar nama & kaki perabot
name_top = floor - 7 * PITCH
gx, gy = name_x % PITCH, name_top % PITCH
cols, rows = (W - gx) // PITCH, (H - gy) // PITCH
name_c0, name_r0 = (name_x - gx) // PITCH, (name_top - gy) // PITCH

tag_w = width(TAGLINE) * TAG_PITCH
tag_x = name_x + (name_w - tag_w) // 2
tag_r0 = name_r0 + 9
tag_y = gy + tag_r0 * PITCH + (3 * PITCH - 7 * TAG_PITCH) // 2
caret_x = tag_x + tag_w + TAG_PITCH
starts, ends, col = [], [], 0
for ch in TAGLINE:
    starts.append(col)
    col += len(FONT[ch].split()[0])
    ends.append(col)
    col += 1


def caret_shift(i):
    """Geseran kursor supaya berdiri tepat setelah huruf ke-i tagline."""
    return tag_x + (ends[i] + 1) * TAG_PITCH - caret_x


# meja kerja: kursi + developer duduk, keyboard, monitor, cangkir
# ukuran dalam satuan piksel sprite supaya ikut membesar bila PX diubah
sit_x = name_x + name_w + 50
desk_x0, desk_x1, desk_y = sit_x + 11 * PX, sit_x + SCENE_W, floor - 7 * PX  # meja setinggi tangan
key_x0, key_x1 = sit_x + 10 * PX, sit_x + 20 * PX
mon_x, mon_y, mon_w, mon_h = sit_x + 22 * PX, floor - 21 * PX, 18 * PX, 12 * PX
screen_cx, screen_cy = mon_x + mon_w / 2, mon_y + mon_h / 2
mug_x = sit_x + 43 * PX
cat_w = len(CAT_TOP[0]) * PX
cat_bed = (mon_x + 10, mon_y)  # kucing tidur di atas monitor
cat_ledge = (name_x + name_w - cat_w - 4, name_top)  # tempat mendarat di ujung nama
dev_walk_w = len(WALK_BODY[0]) * PX
bug_w = len(BUG_WALK[0]) * PX


# ---------------------------------------------------------------- lintasan
class Track:
    """Lintasan satu karakter: segmen (jenis, t0, t1, x0, x1, y0, y1, tinggi / arah)."""

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

    def turn(self, face):
        return self.add("turn", 0, h=face)

    def walk(self, x, speed=SPEED):
        return self.add("walk", abs(x - self.x) / speed, x)

    def jump(self, x, y=None, h=22, dur=0.4):
        return self.add("jump", dur, x, y, h)

    def fly(self, x, y, h, dur):
        return self.add("fly", dur, x, y, h)


def motion(track):
    """Titik (t, x, y); lompat & terbang disampling supaya melengkung."""
    x, y = track.start[:2]
    pts = [(0, x, y)]
    for kind, t0, t1, xa, xb, ya, yb, h in track.segs:
        if kind not in ("jump", "fly"):
            pts.append((t1, xb, yb))
            continue
        n = 24 if kind == "fly" else 10
        for k in range(1, n + 1):
            f = k / n
            y = ya + (yb - ya) * f - 4 * h * f * (1 - f)
            if kind == "fly":
                y += 6 * math.sin(f * 5 * math.pi)  # terbang zig-zag
            pts.append((t0 + (t1 - t0) * f, xa + (xb - xa) * f, y))
    return pts


def poses_of(track):
    """Pose dari jenis segmen: a/b saat jalan, kepak saat terbang, stand/sleep saat diam."""
    events = [(0, track.start[2])]
    for kind, t0, t1, *_ in track.segs:
        if kind == "walk":
            events += alternate(t0, t1, "ab", STEP)
        elif kind == "fly":
            events += alternate(t0, t1, ["fa", "fb"], 0.06)
        elif kind == "jump":
            events.append((t0, "a"))
        elif kind in ("rest", "sleep"):
            events.append((t0, "stand" if kind == "rest" else "sleep"))
    return events


def facings_of(track):
    events = [(0, track.start[3])]
    for kind, t0, _, xa, xb, *_, h in track.segs:
        face = h if kind == "turn" else ("r" if xb > xa else "l") if xb != xa else None
        if face and face != events[-1][1]:
            events.append((t0, face))
    return events


def actor(key, poses, colors, w, phases, base, extra="", pose_extra=None, wrap=""):
    """Karakter dengan phases [(track, timing, pose_events|None)]; base = (x, y, pose, hadap) statis."""
    pose_extra = pose_extra or {}
    face_css = {"r": "none", "l": f"matrix(-1,0,0,1,{w},0)"}
    move, face, pose_anims = [], [], {pose: [] for pose in poses}
    for p, (track, timing, events) in enumerate(phases):
        dur = track.t
        name = keyframes(f"{key}m{p}", [(t, f"transform:translate({x:.1f}px,{y:.1f}px)") for t, x, y in motion(track)], dur)
        move.append(f"{name} {dur:.3f}s linear {timing}")
        events = sorted(events or poses_of(track), key=lambda e: e[0])
        for pose in poses:
            name = keyframes(f"{key}{pose}{p}", [(t, f"opacity:{int(e == pose)}") for t, e in events], dur)
            pose_anims[pose].append(f"{name} {dur:.3f}s step-end {timing}")
        name = keyframes(f"{key}f{p}", [(t, f"transform:{face_css[f]}") for t, f in facings_of(track)], dur)
        face.append(f"{name} {dur:.3f}s step-end {timing}")
    groups = ""
    for pose, art in poses.items():
        art_rows, dx = art if isinstance(art, tuple) else (art, 0)
        groups += (f'<g opacity="{int(pose == base[2])}" style="animation:{",".join(pose_anims[pose])}">'
                   f'{sprite(art_rows, colors, dx * PX)}{pose_extra.get(pose, "")}</g>')
    inner = groups + extra  # extra (tanda "!", z, hati) di atas badan
    if wrap:
        inner = f"<g {wrap}>{inner}</g>"
    inner = f'<g style="transform:{face_css[base[3]]};animation:{",".join(face)}">{inner}</g>'
    return (f'<g style="transform:translate({base[0]:.1f}px,{base[1]:.1f}px);animation:{",".join(move)}">'
            f"{inner}</g>")


# ================================================================ intro
# developer berjalan masuk & duduk; mengetik -> piksel terbang dari layar membangun nama per kolom
dev_intro = Track(W + 20, floor, pose="a", face="l").until(0.3).walk(sit_x, 170).turn("r")
t_sit = dev_intro.t
t_type0 = t_sit + 0.3
column_arrive = {col: t_type0 + 0.2 + col * 0.03 + random.uniform(0, 0.06) + FLY_T
                 for col in sorted({c for c, _, _ in pixels(NAME)})}
build_end = max(column_arrive.values()) + 0.3
type_start, step = build_end + 0.2, 0.045
caret_dur = type_start + (len(TAGLINE) - 2) * step
intro_end = caret_dur + 0.3
dev_intro.until(intro_end)
dev_intro_poses = ([(0, "a")] + alternate(0.3, t_sit, "ab", STEP) + [(t_sit, "sit_a")]
                   + alternate(t_type0, build_end, TYPING, 0.12) + alternate(build_end, intro_end, TYPING, 0.35))

cat_intro = (Track(W + 20, floor, pose="a", face="l").until(1.4).walk(desk_x1 + 6, 150)
             .jump(*cat_bed, h=30, dur=0.5).turn("r").add("rest", 0.5).add("sleep", 0.01))
cat_done = cat_intro.t
LOOP_START = intro_end + 1.0

# ================================================================ loop babak 1: bug keluar dari layar
t_out = 1.0
bite_c0 = width(NAME[:BITE[0]]) + 1
bite_c1 = width(NAME[:BITE[-1] + 1]) - 1
bug_x0 = name_x + bite_c0 * PITCH  # sisi kiri bug saat hinggap
bug_c1 = name_x + (bite_c1 + 1) * PITCH  # titik tengah bug saat diterkam
t_land = t_out + 1.4

cat = Track(*cat_bed, pose="sleep").until(t_out + 0.1, "sleep").until(t_out + 2.0)
cat.jump(*cat_ledge, h=45, dur=0.6)
pounce_x = bug_c1 - cat_w / 2
cat.walk(pounce_x + 40).jump(pounce_x, h=24, dur=0.45)
t_pounce = cat.t
vb = (bug_c1 - bug_w / 2 - bug_x0) / (t_pounce - t_land)
bug1 = (Track(screen_cx - bug_w / 2, screen_cy + 2 * PX, pose="fa").until(t_out)
        .fly(bug_x0, name_top, h=70, dur=t_land - t_out).walk(bug_c1 - bug_w / 2, vb))

# dua baris atas huruf dimakan tepat setelah bug lewat, ditambal piksel hijau dari layar
damage = {}
for col, r, _ in pixels(NAME):
    if bite_c0 <= col <= bite_c1 and r <= 1:
        t_eat = t_land + (name_x + (col + 1) * PITCH - bug_x0) / vb + r * 0.08
        if t_eat < t_pounce:
            damage[col, r] = t_eat
fix_launch = {spot: t_pounce + 0.4 + k * 0.09 for k, spot in enumerate(sorted(damage))}
fix_arrive = {spot: t + FLY_T for spot, t in fix_launch.items()}
fix1_end = max(fix_arrive.values()) + 0.2

cat.until(fix1_end).turn("r").walk(cat_ledge[0]).jump(*cat_bed, h=40, dur=0.6)
t_home = cat.t
cat.until(t_home + 0.4).until(t_home + 2.4, "sleep")

# ================================================================ loop babak 2: kucing duduk di keyboard
t_keys = cat.t
cat.jump(key_x0 + 2, desk_y - PX, h=14, dur=0.4)
t_on_keys = cat.t
cat.until(t_on_keys + 1.3).jump(*cat_bed, h=20, dur=0.45)
t_off_keys = cat.t
garble_at = {i: t_on_keys + 0.15 + k * 0.12 for k, i in enumerate(GARBLE)}
retype_at = {i: t_off_keys + 0.5 + k * 0.22 for k, i in enumerate(GARBLE)}
fix2_end = max(retype_at.values()) + 0.3
cat.until(t_off_keys + 0.4).until(fix2_end + 0.5, "sleep")
PERIOD = fix2_end + 2.2
cat.until(PERIOD, "sleep")
bug1.until(PERIOD)
LOOP = f"{LOOP_START:.2f}s infinite"

dev_loop = Track(sit_x, floor, pose="sit_a").until(PERIOD)
dev_loop_poses = (alternate(0, t_out, TYPING, 0.35) + [(t_out, "sit_a")]
                  + alternate(t_pounce + 0.2, fix1_end, TYPING, 0.1) + alternate(fix1_end, t_on_keys, TYPING, 0.35)
                  + [(t_on_keys, "sit_a")] + alternate(t_off_keys + 0.2, fix2_end, TYPING, 0.1)
                  + alternate(fix2_end, PERIOD, TYPING, 0.35))


def loop_anim(name, points, timing="linear"):
    return f"{keyframes(name, points, PERIOD)} {PERIOD:.3f}s {timing} {LOOP}"


def shown(name, intervals, svg, base=0):
    """Grup yang tampil hanya selama interval tertentu di tiap putaran loop."""
    return f'<g opacity="{base}" style="animation:{loop_anim(name, opacity_points(intervals), "step-end")}">{svg}</g>'


# ---------------------------------------------------------------- karakter
dev_h = len(DEV_POSES["sit_a"]) * PX
alert_dev = sprite(ALERT, {"#": ALERT_COLOR}, 5 * PX, -dev_h - 7 * PX)
dev_extra = (shown("dvalert", [(t_out, t_out + 0.8), (t_on_keys + 0.3, t_on_keys + 1.1)], alert_dev)
             + shown("heart", [(t_home, t_home + 1.2)], f'<g style="animation:rise 1.2s ease-out infinite">'
                     f'{sprite(HEART, {"#": HEART_COLOR}, 3 * PX, -dev_h - 7 * PX)}</g>'))
dev_svg = actor("dv", DEV_POSES, DEV_COLORS, dev_walk_w,
                [(dev_intro, "0s both", dev_intro_poses), (dev_loop, LOOP, dev_loop_poses)],
                (sit_x, floor, "sit_a", "r"), extra=dev_extra)

cat_h = len(CAT_POSES["stand"]) * PX
tail_tips = "".join(f'<rect x="0" y="{r * PX - cat_h}" width="{PX}" height="{PX}" fill="{CAT_COLORS["#"]}" '
                    f'opacity="{1 - k}" style="animation:swap{k} 1.6s step-end infinite"/>' for k, r in enumerate([6, 5]))
zzz = "".join(f'<g opacity="0" style="animation:zz 3s linear {k}s infinite">'
              f'{sprite(ZZZ, {"#": "#8b949e"}, 10 * PX, -9 * PX, px=PX - 1)}</g>' for k in range(3))
asleep = [(0, t_out + 0.1), (t_home + 0.4, t_keys), (t_off_keys + 0.4, PERIOD)]
z_intro = f"{keyframes('zi', opacity_points([(cat_done, None)]), cat_done + 1)} {cat_done + 1:.3f}s step-end both"
z_loop = loop_anim("zl", opacity_points(asleep), "step-end")
cat_extra = (f'<g opacity="0" style="animation:{z_intro},{z_loop}">{zzz}</g>'
             + shown("ctalert", [(t_out + 0.1, t_out + 0.8)], sprite(ALERT, {"#": ALERT_COLOR}, (cat_w - PX) / 2, -cat_h - 7 * PX)))
cat_svg = actor("ct", CAT_POSES, CAT_COLORS, cat_w, [(cat_intro, "0s both", None), (cat, LOOP, None)],
                (*cat_bed, "sleep", "r"), extra=cat_extra, pose_extra={"sleep": tail_tips})

flat = "transform:scale(1.5,.3)"
bug_anim = loop_anim("b1sq", [(0, "opacity:0"), (t_out, "opacity:0"), (t_out + 0.01, "opacity:1;transform:none"),
                              (t_pounce, "opacity:1;transform:none"), (t_pounce + 0.06, f"opacity:1;{flat}"),
                              (t_pounce + 0.3, f"opacity:0;{flat}"), (PERIOD, f"opacity:0;{flat}")])
bug_svg = actor("b1", BUG_POSES, BUG_COLORS, bug_w, [(bug1, LOOP, None)], (*bug1.start[:2], "fa", "r"),
                wrap=f'opacity="0" style="transform-origin:{bug_w / 2}px 0;animation:{bug_anim}"')


# ---------------------------------------------------------------- piksel terbang dari layar
def particle(x1, y1, t0, color=NAME_COLOR, looped=False):
    """Kotak kecil terbang melengkung dari layar ke (x1, y1); sekali di intro, berulang di loop."""
    lift = 50 + abs(x1 - screen_cx) * 0.12 + random.uniform(0, 25)
    path = f"M{screen_cx:.0f} {screen_cy:.0f}Q{(screen_cx + x1) / 2:.0f} {min(screen_cy, y1) - lift:.0f} {x1:.0f} {y1:.0f}"
    if not looped:
        timing = f'begin="{t0:.2f}s" dur="{FLY_T}s" fill="freeze"'
        motion_ = f'<animateMotion path="{path}" {timing}/>'
        fade = f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.9;1" {timing}/>'
    else:
        a, b = t0 / PERIOD, (t0 + FLY_T) / PERIOD
        timing = f'begin="{LOOP_START:.2f}s" dur="{PERIOD:.3f}s" repeatCount="indefinite"'
        motion_ = f'<animateMotion path="{path}" keyPoints="0;0;1;1" keyTimes="0;{a:.4f};{b:.4f};1" calcMode="linear" {timing}/>'
        fade = (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{a:.4f};{b:.4f}" calcMode="discrete" {timing}/>')
    size = 6 if looped else 5  # piksel penambal dibuat lebih besar supaya terlihat
    return f'<rect x="{-size / 2}" y="{-size / 2}" width="{size}" height="{size}" fill="{color}" opacity="0">{motion_}{fade}</rect>'


particles = [particle(name_x + (col + 0.5) * PITCH, name_top + 5, t - FLY_T) for col, t in column_arrive.items()]
particles += [particle(name_x + (col + 0.5) * PITCH, name_top + (r + 0.5) * PITCH, fix_launch[col, r], PLUS_COLOR, True)
              for col, r in damage]


def spark(key, cx, cy, t):
    dots = "".join(f'<rect x="{cx + dx - 1.5:g}" y="{cy + dy - 1.5:g}" width="3" height="3" fill="{FLASH}"/>'
                   for dx, dy in [(-20, 0), (20, 0), (-15, -12), (15, -12)])
    anim = loop_anim(key, [(0, "opacity:0"), (t, "opacity:0;transform:scale(.4)"), (t + 0.03, "opacity:1;transform:scale(.6)"),
                           (t + 0.4, "opacity:0;transform:scale(1.8)"), (PERIOD, "opacity:0")])
    return f'<g opacity="0" style="transform-box:fill-box;transform-origin:50% 100%;animation:{anim}">{dots}</g>'


def plus_one(key, cx, y, t):
    rects = "".join(f'<rect x="{cx - 9 + col * 2:g}" y="{y + r * 2:g}" width="2" height="2"/>' for col, r, _ in pixels("+1"))
    anim = loop_anim(key, [(0, "opacity:0"), (t, "opacity:0;transform:none"), (t + 0.05, "opacity:1;transform:none"),
                           (t + 1.2, "opacity:0;transform:translateY(-18px)"), (PERIOD, "opacity:0")])
    return f'<g opacity="0" fill="{PLUS_COLOR}" style="animation:{anim}">{rects}</g>'


effects = (spark("s1", bug_c1, name_top, t_pounce)
           + plus_one("p1", name_x + (bite_c0 + bite_c1 + 1) / 2 * PITCH, name_top - 34, fix1_end))


# ---------------------------------------------------------------- meja kerja
def code_lines():
    """Baris kode warna-warni yang bergulir di layar (digambar dua kali supaya mulus)."""
    palette = [NAME_COLOR, "#8b949e", "#79c0ff", PLUS_COLOR, "#8b949e"]
    lines, out = 20, []
    for i in range(lines):
        x = mon_x + 5 + random.choice([0, 0, 4, 8])
        for _ in range(random.randint(1, 3)):
            seg = random.choice([4, 6, 8, 10, 14])
            if x + seg > mon_x + mon_w - 5:
                break
            color = random.choice(palette)
            for copy in (0, lines * 4):
                out.append(f'<rect x="{x}" y="{mon_y + 5 + i * 4 + copy}" width="{seg}" height="2" fill="{color}"/>')
            x += seg + 2
    return f'<g style="animation:scroll 6s linear infinite">{"".join(out)}</g>', lines * 4


code, code_h = code_lines()
screen_box = f'x="{mon_x + PX}" y="{mon_y + PX}" width="{mon_w - 2 * PX}" height="{mon_h - 2 * PX}"'
noise = f'<rect {screen_box} fill="#010409"/>' + "".join(
    f'<rect x="{mon_x + 5 + random.randrange(0, mon_w - 12, 2)}" y="{mon_y + 5 + random.randrange(0, mon_h - 10, 2)}" '
    f'width="{random.choice([2, 4, 6])}" height="2" fill="{random.choice([BUG_COLOR, TEXT_COLOR, "#79c0ff"])}"/>' for _ in range(40))

def centered(rows, colors, cx, cy):
    return sprite(rows, colors, cx - len(rows[0]) * PX / 2, cy - len(rows) * PX / 2)


red_screen = (f'<rect {screen_box} fill="{BUG_COLOR}" opacity=".18"/>'
              + centered(CROSS, {"#": BUG_COLOR}, screen_cx, screen_cy))
green_screen = (f'<rect {screen_box} fill="#010409"/><rect {screen_box} fill="{PLUS_COLOR}" opacity=".15"/>'
                + centered(CHECK, {"#": PLUS_COLOR}, screen_cx, screen_cy))
steam = "".join(f'<rect x="{mug_x + PX + k * PX * 1.3:g}" y="{desk_y - 4 * PX - 4}" width="2" height="2" fill="#8b949e" opacity="0" '
                f'style="animation:steam 2.4s ease-out {k * 0.8}s infinite"/>' for k in range(3))
scene = (
    sprite(CHAIR, {"C": "#484f58"}, sit_x, floor - 11 * PX)
    + f'<rect x="{desk_x0}" y="{desk_y}" width="{desk_x1 - desk_x0}" height="{PX + 1}" fill="#484f58"/>'
    + f'<rect x="{desk_x0 + PX}" y="{desk_y + PX + 1}" width="{PX}" height="{floor - desk_y - PX - 1}" fill="#30363d"/>'
    + f'<rect x="{desk_x1 - 2 * PX}" y="{desk_y + PX + 1}" width="{PX}" height="{floor - desk_y - PX - 1}" fill="#30363d"/>'
    + f'<rect x="{key_x0}" y="{desk_y - PX}" width="{key_x1 - key_x0}" height="{PX}" fill="#8b949e"/>'
    + f'<rect x="{screen_cx - PX}" y="{mon_y + mon_h}" width="{2 * PX}" height="{desk_y - mon_y - mon_h}" fill="#484f58"/>'
    + f'<rect x="{mon_x}" y="{mon_y}" width="{mon_w}" height="{mon_h}" rx="2" fill="#484f58"/>'
    + f'<rect {screen_box} fill="#010409"/>'
    + f'<g clip-path="url(#screen)">{code}'
    + shown("scr_red", [(t_out - 0.4, t_pounce)], red_screen)
    + shown("scr_noise", [(t_on_keys, t_off_keys + 0.4)], noise)
    + shown("scr_ok", [(fix1_end - 0.2, fix1_end + 1.2), (fix2_end - 0.2, fix2_end + 1.2)], green_screen)
    + "</g>"
    + sprite(MUG, {"M": LEVELS[4]}, mug_x, desk_y - 4 * PX) + steam
)


def cell(c, r, extra):
    return f'<rect x="{gx + c * PITCH + 1}" y="{gy + r * PITCH + 1}" width="{CELL}" height="{CELL}" rx="1.5" {extra}/>'


# ---------------------------------------------------------------- nama
name_cells = []
for k, (col, r, _) in enumerate(pixels(NAME)):
    grow = column_arrive[col] + r * 0.03
    shine = intro_end + 1 + col * 0.012
    rect = cell(name_c0 + col, name_r0 + r, f'class="n" style="animation-delay:{grow:.2f}s,{shine:.2f}s"')
    if (col, r) not in damage:
        name_cells.append(rect)
        continue
    eat, fix = damage[col, r], fix_arrive[col, r]
    gone = loop_anim(f"nd{k}", [(0, "opacity:1"), (eat, "opacity:1"), (eat + 0.18, "opacity:0"),
                                (fix, "opacity:0"), (fix + 0.01, "opacity:1"), (PERIOD, "opacity:1")])
    flash = loop_anim(f"nf{k}", [(0, f"opacity:0;fill:{BUG_COLOR}"), (eat - 0.01, f"opacity:0;fill:{BUG_COLOR}"),
                                 (eat, f"opacity:1;fill:{BUG_COLOR}"), (eat + 0.18, f"opacity:0;fill:{BUG_COLOR}"),
                                 (fix, f"opacity:0;fill:{PLUS_COLOR}"), (fix + 0.01, f"opacity:1;fill:{PLUS_COLOR}"),
                                 (fix + 0.4, f"opacity:0;fill:{PLUS_COLOR}"), (PERIOD, "opacity:0")])
    name_cells.append(f'<g style="animation:{gone}">{rect}</g>' + cell(name_c0 + col, name_r0 + r, f'opacity="0" style="animation:{flash}"'))

# ---------------------------------------------------------------- tagline
caret_intro = [(0, f"transform:translateX({caret_shift(0)}px)")]
caret_intro += [(type_start + (i - 1) * step, f"transform:translateX({caret_shift(i)}px)") for i in range(1, len(TAGLINE))]
caret_loop = [(0, "transform:none"), (t_off_keys + 0.3, f"transform:translateX({caret_shift(GARBLE[0] - 1)}px)")]
caret_loop += [(retype_at[i], f"transform:translateX({caret_shift(i)}px)") for i in GARBLE]
caret_loop += [(fix2_end, "transform:none")]
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
    if i in garble_at:
        bad, good = garble_at[i], retype_at[i]
        junk = "".join(f'<rect x="{tag_x + (starts[i] + random.randrange(5)) * TAG_PITCH}" y="{tag_y + random.randrange(7) * TAG_PITCH}" '
                       f'width="3" height="3"/>' for _ in range(9))
        group = (shown(f"gd{i}", [(0, bad), (good, None)], group, base=1)
                 + shown(f"gj{i}", [(bad, good)], f'<g fill="{BUG_COLOR}">{junk}</g>'))
    tagline.append(group)

# ---------------------------------------------------------------- latar
scene_cells = {(c, r) for c in range((sit_x - 12 - gx) // PITCH, (desk_x1 + 12 - gx) // PITCH + 1)
               for r in range((cat_bed[1] - 12 * PX - gy) // PITCH, (floor - gy) // PITCH)}
busy = {(c, r) for c in range(name_c0 - 1, name_c0 + width(NAME) + 1) for r in range(name_r0 - 3, name_r0 + 8)}
hole_c0 = (tag_x - gx) // PITCH - 1
hole_c1 = (caret_x + 3 * TAG_PITCH - gx) // PITCH + 1
tag_hole = [(c, r) for c in range(hole_c0, hole_c1 + 1) for r in range(tag_r0, tag_r0 + 3)]
floor_r = (floor - gy) // PITCH
floor_cells = [(c, floor_r) for c in range((sit_x - 20 - gx) // PITCH, cols + 1)]
legend_r, legend_c0 = rows - 3, cols - 10
legend_hole = [(c, legend_r) for c in range(legend_c0 - 4, legend_c0 + 9)]
busy.update(scene_cells, tag_hole, floor_cells, legend_hole)

decor = [cell(c, r, f'fill="{LEVELS[2]}"') for c, r in floor_cells]  # lantai ruang kerja
for r in range(-1, rows + 1):
    for c in range(-1, cols + 1):
        if (c, r) in busy:
            continue
        x, y = gx + (c + 0.5) * PITCH, gy + (r + 0.5) * PITCH
        d = min(1, math.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2)))
        if random.random() > 0.02 + 0.3 * d * d:  # makin ke pinggir makin rapat
            continue
        if random.random() < 0.35:
            level = random.choice([2, 3, 3, 4])
            dur = random.uniform(3, 7)
            decor.append(cell(c, r, f'fill="{LEVELS[0]}" style="animation:tw{level} {dur:.1f}s ease-in-out {-random.uniform(0, dur):.1f}s infinite"'))
        else:
            decor.append(cell(c, r, f'fill="{LEVELS[random.choice([1, 1, 1, 2, 2, 3])]}"'))

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
@keyframes swap0{{50%{{opacity:0}}}}
@keyframes swap1{{50%{{opacity:1}}}}
@keyframes zz{{0%{{opacity:0;transform:none}}20%{{opacity:1}}100%{{opacity:0;transform:translate(10px,-24px)}}}}
@keyframes rise{{from{{transform:none}}to{{transform:translateY(-10px)}}}}
@keyframes steam{{0%{{opacity:0;transform:none}}30%{{opacity:.8}}100%{{opacity:0;transform:translate(3px,-16px)}}}}
@keyframes scroll{{to{{transform:translateY(-{code_h}px)}}}}
{"".join(f"@keyframes tw{k}{{50%{{fill:{LEVELS[k]}}}}}" for k in (2, 3, 4))}
{"".join(CSS)}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
<pattern id="grid" x="{gx}" y="{gy}" width="{PITCH}" height="{PITCH}" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="{CELL}" height="{CELL}" rx="1.5" fill="{LEVELS[0]}"/></pattern>
<filter id="soft" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
<mask id="fade"><rect x="28" y="24" width="{W - 56}" height="{H - 48}" rx="40" fill="#fff" filter="url(#soft)"/>{hole(tag_hole)}{hole(legend_hole)}{hole(list(scene_cells))}</mask>
<radialGradient id="glow"><stop offset="0" stop-color="#8957e5" stop-opacity=".22"/><stop offset="1" stop-color="#8957e5" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<clipPath id="screen"><rect {screen_box}/></clipPath>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="#0d1117" stroke="#30363d"/>
<g mask="url(#fade)"><rect width="{W}" height="{H}" fill="url(#grid)"/>{"".join(decor)}</g>
<ellipse cx="{name_x + name_w / 2}" cy="{name_top + 35}" rx="{name_w * 0.55}" ry="{H * 0.42}" fill="url(#glow)"/>
<ellipse cx="{screen_cx}" cy="{screen_cy}" rx="110" ry="80" fill="url(#glow)"/>
{"".join(name_cells)}
{"".join(tagline)}
<rect x="{caret_x}" y="{tag_y}" width="{3 * TAG_PITCH}" height="{7 * TAG_PITCH}" fill="{LEVELS[4]}" style="animation:{caret_anim}"/>
<g clip-path="url(#card)">{scene}{bug_svg}{cat_svg}{dev_svg}{"".join(particles)}{effects}</g>
<text class="lg" x="{gx + legend_c0 * PITCH - 6}" y="{legend_y + 9}" text-anchor="end">Less</text>
{"".join(legend)}
<text class="lg" x="{gx + (legend_c0 + 5) * PITCH + 4}" y="{legend_y + 9}">More</text>
</svg>
"""

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"banner.svg: {len(svg) // 1024} KB, intro {intro_end:.1f} detik, loop mulai {LOOP_START:.1f}, "
      f"satu putaran {PERIOD:.1f} detik")
