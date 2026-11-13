#!/usr/bin/env python3
"""
render.py - build silent Reels and carousel slides from painting images.

Usage
  python3 tools/render.py posts/<folder>/spec.json

The spec decides everything: sources, shots, timing, framing. See any
posts/*/spec.json for a working example.

Sources are either "<repo>:<path>" (a key of ROOTS below; those repos sit next
to this one, ../yigit etc.) or a plain file path: absolute, or relative to the
folder of the spec.json. On a computer with a local archive, plain paths are
the normal case.

Camera model (reel shots)
  Each shot moves on ONE axis only: a horizontal pan (cx changes), a vertical
  pan (cy changes) or a centre-locked zoom (scale changes, cx = cy = 0.5).
  Anything diagonal is refused. Every shot keeps moving until the cut (no
  shot may stand still, no easing into a stop); only the last shot may hold,
  for at most 2 s, once the painting sits on white.
  Process videos set "camera": "static": nothing moves, only the stages change,
  and every image fits whole on white (nothing cropped). Pan targets are clamped to
  what the frame can really show, so a pan never stalls against an edge.
  Each shot has a source image and two keyframes, "from" and "to".
  A keyframe is {"cx": 0-1, "cy": 0-1, "fit": true} or {"cx", "cy", "cover": k}.
    cover: k  -> the image fills the 9:16 frame, k times closer (1 = just fills)
    fit: true -> the whole image is visible on white, with PAD px of margin
  Scale is interpolated on a log curve so zooms feel even. When the image is
  larger than the frame the view is clamped to the image, so no empty edge
  ever slides into view while zoomed in.

Every reel ends with a 1 s end card: white, the bird-on-chair logo small and
black in the centre (assets/logo-birdchair.png).

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

# Every reel ends on this: 1 s of white with the site's bird-on-chair logo,
# black and small, in the centre.
ENDCARD_DUR = 1.0
ENDCARD_LOGO = os.path.join(REPO, "assets", "logo-birdchair.png")
ENDCARD_LOGO_H = 200


def endcard():
    frame = Image.new("RGB", (W, H), WHITE)
    logo = Image.open(ENDCARD_LOGO).convert("RGBA")
    logo = logo.resize((round(logo.width * ENDCARD_LOGO_H / logo.height), ENDCARD_LOGO_H),
                       Image.LANCZOS)
    frame.paste(logo, ((W - logo.width) // 2, (H - logo.height) // 2), logo)
    return frame

_cache = {}


SPEC_DIR = REPO


def resolve(src):
    """'<repo>:<path>' for the known repos, otherwise a normal file path
    (absolute, or relative to the spec.json folder)."""
    repo, sep, path = src.partition(":")
    if sep and repo in ROOTS:
        return os.path.join(ROOTS[repo], path)
    return src if os.path.isabs(src) else os.path.join(SPEC_DIR, src)


def load(src):
    if src not in _cache:
        # Large local originals must not accumulate across every process stage.
        _cache.clear()
        with Image.open(resolve(src)) as source:
            im = ImageOps.exif_transpose(source)
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                # transparent areas sit on white, never on black
                im = im.convert("RGBA")
                im = Image.alpha_composite(Image.new("RGBA", im.size, WHITE + (255,)), im)
            im = im.convert("RGB")
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
BELL = os.path.join(REPO, "assets", "audio", "zen-bell.mp3")
BELL_FADE = (1.0, 2.5)    # fade-out start and length in seconds: silent from 3.5 s


def add_bell(path):
    """The only sound in a reel: the bell at 0 s, faded out by 3.5 s, then silence.
    The video stream is copied, never re-encoded. Music is added in the app."""
    tmp = path + ".tmp.mp4"
    st, d = BELL_FADE
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-i", BELL,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", f"afade=t=out:st={st}:d={d},apad", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, path)
FAST_INTRO = 2.0          # "fast_intro": true in a spec plays the whole tour in this many seconds first
BAR_Y, BAR_H = 320, 12    # progress bar, below the Reels header
LABEL_X, LABEL_Y = 108, 372   # "label": gallery-label text under the bar, on the covers' 10 % line


def draw_label(fr, label):
    """Black text on white boxes, top left, inside the Reels safe zone."""
    from PIL import ImageDraw, ImageFont
    font_path = os.path.join(REPO, "assets", "fonts", "HankenGrotesk-500.ttf")
    d = ImageDraw.Draw(fr)
    y = LABEL_Y
    for i, line in enumerate(label["lines"]):
        size = label.get("size", 56) if i == 0 else label.get("size2", 38)
        f = ImageFont.truetype(font_path, size)
        pad = round(size * 0.28)
        x0, y0, x1, y1 = d.textbbox((LABEL_X, y), line, font=f)
        d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], fill=(255, 255, 255))
        d.text((LABEL_X, y), line, font=f, fill=(0, 0, 0))
        y = y1 + pad * 2 + 6
    return fr
MAX_HOLD = 2.0   # only the last shot may hold, for at most this long


def reel(spec, outdir):
    shots = spec["shots"]
    static = spec.get("camera") == "static"
    for i, shot in enumerate(shots):
        check_motion(shot, i)
        if static and shot.get("to", shot["from"]) != shot["from"]:
            sys.exit(f"shot {i + 1}: camera is static in this spec, so 'to' must equal 'from'")
        if static and not shot["from"].get("fit"):
            sys.exit(f"shot {i + 1}: in a static (process) reel every image must fit whole on white")
        if shot.get("hold") and i != len(shots) - 1:
            sys.exit(f"shot {i + 1}: only the last shot may hold")
        if float(shot.get("hold", 0)) > MAX_HOLD:
            sys.exit(f"shot {i + 1}: hold is at most {MAX_HOLD} s")
    path = os.path.join(outdir, spec.get("out", "reel.mp4"))
    pad = spec.get("pad", PAD)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
           "-preset", "slow", "-crf", "17", "-threads", "4", "-pix_fmt", "yuv420p",
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
        plan.append((shot["src"], sa, sb, ax, ay, bx, by, dur, hold, shot.get("ease", "linear")))
    # Every body frame as (src, scale, cx, cy); drawn later.
    steps = []
    for src, sa, sb, ax, ay, bx, by, dur, hold, kind in plan:
        n = round(dur * FPS)
        nm = max(1, n - round(hold * FPS))
        for k in range(n):
            # k / nm, not k / (nm - 1): the last frame before a cut is still moving
            # The first held frame is k == nm. Advancing by one here would
            # reach the target a frame early and make a 2 s hold last 61 frames.
            t = ease(min(1.0, k / nm), kind) if not static else 0.0
            sc = math.exp(math.log(sa) + (math.log(sb) - math.log(sa)) * t)
            steps.append((src, sc, ax + (bx - ax) * t, ay + (by - ay) * t))
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = 0
    label = spec.get("label")
    if spec.get("fast_intro"):
        # Hook: the whole tour at high speed in the first FAST_INTRO seconds, a thin
        # bar filling under the Reels header, then the tour again at its own pace.
        m = round(FAST_INTRO * FPS)
        for j in range(m):
            src, sc, cx, cy = steps[min(len(steps) - 1, round(j * len(steps) / m))]
            fr = draw(load(src), sc, cx, cy)
            fr.paste((255, 255, 255), (0, BAR_Y, W, BAR_Y + BAR_H))
            fr.paste((0, 0, 0), (0, BAR_Y, round(W * (j + 1) / m), BAR_Y + BAR_H))
            if label and j / FPS < label.get("until", 3.0):
                draw_label(fr, label)
            proc.stdin.write(fr.tobytes())
        total += m
    last = (None, None)
    t0 = FAST_INTRO if spec.get("fast_intro") else 0.0
    for i, st in enumerate(steps):
        if label and t0 + i / FPS < label.get("until", 3.0):
            proc.stdin.write(draw_label(draw(load(st[0]), *st[1:]), label).tobytes())
            continue
        if st != last[0]:   # static (process) reels repeat the same frame
            last = (st, draw(load(st[0]), *st[1:]).tobytes())
        proc.stdin.write(last[1])
    total += len(steps)
    card = endcard().tobytes()
    for _ in range(round(ENDCARD_DUR * FPS)):
        proc.stdin.write(card)
    total += round(ENDCARD_DUR * FPS)
    proc.stdin.close()
    if proc.wait():
        sys.exit("ffmpeg failed")
    if spec.get("bell"):
        add_bell(path)
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
    global SPEC_DIR
    spec_path = sys.argv[1]
    outdir = os.path.dirname(os.path.abspath(spec_path))
    SPEC_DIR = outdir
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
