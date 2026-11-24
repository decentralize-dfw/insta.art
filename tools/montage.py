"""Montage reels in the approved Virgil V4 format (posts/montage/virgil-barricade-studio).

    python3 tools/montage.py build <recipe> <folder>    # writes <folder>/spec.json, renders reel.mp4
    python3 tools/montage.py render <folder>

The timing is V4's, frame for frame (60 fps), so V4's own Barricade audio fits:
  0-5.800 s     46 full-bleed detail shots: the first 18 frames, then 7-frame cuts
                (one of 8), then the slowing 7, 10, 11, 14 frames. No white, no small pictures.
  5.800-9.550   the picture builds from a 4 x 5 grid of tiles, centre out, 2-3 tiles on
                each of 9 beats (V4's order): one painting fit to the width, or a full-screen
                mosaic of 20 details (works with several paintings: no white at all).
  9.550-11.417  the finished picture
  11.417-12.417 V4's last hit and the black bird-chair logo (V4's own end frame)
Audio: V4's track 0-11.300 s, then 14.600 s to the end (the last hit and its echo), so the
studio part (only Virgil has a studio photo) is left out and every beat still lands.
Whole paintings are never cropped; details and mosaic tiles fill their frame.
"""
import json, math, os, subprocess, sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import workposts  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
W, H = 1080, 1920
PAD = 60                     # around a whole painting in a full frame
GRID_MARGIN, GRID_GAP = 48, 18
ORDER = [(1, 1), (1, 2), (1, 0), (0, 1), (2, 1), (2, 2), (0, 0), (0, 2), (2, 0)]   # (row, col)


# ---------- images ----------

_cache = {}


def load(src):
    if src not in _cache:
        _cache.clear() if len(_cache) > 12 else None
        _cache[src] = workposts.load(workposts.path_of(src) if ":" in src else src)
    return _cache[src]


