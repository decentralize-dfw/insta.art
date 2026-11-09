"""Crop so a whole object (normalized box) is visible in a 1080x1350 frame."""
import json, os, sys
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOTS = {"details": "/home/user/yigitozen-painting-details", "details2": "/home/user/yigitozen-painting-details-2",
         "yigit": "/home/user/yigit"}
OW, OH, M = 1080, 1350, 0.06

def render(src, box, out):
    repo, path = src.split(":", 1)
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOTS[repo], path))).convert("RGB")
    W, H = im.size
    x0, y0, x1, y1 = box[0] * W, box[1] * H, box[2] * W, box[3] * H
    bw, bh = (x1 - x0) * (1 + 2 * M), (y1 - y0) * (1 + 2 * M)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ww = max(bw, bh * OW / OH); wh = ww * OH / OW
    left = min(max(cx - ww / 2, 0), max(W - ww, 0)); top = min(max(cy - wh / 2, 0), max(H - wh, 0))
    if ww > W or wh > H:   # does not fit inside the image: white around it
        s = min(OW / ww, OH / wh)
        frame = Image.new("RGB", (OW, OH), "white")
        part = im.crop((max(left, 0), max(top, 0), min(left + ww, W), min(top + wh, H)))
        part = part.resize((round(part.width * s), round(part.height * s)), Image.LANCZOS)
        frame.paste(part, ((OW - part.width) // 2, (OH - part.height) // 2))
    else:
        frame = im.resize((OW, OH), Image.LANCZOS, box=(left, top, left + ww, top + wh))
    frame.save(out, quality=94, subsampling=0)
    return OW / ww   # >1 means enlarged

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    d = os.path.dirname(os.path.abspath(sys.argv[1]))
    for f in os.listdir(d):
        if f[:2].isdigit() and f.endswith(".jpg"): os.remove(os.path.join(d, f))
    for i, s in enumerate(spec["slides"], 1):
        k = render(s["src"], s["box"], os.path.join(d, f"{i:02d}.jpg"))
        print(f"{i:02d} x{k:.2f} {s['work']}: {s['note']}")
