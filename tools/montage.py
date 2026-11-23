"""Music-locked detail montage (REELS_FORMULU.md, after @studio_paresse's reel).

    python3 tools/montage.py build <recipe> <folder>    # writes <folder>/spec.json, renders reel.mp4
    python3 tools/montage.py render <folder>            # renders <folder>/spec.json

Structure, on a fixed beat (B BPM, T = 60 / B):
  1. N fast shots, each a sixteenth (T / 4), hard cuts, no blending: whole painting,
     detail, detail, ...
  2. four slowing shots: T/4, T/3, 5T/12, T/2 (1.5 beats)
  3. the 3x3 build: one tile per beat on white, in the order centre, middle right,
     middle left, top centre, bottom centre, bottom right, top left, top right, bottom left
  4. the full grid held 2 beats; the video ends on beat 10 after the first tile

Every start is computed from absolute beat time and rounded to a frame, so nothing
drifts. With N = 50 the video is 24 beats: 11.25 s at 128 BPM. The first grid tile
lands on beat L = N/4 + 1.5 (6.5625 s at 128 BPM): put a strong beat of the song there.
The video is silent (the music is added in the Instagram app) and has no end card,
so it loops.

Whole paintings are never cropped (fit on white); details fill the frame (cover crop
over the part with the most brushwork, or at a given position).
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


def detail(src, w, h, pos=None, box=None):
    im = load(src)
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
    return detail(s["src"], W, H, s.get("pos"), s.get("box"))


def cell_rect(r, c):
    cw = (W - 2 * GRID_MARGIN - 2 * GRID_GAP) // 3
    ch = round(cw * 5 / 4)
    top = (H - 3 * ch - 2 * GRID_GAP) // 2
    return GRID_MARGIN + c * (cw + GRID_GAP), top + r * (ch + GRID_GAP), cw, ch


def tile_image(s, cw, ch):
    if s["kind"] == "whole":
        return whole(s["src"], cw, ch, 0, s.get("trim", False))
    return detail(s["src"], cw, ch, s.get("pos"), s.get("box"))


# ---------- timing ----------

def plan(spec):
    B, F, N = spec["bpm"], spec.get("fps", 60), len(spec["fast"])
    T = 60.0 / B
    L = N / 4 + 1.5
    v = lambda b: (b + L) * T                       # video time of beat b (b = 0: first grid tile)
    fr = lambda t: int(math.floor(t * F + 0.5))
    events = [(fr(v(-L + i / 4)), ("shot", s)) for i, s in enumerate(spec["fast"])]
    for b, s in zip((-1.5, -1.25, -11 / 12, -0.5), spec["slow"]):
        events.append((fr(v(b)), ("shot", s)))
    for j in range(9):
        events.append((fr(v(j)), ("grid", j + 1)))
    end = fr(v(10))
    return sorted(events, key=lambda e: e[0]), end, F, T, L


def render(folder):
    spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    assert len(spec["slow"]) == 4 and len(spec["grid"]) == 9
    events, end, F, T, L = plan(spec)
    out = os.path.join(folder, spec.get("out", "reel.mp4"))
    # the grid states 1..9
    base = Image.new("RGB", (W, H), "white")
    grids = []
    for j, s in enumerate(spec["grid"]):
        r, c = ORDER[j]
        x, y, cw, ch = cell_rect(r, c)
        base = base.copy()
        base.paste(tile_image(s, cw, ch), (x, y))
        grids.append(base)
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(F), "-i", "-", "-an", "-c:v", "libx264",
                            "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
                           stdin=subprocess.PIPE)
    log = []
    for k, (f0, (kind, x)) in enumerate(events):
        f1 = events[k + 1][0] if k + 1 < len(events) else end
        frame = shot_image(x) if kind == "shot" else grids[x - 1]
        data = frame.tobytes()
        for _ in range(f1 - f0):
            enc.stdin.write(data)
        log.append({"frame": f0, "ms": round(1000 * f0 / F, 1), "frames": f1 - f0,
                    "what": (x["kind"] + " " + os.path.basename(x["src"])) if kind == "shot" else f"grid {x}/9"})
    enc.stdin.close()
    if enc.wait():
        sys.exit("ffmpeg failed")
    json.dump(log, open(os.path.join(folder, "timeline.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{out}  {end / F:.3f} s  ({len(events)} cuts, first grid tile at {L * T:.4f} s, {spec['bpm']} BPM)")


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


def recipe_sept_neuf():
    master, d = details_of("sept-neuf")
    crops = [(f, p) for p in (0.15, 0.5, 0.85) for f in d]          # 21 different windows over 7 photos
    fast, i = [], 0
    for n in range(50):
        if n % 4 == 0:
            fast.append({"kind": "whole", "src": master})
        else:
            f, p = crops[i % len(crops)]
            i += 1
            fast.append({"kind": "detail", "src": f, "pos": p})
    slow = [{"kind": "whole", "src": master}] + [{"kind": "detail", "src": d[k], "pos": 0.5} for k in (2, 4, 6)]
    # the painting itself opens the grid (centre), its seven detail photos and the hand on the armrest around it
    t = [{"kind": "detail", "src": f} for f in d]
    t[2] = {"kind": "detail", "src": master, "box": [0.40, 0.17, 0.63, 0.44]}      # the hand with the cigarette
    grid = [{"kind": "whole", "src": master}] + t + [
        {"kind": "detail", "src": master, "box": [0.08, 0.47, 0.42, 0.72]}]
    return {"title": "sept neuf", "fast": fast, "slow": slow, "grid": grid}


KOPSTAL = ["angora-mergvs", "kreatine-klaude-kettlebell", "gxd-is-afk-we-banned-it", "virgil-on-virtual-cage-final-final-finalv9",
           "painstaking", "gary-grills-cooper", "sept-neuf", "walls-of-perception"]   # high-resolution details only


def recipe_kopstal():
    data = {s: details_of(s) for s in KOPSTAL}
    fast, n, k = [], 0, {s: 0 for s in KOPSTAL}
    while len(fast) < 50:
        s = KOPSTAL[n % len(KOPSTAL)]
        master, d = data[s]
        if tall_enough(master):
            fast.append({"kind": "whole", "src": master})
        for _ in range(2):
            if len(fast) < 50:
                fast.append({"kind": "detail", "src": d[k[s] % len(d)]})
                k[s] += 1
        n += 1
    m, d = data["angora-mergvs"]
    slow = [{"kind": "whole", "src": m}] + [{"kind": "detail", "src": d[i]} for i in (5, 7, 9)]
    order = ["angora-mergvs", "kreatine-klaude-kettlebell", "gxd-is-afk-we-banned-it", "virgil-on-virtual-cage-final-final-finalv9",
             "gary-grills-cooper", "painstaking", "sept-neuf", "walls-of-perception", "kreatine-klaude-kettlebell"]
    grid, used = [], {}
    for s in order:
        d = data[s][1]
        i = used.get(s, len(d) // 2)
        used[s] = i + 3
        grid.append({"kind": "detail", "src": d[i % len(d)]})
    return {"title": "Kopstal, 2026", "fast": fast, "slow": slow, "grid": grid}


GENERAL_SKIP = {"the-assassination-of-the-crow"}          # Yiğit: not soon
GENERAL_GRID = ["angora-mergvs", "penguin-is-not-a-friend-only-a-sinner", "gxd-is-afk-we-banned-it", "viperella",
                "virgil-on-virtual-cage-final-final-finalv9", "cellular-spleens", "gary-grills-cooper",
                "the-family-dinner-after-a-night-in-jail", "kreatine-klaude-kettlebell"]


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
    fast, i = [], 0
    while len(fast) < 50:                                   # whole, then a detail of it when there is one
        s, m, d = pool[i % len(pool)]
        fast.append({"kind": "whole", "src": m, "trim": s in workposts.TRIM})
        if d and len(fast) < 50:
            fast.append({"kind": "detail", "src": d[(i // len(pool)) % len(d)]})
        i += 1
    m, d = details_of("kreatine-klaude-kettlebell")
    slow = [{"kind": "whole", "src": m}] + [{"kind": "detail", "src": d[i]} for i in (0, 8, 4)]
    grid = [{"kind": "whole", "src": details_of(s)[0], "trim": s in workposts.TRIM} for s in GENERAL_GRID]
    return {"title": "paintings", "fast": fast, "slow": slow, "grid": grid}


RECIPES = {"sept-neuf": recipe_sept_neuf, "kopstal": recipe_kopstal, "genel": recipe_general}


def build(recipe, folder, bpm=128):
    os.makedirs(folder, exist_ok=True)
    spec = {"type": "reel", "reel_type": "music-locked montage (REELS_FORMULU.md)", "bpm": bpm, "fps": 60,
            **RECIPES[recipe]()}
    json.dump(spec, open(os.path.join(folder, "spec.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    render(folder)


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 128)
    else:
        render(sys.argv[2])
