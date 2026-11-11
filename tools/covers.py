"""One frame for every cover in the grid.

    python3 tools/covers.py

Every cover shows in the profile grid (3:4 tiles) with the same white frame,
54 px in a 1012 px wide tile, the image whole inside it: 4:5 posts use a
904x1242 box (88 px left/right, 54 px top/bottom), reels a 965x1325 box in the
middle of the 1080x1920 frame. Carousel grid covers: tools/gridcover.py.

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
MARGIN = 54
# The profile grid shows every tile as 3:4: a 4:5 post loses 34 px a side
# (1012x1350 visible), a 9:16 reel shows its middle 1080x1440. The box is set
# in that visible area so the white frame is the same 54 px (in 1012) on every tile.
POST_BOX = (1012 - 2 * MARGIN, OH - 2 * MARGIN)                 # 904 x 1242
K = 1080 / 1012
REEL_BOX = (round(1080 - 2 * MARGIN * K), round(1440 - 2 * MARGIN * K))  # 965 x 1325

# split covers from reels: seconds of (early frame, finished frame) in the reel as it is now
SPLIT = {
    "kopstal/7-fam-board-game-footage": (5.4, 28.9),
    "kopstal/sept-neuf-footage": (2.2, 55.0),
    "milan/caprocorn-sister-war-plague-earthquake-footage": (4.2, 2.5),
    "milan/viperella-footage": (10.0, 52.0),
    "kopstal/angora-mergvs-model": (5.0, 11.4),
}


def place(im, box, size):
    """The image whole inside the box, centred on a white frame of this size."""
    k = min(box[0] / im.width, box[1] / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    out = Image.new("RGB", size, "white")
    out.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    return out


def fit(im):
    """A 4:5 post (single, carousel cover)."""
    return place(im, POST_BOX, (OW, OH))


def reel_cover(im):
    """A 9:16 reel cover."""
    return place(im, REEL_BOX, (render.W, render.H))


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
        save(reel_cover((split(frame_at(v, dur - render.ENDCARD_DUR - 0.25), frame_at(v, 2.25)))),
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
