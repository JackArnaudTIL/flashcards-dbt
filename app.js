const DIFFICULTIES = ['Easy', 'Medium', 'Hard'];

let DECKS = {}, deck = [], index = 0, flipped = false, ratings = [];
let thumbs = [], flags = [], currentDeckName = '', currentCert = null;
let selectedCategories = new Set(), selectedGroups = new Set(), selectedDifficulties = new Set();

fetch('cards.json')
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(data => { DECKS = data.decks; buildDeckGrid(); })
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

  // Group decks by section
  const sections = {};
  Object.keys(DECKS).forEach(name => {
    const section = DECKS[name].section || 'Other';
    if (!sections[section]) sections[section] = [];
    sections[section].push(name);
  });

  const SECTION_ORDER = ['Professional Development', 'Other Quizzes'];
  const sectionKeys = Object.keys(sections).sort((a, b) => {
    const ai = SECTION_ORDER.indexOf(a);
    const bi = SECTION_ORDER.indexOf(b);
    if (ai === -1 && bi === -1) return a.localeCompare(b);
    if (ai === -1) return 1;
    if (bi === -1) return -1;
    return ai - bi;
  });

  sectionKeys.forEach(section => {
    const heading = document.createElement('h2');
    heading.className = 'deck-section-heading';
    heading.textContent = section;
    grid.appendChild(heading);

    const row = document.createElement('div');
    row.className = 'deck-grid-row';
    grid.appendChild(row);

    sections[section].forEach(name => {
      const cards = DECKS[name].cards;
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
      row.appendChild(tile);
    });
  });
}

function showPicker() { showOnly('deckPicker'); }

// ── Screen 2: Certification picker ────────────────────────────────────────
function selectDeck(name) {
  currentDeckName = name;
  currentCert     = null;
  selectedCategories   = new Set();
  selectedGroups       = new Set();
  selectedDifficulties = new Set();
  selectedDeckSize     = null;

  const cards = DECKS[name].cards;
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
  selectedCategories   = new Set();
  selectedGroups       = new Set();
  selectedDifficulties = new Set();
  selectedDeckSize     = null;
  showFilterPicker();
}

// ── Screen 3: Filter picker ────────────────────────────────────────────────
function filterBack() {
  const certs = [...new Set(DECKS[currentDeckName].cards.map(c => c.certification).filter(Boolean))];
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

// Normalise group field — always returns an array
function cardGroups(card) {
  if (!card.group) return [];
  return Array.isArray(card.group) ? card.group : [card.group];
}

// Strip leading "Anything N: " prefix for display and sorting
function categoryLabel(cat) {
  const match = cat.match(/^[^:]+:\s*(.+)$/);
  return match ? match[1].trim() : cat;
}

function certCards() {
  const all = DECKS[currentDeckName].cards;
  return currentCert ? all.filter(c => c.certification === currentCert) : all;
}

function buildFilterChips() {
  const cards = certCards();

  const categories = [...new Set(cards.map(c => c.category).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));

  // Groups are filtered to only those present in the currently selected categories
  const activeCards = selectedCategories.size > 0
    ? cards.filter(c => selectedCategories.has(c.category))
    : cards;
  const groups = [...new Set(activeCards.flatMap(c => cardGroups(c)))].sort();

  // Remove any selectedGroups that are no longer valid after category change
  for (const g of selectedGroups) {
    if (!groups.includes(g)) selectedGroups.delete(g);
  }

  const diffs = DIFFICULTIES.filter(d => cards.some(c => c.difficulty === d));

  const catSection   = document.getElementById('categorySection');
  const groupSection = document.getElementById('groupSection');

  // Hide entire row if only one option exists
  catSection.style.display   = categories.length > 1 ? 'block' : 'none';
  groupSection.style.display = groups.length > 1     ? 'block' : 'none';

  document.getElementById('categoryChips').innerHTML = categories.map(cat => `
    <div class="chip${selectedCategories.has(cat) ? ' selected' : ''}" onclick="toggleCategory('${CSS.escape(cat)}')">${categoryLabel(cat)}</div>
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
    const grpOk  = selectedGroups.size === 0       || cardGroups(c).some(g => selectedGroups.has(g));
    const diffOk = selectedDifficulties.size === 0 || selectedDifficulties.has(c.difficulty);
    return catOk && grpOk && diffOk;
  });
}

const DECK_SIZES = [10, 20, 50];
let selectedDeckSize = null; // null = all cards

function updateFilterCount() {
  const count  = filteredCards().length;
  const total  = certCards().length;
  const active = selectedCategories.size + selectedGroups.size + selectedDifficulties.size;
  const el     = document.getElementById('filterCount');
  el.innerHTML = active > 0
    ? `<span>${count}</span> of ${total} cards match`
    : `All <span>${total}</span> cards`;

  // If selected size is no longer valid, reset it
  if (selectedDeckSize !== null && selectedDeckSize > count) selectedDeckSize = null;

  // Render deck size tiles
  const row = document.getElementById('deckSizeRow');
  const availableSizes = DECK_SIZES.filter(s => s < count);
  row.innerHTML = '';

  if (availableSizes.length > 0) {
    // "All" tile
    const allTile = document.createElement('div');
    allTile.className = 'size-tile' + (selectedDeckSize === null ? ' selected' : '');
    allTile.textContent = 'All ' + count;
    allTile.onclick = () => selectSize(null);
    row.appendChild(allTile);

    availableSizes.forEach(s => {
      const tile = document.createElement('div');
      tile.className = 'size-tile' + (selectedDeckSize === s ? ' selected' : '');
      tile.textContent = s;
      tile.onclick = () => selectSize(s);
      row.appendChild(tile);
    });
  }

  document.getElementById('startBtn').disabled = count === 0;
}

function selectSize(s) {
  selectedDeckSize = s;
  updateFilterCount();
}

// ── Screen 4: Study view ───────────────────────────────────────────────────
function startFiltered() {
  const shuffled = filteredCards().sort(() => Math.random() - 0.5);
  deck    = selectedDeckSize ? shuffled.slice(0, selectedDeckSize) : shuffled;
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
    card.category   ? `<span class="card-meta-tag">${categoryLabel(card.category)}</span>`  : '',
    ...cardGroups(card).map(g => `<span class="card-meta-tag">${g}</span>`),
    card.difficulty ? `<span class="card-meta-tag ${card.difficulty}">${card.difficulty}</span>` : ''
  ].join('');
  document.getElementById('cardMeta').innerHTML = metaTags;

  const attempted = ratings.filter(r => r !== null).length;
  const got        = ratings.filter(r => r === 'Good').length;
  const ok         = ratings.filter(r => r === 'Ok').length;
  const hard       = ratings.filter(r => r === 'Hard').length;
  document.getElementById('pFill').style.width  = Math.round(attempted / deck.length * 100) + '%';
  document.getElementById('pLabel').textContent = attempted + ' / ' + deck.length + ' attempted';
  document.getElementById('pBreakdown').textContent = attempted > 0
    ? got + ' Got it · ' + ok + ' Ok · ' + hard + ' Hard'
    : '';
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
  document.getElementById('sGood').textContent = ratings.filter(r => r === 'Good').length;
  document.getElementById('sOk').textContent   = ratings.filter(r => r === 'Ok').length;
  document.getElementById('sHard').textContent = ratings.filter(r => r === 'Hard').length;
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
  const studyView = document.getElementById('studyView');
  if (!studyView || studyView.style.display === 'none') return;
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.code === 'Space')      { e.preventDefault(); flip(); }
  if (e.code === 'ArrowRight') next();
  if (e.code === 'ArrowLeft')  prev();
});
