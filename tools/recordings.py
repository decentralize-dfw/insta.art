"""Covers and texts for edited process recordings kept in insta-art-archive.

    python3 tools/recordings.py

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


def main():
    for manifest in sorted(glob.glob(os.path.join(REPO, "posts", "recordings", "*", "videos.json"))):
        folder = os.path.dirname(manifest)
        m = json.load(open(manifest, encoding="utf-8"))
        cap = open(os.path.join(REPO, "posts", "single", m["work"], "caption.txt"), encoding="utf-8").read().strip()
        open(os.path.join(folder, "caption.txt"), "w", encoding="utf-8").write(cap + "\n")
        for v in m["videos"]:
            src = os.path.join(ARCHIVE, v["vpath"], v["file"])
            dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                 "-of", "csv=p=0", src]))
            cover = covers.reel_cover(covers.split(covers.frame_at(src, 0.3), covers.frame_at(src, dur - 0.3)))
            cover.save(os.path.join(folder, v["cover"]), quality=95, subsampling=0)
            print(os.path.relpath(os.path.join(folder, v["cover"]), REPO), f"{dur:.1f}s")


if __name__ == "__main__":
    main()
