#!/usr/bin/env python3
"""
review.py - contact strip and checks for a rendered reel.

Usage
  python3 tools/review.py posts/<folder>

Writes <folder>/review.jpg (15 evenly spaced frames, true 9:16 aspect) and
prints the checks: duration, audio streams, frozen stretches (detail reels
must only freeze in the final 2 s hold and the 1 s end card), and distinct frames (process reels with a
static camera must show exactly one image per stage).
"""

import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def main():
    folder = sys.argv[1]
    reel = os.path.join(folder, "reel.mp4")
    spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", reel]))
    streams = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", reel],
        text=True).split()

    tw, th, n = 180, 320, 15
    strip = Image.new("RGB", (n * (tw + 6), th + 22), (210, 210, 210))
    d = ImageDraw.Draw(strip)
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(n):
            t = dur * (i + 0.5) / n
            f = os.path.join(tmp, f"{i}.jpg")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", reel,
                            "-frames:v", "1", "-vf", f"scale={tw}:{th}", f], check=True)
            strip.paste(Image.open(f), (i * (tw + 6), 20))
            d.text((i * (tw + 6) + 3, 4), f"{t:.1f}s", fill="black")
    strip.save(os.path.join(folder, "review.jpg"), quality=82)

    lines = [f"duration {dur:.1f} s", f"streams: {' '.join(streams)}"]
    if spec.get("camera") == "static":
        out = subprocess.run(["ffmpeg", "-i", reel, "-vf", "mpdecimate=hi=64*12:lo=64*5:frac=0.33",
                              "-f", "null", "-"], capture_output=True, text=True).stderr
        frames = re.findall(r"frame=\s*(\d+)", out)
        lines.append(f"distinct images: {frames[-1] if frames else '?'} "
                     f"(stages + final + end card = {len(spec['shots']) + 1})")
    else:
        out = subprocess.run(["ffmpeg", "-i", reel, "-vf", "freezedetect=n=0.0005:d=0.15",
                              "-map", "0:v", "-f", "null", "-"], capture_output=True, text=True).stderr
        starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", out)]
        mid = [s for s in starts if s < dur - 3.6]  # final 2 s hold + 1 s end card
        lines.append("frozen stretches before the final hold: " +
                     (", ".join(f"{s:.2f}s" for s in mid) if mid else "none"))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
