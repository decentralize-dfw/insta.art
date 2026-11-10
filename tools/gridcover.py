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


def main():
    folder = sys.argv[1]
    spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    slides = sorted(f for f in glob.glob(os.path.join(folder, "[0-9][0-9].jpg"))
                    if not f.endswith("00.jpg"))
    counts = layout(len(slides))
    frame = Image.new("RGB", (OW, OH), "white")
    r = len(counts)
    rh = (OH - GUTTER * (r - 1)) / r
    k = 0
    for i, c in enumerate(counts):
        cw = (OW - GUTTER * (c - 1)) / c
        y0, y1 = round(i * (rh + GUTTER)), round(i * (rh + GUTTER) + rh)
        for j in range(c):
            x0, x1 = round(j * (cw + GUTTER)), round(j * (cw + GUTTER) + cw)
            frame.paste(cover(Image.open(slides[k]).convert("RGB"), x1 - x0, y1 - y0), (x0, y0))
            k += 1

    word = spec.get("theme") or spec.get("label")
    if not word:
        works = json.load(open(WORKS, encoding="utf-8"))
        word = next(w["title"] for w in works if w["slug"] == spec["work"])
    d = ImageDraw.Draw(frame)
    pw, ph, gap = 44, 26, 10
    maxw = OW * 0.78 - 2 * pw
    for size in (64, 56, 48, 42):
        font = ImageFont.truetype(FONT, size)
        lines, cur = [], ""
        for tok in word.split():
            t = (cur + " " + tok).strip()
            if cur and d.textlength(t, font=font) > maxw:
                lines.append(cur)
                cur = tok
            else:
                cur = t
        lines.append(cur)
        if len(lines) <= 3:
            break
    asc, desc = font.getmetrics()
    lh = asc + desc
    tw = max(d.textlength(x, font=font) for x in lines)
    bw, bh = tw + 2 * pw, lh * len(lines) + gap * (len(lines) - 1) + 2 * ph
    bx, by = (OW - bw) / 2, (OH - bh) / 2
    d.rectangle([bx, by, bx + bw, by + bh], fill="white")
    for i, x in enumerate(lines):
        d.text(((OW - d.textlength(x, font=font)) / 2, by + ph + i * (lh + gap)), x, font=font, fill="black")
    frame.save(os.path.join(folder, "00.jpg"), quality=94, subsampling=0)
    print(f"{folder}/00.jpg  {len(slides)} slides in rows {counts}")


if __name__ == "__main__":
    main()
