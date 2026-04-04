const DIFFICULTIES = ['easy', 'medium', 'hard'];

let DECKS = {}, deck = [], index = 0, flipped = false, ratings = [];
let thumbs = [], flags = [], currentDeckName = '', currentCert = null;
let selectedCategories = new Set(), selectedGroups = new Set(), selectedDifficulties = new Set();

fetch('cards.json')
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(data => { DECKS = data; buildDeckGrid(); })
  .catch(() => {
    document.getElementById('app').innerHTML =
      '<div class="error">Could not load cards.json — make sure it is in the same folder as index.html.</div>';
  });

// ── Helpers ────────────────────────────────────────────────────────────────
function show(id) { document.getElementById(id).style.display = 'block'; }
function hide(id) { document.getElementById(id).style.display = 'none'; }
function showOnly(id) {
  ['deckPicker','certPicker','filterPicker','studyView'].forEach(s => hide(s));
  show(id);
}

// ── Screen 1: Deck picker ──────────────────────────────────────────────────
function buildDeckGrid() {
  const grid = document.getElementById('deckGrid');
  grid.innerHTML = '';
  Object.keys(DECKS).forEach(name => {
    const cards = DECKS[name];
    const certs = [...new Set(cards.map(c => c.certification).filter(Boolean))];
    const tile  = document.createElement('div');
    tile.className = 'deck-tile';
    const tagHTML = certs.map(t => `<span class="deck-tile-tag">${t}</span>`).join('');
    tile.innerHTML = `
      <div class="deck-tile-name">${name}</div>
      <div class="deck-tile-count">${cards.length} card${cards.length !== 1 ? 's' : ''}</div>
      ${tagHTML ? `<div class="deck-tile-tags">${tagHTML}</div>` : ''}
    `;
    tile.addEventListener('click', () => selectDeck(name));
    grid.appendChild(tile);
  });
}

function showPicker() { showOnly('deckPicker'); }

// ── Screen 2: Certification picker ────────────────────────────────────────
function selectDeck(name) {
  currentDeckName = name;
  currentCert     = null;
  selectedCategories  = new Set();
  selectedGroups      = new Set();
  selectedDifficulties = new Set();

  const cards = DECKS[name];
  const certs = [...new Set(cards.map(c => c.certification).filter(Boolean))];

  if (certs.length === 0) {
    // No certifications — go straight to filters
    showFilterPicker();
    return;
  }

  document.getElementById('certDeckTitle').textContent = name;
  const grid = document.getElementById('certGrid');
  grid.innerHTML = '';

  certs.forEach(cert => {
    const count = cards.filter(c => c.certification === cert).length;
    const tile  = document.createElement('div');
    tile.className = 'cert-tile';
    tile.innerHTML = `
      <div class="cert-tile-name">${cert}</div>
      <div class="cert-tile-count">${count} card${count !== 1 ? 's' : ''}</div>
    `;
    tile.addEventListener('click', () => selectCert(cert));
    grid.appendChild(tile);
  });

  showOnly('certPicker');
}

function selectCert(cert) {
  currentCert = cert;
  selectedCategories  = new Set();
  selectedGroups      = new Set();
  selectedDifficulties = new Set();
  showFilterPicker();
}

// ── Screen 3: Filter picker ────────────────────────────────────────────────
function filterBack() {
  const certs = [...new Set(DECKS[currentDeckName].map(c => c.certification).filter(Boolean))];
  certs.length > 0 ? showOnly('certPicker') : showOnly('deckPicker');
}

function showFilterPicker() {
  const label = currentCert
    ? `${currentDeckName} · ${currentCert}`
    : currentDeckName;
  document.getElementById('filterDeckTitle').textContent = label;
  buildFilterChips();
  showOnly('filterPicker');
}

function certCards() {
  const all = DECKS[currentDeckName];
  return currentCert ? all.filter(c => c.certification === currentCert) : all;
}

