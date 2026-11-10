#!/usr/bin/env python3
"""
build_index.py - write index.html at the repo root: a small finder for every
post folder under posts/ (reels, carousels, single posts), with full-quality
files, download and share buttons, and the caption / alt text / notes inline
with copy buttons.

Usage
  python3 tools/build_index.py

Run it again whenever posts change. The page uses relative links, so it works
on GitHub Pages (or any static host) straight from the repo.
"""

import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
POSTS = os.path.join(REPO, "posts")

GROUPS = [
    ("kopstal", "Kopstal reels"),
    ("milan", "Milano reels"),
    ("editorial", "Editoryel carousel'ler"),
    ("dated", "İlk hafta"),
]


def read(path):
    try:
        return open(path, encoding="utf-8").read().strip()
    except OSError:
        return ""


def item(folder, rel, group):
    files = sorted(os.listdir(folder))
    spec = {}
    if "spec.json" in files:
        spec = json.load(open(os.path.join(folder, "spec.json"), encoding="utf-8"))
    caption = read(os.path.join(folder, "caption.txt"))
    title = caption.splitlines()[0] if caption else os.path.basename(folder)
    slides = [f for f in files if re.fullmatch(r"\d+\.jpg", f)]
    videos = [f for f in files if f.endswith(".mp4")]
    if videos:
        kind = "süreç" if spec.get("camera") == "static" else "reel"
    elif slides:
        kind = "carousel" if len(slides) > 1 else "post"
    else:
        return None
    return {
        "id": rel.replace("/", "-"),
        "group": group,
        "path": rel,
        "title": title,
        "kind": kind,
        "videos": videos,
        "cover": "cover.jpg" if "cover.jpg" in files else (slides[0] if slides else ""),
        "slides": slides,
        "caption": caption,
        "alt": read(os.path.join(folder, "alt.txt")),
        "notes": read(os.path.join(folder, "notes.md")),
    }


def collect():
    out = []
    for name in sorted(os.listdir(POSTS)):
        top = os.path.join(POSTS, name)
        if not os.path.isdir(top):
            continue
        if name in ("kopstal", "milan", "editorial"):
            for sub in sorted(os.listdir(top)):
                p = os.path.join(top, sub)
                if os.path.isdir(p):
                    it = item(p, f"posts/{name}/{sub}", name)
                    if it:
                        out.append(it)
        else:
            it = item(top, f"posts/{name}", "dated")
            if it:
                out.append(it)
    return out


PAGE = r"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>yigitozen.art · posts</title>
<style>
:root { --fg:#000; --bg:#fff; --muted:#777; --line:#e5e5e5; --soft:#f5f5f5; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
  font:15px/1.45 -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }
header { position:sticky; top:0; z-index:5; background:var(--bg); border-bottom:1px solid var(--line);
  padding:12px 16px; }
