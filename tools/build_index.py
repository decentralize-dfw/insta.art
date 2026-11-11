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
    ("takvim", "Takvim"),
    ("feed", "Feed"),
    ("kopstal", "Kopstal reels"),
    ("milan", "Milano reels"),
    ("single", "Tekli post"),
    ("details", "Detay carousel"),
    ("process-carousel", "Süreç carousel"),
    ("editorial", "Editoryel carousel'ler"),
    ("portfolio", "Portfolyo"),
    ("dated", "İlk hafta"),
]
NESTED = ("kopstal", "milan", "editorial", "single", "details", "process-carousel", "portfolio")

# Videos are served from the insta-art-archive repo (same paths under posts/),
# so this site stays under the 1 GB Pages limit. Full quality, nothing re-encoded.
# Empty string: videos are loaded from this site (local use).
MEDIA_BASE = os.environ.get("MEDIA_BASE", "https://raw.githubusercontent.com/decentralize-dfw/insta-art-archive/main/")


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
    if spec.get("hidden"):
        return None
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


CALENDAR = os.path.join(REPO, ".claude", "instagram", "calendar.json")


def calendar():
    """folder path -> calendar entry (date, day, time, note)."""
    try:
        posts = json.load(open(CALENDAR, encoding="utf-8"))["posts"]
    except (OSError, KeyError, ValueError):
        return {}
    return {p["folder"]: p for p in posts}


THUMBS = os.path.join(REPO, "thumbs")


def thumb(it):
    """Small preview for the grid and calendar cards (the full file opens on tap)."""
    if not it["cover"]:
        return ""
    from PIL import Image
    src = os.path.join(REPO, it["path"], it["cover"])
    name = it["id"] + ".jpg"
    dst = os.path.join(THUMBS, name)
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        os.makedirs(THUMBS, exist_ok=True)
        with Image.open(src) as im:
            im = im.convert("RGB")
            im.thumbnail((360, 640), Image.LANCZOS)
            im.save(dst, quality=82)
    return "thumbs/" + name