def window(im, aspect, pos=None):
    """Crop box of the given aspect (w/h) inside im: along the long axis at pos (0..1), or
    over the most brushwork, pulled toward the centre."""
    iw, ih = im.size
    if iw / ih > aspect:
        win, n_axis = ih * aspect, 0
    else:
        win, n_axis = iw / aspect, 1
    span = (iw if n_axis == 0 else ih) - win
    if pos is None:
        small = np.asarray(im.convert("L").resize((max(2, iw // 16), max(2, ih // 16)))).astype(float)
        e = np.abs(np.diff(small, axis=1))[:-1, :] + np.abs(np.diff(small, axis=0))[:, :-1]
        prof = e.sum(axis=n_axis)
        n = len(prof)
        w = max(1, int(round(win / (iw if n_axis == 0 else ih) * n)))
        cs = np.concatenate([[0], np.cumsum(prof)])
        sc = np.array([cs[i + w] - cs[i] for i in range(n - w + 1)])
        c = (n - w) / 2
        sc = sc * (1 - 0.35 * np.abs(np.arange(len(sc)) - c) / max(c, 1))
        pos = sc.argmax() / max(1, n - w)
    o = span * min(1, max(0, pos))
    return (o, 0, o + win, ih) if n_axis == 0 else (0, o, iw, o + win)


def detail(src, w, h, pos=None, box=None, trim=False):
    im = load(src)
    if trim:                                  # photographed with a white margin around the canvas
        im = workposts.trim_margin(im)
    if box:                                   # a region of the image (fractions), then the cover crop inside it
        x0, y0, x1, y1 = box
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    return im.resize((w, h), Image.LANCZOS, box=window(im, w / h, pos))


def whole(src, w, h, pad, trim=False):
    im = load(src)
    if trim:                                  # photographed with a white margin around the canvas
        im = workposts.trim_margin(im)
    k = min((w - 2 * pad) / im.width, (h - 2 * pad) / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    out = Image.new("RGB", (w, h), "white")
    out.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return out


def shot_image(s):
    if s["kind"] == "whole":
        return whole(s["src"], W, H, PAD, s.get("trim", False))
    return detail(s["src"], W, H, s.get("pos"), s.get("box"), s.get("trim", False))


def cell_rect(r, c):
    cw = (W - 2 * GRID_MARGIN - 2 * GRID_GAP) // 3
    ch = round(cw * 5 / 4)
    top = (H - 3 * ch - 2 * GRID_GAP) // 2
    return GRID_MARGIN + c * (cw + GRID_GAP), top + r * (ch + GRID_GAP), cw, ch


def tile_image(s, cw, ch):
    if s["kind"] == "whole":
        return whole(s["src"], cw, ch, 0, s.get("trim", False))
    return detail(s["src"], cw, ch, s.get("pos"), s.get("box"))


# ---------- timing (Virgil V4) ----------

V4 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "posts", "montage",
                  "virgil-barricade-studio", "reel.mp4")
FAST_CUTS = [0, 18, 25, 32, 39, 46, 53, 60, 67, 74, 81, 88, 95, 102, 109, 116, 123, 130, 137, 144, 151, 158,
             165, 173, 180, 187, 194, 201, 208, 215, 222, 229, 236, 243, 250, 257, 264, 271, 278, 285, 292,
             299, 306, 313, 323, 334]                       # 46 shots, the last ends at frame 348
BUILD = [(348, [(2, 1), (2, 2)]), (376, [(1, 1), (1, 2)]), (405, [(3, 1), (3, 2)]), (433, [(2, 0), (2, 3)]),
         (461, [(1, 0), (1, 3)]), (489, [(3, 0), (3, 3)]), (517, [(0, 1), (0, 2)]),
         (545, [(0, 0), (4, 1), (4, 2)]), (573, [(0, 3), (4, 0), (4, 3)])]     # (frame, [(row, col)])
LOGO_AT, END = 685, 745                                     # 11.417 s, 12.417 s
XFADE = 0.015
AUDIO = [(0.0, 11.300), (14.600 - XFADE, None)]             # seconds of V4's audio, joined (the crossfade
                                                            # overlaps, so the last hit stays on 11.417 s)
FPS = 60
ROWS, COLS = 5, 4


def v4_logo():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "15.3", "-i", V4, "-frames:v", "1", "-f", "image2pipe",
                          "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    import io
    return Image.open(io.BytesIO(raw)).convert("RGB")


def build_final(spec):
    """The finished picture (1080 x 1920) and the box of each of the 20 tiles."""
    a = spec["assembly"]
    out = Image.new("RGB", (W, H), "white")
    if a["kind"] == "painting":
        im = load(a["src"])
        if a.get("trim"):
            im = workposts.trim_margin(im)
        k = min(W / im.width, H / im.height)
        pw, ph = round(im.width * k), round(im.height * k)
        x0, y0 = (W - pw) // 2, (H - ph) // 2
        out.paste(im.resize((pw, ph), Image.LANCZOS), (x0, y0))
    else:                                                       # mosaic: 20 details, full screen
        x0, y0, pw, ph = 0, 0, W, H
    boxes = {}
    for r in range(ROWS):
        for c in range(COLS):
            bx = (x0 + round(c * pw / COLS), y0 + round(r * ph / ROWS),
                  x0 + round((c + 1) * pw / COLS), y0 + round((r + 1) * ph / ROWS))
            boxes[(r, c)] = bx
            if a["kind"] == "mosaic":
                t = a["tiles"][r * COLS + c]
                out.paste(detail(t["src"], bx[2] - bx[0], bx[3] - bx[1], t.get("pos"), t.get("box"), t.get("trim", False)),
                          bx[:2])
    return out, boxes


def audio(path):
    import tempfile
    tmp = tempfile.mkdtemp()
    parts = []
    for i, (a, b) in enumerate(AUDIO):
        f = os.path.join(tmp, f"{i}.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), *(["-to", str(b)] if b else []), "-i", V4,
                        "-vn", "-ac", "2", "-ar", "48000", f], check=True)
        parts.append(f)
    out = os.path.join(tmp, "audio.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", parts[0], "-i", parts[1], "-filter_complex",
                    f"[0][1]acrossfade=d={XFADE}:c1=tri:c2=tri[a]", "-map", "[a]", out], check=True)
    return out


def render(folder):
    spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    assert len(spec["fast"]) == len(FAST_CUTS)
    final, boxes = build_final(spec)
    logo = v4_logo()
    silent = os.path.join(folder, ".silent.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
                            "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    log = []

    def put(img, n, what):
        data = img.tobytes()
        for _ in range(n):
            enc.stdin.write(data)
        log.append({"frames": n, "what": what})

    cuts = FAST_CUTS + [BUILD[0][0]]
    for k, s in enumerate(spec["fast"]):
        put(shot_image(s), cuts[k + 1] - cuts[k], f"{s['kind']} {os.path.basename(s['src'])}")
    state = Image.new("RGB", (W, H), "white")
    marks = [f for f, _ in BUILD] + [LOGO_AT]
    for i, (f, cells) in enumerate(BUILD):
        state = state.copy()
        for rc in cells:
            state.paste(final.crop(boxes[rc]), boxes[rc][:2])
        put(state, marks[i + 1] - f, f"build {i + 1}/9")
    put(logo, END - LOGO_AT, "logo")
    enc.stdin.close()
    if enc.wait():
        sys.exit("ffmpeg failed")
    out = os.path.join(folder, spec.get("out", "reel.mp4"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", audio(folder), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", "apad", "-c:a", "aac", "-b:a", "256k", "-t", f"{END / FPS:.4f}",
                    "-movflags", "+faststart", out],
                   check=True)
    os.remove(silent)
    json.dump(log, open(os.path.join(folder, "timeline.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{out}  {END / FPS:.3f} s")


# ---------- recipes ----------

def works_json():
    w = json.load(open(workposts.WORKS, encoding="utf-8"))
    return w if isinstance(w, list) else w.get("works", w)


def src_of(path):
    for k, root in workposts.ROOTS.items():
        if path.startswith(root + os.sep):
            return k + ":" + os.path.relpath(path, root)
    return path


def details_of(slug):
    master, files = workposts.sources(slug)
    return master, [src_of(f) for f in files]


def tall_enough(src):
    """A whole painting reads in a 9:16 frame only if it is not much wider than tall (a triptych is not)."""
    w, h = Image.open(workposts.path_of(src)).size
    return w / h <= 1.3


def busy(s):
    """How much brushwork a shot's frame holds (mean gradient of its 9:16 crop)."""
    im = load(s["src"])
    if s.get("box"):
        x0, y0, x1, y1 = s["box"]
        im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    small = im.crop(window(im, W / H, s.get("pos"))).convert("L").resize((90, 160))
    a = np.asarray(small).astype(float)
    return float(np.abs(np.diff(a, axis=0)).mean() + np.abs(np.diff(a, axis=1)).mean())


def keep_busy(shots, ratio=0.8):
    """Drop crops that are mostly empty ground: under ratio x the median."""
    e = [busy(x) for x in shots]
    m = float(np.median(e))
    return [x for x, v in zip(shots, e) if v >= ratio * m]


def spread(groups, n, first=None):
    """n shots, round robin over groups (lists of shots), never the same source twice in a row."""
    out = [first] if first else []
    idx = [0] * len(groups)
    g = 0
    while len(out) < n:
        grp = groups[g % len(groups)]
        shot = grp[idx[g % len(groups)] % len(grp)]
        idx[g % len(groups)] += 1
        g += 1
        if out and shot["src"] == out[-1]["src"] and shot.get("pos") == out[-1].get("pos"):
            continue
        out.append(shot)
    return out


def by_name(files, name):
    return next(f for f in files if os.path.basename(f).startswith(name))


def recipe_sept_neuf():
    master, d = details_of("sept-neuf")
    shots = [{"kind": "detail", "src": f, "pos": p} for p in (None, 0.0, 1.0) for f in d]
    shots += [{"kind": "detail", "src": master, "box": b} for b in
              ([0.0, 0.1, 0.55, 0.75], [0.5, 0.2, 1.0, 0.8], [0.2, 0.5, 0.8, 1.0])]   # tall regions: sharp at 9:16
    # chosen by eye (23 Nov): these windows are mostly empty green ground
    shots = [x for i, x in enumerate(shots) if i not in {7, 9, 10, 11, 15, 17}]
    fast = spread([shots], len(FAST_CUTS) - 4, first={"kind": "detail", "src": d[0]})
    fast += [{"kind": "detail", "src": d[6]}, {"kind": "detail", "src": d[3]},
             {"kind": "detail", "src": d[4]}, {"kind": "detail", "src": d[0], "pos": 1.0}]
    return {"title": "sept neuf", "works": ["sept-neuf"], "fast": fast,
            "assembly": {"kind": "painting", "src": master}}


KOPSTAL = ["angora-mergvs", "kreatine-klaude-kettlebell", "gxd-is-afk-we-banned-it", "virgil-on-virtual-cage-final-final-finalv9",
           "painstaking", "gary-grills-cooper", "sept-neuf", "walls-of-perception"]   # high-resolution details only


def recipe_kopstal():
    data = {s: details_of(s)[1] for s in KOPSTAL}
    groups = [[{"kind": "detail", "src": f} for f in data[s]] for s in KOPSTAL]
    first = {"kind": "detail", "src": by_name(data["kreatine-klaude-kettlebell"], "kreatine-klaude-kettlebell-detail-01")}
    fast = spread(groups, len(FAST_CUTS), first)
    used = {x["src"] for x in fast}
    tiles, looks = [], []

    def look(f):                                             # the tile as it will be seen, small and grey
        return np.asarray(detail(f, 270, 384).convert("L").resize((27, 38))).astype(float)

    for s in KOPSTAL * 6:                                    # 20 tiles: unused in the fast part where possible,
        spaced = data[s][1::3] + data[s][2::3] + data[s][::3]           # neighbours in a list look alike
        for f in [f for f in spaced if f not in used] + spaced:       # and never two that look alike
            lk = look(f)
            if all(np.abs(lk - o).mean() > 20 for o in looks):
                break
        else:
            continue
        used.add(f)
        looks.append(lk)
        tiles.append({"kind": "detail", "src": f, "work": s})
        if len(tiles) == 20:
            break
    grid, pool = [], tiles[:]                                # no work next to itself (left or above)
    for i in range(20):
        nb = {grid[i - 1]["work"] if i % COLS else None, grid[i - COLS]["work"] if i >= COLS else None}
        t = next((x for x in pool if x["work"] not in nb), pool[0])
        pool.remove(t)
        grid.append(t)
    tiles = grid
    return {"title": "Kopstal, 2026", "works": KOPSTAL, "fast": fast, "assembly": {"kind": "mosaic", "tiles": tiles}}


GENERAL_SKIP = {"the-assassination-of-the-crow"}          # Yiğit: not soon


def recipe_general():
    works = [w for w in works_json() if (w.get("slug") or w.get("id")) not in GENERAL_SKIP]
    works.sort(key=lambda w: (str(w.get("year")), w.get("slug") or w.get("id")), reverse=True)
    pool = []
    for w in works:
        s = w.get("slug") or w.get("id")
        m, d = details_of(s)
        if not os.path.exists(workposts.path_of(m)) or not tall_enough(m):
            continue
        hi = [x for x in d if min(Image.open(workposts.path_of(x)).size) >= 1700]
        pool.append((s, m, hi))
    groups = []
    for s, m, d in pool:                                     # each work: the painting filling the frame, then its details
        groups.append([{"kind": "detail", "src": m, "trim": s in workposts.TRIM, "work": s}] +
                      [{"kind": "detail", "src": x, "work": s} for x in d[:2]])
    flat = [g[i] for i in range(3) for g in groups if i < len(g)]
    gxd = details_of("gxd-is-afk-we-banned-it")[1]
    fast = spread([flat], len(FAST_CUTS), {"kind": "detail", "src": by_name(gxd, "IMG_6743")})
    mosaic = [{"kind": "detail", "src": m, "trim": s in workposts.TRIM, "work": s} for s, m, d in pool[:20]]
    centre = {"angora-mergvs": 5, "kreatine-klaude-kettlebell": 6, "penguin-is-not-a-friend-only-a-sinner": 9,
              "gxd-is-afk-we-banned-it": 10}
    for slug, cell in centre.items():                       # strong works in the first tiles to land
        j = next((i for i, t in enumerate(mosaic) if t["work"] == slug), None)
        if j is not None:
            mosaic[cell], mosaic[j] = mosaic[j], mosaic[cell]
    return {"title": "paintings", "works": [t["work"] for t in mosaic], "fast": fast,
            "assembly": {"kind": "mosaic", "tiles": mosaic}}


RECIPES = {"sept-neuf": recipe_sept_neuf, "kopstal": recipe_kopstal, "genel": recipe_general}


def build(recipe, folder):
    os.makedirs(folder, exist_ok=True)
    spec = {"type": "reel", "reel_type": "montage in the Virgil V4 format (REELS_FORMULU.md, approved 23 Nov)",
            "fps": FPS, "music": "Axwell, Barricade (V4's audio, studio part left out)", **RECIPES[recipe]()}
    json.dump(spec, open(os.path.join(folder, "spec.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    render(folder)


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3])
    else:
        render(sys.argv[2])
