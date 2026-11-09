"""Build the local, dependency-free cover and profile-grid review book.

The renderer owns image exports and covers.json. This file only builds HTML;
it never alters the plan, covers, archive, or Instagram account.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN_DIR = HERE.parent / "publication-plan-180-posts"
OUTPUT = HERE / "GRID-VE-KAPAKLAR.html"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def e(value) -> str:
    return html.escape(str(value), quote=True)


CSS = r"""
@font-face{font-family:'Hanken Grotesk';font-style:normal;font-weight:100 900;font-display:swap;src:url('fonts/hanken-normal-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'Hanken Grotesk';font-style:normal;font-weight:100 900;font-display:swap;src:url('fonts/hanken-normal-latin.woff2') format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
:root{--paper:#fff;--card:#fff;--ink:#000;--muted:#000;--line:#000;--olive:#000;--soft:#fff;--white:#fff;--radius:0}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:22px}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 'Hanken Grotesk',Arial,sans-serif}a{color:var(--olive);text-decoration-thickness:1px;text-underline-offset:3px}button,input,select{font:inherit;color:inherit}button,a,input,select,summary{touch-action:manipulation}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #000;outline-offset:4px}main{max-width:1540px;margin:auto;padding:44px 36px 96px}header.masthead{max-width:1110px;margin-bottom:38px}.eyebrow,.overline{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 13px}h1{font:500 clamp(28px,3.6vw,48px)/1.16 'Hanken Grotesk',Arial,sans-serif;letter-spacing:normal;margin:20px 0 24px;max-width:1100px}h2{font:500 clamp(24px,2.6vw,34px)/1.2 'Hanken Grotesk',Arial,sans-serif;letter-spacing:normal;margin:0 0 20px}h3{font-weight:500;line-height:1.3;margin:0 0 12px}p{margin:0 0 16px}.lead{font-size:20px;line-height:1.6;max-width:960px}.muted,small{color:var(--muted)}.textlimit{max-width:910px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:25px 0 0}nav a,.button,.steps button,.mode button,.controlbutton{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:8px 14px;border:1px solid var(--line);border-radius:0;background:var(--card);text-decoration:none;color:var(--ink);font-size:14px;line-height:1.3}nav a:hover,.button:hover,.steps button:hover,.controlbutton:hover{background:#fff}.stats{display:flex;flex-wrap:wrap;gap:28px;padding:25px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:30px 0}.stat{min-width:120px}.stat strong{display:block;font:36px/1.15 'Hanken Grotesk',Arial,sans-serif}.stat span{font-size:13px;color:var(--muted)}section{margin:48px 0}.sectionintro{display:flex;align-items:flex-start;justify-content:space-between;gap:24px;margin-bottom:24px}.sectionintro p{max-width:680px}.tag{display:inline-block;padding:4px 8px;border:1px solid var(--line);border-radius:0;font-size:11px;line-height:1.4;color:var(--muted)}.note{background:var(--soft);border-left:3px solid #000;padding:17px 21px;max-width:1040px;font-size:14px}.note p:last-child{margin:0}.simulator{display:grid;grid-template-columns:minmax(320px,.95fr) minmax(380px,1.15fr);gap:44px;padding:30px;border:1px solid var(--line);background:var(--card)}.controls{min-width:0}.mode{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0 23px}.mode button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}.mode button{font-size:13px}.sliderlabel{display:flex;align-items:baseline;justify-content:space-between;gap:15px;margin:22px 0 8px}.sliderlabel strong{font:30px/1 'Hanken Grotesk',Arial,sans-serif}.range{width:100%;accent-color:var(--olive);margin:12px 0}.stepcontrols{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:8px 0 19px}.stepcontrols input{width:83px;min-height:42px;border:1px solid var(--line);background:#fff;padding:5px 9px}.stepcontrols label{font-size:13px}.steps{display:flex;gap:7px;flex-wrap:wrap}.steps button{font-size:12px;min-height:36px;padding:7px 9px}.steps button[aria-current=true]{background:#fff;border-color:#000}.context{font-size:14px;margin:24px 0 18px;padding-top:17px;border-top:1px solid var(--line)}.context p{margin-bottom:9px}.currentpost{padding:16px;background:var(--paper);border:1px solid var(--line);font-size:14px}.currentpost strong{display:block;font-size:16px;line-height:1.4;margin:6px 0 8px}.profile{max-width:540px;width:100%;margin:auto}.profilehead{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 0 14px;font-size:14px}.profilehead strong{font-weight:500;font-size:17px}.profilegrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3px;background:var(--card)}.tile{position:relative;display:block;aspect-ratio:3/4;border:0;padding:0;background:var(--soft);text-decoration:none;overflow:hidden}.tile img{display:block;width:100%;height:100%;object-fit:cover}.tile .hoverid{position:absolute;left:5px;bottom:5px;background:#fff;color:var(--ink);padding:2px 5px;font-size:11px;line-height:1.3;opacity:0;transition:opacity .15s}.tile:hover .hoverid,.tile:focus-visible .hoverid{opacity:1}.tile .pin{position:absolute;right:7px;top:7px;width:17px;height:17px;filter:none;color:white}.tile.unknown{display:flex;align-items:center;justify-content:center;padding:14px;font-size:11px;color:#000;text-align:center;background:repeating-linear-gradient(135deg,#fff,#fff 1px,#fff 1px,#fff 14px)}.profilecaption{margin-top:13px;font-size:12px;line-height:1.6}.roworder{font-family:'Hanken Grotesk',Arial,sans-serif;font-size:11px;overflow-wrap:anywhere}.gridlinks{display:flex;gap:15px;flex-wrap:wrap;margin:14px 0;font-size:13px}.opening{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:13px;margin:22px 0}.opening a{display:block;text-decoration:none;color:var(--ink)}.opening img{display:block;width:100%;aspect-ratio:3/4;object-fit:cover;border:1px solid var(--line);background:var(--card)}.opening .opmeta{font-size:11px;line-height:1.5;margin-top:9px;color:var(--muted)}.opening strong{display:block;font-size:13px;line-height:1.4;margin:3px 0}.systemgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.systemitem{padding:23px;border-top:2px solid #000;background:var(--card)}.systemitem p{font-size:14px;margin-bottom:0}.systemitem h3{font-size:17px}.filterbar{display:grid;grid-template-columns:minmax(230px,1fr) 185px 155px auto;gap:10px;background:var(--soft);padding:18px;margin:24px 0 13px;border:1px solid var(--line)}.filterbar label{font-size:11px;color:var(--muted);display:block}.filterbar input,.filterbar select{width:100%;height:42px;padding:9px 10px;background:#fff;border:1px solid #000;border-radius:0;margin-top:4px}.filterbar button{align-self:end;height:42px}.resultcount{font-size:13px;color:var(--muted);margin:0 0 24px}.covercatalogue{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:25px}.covercard{min-width:0;border:1px solid var(--line);background:var(--card);scroll-margin-top:26px}.covercard.hidden{display:none}.covervisual{height:400px;background:#fff;display:flex;align-items:center;justify-content:center;padding:18px;border-bottom:1px solid var(--line)}.covervisual a{display:flex;align-items:center;justify-content:center;width:100%;height:100%}.covervisual img{max-width:100%;max-height:100%;width:auto;height:auto;display:block;box-shadow:none}.cardbody{padding:23px}.cardmeta{display:flex;justify-content:space-between;gap:12px;color:var(--muted);font-size:11px;margin:0 0 11px;line-height:1.5}.covercard h3{font-size:20px;line-height:1.35;margin-bottom:15px}.covercard .headline{font-size:14px;color:#000;border-left:2px solid #000;padding-left:10px;margin-bottom:17px}.covercard .rationale{font-size:14px;line-height:1.6}.covercard dl{font-size:13px;line-height:1.6;margin:16px 0}.covercard dt{font-weight:500;margin-top:11px}.covercard dd{margin:3px 0 0;color:var(--muted)}.cardlinks{display:flex;flex-wrap:wrap;gap:8px 14px;font-size:12px;border-top:1px solid var(--line);padding-top:15px}.cardlinks button{padding:0;background:none;border:0;text-decoration:underline;text-underline-offset:3px;color:var(--olive);font-size:12px}.covercard details{margin-top:18px;padding-top:16px;border-top:1px solid var(--line);font-size:13px}.covercard summary{cursor:pointer;font-weight:500;line-height:1.45}.covercard details[open] summary{margin-bottom:17px}.covercard details p{margin-bottom:12px}.cropcompare{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:15px 0 18px;align-items:start}.cropcompare figure{margin:0}.cropcompare img{display:block;width:100%;height:auto;background:var(--paper);border:1px solid var(--line)}.cropcompare figcaption{font-size:11px;line-height:1.4;margin-top:7px;color:var(--muted)}pre.caption{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.6 'Hanken Grotesk',Arial,sans-serif;background:var(--paper);padding:16px;border:1px solid var(--line);margin:12px 0 0}.evidence{background:var(--card);border:1px solid var(--line);padding:30px}.evidencegrid{display:grid;grid-template-columns:1fr 1fr;gap:35px}.evidence h3{font-size:18px}.evidence p,.evidence li{font-size:14px}.evidence ul{padding-left:19px;margin:0 0 17px}.evidence li{margin-bottom:8px}.filelinks{display:flex;flex-wrap:wrap;gap:10px 20px;font-size:13px}.foot{border-top:1px solid var(--line);padding-top:23px;font-size:12px;color:var(--muted);margin-top:42px}.noprint{}@media(min-width:1450px){.covervisual{height:440px}}@media(max-width:1050px){.simulator{gap:25px;padding:22px;grid-template-columns:minmax(300px,1fr) minmax(300px,1fr)}.covercatalogue{grid-template-columns:repeat(2,minmax(0,1fr))}.opening{grid-template-columns:repeat(3,minmax(0,1fr))}.filterbar{grid-template-columns:1fr 160px 130px}.filterbar button{grid-column:1/-1}.evidencegrid{gap:22px}}@media(max-width:750px){main{padding:28px 18px 65px}.lead{font-size:18px}.sectionintro{display:block}.simulator{grid-template-columns:1fr;padding:18px}.controls{order:0}.profile{max-width:510px;order:1}.systemgrid{grid-template-columns:1fr}.systemitem{padding:20px}.filterbar{grid-template-columns:1fr 1fr;padding:13px}.filterbar .searchlabel{grid-column:1/-1}.filterbar button{grid-column:auto}.covercatalogue{gap:16px}.cardbody{padding:17px}.covervisual{height:290px;padding:12px}.covercard h3{font-size:18px}.covercard .rationale{font-size:13px}.cardmeta{display:block}.cardmeta span{display:block}.covercard dl{font-size:12px}.evidencegrid{grid-template-columns:1fr}.evidence{padding:23px}.stats{gap:22px}.stat strong{font-size:31px}.opening{gap:10px}.opening strong{font-size:12px}}@media(max-width:480px){.covercatalogue{grid-template-columns:1fr}.covervisual{height:430px}.cardbody{padding:22px}.cardmeta{display:flex}.cardmeta span{display:inline}.covercard h3{font-size:22px}.covercard .rationale,.covercard dl{font-size:14px}.profilegrid{gap:2px}.tile.unknown{font-size:9px;padding:7px}.opening{grid-template-columns:repeat(3,minmax(0,1fr))}.opening .opmeta{font-size:10px}.filterbar{grid-template-columns:1fr 1fr}.sliderlabel strong{font-size:27px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}@media print{main{max-width:none;padding:0}nav,.filterbar,.steps,.stepcontrols,.range,.mode,.cardlinks,.gridlinks{display:none}.simulator{display:block}.profile{max-width:450px}.covercatalogue{grid-template-columns:repeat(2,minmax(0,1fr))}.covercard{break-inside:avoid}.covervisual{height:300px}.opening{grid-template-columns:repeat(6,minmax(0,1fr))}.covercard details:not([open]){display:none}section{margin:25px 0}.evidence{break-inside:avoid}.note{background:white}}
strong,b{font-weight:500}.steps button[aria-current=true]{border-width:2px}.tile.unknown{background:#fff;border:1px dashed #000}.covervisual img{box-shadow:none}.profilegrid{background:#fff}

"""


CSS += "\n.cropcompare .adapted{grid-column:1/-1;padding-top:12px;border-top:1px solid var(--line)}.cropcompare .adapted img{max-width:240px;margin:auto}.cropcompare .adapted figcaption{text-align:center}.cropcompare .adapted a{display:block}.cropcompare .adapted .adapt-download{display:inline;font-size:12px}\n"


JS = r"""
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('viewer-data').textContent);
  const posts = new Map(data.posts.map(p => [p.n, p]));
  const baseline = data.baseline;
  const grid = document.getElementById('profile-grid');
  const range = document.getElementById('state-range');
  const number = document.getElementById('state-number');
  const modeButtons = [...document.querySelectorAll('[data-mode]')];
  const steps = [...document.querySelectorAll('[data-step]')];
  let state = 6;
  let mode = 'chronological';
  const pad = n => String(n).padStart(3, '0');
  const pid = n => 'P' + pad(n);
  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  function pinsFor(n) {
    return (n < 30 ? [1, 3, 5] : [1, 5, 30]).filter(x => x <= n);
  }
  function pinMark() {
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('class', 'pin');
    svg.setAttribute('aria-hidden', 'true');
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', 'M8 2h8l-1 7 4 4v2h-6v7l-1-1-1 1v-7H5v-2l4-4z');
    path.setAttribute('fill', 'currentColor');
    svg.appendChild(path);
    return svg;
  }
  function tileFor(item, pinned) {
    if (typeof item === 'number') {
      const post = posts.get(item);
      const a = el('a', 'tile');
      a.href = '#' + pid(item);
      a.title = `${pid(item)} · Gün ${post.day} · ${post.format} · ${post.title_en}`;
      a.setAttribute('aria-label', a.title + (pinned ? ' · Planlanan sabit' : ''));
      const img = el('img');
      img.src = `tiles/${pid(item)}.png`;
      img.alt = post.headline_en || post.title_en;
      img.width = 270; img.height = 360;
      a.appendChild(img);
      a.appendChild(el('span', 'hoverid', pid(item)));
      if (pinned) a.appendChild(pinMark());
      a.addEventListener('click', () => revealCard(item));
      return a;
    }
    if (item && item.id) {
      const a = el('a', 'tile baseline');
      a.href = item.url;
      a.target = '_blank';
      a.rel = 'noopener';
      a.title = `${item.id} · Önceden gözlemlenen gönderi · ${item.description}`;
      const img = el('img');
      img.src = item.path;
      img.alt = `Gözlemlenen mevcut profil görseli ${item.id}`;
      a.appendChild(img);
      a.appendChild(el('span', 'hoverid', item.id + ' · Mevcut'));
      return a;
    }
    const empty = el('div', 'tile unknown', 'Önceki gönderiler doğrulanmadı');
    empty.setAttribute('aria-label', 'Arşiv derinliği bilinmiyor; bu kutu bir gönderi değildir.');
    return empty;
  }
  function update(next) {
    state = Math.max(0, Math.min(180, Math.round(Number(next) || 0)));
    const desiredPins = mode === 'pinned' ? pinsFor(state) : [];
    const chron = Array.from({length: state}, (_, i) => state - i)
      .filter(n => !desiredPins.includes(n));
    const items = [...desiredPins, ...chron, ...baseline].slice(0, 12);
    while (items.length < 12) items.push(null);
    grid.replaceChildren(...items.map(item => tileFor(item, desiredPins.includes(item))));
    range.value = String(state);
    number.value = String(state);
    document.getElementById('state-value').textContent = state === 0 ? 'Başlangıç' : pid(state) + ' sonrası';
    document.getElementById('state-day').textContent = state === 0
      ? 'Henüz yeni yayın yok'
      : `Gün ${posts.get(state).day} · ${state} yeni yayın`;
    document.getElementById('state-caption').textContent = mode === 'chronological'
      ? 'Yeni sabit eklenmediği varsayılan sıra. Yeni yayınlar en başa gelir.'
      : 'Planlanan sabitler soldan sağa gösterilir. Gerçek hesapta henüz uygulanmadı; mevcut sabitler teyit bekliyor.';
    document.getElementById('pins-label').textContent = desiredPins.length
      ? 'Planlanan sabitler: ' + desiredPins.map(pid).join(' · ')
      : 'Bu görünümde yeni sabit yok.';
    document.getElementById('row-order').textContent = items.map(item =>
      typeof item === 'number' ? pid(item) : item?.id || '?').join(' / ');
    document.getElementById('profile-state').textContent = state === 0 ? 'Başlangıç' : `+${state} yayın`;
    const current = document.getElementById('current-post');
    current.replaceChildren();
    if (state) {
      const p = posts.get(state);
      current.appendChild(el('span', 'muted', `${pid(state)} · Gün ${p.day} · ${p.time} ${p.timezone} · ${p.format}`));
      const title = el('strong', '', p.title_en);
      title.lang = 'en'; current.appendChild(title);
      current.appendChild(el('p', '', p.why_visual_tr));
      const link = el('a', '', 'Kapağın gerekçesine ve dosyalarına git');
      link.href = '#' + pid(state);
      link.addEventListener('click', () => revealCard(state));
      current.appendChild(link);
    } else {
      current.appendChild(el('strong', '', 'Yeni seri başlamadan önce'));
      current.appendChild(el('p', '', '4 Kasım 2026 tarihinde oturumsuz web görünümünde üç görsel gözlemlendi. Bu, hesabın bütün gönderilerinin veya mevcut sabitlerinin doğrulandığı anlamına gelmiyor.'));
    }
    const gridFile = `grids/${mode}/S${pad(state)}.jpg`;
    const gridLink = document.getElementById('grid-file');
    gridLink.href = gridFile;
    gridLink.textContent = 'Bu grid durumunu büyük aç';
    const gridOther = document.getElementById('grid-other');
    gridOther.href = `grids/${mode === 'pinned' ? 'chronological' : 'pinned'}/S${pad(state)}.jpg`;
    gridOther.textContent = mode === 'pinned' ? 'Aynı anı sabitsiz karşılaştır' : 'Aynı anı planlanan sabitlerle karşılaştır';
    modeButtons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
    steps.forEach(b => b.setAttribute('aria-current', String(Number(b.dataset.step) === state)));
    document.getElementById('state-announcement').textContent = `Gönderi ${state} sonrası, ${mode === 'pinned' ? 'planlanan sabitlerle' : 'kronolojik'} grid gösteriliyor.`;
  }
  range.addEventListener('input', event => update(event.target.value));
  number.addEventListener('change', event => update(event.target.value));
  document.getElementById('previous').addEventListener('click', () => update(state - 1));
  document.getElementById('next').addEventListener('click', () => update(state + 1));
  modeButtons.forEach(b => b.addEventListener('click', () => { mode = b.dataset.mode; update(state); }));
  steps.forEach(b => b.addEventListener('click', () => update(b.dataset.step)));
  const search = document.getElementById('search');
  const phase = document.getElementById('phase');
  const format = document.getElementById('format');
  const cards = [...document.querySelectorAll('.covercard')];
  const normalized = value => String(value).toLocaleLowerCase('tr-TR').normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  function applyFilters() {
    const query = normalized(search.value.trim());
    let shown = 0;
    for (const card of cards) {
      const match = (!phase.value || card.dataset.phase === phase.value)
        && (!format.value || card.dataset.format === format.value)
        && (!query || normalized(card.dataset.search).includes(query));
      card.classList.toggle('hidden', !match);
      if (match) shown++;
    }
    document.getElementById('result-count').textContent = `${shown} / 180 kapak gösteriliyor`;
    document.getElementById('no-results').hidden = shown !== 0;
  }
  function resetFilters() { search.value = ''; phase.value = ''; format.value = ''; applyFilters(); }
  function revealCard(n) {
    const card = document.getElementById(pid(n));
    if (card && card.classList.contains('hidden')) resetFilters();
  }
  search.addEventListener('input', applyFilters);
  phase.addEventListener('change', applyFilters);
  format.addEventListener('change', applyFilters);
  document.getElementById('clear-filters').addEventListener('click', resetFilters);
  document.querySelectorAll('[data-show-state]').forEach(b => b.addEventListener('click', () => {
    update(b.dataset.showState);
    document.getElementById('grid').scrollIntoView({behavior: 'smooth', block: 'start'});
  }));
  document.querySelectorAll('.opening a').forEach(a => a.addEventListener('click', () => revealCard(Number(a.dataset.post))));
  window.addEventListener('hashchange', () => {
    const match = location.hash.match(/^#P(\d{3})$/);
    if (match) revealCard(Number(match[1]));
  });
  const stateFromHash = location.hash.match(/^#state-(\d{1,3})$/);
  const cardFromHash = location.hash.match(/^#P(\d{3})$/);
  update(stateFromHash ? Number(stateFromHash[1]) : 6);
  if (cardFromHash) revealCard(Number(cardFromHash[1]));
  applyFilters();
})();
"""


def cover_card(cover: dict, post: dict) -> str:
    n = int(cover["n"])
    pid = f"P{n:03}"
    render = cover.get("render") or {}
    headline = cover.get("headline_en") or ""
    width = render.get("width", 1080)
    height = render.get("height", 1920 if post["format"] == "Reel" else 1350)
    source_ids = " · ".join(cover.get("hero_ids", []))
    public_text = post.get("caption_with_credit_en", post.get("caption_en", ""))
    search_text = " ".join([
        pid, str(n), post.get("title_en", ""), headline,
        " ".join(post.get("works", [])), source_ids,
        cover.get("why_visual_tr", ""), cover.get("grid_role_tr", ""),
    ])
    crop_status = render.get("grid_crop_ok")
    crop_line = (
        "Yerel 3:4 kırpma geometrisi kontrolü: geçti."
        if crop_status is True else
        "Yerel 3:4 kırpma geometrisi: kontrol kaydına bakın."
    )
    square_line = (
        "Kare merkez kırpma bu kapağın görsel bilgisini kesiyor. Kare yüzey seçilirse aşağıdaki ayrı uyarlamayı kullanın."
        if render.get("square_stress_crop_ok") is False else
        "Kare yüzey için ayrı, kaynak oranını koruyan uyarlama hazırlandı; ana 3:4 profil dosyası değişmedi."
    )
    return f'''<article class="covercard" id="{pid}" data-phase="{e(post.get('phase', (n-1)//30+1))}" data-format="{e(post['format'])}" data-search="{e(search_text)}">
  <div class="covervisual"><a href="exports/{pid}.webp" target="_blank" rel="noopener"><img src="exports/{pid}.webp" alt="{e(headline or post['title_en'])}" loading="lazy" width="{e(width)}" height="{e(height)}"></a></div>
  <div class="cardbody">
    <div class="cardmeta"><span>{pid} · GÜN {e(post['day'])} · {e(post['format'])}</span><span>BLOK {e(post.get('phase', (n-1)//30+1))} · {e(post.get('goal', ''))}</span></div>
    <h3 lang="en">{e(post['title_en'])}</h3>
    <p class="headline">{('<span lang="en">' + e(headline) + '</span>') if headline else 'Kapak başlığı yok; görsel tek başına çalışır.'}</p>
    <p class="rationale">{e(cover.get('why_visual_tr', ''))}</p>
    <dl><dt>Griddeki görevi</dt><dd>{e(cover.get('grid_role_tr', ''))}</dd>
    <dt>Korunan görsel bilgi</dt><dd>{e(cover.get('must_preserve_tr', ''))}</dd>
    <dt>Kaynak ve dosya</dt><dd>{e(source_ids)} · {e(width)} × {e(height)} px · {e(cover.get('layout', ''))}</dd></dl>
    <div class="cardlinks"><a href="exports/{pid}.webp" target="_blank" rel="noopener">PNG</a><a href="exports/{pid}.svg" target="_blank" rel="noopener">Vektör yerleşim SVG</a><a href="tiles/{pid}.webp" target="_blank" rel="noopener">Grid kutusu</a><button type="button" data-show-state="{n}">Bu yayın sonrası grid</button><a href="../publication-plan-180-posts/VIZYON-VE-180-POST.html#{pid}">Plan kartı</a></div>
    <details><summary>Kırpma, ilk kare ve kontrol notları</summary>
      <div class="cropcompare"><figure><a href="tiles/{pid}.webp" target="_blank" rel="noopener"><img src="tiles/{pid}.webp" alt="{pid} 3:4 profil kutusu simülasyonu" loading="lazy" width="270" height="360"></a><figcaption>3:4 profil kutusu · hesap web görünümünden ölçülen oran</figcaption></figure><figure><a href="crops/{pid}-square.webp" target="_blank" rel="noopener"><img src="crops/{pid}-square.webp" alt="{pid} kare merkez kırpma stres denemesi" loading="lazy" width="270" height="270"></a><figcaption>1:1 merkez kırpma · stres denemesi; mevcut grid iddiası değil</figcaption></figure><figure class="adapted"><a href="crops/{pid}-square-adapted.webp" target="_blank" rel="noopener"><img src="crops/{pid}-square-adapted.webp" alt="{pid} kare yüzey için kaynak oranı korunan ayrı uyarlama" loading="lazy" width="1080" height="1080"></a><figcaption>Kare yüzey seçilirse hazırlanmış uyarlama · 1080 × 1080 px<br><a class="adapt-download" href="crops/{pid}-square-adapted.webp" download="{pid}-square-adapted.webp">Kare uyarlama PNG dosyasını indir</a></figcaption></figure></div>
      <p>{e(crop_line)}</p><p>{e(square_line)}</p><p><b>İlk kare / ilk sayfa:</b> {e(cover.get('first_frame_tr', ''))}</p>
      <p><b>Bakılacak nokta:</b> {e(cover.get('render_risk_tr', ''))}</p>
      <p class="muted">Yerel tasarım üretildi. Gerçek yükleme yolundaki mobil önizleme, cover seçimi ve kırpma konumu henüz onaylanmış değil.</p>
    </details>
    <details><summary>İngilizce caption ve künye</summary><pre class="caption" lang="en">{e(public_text)}</pre></details>
  </div>
</article>'''


def build() -> Path:
    plan = load(PLAN_DIR / "PLAN-180-POST.json")
    brief = load(HERE / "design-brief.json")
    cover_data = load(HERE / "covers.json")
    covers = cover_data["covers"] if isinstance(cover_data, dict) else cover_data
    posts = {int(p["n"]): p for p in plan["posts"]}
    cover_map = {int(c["n"]): c for c in covers}
    if len(covers) != 180 or sorted(cover_map) != list(range(1, 181)):
        raise ValueError("covers.json must contain exactly one decision for every post 1–180")
    if sorted(posts) != list(range(1, 181)):
        raise ValueError("The source plan must contain posts 1–180")
    missing = [str(HERE / "exports" / f"P{n:03}.webp") for n in range(1, 181)
               if not (HERE / "exports" / f"P{n:03}.webp").is_file()]
    if missing:
        raise FileNotFoundError(f"Render all covers before building the viewer: {len(missing)} PNG exports missing; first: {missing[0]}")
    catalogue = "\n".join(cover_card(cover_map[n], posts[n]) for n in range(1, 181))
    opening = "\n".join(
        f'<a href="#P{n:03}" data-post="{n}"><img src="tiles/P{n:03}.webp" alt="{e(cover_map[n].get("headline_en") or posts[n]["title_en"])}" width="270" height="360"><div class="opmeta">Gün {posts[n]["day"]} · P{n:03} · {e(posts[n]["format"])}</div><strong lang="en">{e(cover_map[n].get("headline_en") or posts[n]["title_en"])}</strong></a>'
        for n in range(1, 7)
    )
    steps = ''.join(f'<button type="button" data-step="{n}">{"Başlangıç" if n == 0 else f"P{n:03}"}</button>'
                    for n in [0, 1, 2, 3, 4, 5, 6, 30, 60, 90, 120, 150, 180])
    compact_posts = []
    for n in range(1, 181):
        p, c = posts[n], cover_map[n]
        compact_posts.append({key: p.get(key) for key in ["n", "day", "time", "timezone", "format", "title_en"]}
                             | {key: c.get(key, "") for key in ["headline_en", "why_visual_tr"]})
    viewer_data = json.dumps({"posts": compact_posts, "baseline": brief["baseline"]["items"]}, ensure_ascii=False).replace("</", "<\\/")
    document = f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>180 kapak · Grid tasarım kitabı — Yiğit Özen</title><style>{CSS}</style></head>
<body><main id="top">
<header class="masthead"><p class="eyebrow">YIĞIT ÖZEN · 180 AYRI YAYIN · YEREL TASARIM TASLAĞI</p><h1>Her kapak kendi başına.<br>Grid, birlikte görülen eserler.</h1>
<p class="lead">180 gönderinin kapakları ve her yeni yayınla değişen profil görünümü. Kapak, gönderinin somut sorusunu açar; eser seçimini ve anlatı sırasını destekler.</p>
<nav><a href="#grid">Gridi adım adım incele</a><a href="#first14">İlk 14 gün</a><a href="#covers">180 kapağın tamamı</a><a href="#evidence">Kontrol sınırları</a><a href="../publication-plan-180-posts/VIZYON-VE-180-POST.html">Vizyon ve yayın planı ↗</a></nav>
</header>
<p class="note">Görsel referans: <a href="https://yigitozen.art/paintings/">yigitozen.art</a> üzerindeki Hanken Grotesk tipografisi. Zemin beyaz, yazı siyah; ek vurgu rengi kullanılmıyor. Bu inceleme sayfasının yerleşimi web sitesinin birebir kopyası değildir.</p>
<div class="stats"><div class="stat"><strong>180</strong><span>tek tek kapak kararı</span></div><div class="stat"><strong>3:4</strong><span>gözlemlenen web grid oranı</span></div><div class="stat"><strong>2</strong><span>sıra senaryosu</span></div><div class="stat"><strong>6</strong><span>ilk 14 gündeki yayın</span></div><div class="stat"><strong>0</strong><span>bu çalışma ile yayımlanan içerik</span></div></div>

<section id="grid"><div class="sectionintro"><div><p class="overline">SIRA + KOMŞULUK + SABİTLER</p><h2>Her yayından sonra<br>profil nasıl görünecek?</h2></div><p class="muted">Kaydırıcı, 180 ayrı yayın anını ve başlangıcı gösterir. “Planlanan sabitler” ayrı bir senaryodur. Griddeki görsele tıklayarak o kapağın gerekçesine ulaşabilirsin.</p></div>
<div class="simulator"><div class="controls">
<label class="overline" for="state-range">Yayın sayısı</label><div class="sliderlabel"><strong id="state-value">P006 sonrası</strong><span id="state-day" class="muted">Gün 12 · 6 yeni yayın</span></div>
<input class="range" type="range" id="state-range" min="0" max="180" step="1" value="6" aria-label="Gönderi sayısına göre grid görünümü">
<div class="stepcontrols"><button class="controlbutton" id="previous" type="button" aria-label="Bir önceki yayın anı">← Önceki</button><label for="state-number">Yayın</label><input id="state-number" type="number" min="0" max="180" value="6"><button class="controlbutton" id="next" type="button" aria-label="Bir sonraki yayın anı">Sonraki →</button></div>
<div class="mode" role="group" aria-label="Grid sıralama senaryosu"><button type="button" data-mode="chronological" aria-pressed="true">Kronolojik</button><button type="button" data-mode="pinned" aria-pressed="false">Planlanan sabitlerle</button></div>
<div class="steps" aria-label="Hızlı yayın seçimi">{steps}</div>
<div class="context"><p id="state-caption">Yeni sabit eklenmediği varsayılan sıra.</p><p id="pins-label" class="muted"></p><p class="muted">Sabitler, yayımlandıkları andan itibaren eklenir: P001 → P003 → P005. P030 sonrası soldan sağa P001 / P005 / P030 önerilir. Sabit bir gönderi alttaki akışta tekrar gösterilmez.</p></div>
<div class="currentpost" id="current-post"></div>
<div class="gridlinks"><a href="grids/chronological/S006.webp" id="grid-file" target="_blank" rel="noopener">Bu grid durumunu büyük aç</a><a href="grids/pinned/S006.webp" id="grid-other" target="_blank" rel="noopener">Aynı anı planlanan sabitlerle karşılaştır</a></div>
<p class="muted" style="font-size:12px">Simülasyon kronolojik birikimi kullanır. Hesaba özgü yeniden sıralama özelliğinin varlığına veya sonradan düzeltmeye dayanmıyor.</p>
</div><div class="profile"><div class="profilehead"><strong>yigitozen.art</strong><span class="tag" id="profile-state">+6 yayın</span></div><div class="profilegrid" id="profile-grid" aria-label="Simüle edilmiş ilk 12 profil kutusu"></div><div class="profilecaption"><p id="row-order" class="roworder"></p><p>Başlangıçta B01–B03, 4 Kasım 2026 tarihinde herkese açık profilde görülen üç görseldir. Bunların altı ve mevcut sabitlerin durumu doğrulanmadı; taralı kutular bu bilinmeyen alanı gösterir.</p><p>3:4 kutu ölçüsü bu hesabın web görünümünde ölçüldü. Bu yerel model, gerçek mobil yükleme önizlemesinin yerine geçmez.</p></div></div></div>
<div id="state-announcement" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)"></div></section>

<section id="first14"><p class="overline">GÜN 1 / 3 / 5 / 8 / 10 / 12</p><h2>İlk 14 günün altı kapağı</h2><p class="textlimit">Angora kişisel mekânla açar; Gary ve Cellular beden dilini genişletir. Sept gerçek renk değişimini gösterir. Painstaking, üç yüzün farklı dengelerine ayrılır. Ciao çizimi, bitmiş yüzeyden çizginin kurduğu bedene geçiş sağlar. Bu altı yayının aralarında üretim ve ölçüm günleri vardır.</p><div class="opening">{opening}</div><a class="button" href="../publication-plan-180-posts/ILK-14-GUN.html">Caption, storyboard ve günlük iş planını aç ↗</a></section>

<section id="system"><p class="overline">ORTAK GÖRSEL DİL</p><h2>Eser görünür kalır.<br>Başlık, bakılacak şeyi netleştirir.</h2><div class="systemgrid"><div class="systemitem"><h3>Eser bütünü</h3><p>Güçlü tek görsel, başlıksız ve kendi oranında. Kaynak, dikey kutuyu doldurmak için esnetilmez; kompozisyon kenarları korunur.</p></div><div class="systemitem"><h3>Tek somut soru</h3><p>Bütün eser veya önceden seçilmiş gerçek detay. Kısa İngilizce başlık, resmin üzerine değil ayrı boş alana yerleşir. Kapak sorusu içerikte karşılanır.</p></div><div class="systemitem"><h3>Gerekçeli karşılaştırma</h3><p>İki görüntü, ayrı alanlarda ve tam oranlarıyla. Bu yerleşim eserlerin fiziksel boyutlarının eşit olduğunu söylemez; ölçü bilgisi içerikte ayrıca açıklanır.</p></div></div><p class="note" style="margin-top:20px">Renk ve boşluk düzeni ortak; her üçüncü kutuyu aynı renge bağlayan bir şablon yok. Her yayın kendi başına okunur. Yeni bir yayın, erteleme veya sabitleme bütün görüntüyü bozmamalıdır.</p></section>

<section id="covers"><div class="sectionintro"><div><p class="overline">DOSYA + GEREKÇE + KIRPMA</p><h2>180 kapağın tasarım kaydı</h2></div><p class="muted">Kartın üstündeki görsel gerçek boyut oranındaki kapak dosyasıdır. Açılır bölümde 3:4 profil kutusu ve kare kırpma stres denemesi karşılaştırılır. Başlıklar ve yayın caption’ları İngilizcedir.</p></div>
<div class="filterbar"><label class="searchlabel" for="search">Gönderi, eser, başlık veya kaynak<input id="search" type="search" placeholder="P005, Angora, A1378…"></label><label for="phase">Plan bloğu<select id="phase"><option value="">Altı bloğun tamamı</option><option value="1">1 · P001–030</option><option value="2">2 · P031–060</option><option value="3">3 · P061–090</option><option value="4">4 · P091–120</option><option value="5">5 · P121–150</option><option value="6">6 · P151–180</option></select></label><label for="format">Yayın biçimi<select id="format"><option value="">Tüm biçimler</option><option value="Reel">Reel</option><option value="Carousel">Carousel</option><option value="Single">Tek görsel</option></select></label><button class="controlbutton" id="clear-filters" type="button">Filtreyi temizle</button></div><p id="result-count" class="resultcount" aria-live="polite">180 / 180 kapak gösteriliyor</p><p id="no-results" hidden>Bu aramayla eşleşen kapak yok.</p>
<div class="covercatalogue">{catalogue}</div></section>

<section class="evidence" id="evidence"><p class="overline">BİLİNENLER VE YAYIN ÖNCESİ KONTROL</p><h2>Üretilmiş dosya ile<br>hesapta doğrulanmış görünüm ayrı.</h2><div class="evidencegrid"><div><h3>Bu çalışmanın kapsadığı</h3><ul><li>Her gönderi için kaynak seçimi, İngilizce kapak başlığı veya başlıksız görsel kararı ve yerleşim dosyası.</li><li>Özgün kaynak oranını koruyan yerleşimler; orijinaller değiştirilmeden yerel dışa aktarımlar.</li><li>Her yayın sonrasındaki kronolojik ve planlanan sabitli grid görünümü.</li><li>Gözlemlenen 3:4 profil oranı ile kare merkez kırpma stres denemesinin ayrı gösterilmesi.</li></ul><p>Mevcut web profilinde ölçülen kutu yaklaşık 310,66 × 414,21 piksel: 3:4. Yeni feed kapaklarında 1080 × 1350, Reel kapaklarında 1080 × 1920 çalışma tuvali seçildi; bunlar bu projenin üretim tercihidir.</p></div><div><h3>Gerçek yayından önce teyit edilecek</h3><ul><li>Kullanılacak hesap ve yükleme yolunda feed, carousel ilk sayfası, Reel kapağı ve profil kırpması.</li><li>Mobil küçük görünümde metin, yüz, el, panel ve eser kenarlarının okunması.</li><li>Hesabın mevcut sabitleri, önerilen sabit sırası ve gerçek başlangıç durumu.</li><li>Renklerin kullanılan ekranda ve platform sıkıştırması sonrası görünümü.</li></ul><p>Yerel kapak tasarımı, içeriklerin yayımlandığı veya videoların tamamlandığı anlamına gelmez. İlk iki haftadaki Reel’ler için yeni İngilizce ses kayıtları ve son kurgu çalışması ayrıca gerekir.</p><p>İzleyici tepkisi ve erişim garanti edilemez. Gerçek sonuçlara göre sonraki eser atamaları değişirse, etkilenen kapak ve grid durumları yeniden üretilir.</p></div></div>
<p><a href="https://about.fb.com/ja/news/2022/06/grid_pinning_on_profile/" target="_blank" rel="noopener">Meta’nın sabitleme açıklaması</a>, en fazla üç gönderi veya Reel’in sabitlenebildiğini belgeler; bu hesaptaki mevcut düzeni doğrulamaz. <a href="https://about.fb.com/news/2025/06/inspiring-creativity-that-brings-people-together/" target="_blank" rel="noopener">2025 yeniden sıralama duyurusu</a> geleceğe dönük bir açıklamadır; bu tasarım hesabın bu özelliğe sahip olduğu varsayımına bağlı değildir.</p>
<div class="filelinks"><a href="covers.json">180 kapak kararının verisi</a><a href="design-brief.json">Görsel sistem ve başlangıç kaydı</a><a href="../planning-180-posts/grid-platform-evidence.json">Platform kanıtları ve sınırları</a><a href="../publication-plan-180-posts/PLAN-180-POST.json">180 gönderinin ana verisi</a><a href="../publication-plan-180-posts/PROFILE-ENTRY.html">Profil ve seçki girişi</a></div></section>
<footer class="foot">Yerel tasarım incelemesi · 4 Kasım 2026 · Instagram’da yayın, sabitleme veya profil değişikliği yapılmadı. Tam yayın sırası strateji taslağına aittir; kapak tasarımı büyüme sonucunun doğrulandığı anlamına gelmez. <a href="#top">Başa dön ↑</a></footer>
</main><script id="viewer-data" type="application/json">{viewer_data}</script><script>{JS}</script></body></html>'''
    OUTPUT.write_text(document, encoding="utf-8")
    return OUTPUT


if __name__ == "__main__":
    print(build())
