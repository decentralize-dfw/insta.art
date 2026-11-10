"""Turn a raw painting video (hand, brush, canvas) into an Instagram reel.

    python3 tools/footage.py <src.mp4> <out_dir> [--crop x,y,w,h] [--trim start,end]

The video is fitted to the full 1080 width on a white 1080x1920 frame, the
audio is dropped (music is added in the app), and the 1 s bird end card is
appended. H.264 CRF 17, preset slow, yuv420p, 30 fps: same as tools/render.py.
"""
import argparse, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402  (W, H, endcard)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out_dir")
    ap.add_argument("--crop", help="x,y,w,h of the painting inside the source frame")
    ap.add_argument("--trim", help="start,end in seconds")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    card = os.path.join(tempfile.mkdtemp(), "endcard.png")
    render.endcard().save(card)
    f = []
    if a.crop:
        x, y, w, h = a.crop.split(",")
        f.append(f"crop={w}:{h}:{x}:{y}")
    f += [f"scale={render.W}:-2:flags=lanczos",
          f"pad={render.W}:{render.H}:(ow-iw)/2:(oh-ih)/2:white",
          "setsar=1", "fps=30", "format=yuv420p"]
    trim = []
    if a.trim:
        s, e = a.trim.split(",")
        trim = ["-ss", s, "-to", e]
    graph = (f"[0:v]{','.join(f)}[v0];"
             f"[1:v]scale={render.W}:{render.H},setsar=1,fps=30,format=yuv420p[v1];"
             "[v0][v1]concat=n=2:v=1:a=0[v]")
    out = os.path.join(a.out_dir, "reel.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *trim, "-i", a.src,
           "-loop", "1", "-t", "1", "-framerate", "30", "-i", card,
           "-filter_complex", graph, "-map", "[v]", "-an",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == "__main__":
    main()
