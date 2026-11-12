"""Covers and texts for edited process recordings kept in insta-art-archive.

    python3 tools/recordings.py            covers and captions
    python3 tools/recordings.py --render   Instagram versions (fast opening, bell, logo)

Reads posts/recordings/<work>/videos.json (one entry per video: archive folder,
file, display name, duration, alt text). The videos stay in the archive repo
(next to this one); each gets a cover here in the cover layout (top left, 60 %):
left half its first moment, right half its last. caption.txt is the work's
caption (title + künye). build_index.py lists every video as its own post.
"""
import glob, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import covers  # noqa: E402

REPO = covers.REPO
ARCHIVE = os.path.join(os.path.dirname(REPO), "insta-art-archive")


END_FADE, LOGO_IN, LOGO_HOLD = 1.0, 1.0, 1.0   # same soft ending as the process reels


def render_reel(src, out):
    """Instagram version, one encode (CRF 17): 2 s fast pass of the whole video with
    the bar, the video at its own pace, its last frame fading to white over 1 s,
    the logo fading in over 1 s and staying 1 s; then the bell."""
    import render
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", src]))
    W, H, fps = render.W, render.H, render.FPS
    m = round(render.FAST_INTRO * fps)
    y, h = render.BAR_Y, render.BAR_H
    card = out + ".card.png"
    render.endcard().save(card)
    graph = (f"[0:v]fps={fps},scale={W}:{H},setsar=1,split=2[a][b];"
             f"[a]setpts=(PTS-STARTPTS)/{dur / render.FAST_INTRO},fps={fps},trim=end_frame={m}[f0];"
             f"color=c=white:s={W}x{h}:r={fps}:d={render.FAST_INTRO}[t];[f0][t]overlay=x=0:y={y}:eof_action=pass[f1];"
             f"color=c=black:s={W}x{h}:r={fps}:d={render.FAST_INTRO}[bk];"
             f"[f1][bk]overlay=x='-{W}+{W}*(n+1)/{m}':y={y}:eof_action=pass,setsar=1[f];"
             f"[b]tpad=stop_mode=clone:stop_duration={END_FADE},"
             f"fade=t=out:st={dur:.3f}:d={END_FADE}:color=white,setsar=1[n];"
             f"[1:v]fps={fps},scale={W}:{H},setsar=1,fade=t=in:st=0:d={LOGO_IN}:color=white[e];"
             f"[f][n][e]concat=n=3:v=1:a=0,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                    "-loop", "1", "-framerate", str(fps), "-t", str(LOGO_IN + LOGO_HOLD), "-i", card,
                    "-filter_complex", graph, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
    os.remove(card)
    render.add_bell(out)


def render_all():
    """Write the Instagram versions to the archive at posts/recordings/<work>/<id>.mp4
    and point videos.json at them; the uploaded files stay where they are."""
    for manifest in sorted(glob.glob(os.path.join(REPO, "posts", "recordings", "*", "videos.json"))):
        m = json.load(open(manifest, encoding="utf-8"))
        rel = os.path.relpath(os.path.dirname(manifest), REPO)
        os.makedirs(os.path.join(ARCHIVE, rel), exist_ok=True)
        for v in m["videos"]:
            v.setdefault("source", f"{v['vpath']}/{v['file']}")
            out = os.path.join(ARCHIVE, rel, v["id"] + ".mp4")
            if not os.path.exists(out):
                render_reel(os.path.join(ARCHIVE, v["source"]), out)
            v["vpath"], v["file"] = rel, v["id"] + ".mp4"
            v["lfs"] = os.path.getsize(out) > 95 * 1024 * 1024
            print(rel + "/" + v["file"], f"{os.path.getsize(out) / 1e6:.0f} MB", "LFS" if v["lfs"] else "")
        with open(manifest, "w", encoding="utf-8") as f:
            json.dump(m, f, indent=1, ensure_ascii=False)


def main():
    for manifest in sorted(glob.glob(os.path.join(REPO, "posts", "recordings", "*", "videos.json"))):
        folder = os.path.dirname(manifest)
        m = json.load(open(manifest, encoding="utf-8"))
        cap = open(os.path.join(REPO, "posts", "single", m["work"], "caption.txt"), encoding="utf-8").read().strip()
        open(os.path.join(folder, "caption.txt"), "w", encoding="utf-8").write(cap + "\n")
        for v in m["videos"]:
            src = os.path.join(ARCHIVE, v.get("source") or f"{v['vpath']}/{v['file']}")
            dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                 "-of", "csv=p=0", src]))
            cover = covers.reel_cover(covers.split(covers.frame_at(src, 0.3), covers.frame_at(src, dur - 0.3)))
            cover.save(os.path.join(folder, v["cover"]), quality=95, subsampling=0)
            print(os.path.relpath(os.path.join(folder, v["cover"]), REPO), f"{dur:.1f}s")


if __name__ == "__main__":
    render_all() if "--render" in sys.argv else main()
