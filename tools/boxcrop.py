"""Show one object whole and centred: crop its box, fit it in 1080x1350 with a 5% white margin."""
import json, os, sys
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOTS = {"details": "/home/user/yigitozen-painting-details", "details2": "/home/user/yigitozen-painting-details-2",
         "yigit": "/home/user/yigit"}
OW, OH, M = 1080, 1350, 0.05   # the object fills the frame up to a 5% white margin

def render_fill(src, box, out):
    """Fit the object's box in a 4:5 window of the painting itself (no white):
    centred on the object, moved only as far as needed to stay inside the
    painting, so where the painting ends the frame ends."""
    repo, path = src.split(":", 1)
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOTS[repo], path))).convert("RGB")
    W, H = im.size
    x0, y0, x1, y1 = box[0] * W, box[1] * H, box[2] * W, box[3] * H
    ww = max(x1 - x0, (y1 - y0) * OW / OH)
    wh = ww * OH / OW
    if ww > W or wh > H:
        print(f"  ! window larger than the painting, white fills the rest: {path}")
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    left = min(max(cx - ww / 2, 0), max(W - ww, 0))
    top = min(max(cy - wh / 2, 0), max(H - wh, 0))
    if ww <= W and wh <= H:
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
        if f[:2].isdigit() and f.endswith(".jpg"): os.remove(os.path.join(d, f))
    for i, s in enumerate(spec["slides"], 1):
        fn = render_fill if spec.get("fit") == "fill" else render
        k = fn(s["src"], s["box"], os.path.join(d, f"{i:02d}.jpg"))
        print(f"{i:02d} x{k:.2f} {s['work']}: {s['note']}")
