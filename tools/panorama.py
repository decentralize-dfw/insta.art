"""A detail carousel that reads as one strip: swipe and the next photo goes on.

    python3 tools/panorama.py <folder>

<folder>/spec.json lists "details" (photos, in order) and "cover" (the
master). Every photo is fit to the slide height (1350) and the photos sit side
by side with a thin white GAP; the strip is cut into 1080 x 1350 slides
(01.jpg, 02.jpg, ...). Each photo is trimmed a few pixels at its sides so the
strip ends exactly on a slide edge. 00.jpg is the cover: the whole painting
in the usual cover layout (tools/covers.py). With "end": "full" the last slide
is the whole painting again, filling the slide edge to edge.
"""
import json, os, sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import covers  # noqa: E402
import workposts  # noqa: E402

OW, OH = 1080, 1350
GAP = 20
MAX_SLIDES = 20


def strip(paths):
    ims = [workposts.load(workposts.path_of(p)) for p in paths]
    n = len(ims)
    natural = sum(round(im.width * OH / im.height) for im in ims) + GAP * (n - 1)
    slides = round(natural / OW)
    room = slides * OW - GAP * (n - 1)
    widths = [room * (i + 1) // n - room * i // n for i in range(n)]
    out = Image.new("RGB", (slides * OW, OH), "white")
    x = 0
    for im, w in zip(ims, widths):
        k = max(w / im.width, OH / im.height)          # cover the cell, trim the overflow
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        l, t = (im.width - w) // 2, (im.height - OH) // 2
        out.paste(im.crop((l, t, l + w, t + OH)), (x, 0))
        x += w + GAP
    return out, slides


def main(folder):
    spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    im, n = strip(spec["details"])
    end = spec.get("end") == "full"
    if n + 1 + end > MAX_SLIDES:
        sys.exit(f"{n} slides + cover is over Instagram's {MAX_SLIDES}")
    for i in range(n):
        im.crop((i * OW, 0, (i + 1) * OW, OH)).save(os.path.join(folder, f"{i + 1:02d}.jpg"),
                                                     quality=95, subsampling=0)
    master = covers.content(workposts.load(workposts.path_of(spec["cover"])))
    covers.save(covers.fit(master), os.path.join(folder, "00.jpg"))
    if end:
        k = max(OW / master.width, OH / master.height)
        full = master.resize((round(master.width * k), round(master.height * k)), Image.LANCZOS)
        l, t = (full.width - OW) // 2, (full.height - OH) // 2
        covers.save(full.crop((l, t, l + OW, t + OH)), os.path.join(folder, f"{n + 1:02d}.jpg"))
        n += 1
    print(f"{folder}: cover + {n} slides, {len(spec['details'])} photos")


if __name__ == "__main__":
    main(sys.argv[1])