h1 { font-size:15px; font-weight:600; margin:0 0 10px; letter-spacing:.02em; }
.bar { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.tab { border:1px solid var(--fg); background:var(--bg); color:var(--fg); padding:6px 10px;
  font:inherit; font-size:13px; cursor:pointer; }
.tab.on { background:var(--fg); color:var(--bg); }
input[type=search] { flex:1 1 160px; min-width:0; border:1px solid var(--line); padding:7px 10px; font:inherit; }
main { padding:16px; max-width:1200px; margin:0 auto; }
.grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(160px, 1fr)); gap:14px; }
.card { cursor:pointer; }
.card .thumb { aspect-ratio:4/5; background:var(--soft); overflow:hidden; }
.card img { width:100%; height:100%; object-fit:contain; display:block; }
.card .t { font-size:13px; margin-top:6px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.card .k { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
.empty { color:var(--muted); padding:40px 0; }
dialog { border:0; padding:0; width:100%; max-width:760px; max-height:100dvh; margin:auto; }
dialog::backdrop { background:rgba(0,0,0,.6); }
.view { padding:16px; }
.view .top { display:flex; justify-content:space-between; gap:10px; align-items:flex-start; }
.view h2 { font-size:16px; margin:0; }
.view .path { font-size:12px; color:var(--muted); word-break:break-all; }
.close { border:1px solid var(--fg); background:var(--bg); padding:4px 10px; font:inherit; cursor:pointer; }
video { width:100%; max-height:70dvh; background:#000; display:block; margin:12px 0 8px; }
.slides { display:grid; grid-template-columns:repeat(auto-fill, minmax(140px, 1fr)); gap:8px; margin:12px 0; }
.slide img { width:100%; aspect-ratio:4/5; object-fit:contain; background:var(--soft); display:block; }
.slide .n { font-size:12px; color:var(--muted); display:flex; justify-content:space-between; margin-top:3px; }
.btns { display:flex; gap:8px; flex-wrap:wrap; margin:8px 0; }
.btn { border:1px solid var(--fg); background:var(--bg); color:var(--fg); padding:7px 12px; font:inherit;
  font-size:13px; cursor:pointer; text-decoration:none; display:inline-block; }
.btn.dark { background:var(--fg); color:var(--bg); }
.btn:disabled { opacity:.45; }
.text { margin:14px 0; }
.text .h { display:flex; justify-content:space-between; align-items:center; font-size:12px;
  text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }
pre { white-space:pre-wrap; word-wrap:break-word; background:var(--soft); padding:10px; margin:6px 0 0;
  font:13px/1.5 ui-monospace, Menlo, Consolas, monospace; }
details summary { cursor:pointer; font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); }
.toast { position:fixed; left:50%; bottom:20px; transform:translateX(-50%); background:var(--fg); color:var(--bg);
  padding:8px 14px; font-size:13px; opacity:0; transition:opacity .2s; pointer-events:none; z-index:20; }
.toast.on { opacity:1; }
</style>
</head>
<body>
<header>
  <h1>yigitozen.art · posts</h1>
  <div class="bar" id="tabs"></div>
  <div class="bar" style="margin-top:8px"><input type="search" id="q" placeholder="ara: eser adı, tür"></div>
</header>
<main><div class="grid" id="grid"></div><div class="empty" id="empty" hidden>Sonuç yok.</div></main>
<dialog id="dlg"><div class="view" id="view"></div></dialog>
<div class="toast" id="toast"></div>
<script>
const DATA = __DATA__;
const GROUPS = __GROUPS__;
let group = "all";
const $ = s => document.querySelector(s);
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const url = (it, f) => it.path + "/" + f;

function toast(m) { const t = $("#toast"); t.textContent = m; t.classList.add("on"); setTimeout(() => t.classList.remove("on"), 1600); }

function tabs() {
  const all = [["all", "Hepsi"], ...GROUPS.filter(([k]) => DATA.some(d => d.group === k))];
  $("#tabs").innerHTML = all.map(([k, n]) =>
    `<button class="tab${k === group ? " on" : ""}" data-g="${k}">${esc(n)} <span style="opacity:.6">${k === "all" ? DATA.length : DATA.filter(d => d.group === k).length}</span></button>`).join("");
  $("#tabs").querySelectorAll(".tab").forEach(b => b.onclick = () => { group = b.dataset.g; tabs(); grid(); });
}

function grid() {
  const q = $("#q").value.trim().toLowerCase();
  const items = DATA.filter(d => (group === "all" || d.group === group) &&
    (!q || (d.title + " " + d.kind + " " + d.path).toLowerCase().includes(q)));
  $("#grid").innerHTML = items.map(d => `
    <div class="card" data-id="${d.id}">
      <div class="thumb">${d.cover ? `<img loading="lazy" src="${esc(url(d, d.cover))}" alt="">` : ""}</div>
      <div class="t">${esc(d.title)}</div>
      <div class="k">${esc(d.kind)}${d.slides.length > 1 ? " · " + d.slides.length : ""}</div>
    </div>`).join("");
  $("#empty").hidden = items.length > 0;
  $("#grid").querySelectorAll(".card").forEach(c => c.onclick = () => open(DATA.find(d => d.id === c.dataset.id)));
}

// iOS Safari only opens the share sheet straight from a tap, so files are
// fetched as soon as a post is opened and the tap shares what is ready.
const cache = {};
const canShareFiles = !!(navigator.canShare && navigator.share);
function prep(it, f) {
  const u = url(it, f);
  if (!cache[u]) {
    cache[u] = fetch(u).then(r => r.blob()).then(b => {
      const file = new File([b], f, { type: b.type || (f.endsWith(".mp4") ? "video/mp4" : "image/jpeg") });
      cache[u].file = file; return file;
    });
  }
  return cache[u];
}
function download(it, files) {
  files.forEach(f => { const a = document.createElement("a"); a.href = url(it, f); a.download = f; document.body.appendChild(a); a.click(); a.remove(); });
}
function share(it, files) {
  if (!canShareFiles) { download(it, files); return; }
  const ready = files.map(f => (cache[url(it, f)] || {}).file);
  if (ready.every(Boolean)) {
    if (!navigator.canShare({ files: ready })) { download(it, files); return; }
    navigator.share({ files: ready }).catch(e => { if (e.name !== "AbortError") download(it, files); });
    return;
  }
  files.forEach(f => prep(it, f));
  toast("Hazırlanıyor, birazdan tekrar dokun");
}
function armButtons(it) {
  if (!canShareFiles) return;
  $("#view").querySelectorAll("[data-share]").forEach(b => {
    const files = JSON.parse(b.dataset.share);
    if (b.tagName !== "BUTTON") { files.forEach(f => prep(it, f)); return; }
    const label = b.textContent;
    b.disabled = true; b.textContent = "Hazırlanıyor…";
    Promise.all(files.map(f => prep(it, f)))
      .then(() => { b.disabled = false; b.textContent = label; })
      .catch(() => { b.disabled = false; b.textContent = label; });
  });
}

function textBlock(label, text, id) {
  if (!text) return "";
  return `<div class="text"><div class="h"><span>${label}</span><button class="btn" data-copy="${id}">Kopyala</button></div><pre id="${id}">${esc(text)}</pre></div>`;
}

function open(it) {
  const v = it.videos.map(f => `
    <video controls playsinline preload="metadata" poster="${it.cover ? esc(url(it, it.cover)) : ""}" src="${esc(url(it, f))}"></video>
    <div class="btns">
      ${it.cover ? `<button class="btn dark" data-share='${esc(JSON.stringify([f, it.cover]))}'>Fotoğraflara kaydet (video + kapak)</button>` : ""}
      <button class="btn${it.cover ? "" : " dark"}" data-share='${esc(JSON.stringify([f]))}'>Fotoğraflara kaydet (video)</button>
      <a class="btn" href="${esc(url(it, f))}" download="${esc(f)}">İndir (${esc(f)})</a>
      ${it.cover ? `<a class="btn" href="${esc(url(it, it.cover))}" download="cover.jpg">Kapak</a>` : ""}
    </div>`).join("");
  const s = it.slides.length ? `
    ${it.slides.length > 1 ? `<div class="btns"><button class="btn dark" data-share='${esc(JSON.stringify(it.slides))}'>Fotoğraflara kaydet (${it.slides.length} sayfa)</button></div>` : `<div class="btns"><button class="btn dark" data-share='${esc(JSON.stringify(it.slides))}'>Fotoğraflara kaydet</button></div>`}
    <div class="slides">${it.slides.map((f, i) => `
      <div class="slide"><a href="${esc(url(it, f))}" target="_blank" rel="noopener"><img loading="lazy" src="${esc(url(it, f))}" alt=""></a>
        <div class="n"><span>${i + 1}</span><span><a href="${esc(url(it, f))}" download="${esc(f)}">indir</a> · <a href="#" data-share='${esc(JSON.stringify([f]))}'>paylaş</a></span></div>
      </div>`).join("")}</div>` : "";
  $("#view").innerHTML = `
    <div class="top"><div><h2>${esc(it.title)}</h2><div class="path">${esc(it.kind)} · ${esc(it.path)}</div></div>
      <button class="close" id="x">Kapat</button></div>
    ${v}${s}
    ${textBlock("Caption", it.caption, "t-cap")}
    ${textBlock("Alt text", it.alt, "t-alt")}
    ${it.notes ? `<details class="text"><summary>Notlar</summary><pre>${esc(it.notes)}</pre></details>` : ""}`;
  $("#x").onclick = () => $("#dlg").close();
  $("#view").querySelectorAll("[data-copy]").forEach(b => b.onclick = async () => {
    const t = document.getElementById(b.dataset.copy).textContent;
    try { await navigator.clipboard.writeText(t); toast("Kopyalandı"); }
    catch { const r = document.createRange(); r.selectNodeContents(document.getElementById(b.dataset.copy));
      const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); toast("Seçildi, kopyala"); }
  });
  $("#view").querySelectorAll("[data-share]").forEach(b => b.onclick = e => { e.preventDefault(); share(it, JSON.parse(b.dataset.share)); });
  armButtons(it);
  $("#dlg").showModal();
  history.replaceState(null, "", "#" + it.id);
}

$("#dlg").addEventListener("close", () => { $("#view").querySelectorAll("video").forEach(v => v.pause()); history.replaceState(null, "", location.pathname); });
$("#dlg").addEventListener("click", e => { if (e.target.id === "dlg") $("#dlg").close(); });
$("#q").oninput = grid;
tabs(); grid();
if (location.hash) { const it = DATA.find(d => d.id === location.hash.slice(1)); if (it) open(it); }
</script>
</body>
</html>
"""


def main():
    data = collect()
    page = PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False)) \
               .replace("__GROUPS__", json.dumps(GROUPS, ensure_ascii=False))
    open(os.path.join(REPO, "index.html"), "w", encoding="utf-8").write(page)
    print(f"index.html: {len(data)} items")


if __name__ == "__main__":
    main()
