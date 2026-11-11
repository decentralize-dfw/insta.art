"""One frame for every cover in the grid.

    python3 tools/covers.py

Every cover is laid out in what the profile grid shows (a 3:4 tile): the image
top left, 10 % of the tile width in from the left and the top, whole inside 60 %
of the tile, on white. Carousel collage covers: tools/gridcover.py (same layout).

  detail reels         spec "cover" image
  process reels        split: left half sketch, right half finished (from the reel)
  footage, 3D model    split: left half early frame, right half finished (from the reel)
  single posts         01.jpg, the whole painting from its master file
  process carousel     00.jpg, split of slides 03 (interim) and 04 (finished)
"""
import glob, io, json, os, subprocess, sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402
import workposts  # noqa: E402

REPO = render.REPO
OW, OH = 1080, 1350
# The profile grid shows every tile as 3:4: a 4:5 post shows its middle 1012x1350,
# a 9:16 reel its middle 1080x1440. In that visible tile the image sits top left,
# BORDER of the tile width in from the left and the top, whole inside a box of
# SIZE of the tile width and height. Titles (collages) go under the image.
BORDER = 0.10
SIZE = 0.60
TITLE = 10.5 / 130   # title size as a share of the tile width: ~10.5 px on a phone tile
FONT = os.path.join(render.REPO, "assets", "fonts", "HankenGrotesk-500.ttf")

# split covers from reels: seconds of (early frame, finished frame) in the reel as it is now
SPLIT = {
    "kopstal/7-fam-board-game-footage": (5.4, 28.9),
    "kopstal/sept-neuf-footage": (2.2, 55.0),
    "milan/caprocorn-sister-war-plague-earthquake-footage": (4.2, 2.5),
    "milan/viperella-footage": (10.0, 52.0),
    "kopstal/angora-mergvs-model": (5.0, 11.4),
}


def layout(im, reel=False, title=None):
    """The image top left in the visible 3:4 tile, on white; optional title under it."""
    from PIL import ImageDraw, ImageFont
    if reel:
        size, vis_w, vis_h, vx, vy = (render.W, render.H), 1080, 1440, 0, (render.H - 1440) // 2
    else:
        size, vis_w, vis_h, vx, vy = (OW, OH), 1012, OH, (OW - 1012) // 2, 0
    k = min(vis_w * SIZE / im.width, vis_h * SIZE / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    out = Image.new("RGB", size, "white")
    x, y = round(vx + vis_w * BORDER), round(vy + vis_w * BORDER)
    out.paste(im, (x, y))
    if title:
        fs = round(vis_w * TITLE)
        ImageDraw.Draw(out).text((x, y + im.height + round(fs * 0.5)), title,
                                 font=ImageFont.truetype(FONT, fs), fill="black")
    return out


def fit(im, title=None):
    """A 4:5 post (single, carousel cover)."""
    return layout(im, False, title)


def reel_cover(im):
    """A 9:16 reel cover."""
    return layout(im, True)


def content(im):
    """Crop the white around a painting (or a video frame on white)."""
    g = im.convert("L").point(lambda v: 255 if v < 245 else 0)
    return im.crop(g.getbbox() or (0, 0) + im.size)


def frame_at(video, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGB")


def split(early, done):
    """Left half from the early image, right half from the finished one, same box."""
    box = Image.new("L", early.size)
    a, b = content(early), content(done)
    b = b.resize(a.size, Image.LANCZOS) if b.size != a.size else b
    out = b.copy()
    out.paste(a.crop((0, 0, a.width // 2, a.height)), (0, 0))
    return out


def save(im, path):
    im.save(path, quality=95, subsampling=0)
    print(os.path.relpath(path, REPO))


def main():
    os.chdir(REPO)
    for sp in sorted(glob.glob("posts/kopstal/*-details/spec.json") + glob.glob("posts/milan/*-details/spec.json")):
        c = json.load(open(sp)).get("cover")
        if c:
            save(reel_cover((content(render.load(c["src"])))), os.path.join(os.path.dirname(sp), "cover.jpg"))
    for d in sorted(glob.glob("posts/kopstal/*-process")):
        v = os.path.join(d, "reel.mp4")
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", v]))
        # the loop: finished painting right after the 2 s opening, sketch just before the end card
        spec = json.load(open(os.path.join(d, "spec.json")))
        if "dissolve" in spec.get("loop", ""):
            import processloop as pl   # sketch, then fade, logo in, logo: take the middle of the sketch
            sketch_t = dur - pl.LOGO_HOLD - pl.LOGO_IN - pl.FADE - pl.LAST / 2
        else:
            sketch_t = dur - render.ENDCARD_DUR - 0.25
        save(reel_cover((split(frame_at(v, sketch_t), frame_at(v, 2.25)))),
             os.path.join(d, "cover.jpg"))
    for rel, (t0, t1) in SPLIT.items():
        v = os.path.join("posts", rel, "reel.mp4")
        save(reel_cover((split(frame_at(v, t0), frame_at(v, t1)))), os.path.join("posts", rel, "cover.jpg"))
    for sp in sorted(glob.glob("posts/single/*/spec.json")):
        s = json.load(open(sp))
        im = workposts.load(workposts.path_of(s["src"]))
        if s.get("trim"):
            im = workposts.trim_margin(im)
        save(fit(im), os.path.join(os.path.dirname(sp), "01.jpg"))
    pc = "posts/process-carousel/painstaking"
    save(fit(split(Image.open(f"{pc}/03.jpg").convert("RGB"), Image.open(f"{pc}/04.jpg").convert("RGB"))),
         f"{pc}/00.jpg")


if __name__ == "__main__":
    main()
