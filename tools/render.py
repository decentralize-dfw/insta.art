#!/usr/bin/env python3
"""
render.py - build silent Reels and carousel slides from painting images.

Usage
  python3 tools/render.py posts/<folder>/spec.json

The spec decides everything: sources, shots, timing, framing. See any
posts/*/spec.json for a working example.

Sources are written as "<repo>:<path>", where <repo> is one of the keys in
ROOTS below. The repos are expected next to this one (../yigit etc.).

Camera model (reel shots)
  Each shot moves on ONE axis only: a horizontal pan (cx changes), a vertical
  pan (cy changes) or a centre-locked zoom (scale changes, cx = cy = 0.5).
  Anything diagonal is refused. Every shot keeps moving until the cut (no
  shot may stand still, no easing into a stop); only the last shot may hold,
  for at most 2 s, once the painting sits on white.
  Process videos set "camera": "static": nothing moves, only the stages change. Pan targets are clamped to
  what the frame can really show, so a pan never stalls against an edge.
  Each shot has a source image and two keyframes, "from" and "to".
  A keyframe is {"cx": 0-1, "cy": 0-1, "fit": true} or {"cx", "cy", "cover": k}.
    cover: k  -> the image fills the 9:16 frame, k times closer (1 = just fills)
    fit: true -> the whole image is visible on white, with PAD px of margin
  Scale is interpolated on a log curve so zooms feel even. When the image is
  larger than the frame the view is clamped to the image, so no empty edge
  ever slides into view while zoomed in.

Output is H.264, 30 fps, 1080x1920, no audio track. Music is added in the
Instagram app.
"""

import json
import math
import os
import subprocess
import sys

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PARENT = os.path.dirname(REPO)
ROOTS = {
    "yigit": os.path.join(PARENT, "yigit"),
    "details": os.path.join(PARENT, "yigitozen-painting-details"),
    "details2": os.path.join(PARENT, "yigitozen-painting-details-2"),
    "insta": REPO,
}

W, H, FPS = 1080, 1920, 30
PAD = 40
WHITE = (255, 255, 255)

_cache = {}


def load(src):
    if src not in _cache:
        repo, path = src.split(":", 1)
        im = Image.open(os.path.join(ROOTS[repo], path))
        im = ImageOps.exif_transpose(im).convert("RGB")
        _cache[src] = im
    return _cache[src]


def ease(t, kind):
    if kind == "linear":
        return t
    if kind == "out":
        return 1 - (1 - t) ** 2
    if kind == "in":
        return t * t
    return t * t * (3 - 2 * t)  # inout


def scale_for(im, key, fw, fh, pad):
    iw, ih = im.size
    if key.get("fit"):
        return min((fw - 2 * pad) / iw, (fh - 2 * pad) / ih)
    return max(fw / iw, fh / ih) * float(key.get("cover", 1.0))


def place(im, s, cx, cy, fw, fh):
    """Top-left of the scaled image on the frame, clamped/centred."""
    iw, ih = im.size
    dw, dh = iw * s, ih * s
    left = fw / 2 - cx * dw
    top = fh / 2 - cy * dh
    left = min(0, max(fw - dw, left)) if dw >= fw else (fw - dw) / 2
    top = min(0, max(fh - dh, top)) if dh >= fh else (fh - dh) / 2
    return left, top, dw, dh


def draw(im, s, cx, cy, fw=W, fh=H):
    frame = Image.new("RGB", (fw, fh), WHITE)
    left, top, dw, dh = place(im, s, cx, cy, fw, fh)
    x0, y0 = max(0, left), max(0, top)
    x1, y1 = min(fw, left + dw), min(fh, top + dh)
    dx0, dy0, dx1, dy1 = round(x0), round(y0), round(x1), round(y1)
    if dx1 <= dx0 or dy1 <= dy0:
        return frame
    iw, ih = im.size
    box = (max(0.0, (dx0 - left) / s), max(0.0, (dy0 - top) / s),
           min(float(iw), (dx1 - left) / s), min(float(ih), (dy1 - top) / s))
    part = im.resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS, box=box)
    frame.paste(part, (dx0, dy0))
    return frame


def check_motion(shot, i):
    """One axis per shot: pan-x, pan-y, or a centre-locked zoom. Nothing diagonal."""
    a = shot["from"]
    b = shot.get("to", a)
    moved_x = abs(a["cx"] - b["cx"]) > 1e-9
    moved_y = abs(a["cy"] - b["cy"]) > 1e-9
    zoomed = bool(a.get("fit")) != bool(b.get("fit")) or \
        abs(float(a.get("cover", 1)) - float(b.get("cover", 1))) > 1e-9
    if moved_x + moved_y + zoomed > 1:
        sys.exit(f"shot {i + 1}: only one axis per shot (pan-x, pan-y or zoom)")
    if zoomed and not (a["cx"] == b["cx"] == 0.5 and a["cy"] == b["cy"] == 0.5):
        sys.exit(f"shot {i + 1}: a zoom must be centre-locked (cx = cy = 0.5)")


