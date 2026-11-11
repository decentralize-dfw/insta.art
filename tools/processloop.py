"""Process reels as a loop: fast forward, then the stages backwards.

    python3 tools/processloop.py <folder> <plain_reel.mp4>

<plain_reel.mp4> is the process reel without opening and sound (stages, final
painting, 1 s end card). Output, one encode (CRF 17):
  2 s   every stage at high speed, sketch to finished, thin bar   (the hook)
  ...   the stages backwards, finished to sketch: each stage shows 0.5 s,
        with a 0.5 s cross dissolve into the next
  1 s   the sketch stays, then 1 s fade to white
  2 s   end card: the logo fades in over 1 s, then stays 1 s
The reel starts again on the sketch, so it loops. Then the bell.
"""
import json, os, subprocess, sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402

W, H, FPS = render.W, render.H, render.FPS
SHOW = 0.5       # each stage, fully visible
DISSOLVE = 0.5   # cross dissolve between stages
LAST = 1.0       # the sketch at the end, fully visible
FADE = 1.0       # then to white
LOGO_IN = 1.0    # the end card logo fades in from white
LOGO_HOLD = 1.0  # and stays
CUT = 3.0        # mean grey difference (0-255) between frames that counts as a new stage


def probe_dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]))


def frames(path, vf, size):
    """Decode with a filter to raw RGB frames of this size."""
    w, h = size
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-fps_mode", "passthrough", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    n = len(raw) // (w * h * 3)
    return np.frombuffer(raw, np.uint8)[: n * w * h * 3].reshape(n, h, w, 3)


def stages(plain, body):
    """One full-size image per stage, in painting order (sketch first, finished last)."""
    small = frames(plain, f"trim=0:{body},scale=108:192,format=gray,format=rgb24", (108, 192))[..., 0].astype(float)
    diff = np.abs(np.diff(small, axis=0)).mean(axis=(1, 2))
    bounds = [0] + [i + 1 for i, d in enumerate(diff) if d > CUT] + [len(small)]
    picks = [(a + b - 1) // 2 for a, b in zip(bounds, bounds[1:]) if b - a >= 3]
    sel = "+".join(f"eq(n\\,{i})" for i in picks)
    full = frames(plain, f"select='{sel}'", (W, H))
    return [Image.fromarray(f) for f in full]


def main(folder, plain):
    body = probe_dur(plain) - render.ENDCARD_DUR
    imgs = stages(plain, body)
    m = round(render.FAST_INTRO * FPS)
    fast = frames(plain, f"trim=0:{body},setpts=(PTS-STARTPTS)/{body / render.FAST_INTRO},fps={FPS}", (W, H))[:m]
    out = os.path.join(folder, "reel.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264",
                            "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
                           stdin=subprocess.PIPE)
    put = lambda im: enc.stdin.write(im.tobytes())
    y, h = render.BAR_Y, render.BAR_H
    for j, f in enumerate(fast):
        fr = Image.fromarray(f)
        fr.paste((255, 255, 255), (0, y, W, y + h))
        fr.paste((0, 0, 0), (0, y, round(W * (j + 1) / m), y + h))
        put(fr)
    back = imgs[::-1]
    show, dis = round(SHOW * FPS), round(DISSOLVE * FPS)
    for i, im in enumerate(back[:-1]):
        for _ in range(show):
            put(im)
        nxt = back[i + 1]
        for t in range(1, dis + 1):
            put(Image.blend(im, nxt, t / (dis + 1)))
    sketch = back[-1]
    for _ in range(round(LAST * FPS)):
        put(sketch)
    white = Image.new("RGB", (W, H), "white")
    fade = round(FADE * FPS)
    for t in range(1, fade + 1):
        put(Image.blend(sketch, white, t / fade))
    card = render.endcard()
    n_in = round(LOGO_IN * FPS)
    for t in range(1, n_in + 1):
        put(Image.blend(white, card, t / n_in))
    for _ in range(round(LOGO_HOLD * FPS)):
        put(card)
    enc.stdin.close()
    if enc.wait():
        sys.exit("ffmpeg failed")
    render.add_bell(out)
    sp = os.path.join(folder, "spec.json")
    spec = json.load(open(sp)) if os.path.exists(sp) else {}
    spec.update({"fast_intro": True, "bell": True,
                 "loop": "fast forward, then the stages backwards with 0.5 s cross dissolves"})
    with open(sp, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"{out}  {probe_dur(out):.1f}s  ({len(imgs)} stages)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
