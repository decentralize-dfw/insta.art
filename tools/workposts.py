#!/usr/bin/env python3
"""
workposts.py - for every painting, two posts besides its reels:

  posts/single/<slug>/01.jpg    the whole painting, its own proportions, on white
  posts/details/<slug>/NN.jpg   its detail photos as a carousel, 4:5, no white

Usage
  python3 tools/workposts.py [slug ...]      (no slug: every work)

Masters and detail photos are listed in SOURCES below. Detail photos are
cropped to 4:5 around the busiest part of the photo (most brushwork), with a
pull toward the centre; near-duplicate photos are skipped and a carousel
holds at most 20 slides (Instagram's limit). Works with no detail photos get
only the single post.
"""

import glob
import json
import os
import re
import sys

import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PARENT = os.path.dirname(REPO)
ROOTS = {"yigit": os.path.join(PARENT, "yigit"),
         "details": os.path.join(PARENT, "yigitozen-painting-details"),
         "details2": os.path.join(PARENT, "yigitozen-painting-details-2")}
WORKS = os.path.join(ROOTS["yigit"], "v3", "content", "works.json")
OW, OH = 1080, 1350
PAD = 60
MAX_SLIDES = 20

# slug: (master, [detail globs]); trim=True strips the white photo margin
D1, D2, Y = "details:", "details2:", "yigit:img/full/"
SOURCES = {
    "painstaking": (D1 + "painstaking/painstaking-triptic-transparent.png", [D1 + "painstaking/painstaking-detail-*.jpg"]),
    "angora-mergvs": (D1 + "angora-mergvs/angora-mergvs-10mb.jpg", [D1 + "angora-mergvs/angora-mergvs-detail-*.jpg"]),
    "gxd-is-afk-we-banned-it": (D1 + "gxdisbanned/gxd-is-banned2.png", [D1 + "gxdisbanned/IMG_*.jpg"]),
    "sept-neuf": (D1 + "sept-neuf/inverted-silvia--7-9.png", [D1 + "sept-neuf/IMG_*.JPG"]),
    "7-fam-board-game": (D1 + "7famboardgame/7fam-board-game.png", [D1 + "7famboardgame/[0-9].jpg"]),
    "virgil-on-virtual-cage-final-final-finalv9": (D1 + "masters/virgil-on-virtual-cage-RESOLUTION.png",
                                                   [D1 + "virgilonvirtualcage/virgilonvirtualcage_detail_*.png"]),
    "gary-grills-cooper": (Y + "gary-grills-cooper.jpg", [D1 + "garygrillscooper/garlgrillscooper_detail_*.png"]),
    "walls-of-perception": (Y + "walls-of-perception.jpg", [D1 + "wallsofperception/wallofperception_detail_*.png"]),
    "articulo-attack-on-mandarin": (Y + "articulo-attack-on-mandarin.jpg", [D1 + "articuloattackonmandarin/arcitul0_detail_*.png"]),
    "s-t-lop": (Y + "s-t-lop.jpg", [D1 + "stlop/stlop_detail_*.png"]),
}
TRIM = {"bacchus-2", "the-on-top-ruler", "despite-transgression", "see-u-in-the-other-side",
        "society-screwing-balance", "remixed-execution-of-lucid-drowning",
        "penguin-is-not-a-friend-only-a-sinner", "burningman-fast"}


def path_of(src):
    repo, p = src.split(":", 1)
    return os.path.join(ROOTS[repo], p)


def load(p):
    im = ImageOps.exif_transpose(Image.open(p))
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
    return im.convert("RGB")