function buildFilterChips() {
  const cards = certCards();

  const categories = [...new Set(cards.map(c => c.category).filter(Boolean))].sort();
  const groups     = [...new Set(cards.map(c => c.group).filter(Boolean))].sort();
  const diffs      = DIFFICULTIES.filter(d => cards.some(c => c.difficulty === d));

  const catSection = document.getElementById('categorySection');
  catSection.style.display = categories.length ? 'block' : 'none';

  const groupSection = document.getElementById('groupSection');
  groupSection.style.display = groups.length ? 'block' : 'none';

  document.getElementById('categoryChips').innerHTML = categories.map(cat => `
    <div class="chip${selectedCategories.has(cat) ? ' selected' : ''}" onclick="toggleCategory('${CSS.escape(cat)}')">${cat}</div>
  `).join('');

  document.getElementById('groupChips').innerHTML = groups.map(g => `
    <div class="chip${selectedGroups.has(g) ? ' selected' : ''}" onclick="toggleGroup('${CSS.escape(g)}')">${g}</div>
  `).join('');

  document.getElementById('difficultyChips').innerHTML = diffs.map(d => `
    <div class="chip diff-${d}${selectedDifficulties.has(d) ? ' selected' : ''}" onclick="toggleDifficulty('${d}')">${d}</div>
  `).join('');

  updateFilterCount();
}

function toggleCategory(cat) {
  selectedCategories.has(cat) ? selectedCategories.delete(cat) : selectedCategories.add(cat);
  buildFilterChips();
}
function toggleGroup(g) {
  selectedGroups.has(g) ? selectedGroups.delete(g) : selectedGroups.add(g);
  buildFilterChips();
}
function toggleDifficulty(d) {
  selectedDifficulties.has(d) ? selectedDifficulties.delete(d) : selectedDifficulties.add(d);
  buildFilterChips();
}

function filteredCards() {
  return certCards().filter(c => {
    const catOk  = selectedCategories.size === 0  || selectedCategories.has(c.category);
    const grpOk  = selectedGroups.size === 0       || selectedGroups.has(c.group);
    const diffOk = selectedDifficulties.size === 0 || selectedDifficulties.has(c.difficulty);
    return catOk && grpOk && diffOk;
  });
}

function updateFilterCount() {
  const count  = filteredCards().length;
  const total  = certCards().length;
  const active = selectedCategories.size + selectedGroups.size + selectedDifficulties.size;
  const el     = document.getElementById('filterCount');
  el.innerHTML = active > 0
    ? `<span>${count}</span> of ${total} cards match`
    : `All <span>${total}</span> cards`;
  document.getElementById('startBtn').disabled = count === 0;
}

// ── Screen 4: Study view ───────────────────────────────────────────────────
function startFiltered() {
  deck    = filteredCards().sort(() => Math.random() - 0.5);
  ratings = Array(deck.length).fill(null);
  thumbs  = Array(deck.length).fill(null);
  flags   = Array(deck.length).fill(null);
  index   = 0;
  flipped = false;
  showOnly('studyView');
  hide('summary');
  show('cardArea');
  render();
}

function render() {
  document.getElementById('cardInner').classList.remove('flipped');
  flipped = false;
  const card = deck[index];
  document.getElementById('frontText').textContent   = card.q;
  document.getElementById('backText').textContent    = card.a;
  document.getElementById('cardNum').textContent     = (index + 1) + ' of ' + deck.length;
  document.getElementById('prevBtn').disabled        = index === 0;
  document.getElementById('nextBtn').disabled        = index === deck.length - 1;
  document.getElementById('hintText').textContent    = 'Click the card to reveal the answer';
  document.getElementById('ratingRow').style.display = 'none';
  document.getElementById('flagPanel').style.display = 'none';
  document.getElementById('flagNote').value          = flags[index] || '';

  const metaTags = [
    card.category   ? `<span class="card-meta-tag">${card.category}</span>`            : '',
    card.group      ? `<span class="card-meta-tag">${card.group}</span>`               : '',
    card.difficulty ? `<span class="card-meta-tag ${card.difficulty}">${card.difficulty}</span>` : ''
  ].join('');
  document.getElementById('cardMeta').innerHTML = metaTags;

  const done = ratings.filter(r => r !== null).length;
  document.getElementById('pFill').style.width     = Math.round(done / deck.length * 100) + '%';
  document.getElementById('pLabel').textContent    = done + ' / ' + deck.length;
  const label = currentCert ? `${currentCert}` : currentDeckName;
  document.getElementById('deckCount').textContent = label + ' · ' + deck.length + ' cards';
  renderThumbs();
}

