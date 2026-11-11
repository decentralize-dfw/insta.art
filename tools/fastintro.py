"""Put the fast opening and the bell on a finished reel without re-encoding it.

    python3 tools/fastintro.py <folder> [<folder> ...]

For reels that are not rendered from a spec by tools/render.py (process reels
made from uploads, footage, the 3D model clip): the whole reel without its 1 s
end card plays in the first 2 s with the thin bar, then the reel as it is.
Only the 2 s opening is encoded (same settings as the reel, CRF 17); it is
joined to the untouched reel with the concat demuxer (-c copy). Then the bell
(render.add_bell). The folder's spec.json gets "fast_intro" and "bell".
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402

ENDCARD = render.ENDCARD_DUR


def probe(path, what):
    return subprocess.check_output(["ffprobe", "-v", "error", *what, "-of", "csv=p=0", path], text=True).strip()


def apply(folder, maxrate=None):
    reel = os.path.join(folder, "reel.mp4")
    if probe(reel, ["-select_streams", "a", "-show_entries", "stream=index"]):
        sys.exit(f"{reel}: already has sound, so it was already done")
    dur = float(probe(reel, ["-show_entries", "format=duration"]))
    body = dur - ENDCARD
    k = body / render.FAST_INTRO
    m = round(render.FAST_INTRO * render.FPS)
    tmp = tempfile.mkdtemp()
    fast = os.path.join(tmp, "fast.mp4")
    y, h = render.BAR_Y, render.BAR_H
    graph = (f"[0:v]trim=0:{body},setpts=(PTS-STARTPTS)/{k},fps={render.FPS}[f0];"
             f"color=c=white:s={render.W}x{h}:r={render.FPS}:d={render.FAST_INTRO}[track];"
             f"[f0][track]overlay=x=0:y={y}:eof_action=pass[f1];"
             f"color=c=black:s={render.W}x{h}:r={render.FPS}:d={render.FAST_INTRO}[bar];"
             f"[f1][bar]overlay=x='-{render.W}+{render.W}*(n+1)/{m}':y={y}:eof_action=pass,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", reel, "-filter_complex", graph,
                    "-map", "[v]", "-frames:v", str(m), "-an", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "17", "-profile:v", "high", "-level", "5.0", "-pix_fmt", "yuv420p",
                    *(["-maxrate", maxrate, "-bufsize", maxrate] if maxrate else []),
                    "-video_track_timescale", "15360", fast], check=True)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.write(f"file '{fast}'\nfile '{os.path.abspath(reel)}'\n")
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", "-movflags", "+faststart", joined], check=True)
    # the joined file must decode end to end
    subprocess.run(["ffmpeg", "-v", "error", "-xerror", "-i", joined, "-f", "null", "-"], check=True)
    os.replace(joined, reel)
    render.add_bell(reel)
    sp = os.path.join(folder, "spec.json")
    spec = json.load(open(sp)) if os.path.exists(sp) else {}
    spec.update({"fast_intro": True, "bell": True})
    with open(sp, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"{reel}  {float(probe(reel, ['-show_entries', 'format=duration'])):.1f}s  x{k:.1f}")


if __name__ == "__main__":
    args = sys.argv[1:]
    cap = None
    if args and args[0].startswith("--maxrate="):
        cap = args.pop(0).split("=", 1)[1]
    for folder in args:
        apply(folder, cap)
