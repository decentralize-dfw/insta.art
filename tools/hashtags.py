"""Five topic hashtags at the end of every caption.txt (Yiğit, 13 Nov 2026).

    python3 tools/hashtags.py

Caption = title, künye, empty line, hashtags. Three fixed tags, one for the
kind of post, one for where the work was made (2026 Kopstal → Luxembourg,
2019–2020 → Milano). Running it again replaces the hashtag line.
"""
import glob, json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKS = os.path.join(os.path.dirname(REPO), "yigit", "v3", "content", "works.json")
BASE = ["#figurativepainting", "#contemporarypainting", "#acrylicpainting"]


def kind_tag(rel):
    if rel.startswith("posts/portfolio/"):
        return "#artistbook"
    if rel.startswith("posts/single/"):
        return "#contemporaryart"
    if rel.startswith("posts/recordings/") or rel.endswith(("-process", "-footage", "-model")) \
            or rel.startswith("posts/process-carousel/"):
        return "#paintingprocess"
    return "#paintingdetail"


def place_tag(year):
    if year == 2026:
        return "#luxembourgartist"
    if year in (2019, 2020):
        return "#milanart"
    return "#figurativeart"


def main():
    works = {w["slug"]: w for w in json.load(open(WORKS, encoding="utf-8"))}
    years = {w["title"].strip().lower(): int(w["year"]) for w in works.values()}
    n = 0
    for cap in sorted(glob.glob(os.path.join(REPO, "posts", "**", "caption.txt"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(cap), REPO)
        lines = [l for l in open(cap, encoding="utf-8").read().strip().splitlines() if not l.startswith("#")]
        while lines and not lines[-1].strip():
            lines.pop()
        if not lines:
            continue
        year = years.get(lines[0].strip().lower())
        if year is None and len(lines) > 1 and lines[1][:4].isdigit():
            year = int(lines[1][:4])
        tags = BASE + [kind_tag(rel), place_tag(year)]
        open(cap, "w", encoding="utf-8").write("\n".join(lines) + "\n\n" + " ".join(tags) + "\n")
        n += 1
    print(n, "captions")


if __name__ == "__main__":
    main()