function renderThumbs() {
  document.getElementById('thumbUp').classList.toggle('active-up',     thumbs[index] === 'up');
  document.getElementById('thumbDown').classList.toggle('active-down', thumbs[index] === 'down');
}

function thumb(direction) {
  if (thumbs[index] === direction) {
    thumbs[index] = null;
    if (direction === 'down') hide('flagPanel');
  } else {
    thumbs[index] = direction;
    if (direction === 'down') {
      show('flagPanel');
      document.getElementById('flagNote').focus();
    } else {
      hide('flagPanel');
      flags[index] = null;
    }
  }
  renderThumbs();
}

function cancelFlag() {
  thumbs[index] = null;
  flags[index]  = null;
  hide('flagPanel');
  document.getElementById('flagNote').value = '';
  renderThumbs();
}

function submitFlag() {
  flags[index] = document.getElementById('flagNote').value.trim() || '(no note provided)';
  hide('flagPanel');
}

function flip() {
  flipped = !flipped;
  document.getElementById('cardInner').classList.toggle('flipped', flipped);
  if (flipped) {
    document.getElementById('hintText').textContent = 'How well did you know this?';
    document.getElementById('ratingRow').style.display = 'flex';
  }
}

function prev() { if (index > 0) { index--; render(); } }
function next() { if (index < deck.length - 1) { index++; render(); } }

function rate(r) {
  ratings[index] = r;
  if (index < deck.length - 1) { index++; render(); }
  else { showSummary(); }
}

function showSummary() {
  hide('cardArea');
  show('summary');
  document.getElementById('sGood').textContent = ratings.filter(r => r === 'good').length;
  document.getElementById('sOk').textContent   = ratings.filter(r => r === 'ok').length;
  document.getElementById('sHard').textContent = ratings.filter(r => r === 'hard').length;
  const flagged = deck.filter((_, i) => thumbs[i] === 'down');
  const flagSummary = document.getElementById('flagSummary');
  flagSummary.style.display = flagged.length > 0 ? 'block' : 'none';
  if (flagged.length > 0) document.getElementById('flagCount').textContent = flagged.length;
}

function exportFlags() {
  const lines = deck
    .map((card, i) => ({ card, thumb: thumbs[i], note: flags[i] }))
    .filter(item => item.thumb === 'down')
    .map(f => `Deck: ${currentDeckName}\nCertification: ${currentCert || 'n/a'}\nQuestion: ${f.card.q}\nAnswer: ${f.card.a}\nNote: ${f.note || ''}\n`)
    .join('\n---\n\n');
  const a    = document.createElement('a');
  a.href     = URL.createObjectURL(new Blob([lines], { type: 'text/plain' }));
  a.download = `flagged-${(currentCert || currentDeckName).toLowerCase().replace(/\s+/g, '-')}.txt`;
  a.click();
}

function restart() { startFiltered(); }

document.addEventListener('keydown', e => {
  if (document.getElementById('studyView').style.display === 'none') return;
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.code === 'Space')      { e.preventDefault(); flip(); }
  if (e.code === 'ArrowRight') next();
  if (e.code === 'ArrowLeft')  prev();
});
