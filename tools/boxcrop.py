"""Show one object whole and centred: crop its box, fit it in 1080x1350 with a 5% white margin."""
import json, os, sys
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
ROOTS = {"details": "/home/user/yigitozen-painting-details", "details2": "/home/user/yigitozen-painting-details-2",
         "yigit": "/home/user/yigit"}
OW, OH, M = 1080, 1350, 0.05   # the object fills the frame up to a 5% white margin

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
        k = render(s["src"], s["box"], os.path.join(d, f"{i:02d}.jpg"))
        print(f"{i:02d} x{k:.2f} {s['work']}: {s['note']}")