def clamp_center(im, s, cx, cy, fw=W, fh=H):
    """The centre the frame will really show at scale s (edges never slide in)."""
    iw, ih = im.size
    dw, dh = iw * s, ih * s
    if dw > fw:
        m = fw / (2 * dw)
        cx = min(1 - m, max(m, cx))
    if dh > fh:
        m = fh / (2 * dh)
        cy = min(1 - m, max(m, cy))
    return cx, cy


MIN_SPEED = 40   # px per second on screen; every shot keeps moving
MAX_HOLD = 2.0   # only the last shot may hold, for at most this long


def reel(spec, outdir):
    shots = spec["shots"]
    static = spec.get("camera") == "static"
    for i, shot in enumerate(shots):
        check_motion(shot, i)
        if static and shot.get("to", shot["from"]) != shot["from"]:
            sys.exit(f"shot {i + 1}: camera is static in this spec, so 'to' must equal 'from'")
        if shot.get("hold") and i != len(shots) - 1:
            sys.exit(f"shot {i + 1}: only the last shot may hold")
        if float(shot.get("hold", 0)) > MAX_HOLD:
            sys.exit(f"shot {i + 1}: hold is at most {MAX_HOLD} s")
    path = os.path.join(outdir, spec.get("out", "reel.mp4"))
    pad = spec.get("pad", PAD)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
           "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", path]
    plan = []
    for i, shot in enumerate(shots):
        im = load(shot["src"])
        a = shot["from"]
        b = shot.get("to", a)
        sa = scale_for(im, a, W, H, pad)
        sb = scale_for(im, b, W, H, pad)
        ax, ay = clamp_center(im, sa, a["cx"], a["cy"])
        bx, by = clamp_center(im, sb, b["cx"], b["cy"])
        dur = float(shot["dur"])
        hold = float(shot.get("hold", 0))
        if sa == sb and not static:
            travel = abs(bx - ax) * im.size[0] * sa + abs(by - ay) * im.size[1] * sa
            speed = travel / max(1e-6, dur - hold)
            if speed < MIN_SPEED:
                sys.exit(f"shot {i + 1}: moves {speed:.0f} px/s on screen; needs at least "
                         f"{MIN_SPEED}. Raise 'cover' or widen the pan.")
        plan.append((im, sa, sb, ax, ay, bx, by, dur, hold, shot.get("ease", "linear")))
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = 0
    for im, sa, sb, ax, ay, bx, by, dur, hold, kind in plan:
        n = round(dur * FPS)
        nm = max(1, n - round(hold * FPS))
        for k in range(n):
            # k / nm, not k / (nm - 1): the last frame before a cut is still moving
            t = ease(min(1.0, (k + 1) / nm if hold else k / nm), kind)
            s = math.exp(math.log(sa) + (math.log(sb) - math.log(sa)) * t)
            cx = ax + (bx - ax) * t
            cy = ay + (by - ay) * t
            proc.stdin.write(draw(im, s, cx, cy).tobytes())
        total += n
    proc.stdin.close()
    if proc.wait():
        sys.exit("ffmpeg failed")
    print(f"{path}  {total / FPS:.1f}s")


def still(item, size, pad):
    im = load(item["src"])
    fw, fh = size
    key = {"cx": item.get("cx", 0.5), "cy": item.get("cy", 0.5)}
    if item.get("fit"):
        key["fit"] = True
    else:
        key["cover"] = item.get("cover", 1.0)
    return draw(im, scale_for(im, key, fw, fh, item.get("pad", pad)),
                key["cx"], key["cy"], fw, fh)


def main():
    spec_path = sys.argv[1]
    outdir = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    pad = spec.get("pad", PAD)
    if spec["type"] == "reel":
        reel(spec, outdir)
    for i, item in enumerate(spec.get("slides", []), 1):
        out = os.path.join(outdir, f"{i:02d}.jpg")
        still(item, (1080, 1350), pad).save(out, quality=95, subsampling=0)
        print(out)
    if "cover" in spec:
        c = spec["cover"]
        frame = Image.new("RGB", (W, H), WHITE)
        inner = still(dict(c, fit=c.get("fit", True)), (1080, 1350), c.get("pad", pad))
        frame.paste(inner, (0, (H - 1350) // 2))
        out = os.path.join(outdir, "cover.jpg")
        frame.save(out, quality=95, subsampling=0)
        print(out)


if __name__ == "__main__":
    main()
