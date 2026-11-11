"""Process reels as a loop: fast forward, then the stages backwards.

    python3 tools/processloop.py <folder> <plain_reel.mp4>

<plain_reel.mp4> is the process reel without opening and sound (stages, final
painting, 1 s end card). Output, one encode (CRF 17):
  2 s   every stage at high speed, sketch to finished, thin bar   (the hook)
  ...   the stages at their own pace backwards, finished to sketch;
        the finished painting holds 0.5 s at most
  1 s   end card
The reel starts again on the sketch, so it loops. Then the bell.
"""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402

HOLD = 0.5   # finished painting at the start of the backwards part


def main(folder, plain):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", plain]))
    body = dur - render.ENDCARD_DUR
    # where the finished painting starts to stand still at the end of the stages
    log = subprocess.run(["ffmpeg", "-i", plain, "-t", str(body), "-vf", "freezedetect=n=0.002:d=0.4",
                          "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", log)]
    final = max([s for s in starts if s > body - 3.0], default=body)
    keep = min(body, final + HOLD)
    k = body / render.FAST_INTRO
    m = round(render.FAST_INTRO * render.FPS)
    y, h, W, fps = render.BAR_Y, render.BAR_H, render.W, render.FPS
    graph = (f"[0:v]split=3[a][b][c];"
             f"[a]trim=0:{body},setpts=(PTS-STARTPTS)/{k},fps={fps},trim=end_frame={m}[f0];"
             f"color=c=white:s={W}x{h}:r={fps}:d={render.FAST_INTRO}[track];"
             f"[f0][track]overlay=x=0:y={y}:eof_action=pass[f1];"
             f"color=c=black:s={W}x{h}:r={fps}:d={render.FAST_INTRO}[bar];"
             f"[f1][bar]overlay=x='-{W}+{W}*(n+1)/{m}':y={y}:eof_action=pass[f];"
             f"[b]trim=0:{keep},setpts=PTS-STARTPTS,reverse[r];"
             f"[c]trim=start={body},setpts=PTS-STARTPTS[e];"
             f"[f][r][e]concat=n=3:v=1:a=0,format=yuv420p[v]")
    out = os.path.join(folder, "reel.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", plain, "-filter_complex", graph,
                    "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    render.add_bell(out)
    sp = os.path.join(folder, "spec.json")
    spec = json.load(open(sp)) if os.path.exists(sp) else {}
    spec.update({"fast_intro": True, "bell": True, "loop": "fast forward, then the stages backwards"})
    with open(sp, "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", out]))
    print(f"{out}  {total:.1f}s  (backwards part {keep:.1f}s, finished held {keep - final:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