def sources(slug):
    if slug in SOURCES:
        master, globs = SOURCES[slug]
    else:
        d2 = os.path.join(ROOTS["details2"], slug)
        m = [f for f in (f"{d2}/{slug}.png", f"{d2}/{slug}.jpg") if os.path.exists(f)]
        master = (D2 + os.path.relpath(m[0], ROOTS["details2"])) if m else Y + slug + ".jpg"
        globs = [D2 + f"{slug}/{slug}-detail-*.jpg"]
    files = []
    for g in globs:
        files += glob.glob(path_of(g))
    nat = lambda f: [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", os.path.basename(f))]
    return master, sorted(files, key=nat)


def trim_margin(im):
    a = np.asarray(im.convert("L")).astype(int)
    rows = np.where((a < 235).mean(axis=1) > 0.5)[0]
    cols = np.where((a < 235).mean(axis=0) > 0.5)[0]
    if len(rows) and len(cols):
        im = im.crop((cols.min(), rows.min(), cols.max() + 1, rows.max() + 1))
    return im


def single(im):
    k = min((OW - 2 * PAD) / im.width, (OH - 2 * PAD) / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    frame = Image.new("RGB", (OW, OH), "white")
    frame.paste(im, ((OW - im.width) // 2, (OH - im.height) // 2))
    return frame


def smart_crop(im):
    """4:5 window over the part with the most brushwork, pulled toward the centre."""
    W, H = im.size
    small = np.asarray(im.convert("L").resize((max(1, W // 8), max(1, H // 8)))).astype(float)
    gx = np.abs(np.diff(small, axis=1))[:-1, :]
    gy = np.abs(np.diff(small, axis=0))[:, :-1]
    energy = gx + gy
    if W / H > OW / OH:
        win = H * OW / OH
        prof = energy.sum(axis=0)
        n = len(prof)
        w = max(1, int(round(win / W * n)))
        csum = np.concatenate([[0], np.cumsum(prof)])
        scores = np.array([csum[i + w] - csum[i] for i in range(n - w + 1)])
        centre = (n - w) / 2
        scores *= 1 - 0.35 * np.abs(np.arange(len(scores)) - centre) / max(centre, 1)
        x0 = scores.argmax() / n * W
        box = (x0, 0, x0 + win, H)
    else:
        win = W * OH / OW
        prof = energy.sum(axis=1)
        n = len(prof)
        w = max(1, int(round(win / H * n)))
        csum = np.concatenate([[0], np.cumsum(prof)])
        scores = np.array([csum[i + w] - csum[i] for i in range(n - w + 1)])
        centre = (n - w) / 2
        scores *= 1 - 0.35 * np.abs(np.arange(len(scores)) - centre) / max(centre, 1)
        y0 = scores.argmax() / n * H
        box = (0, y0, W, y0 + win)
    return im.resize((OW, OH), Image.LANCZOS, box=box)


def thumb(im):
    return np.asarray(im.convert("L").resize((24, 24))).astype(float)


def caption(w):
    m = w["medium"].lower()
    if w.get("panel_count"):
        line = f"{w['year']} · {m} · triptych · {w['panel_count']} panels, each {w['panel_height_cm']} × {w['panel_width_cm']} cm"
    else:
        size = f"{w['height_cm']:g} × {w['width_cm']:g} cm"
        line = f"{w['year']} · {m} · {size}"
    return f"{w['title']}\n{line}\n"


def clear(d):
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, "[0-9][0-9].jpg")):
        os.remove(f)


def main():
    works = {w["slug"]: w for w in json.load(open(WORKS, encoding="utf-8"))}
    slugs = sys.argv[1:] or list(works)
    for slug in slugs:
        w = works[slug]
        master, details = sources(slug)
        desc = re.split(r"(?<=[.!?])\s+", w.get("description") or "")
        alt_desc = " ".join(desc[:2])

        mp = path_of(master)
        if not os.path.exists(mp):
            print(f"{slug}: no master, skipped")
            continue
        im = load(mp)
        if slug in TRIM:
            im = trim_margin(im)
        d = os.path.join(REPO, "posts", "single", slug)
        clear(d)
        single(im).save(os.path.join(d, "01.jpg"), quality=92, subsampling=0)
        open(os.path.join(d, "caption.txt"), "w", encoding="utf-8").write(caption(w))
        open(os.path.join(d, "alt.txt"), "w", encoding="utf-8").write(f"Acrylic painting by Yiğit Özen. {alt_desc}\n")
        json.dump({"type": "single", "work": slug, "src": master, "trim": slug in TRIM},
                  open(os.path.join(d, "spec.json"), "w"), indent=2, ensure_ascii=False)

        d = os.path.join(REPO, "posts", "details", slug)
        if not details:
            print(f"{slug}: single only (no detail photos)")
            continue
        clear(d)
        kept, seen = [], []
        for f in details:
            dim = load(f)
            t = thumb(dim)
            if any(np.abs(t - s).mean() < 6 for s in seen):
                continue
            seen.append(t)
            kept.append(f)
            smart_crop(dim).save(os.path.join(d, f"{len(kept):02d}.jpg"), quality=90, subsampling=0)
            if len(kept) == MAX_SLIDES:
                break
        open(os.path.join(d, "caption.txt"), "w", encoding="utf-8").write(caption(w))
        open(os.path.join(d, "alt.txt"), "w", encoding="utf-8").write(
            f"{len(kept)} close details of an acrylic painting by Yiğit Özen. {alt_desc}\n")
        json.dump({"type": "carousel", "work": slug, "kind": "details",
                   "slides": [os.path.relpath(f, PARENT) for f in kept]},
                  open(os.path.join(d, "spec.json"), "w"), indent=2, ensure_ascii=False)
        print(f"{slug}: single + {len(kept)} details (of {len(details)})")


if __name__ == "__main__":
    main()
