"""Show one object whole and centred: crop its box, fit it in 1080x1350 with a 5% white margin."""
import json, os, sys
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOTS = {"details": "/home/user/yigitozen-painting-details", "details2": "/home/user/yigitozen-painting-details-2",
         "yigit": "/home/user/yigit"}
OW, OH, M = 1080, 1350, 0.05   # the object fills the frame up to a 5% white margin

def render_fill(src, box, out, bounds=None, fit_width=False, valign="center"):
    """Fit the object's box in a 4:5 window of the painting itself (no white):
    centred on the object, moved only as far as needed to stay inside the
    painting, so where the painting ends the frame ends."""
    repo, path = src.split(":", 1)
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOTS[repo], path))).convert("RGB")
    W, H = im.size
    x0, y0, x1, y1 = box[0] * W, box[1] * H, box[2] * W, box[3] * H
    ww = max(x1 - x0, (y1 - y0) * OW / OH)
    if fit_width:   # the object is the whole canvas: use the full width, trim top and bottom
        ww = ((bounds or [0, 0, 1, 1])[2] - (bounds or [0, 0, 1, 1])[0]) * W
    wh = ww * OH / OW
    if ww > W or wh > H:
        print(f"  ! window larger than the painting, white fills the rest: {path}")
    # bounds: the painted area inside the photo (normalised), when the photo
    # has paper or wall around the painting
    bx0, by0, bx1, by1 = [v * d for v, d in zip(bounds or [0, 0, 1, 1], (W, H, W, H))]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    left = min(max(cx - ww / 2, bx0), max(bx1 - ww, bx0))
    top = min(max(cy - wh / 2, by0), max(by1 - wh, by0))
    if valign == "top":   # keep the top of the painting, trim only from the bottom
        top = by0
    if ww <= bx1 - bx0 and wh <= by1 - by0:
        frame = im.resize((OW, OH), Image.LANCZOS, box=(left, top, left + ww, top + wh))
    else:
        k = min(OW / ww, OH / wh)
        part = im.crop((round(max(left, 0)), round(max(top, 0)), round(min(left + ww, W)), round(min(top + wh, H))))
        part = part.resize((round(part.width * k), round(part.height * k)), Image.LANCZOS)
        frame = Image.new("RGB", (OW, OH), "white")
        frame.paste(part, ((OW - part.width) // 2, (OH - part.height) // 2))
    frame.save(out, quality=94, subsampling=0)
    return OW / ww


def render(src, box, out):
    """Crop exactly the object's box and centre it on white; nothing around it."""
    repo, path = src.split(":", 1)
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOTS[repo], path))).convert("RGB")
    W, H = im.size
    crop = im.crop((round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H)))
    aw, ah = OW * (1 - 2 * M), OH * (1 - 2 * M)
    k = min(aw / crop.width, ah / crop.height)
    crop = crop.resize((round(crop.width * k), round(crop.height * k)), Image.LANCZOS)
    frame = Image.new("RGB", (OW, OH), "white")
    frame.paste(crop, ((OW - crop.width) // 2, (OH - crop.height) // 2))
    frame.save(out, quality=94, subsampling=0)
    return k   # >1 means enlarged

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    d = os.path.dirname(os.path.abspath(sys.argv[1]))
    for f in os.listdir(d):
        if f[:2].isdigit() and f.endswith(".jpg") and f != "00.jpg":   # 00.jpg is the grid cover
            os.remove(os.path.join(d, f))
    for i, s in enumerate(spec["slides"], 1):
        fn = render_fill if spec.get("fit") == "fill" else render
        out = os.path.join(d, f"{i:02d}.jpg")
        k = fn(s["src"], s["box"], out, s.get("bounds"), s.get("fit_width", False),
               s.get("valign", "center")) if fn is render_fill \
            else fn(s["src"], s["box"], out)
        print(f"{i:02d} x{k:.2f} {s['work']}: {s['note']}")
