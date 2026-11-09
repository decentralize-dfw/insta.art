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


def reel(spec, outdir):
    path = os.path.join(outdir, spec.get("out", "reel.mp4"))
    pad = spec.get("pad", PAD)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
           "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = 0
    for shot in spec["shots"]:
        im = load(shot["src"])
        a = shot["from"]
        b = shot.get("to", a)
        sa = scale_for(im, a, W, H, pad)
        sb = scale_for(im, b, W, H, pad)
        hold = float(shot.get("hold", 0))
        n = round(float(shot["dur"]) * FPS)
        nh = round(hold * FPS)
        nm = max(1, n - nh)
        for i in range(n):
            t = ease(min(1.0, i / max(1, nm - 1)), shot.get("ease", "inout"))
            s = math.exp(math.log(sa) + (math.log(sb) - math.log(sa)) * t)
            cx = a["cx"] + (b["cx"] - a["cx"]) * t
            cy = a["cy"] + (b["cy"] - a["cy"]) * t
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
