#!/usr/bin/env python3
"""
processcover.py - cover for a process reel: the left half of the painting as
its first (barest) stage, the right half as the finished painting, on white,
in the same place the painting sits in the video.

Usage
  python3 tools/processcover.py posts/<folder>        (reads <folder>/reel.mp4)

The first frame of the reel is the first stage; the finished painting is read
1.5 s before the end (inside the 2 s hold, before the 1 s end card). The stage
is scaled onto the finished painting's rectangle so the two halves line up.
"""

import io
import os
import subprocess
import sys

import numpy as np
from PIL import Image

W, H = 1080, 1920


def frame(video, t):
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGB")


def bbox(im):
    a = np.asarray(im.convert("L"))
    ys, xs = np.where(a < 245)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def main():
    folder = sys.argv[1]
    video = os.path.join(folder, "reel.mp4")
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", video]))
    first, final = frame(video, 0), frame(video, dur - 1.5)
    fb, lb = bbox(first), bbox(final)
    stage = first.crop(fb).resize((lb[2] - lb[0], lb[3] - lb[1]), Image.LANCZOS)
    done = final.crop(lb)
    half = stage.width // 2
    split = done.copy()
    split.paste(stage.crop((0, 0, half, stage.height)), (0, 0))
    cover = Image.new("RGB", (W, H), "white")
    cover.paste(split, (lb[0], lb[1]))
    cover.save(os.path.join(folder, "cover.jpg"), quality=94, subsampling=0)
    print(f"{folder}/cover.jpg")


if __name__ == "__main__":
    main()
