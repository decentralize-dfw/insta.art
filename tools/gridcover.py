#!/usr/bin/env python3
"""
gridcover.py - first slide for an editorial carousel: every slide of the
carousel in a grid that fills the 1080x1350 frame, with the theme word in a
small white label in the middle.

Usage
  python3 tools/gridcover.py posts/editorial/<theme>

Reads <folder>/spec.json ("theme") and the slides 01.jpg, 02.jpg ... and
writes <folder>/00.jpg. Rows are chosen so the cells stay close to the 4:5
shape of the slides; each slide is centre-cropped into its cell (the slides
are already centred on their object).
"""

import glob
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(os.path.dirname(HERE), "assets", "fonts", "HankenGrotesk-500.ttf")
OW, OH = 1080, 1350
GUTTER = 6
TARGET = OW / OH
WORKS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "yigit", "v3", "content", "works.json")


def layout(n):
    """Rows with as-even-as-possible counts, cells closest to 4:5 (extra cells go to the middle rows)."""
    best = None
    for r in range(1, n + 1):
        base, extra = divmod(n, r)
        counts = [base] * r
        order = sorted(range(r), key=lambda i: abs(i - (r - 1) / 2))
        for i in order[:extra]:
            counts[i] += 1
        if min(counts) == 0:
            break
        rh = (OH - GUTTER * (r - 1)) / r
        score = sum(abs(math.log(((OW - GUTTER * (c - 1)) / c) / rh / TARGET)) * c for c in counts) / n
        if best is None or score < best[0]:
            best = (score, counts)
    return best[1]


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


MARGIN = 54          # white frame around the grid, top and bottom
MARGIN_X = 88        # left and right: the profile grid cuts 4:5 posts to 3:4 (34 px a side),
                     # so 88 here shows as the same 54 px frame there (tools/covers.py)
GAP = 12             # white between the images
BAND = 150           # white band under the grid for the title


def title_of(spec):
    word = spec.get("theme") or spec.get("label")
    if not word:
        works = json.load(open(WORKS, encoding="utf-8"))
        word = next(w["title"] for w in works if w["slug"] == spec["work"])
    return word


def collage(slides):
    """First 9 slides as 3x3, or first 4 as 2x2 when there are fewer than 9.
    Slides keep their 4:5 shape, nothing is cut."""
    n = 3 if len(slides) >= 9 else 2
    slides = slides[:n * n]
    cw, ch, gap = 600, 750, 18
    out = Image.new("RGB", (n * cw + (n - 1) * gap, n * ch + (n - 1) * gap), "white")
    for i, f in enumerate(slides):
        im = Image.open(f).convert("RGB").resize((cw, ch), Image.LANCZOS)
        out.paste(im, ((i % n) * (cw + gap), (i // n) * (ch + gap)))
    return out, n


def main():
    import covers
    folder = sys.argv[1]
    spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    slides = sorted(f for f in glob.glob(os.path.join(folder, "[0-9][0-9].jpg"))
                    if not f.endswith("00.jpg"))
    im, n = collage(slides)
    covers.fit(im, title_of(spec)).save(os.path.join(folder, "00.jpg"), quality=94, subsampling=0)
    print(f"{folder}/00.jpg  {n}x{n} of {len(slides)} slides")


def layout_in(n, gw, gh):
    """Rows with as-even-as-possible counts, cells closest to 4:5 inside the grid area."""
    best = None
    for r in range(1, n + 1):
        base, extra = divmod(n, r)
        counts = [base] * r
        order = sorted(range(r), key=lambda i: abs(i - (r - 1) / 2))
        for i in order[:extra]:
            counts[i] += 1
        if min(counts) == 0:
            break
        rh = (gh - GAP * (r - 1)) / r
        score = sum(abs(math.log(((gw - GAP * (c - 1)) / c) / rh / (OW / OH))) * c for c in counts) / n
        if best is None or score < best[0]:
            best = (score, counts)
    return best[1]


if __name__ == "__main__":
    main()
