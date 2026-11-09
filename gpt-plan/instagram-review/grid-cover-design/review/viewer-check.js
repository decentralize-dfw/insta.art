
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