def collect():
    cal = calendar()
    out = []
    for name in sorted(os.listdir(POSTS)):
        top = os.path.join(POSTS, name)
        if not os.path.isdir(top):
            continue
        if name in NESTED:
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
    for it in out:
        c = cal.get(it["path"])
        it["date"] = c["date"] if c else ""
        it["when"] = f'{c["date"]} {c["day"]} {c.get("time", "")}'.strip() if c else ""
        it["note"] = c.get("note", "") if c else ""
        it["week"] = c.get("week", 0) if c else 0
        it["ckind"] = c.get("kind", "") if c else ""
        it["thumb"] = thumb(it)
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
.fbar { display:flex; gap:12px; align-items:center; margin:0 0 12px; font-size:13px; }
.fbar select { font:inherit; padding:6px 8px; border:1px solid var(--line); background:#fff; }
.fprof { display:flex; gap:12px; align-items:center; margin:0 0 12px; font-size:14px; }
.fav { width:56px; height:56px; border-radius:50%; background:#000 url(thumbs/avatar.jpg) center/cover; border:1px solid var(--line); }
.fcount { color:var(--muted); font-size:13px; }
.fgrid { display:grid; grid-template-columns:repeat(3, 1fr); gap:2px; max-width:620px; }
.ft { position:relative; aspect-ratio:3/4; overflow:hidden; background:var(--soft); cursor:pointer; }
.ft img { width:100%; height:100%; object-fit:cover; display:block; }
.ft .fi { position:absolute; top:6px; right:6px; filter:drop-shadow(0 0 2px rgba(0,0,0,.6)); }
.ft .fd { position:absolute; left:4px; top:4px; font-size:10px; background:rgba(255,255,255,.85); padding:0 3px; }
.now-line { font-size:12px; color:var(--muted); margin:0 0 10px; }
.cal { display:grid; grid-template-columns:46px repeat(7, minmax(0,1fr)); gap:3px; }
.cal .hd { font-size:11px; font-weight:600; text-align:center; padding:4px 0; }
.cal .wk { font-size:11px; font-weight:600; line-height:1.2; padding:4px 2px; border-top:1px solid var(--line); }
.cal .wk span { display:block; font-weight:400; color:var(--muted); font-size:10px; }
.cal .wk.cur { background:#000; color:#fff; }
.cal .wk.cur span { color:#ccc; }
.cell { border:1px solid var(--line); min-height:64px; padding:2px; font-size:10px; line-height:1.2; overflow:hidden; background:#fff; }
.cell.off { background:var(--soft); border-color:var(--soft); color:#bbb; }
.cell .n { display:flex; justify-content:space-between; gap:2px; }
.cell .im { aspect-ratio:4/5; background:var(--soft); margin:2px 0; overflow:hidden; }
.cell .im img { width:100%; height:100%; object-fit:cover; display:block; }
.cell .k { font-weight:600; word-break:break-word; hyphens:auto; }
.cell .st { margin-top:1px; white-space:nowrap; }
.cell.post { cursor:pointer; }
.cell.past { opacity:.45; }
.cell.today { border:2px solid #000; }
.cell.next { border:2px solid #000; }
.cell .st.b { background:#000; color:#fff; padding:0 2px; display:inline-block; }
@media (min-width:700px) { .cal { grid-template-columns:80px repeat(7, minmax(0,1fr)); gap:6px; } .cell { font-size:12px; padding:4px; } .cal .wk { font-size:13px; } .cal .wk span { font-size:11px; } }
.card .d { font-size:12px; font-weight:600; margin-top:6px; }
.card .d.past { color:var(--muted); font-weight:400; }
.card .d.now { background:#000; color:#fff; display:inline-block; padding:0 5px; }
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
let group = DATA.some(d => d.date) ? "takvim" : "all";
const $ = s => document.querySelector(s);
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const MEDIA = __MEDIA__;
const url = (it, f) => (MEDIA && f.endsWith(".mp4") ? MEDIA : "") + it.path + "/" + f;

function toast(m) { const t = $("#toast"); t.textContent = m; t.classList.add("on"); setTimeout(() => t.classList.remove("on"), 1600); }

const inGroup = (d, k) => k === "all" || (k === "takvim" || k === "feed" ? !!d.date : d.group === k);
const today = new Date().toISOString().slice(0, 10);
const MONTHS = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
const short = d => { const [y, m, g] = d.date.split("-"); return `${+g} ${MONTHS[+m - 1]} ${d.when.split(" ")[1] || ""}`; };

function tabs() {
  const all = [["all", "Hepsi"], ...GROUPS.filter(([k]) => DATA.some(d => inGroup(d, k)))];
  $("#tabs").innerHTML = all.map(([k, n]) =>
    `<button class="tab${k === group ? " on" : ""}" data-g="${k}">${esc(n)} <span style="opacity:.6">${k === "all" ? DATA.length : DATA.filter(d => inGroup(d, k)).length}</span></button>`).join("");
  $("#tabs").querySelectorAll(".tab").forEach(b => b.onclick = () => { group = b.dataset.g; tabs(); grid(); });
}

// Current Paris time from the internet; device clock as fallback.
let NOW = null, NOW_SRC = "cihaz";
function parisParts(d) {
  const f = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Paris", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false });
  const o = Object.fromEntries(f.formatToParts(d).map(p => [p.type, p.value]));
  return { date: `${o.year}-${o.month}-${o.day}`, hm: `${o.hour === "24" ? "00" : o.hour}:${o.minute}` };
}
function withTimeout(p, ms) { return Promise.race([p, new Promise((_, r) => setTimeout(() => r(new Error("timeout")), ms))]); }
async function netTime() {
  const tries = [
    fetch("https://worldtimeapi.org/api/timezone/Europe/Paris").then(r => r.json()).then(j => new Date(j.utc_datetime || j.datetime)),
    fetch("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FParis").then(r => r.json()).then(j => new Date(j.dateTime + "Z").getTime() ? j : Promise.reject())
      .then(j => ({ paris: true, date: j.dateTime.slice(0, 10), hm: j.dateTime.slice(11, 16) })),
  ];
  try {
    const v = await withTimeout(Promise.any(tries), 5000);
    NOW = v instanceof Date ? parisParts(v) : v; NOW_SRC = "internet";
  } catch { NOW = parisParts(new Date()); NOW_SRC = "cihaz"; }
}
const DAYN = ["Pzt", "Sal", "Çrş", "Per", "Cum", "Cmt", "Paz"];
const addDays = (iso, n) => { const d = new Date(iso + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
const dayDiff = (a, b) => Math.round((new Date(b + "T12:00:00Z") - new Date(a + "T12:00:00Z")) / 864e5);
const KIND = { "reel-detay": "Reel detay", "reel-süreç": "Reel süreç", "reel-kayıt": "Reel kayıt", "reel-model": "Reel 3D", "reel-portfolyo": "Reel portf.", "tek": "Tek resim", "carousel-detay": "Car. detay", "carousel-editorial": "Car. edit.", "carousel-süreç": "Car. süreç" };
function status(d) {
  const now = NOW || parisParts(new Date());
  const diff = dayDiff(now.date, d.date);
  const time = (d.when.split(" ")[2] || "19:00");
  if (diff < 0 || (diff === 0 && now.hm >= time)) return ["past", "geçti"];
  if (diff === 0) return ["today", "bugün " + time];
  if (diff === 1) return ["", "yarın"];
  return ["", diff + " gün"];
}
function calendar() {
  const posts = DATA.filter(d => d.date).sort((a, b) => a.date.localeCompare(b.date));
  const byDate = Object.fromEntries(posts.map(p => [p.date, p]));
  const first = posts[0].date, last = posts[posts.length - 1].date;
  const startDow = (new Date(first + "T12:00:00Z").getUTCDay() + 6) % 7;
  const monday = addDays(first, -startDow);
  const now = NOW || parisParts(new Date());
  const nextPost = posts.find(p => status(p)[0] !== "past");
  let html = `<div class="now-line">Şimdi: ${esc(now.date)} ${esc(now.hm)} Paris saati (${NOW_SRC === "internet" ? "internetten" : "cihaz saati"}) · paylaşımlar her gün 19:00${nextPost ? ` · <b>sıradaki: ${esc(short(nextPost))}, ${esc(nextPost.title)}</b>` : ""}</div><div class="cal"><div></div>${DAYN.map(n => `<div class="hd">${n}</div>`).join("")}`;
  for (let w = 0, m = monday; m <= last; w++, m = addDays(m, 7)) {
    const sun = addDays(m, 6), cur = now.date >= m && now.date <= sun;
    const [, mm, dd] = m.split("-"), [, sm, sd] = sun.split("-");
    html += `<div class="wk${cur ? " cur" : ""}" id="${cur ? "curweek" : ""}">Hafta ${w + 1}<span>${+dd} ${MONTHS[+mm - 1]}–${+sd} ${MONTHS[+sm - 1]}</span></div>`;
    for (let i = 0; i < 7; i++) {
      const day = addDays(m, i), p = byDate[day], dn = +day.slice(8);
      if (!p) { html += `<div class="cell off"><div class="n"><span>${dn}</span></div>${day === now.date ? "<div>bugün</div>" : ""}</div>`; continue; }
      let [cls, txt] = status(p);
      if (p === nextPost) cls += " next";
      html += `<div class="cell post ${cls}" data-id="${p.id}">
        <div class="n"><span>${dn}</span></div>
        <div class="im">${p.thumb ? `<img loading="lazy" src="${esc(p.thumb)}" alt="">` : ""}</div>
        <div class="k">${esc(KIND[p.ckind] || p.kind)}</div>
        <div class="st${p === nextPost ? " b" : ""}">${esc(txt)}</div></div>`;
    }
  }
  html += "</div>";
  $("#grid").className = "";
  $("#grid").innerHTML = html;
  $("#empty").hidden = true;
  $("#grid").querySelectorAll(".cell.post").forEach(c => c.onclick = () => open(DATA.find(d => d.id === c.dataset.id)));
  const cw = document.getElementById("curweek"); if (cw && !grid.scrolled) { grid.scrolled = true; cw.scrollIntoView({ block: "start" }); }
}

// Feed: the profile grid as it will look on a chosen day, newest first,
// 3 columns of 3:4 tiles like Instagram (covers already carry the white frame).
let feedUntil = null, feedDates = true;
const ICON_REEL = '<svg viewBox="0 0 24 24" width="18" height="18"><path fill="#fff" d="M8 5v14l11-7z"/></svg>';
const ICON_CAR = '<svg viewBox="0 0 24 24" width="18" height="18"><rect x="7" y="3" width="14" height="14" rx="2" fill="none" stroke="#fff" stroke-width="2"/><rect x="3" y="7" width="14" height="14" rx="2" fill="#fff"/></svg>';
function feed() {
  const posts = DATA.filter(d => d.date).sort((a, b) => b.date.localeCompare(a.date));
  const now = NOW || parisParts(new Date());
  const days = [...new Set(posts.map(p => p.date))].sort();
  const weeks = [...new Set(posts.map(p => p.week))].sort((a, b) => a - b);
  if (!feedUntil) feedUntil = "all";
  const opts = [["now", `Bugün (${now.date.slice(8)} ${MONTHS[+now.date.slice(5, 7) - 1]})`],
    ...weeks.map(w => { const last = posts.filter(p => p.week === w).map(p => p.date).sort().pop();
      return [last, `Hafta ${w} sonu (${+last.slice(8)} ${MONTHS[+last.slice(5, 7) - 1]})`]; }),
    ["all", "Hepsi (planın tamamı)"]];
  const lim = feedUntil === "all" ? "9999" : feedUntil === "now" ? now.date : feedUntil;
  const shown = posts.filter(p => p.date < lim || (p.date === lim && (feedUntil !== "now" || now.hm >= "19:00")));
  const tile = p => {
    const ic = p.ckind.startsWith("reel") ? ICON_REEL : p.ckind.startsWith("carousel") ? ICON_CAR : "";
    return `<div class="ft" data-id="${p.id}"><img loading="lazy" src="${esc(p.thumb)}" alt="">
      ${ic ? `<span class="fi">${ic}</span>` : ""}${feedDates ? `<span class="fd">${esc(short(p))}</span>` : ""}</div>`;
  };
  $("#grid").className = "";
  $("#grid").innerHTML = `
    <div class="fbar"><select id="fsel">${opts.map(([v, n]) => `<option value="${v}"${v === feedUntil ? " selected" : ""}>${esc(n)}</option>`).join("")}</select>
      <label><input type="checkbox" id="fdt"${feedDates ? " checked" : ""}> tarihler</label></div>
    <div class="fprof"><div class="fav"></div><div><b>yigitozen.art</b><div class="fcount">${shown.length} gönderi</div></div></div>
    <div class="fgrid">${shown.map(tile).join("")}</div>
    ${shown.length ? "" : '<div class="empty">Bu tarihe kadar post yok.</div>'}`;
  $("#empty").hidden = true;
  $("#fsel").onchange = e => { feedUntil = e.target.value; feed(); };
  $("#fdt").onchange = e => { feedDates = e.target.checked; feed(); };
  $("#grid").querySelectorAll(".ft").forEach(c => c.onclick = () => open(DATA.find(d => d.id === c.dataset.id)));
}

function grid() {
  $("#q").style.display = group === "takvim" || group === "feed" ? "none" : "";
  if (group === "takvim") return calendar();
  if (group === "feed") return feed();
  $("#grid").className = "grid";
  const q = $("#q").value.trim().toLowerCase();
  let items = DATA.filter(d => inGroup(d, group) &&
    (!q || (d.title + " " + d.kind + " " + d.path + " " + d.date).toLowerCase().includes(q)));
  if (group === "takvim") items = items.slice().sort((a, b) => a.date.localeCompare(b.date));
  $("#grid").innerHTML = items.map(d => `
    <div class="card" data-id="${d.id}">
      <div class="thumb">${d.thumb ? `<img loading="lazy" src="${esc(d.thumb)}" alt="">` : ""}</div>
      ${d.date ? `<div class="d${d.date < today ? " past" : d.date === today ? " now" : ""}">${esc(short(d))}</div>` : ""}
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
      const type = f.endsWith(".mp4") ? "video/mp4" : (b.type || "image/jpeg");
      const file = new File([b], f, { type });
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
    <video controls playsinline preload="none" poster="${it.cover ? esc(url(it, it.cover)) : ""}" data-file="${esc(f)}"></video>
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
    <div class="top"><div><h2>${esc(it.title)}</h2><div class="path">${it.when ? esc(it.when) + " · " : ""}${esc(it.kind)} · ${esc(it.path)}</div>
      ${it.note ? `<div class="path">${esc(it.note)}</div>` : ""}</div>
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
  // raw.githubusercontent serves videos as octet-stream, which iPhone will not
  // play directly: fetch the file and play it from memory as video/mp4.
  $("#view").querySelectorAll("video[data-file]").forEach(v =>
    prep(it, v.dataset.file).then(file => { if (v.isConnected) v.src = URL.createObjectURL(file); }));
  $("#dlg").showModal();
  history.replaceState(null, "", "#" + it.id);
}

$("#dlg").addEventListener("close", () => { $("#view").querySelectorAll("video").forEach(v => v.pause()); history.replaceState(null, "", location.pathname); });
$("#dlg").addEventListener("click", e => { if (e.target.id === "dlg") $("#dlg").close(); });
$("#q").oninput = grid;
tabs(); grid();
netTime().then(() => { if (group === "takvim") calendar(); if (group === "feed") feed(); });
setInterval(() => netTime().then(() => { if (group === "takvim") calendar(); }), 10 * 60 * 1000);
if (location.hash) { const it = DATA.find(d => d.id === location.hash.slice(1)); if (it) open(it); }
</script>
</body>
</html>
"""


def main():
    data = collect()
    page = PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False)) \
               .replace("__GROUPS__", json.dumps(GROUPS, ensure_ascii=False)) \
               .replace("__MEDIA__", json.dumps(MEDIA_BASE))
    open(os.path.join(REPO, "index.html"), "w", encoding="utf-8").write(page)
    print(f"index.html: {len(data)} items")


if __name__ == "__main__":
    main()
