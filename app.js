const DIFFICULTIES = ['easy', 'medium', 'hard'];

let DECKS = {}, deck = [], index = 0, flipped = false, ratings = [];
let thumbs = [], flags = [], currentDeckName = '';
let selectedGroups = new Set(), selectedDifficulties = new Set();

fetch('cards.json')
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(data => { DECKS = data; buildDeckGrid(); })
  .catch(() => {
    document.getElementById('app').innerHTML =
      '<div class="error">Could not load cards.json — make sure it is in the same folder as index.html.</div>';
  });

function buildDeckGrid() {
  const grid = document.getElementById('deckGrid');
  grid.innerHTML = '';
  Object.keys(DECKS).forEach(name => {
    const cards  = DECKS[name];
    const groups = [...new Set(cards.map(c => c.group).filter(Boolean))];
    const diffs  = [...new Set(cards.map(c => c.difficulty).filter(Boolean))];
    const tile   = document.createElement('div');
    tile.className = 'deck-tile';
    const tagHTML = [...groups, ...diffs.sort((a,b) => DIFFICULTIES.indexOf(a) - DIFFICULTIES.indexOf(b))]
      .map(t => `<span class="deck-tile-tag">${t}</span>`).join('');
    tile.innerHTML = `
      <div class="deck-tile-name">${name}</div>
      <div class="deck-tile-count">${cards.length} card${cards.length !== 1 ? 's' : ''}</div>
      ${tagHTML ? `<div class="deck-tile-tags">${tagHTML}</div>` : ''}
    `;
    tile.addEventListener('click', () => showFilterPicker(name));
    grid.appendChild(tile);
  });
}

function showPicker() {
  show('deckPicker');
  hide('filterPicker');
  hide('studyView');
}

function showFilterPicker(name) {
  if (name) {
    currentDeckName = name;
    selectedGroups      = new Set();
    selectedDifficulties = new Set();
  }
  document.getElementById('filterDeckTitle').textContent = currentDeckName;
  buildFilterChips();
  show('filterPicker');
  hide('deckPicker');
  hide('studyView');
}

function buildFilterChips() {
  const cards  = DECKS[currentDeckName];
  const groups = [...new Set(cards.map(c => c.group).filter(Boolean))].sort();
  const diffs  = DIFFICULTIES.filter(d => cards.some(c => c.difficulty === d));

  const groupEl = document.getElementById('groupChips');
  const diffEl  = document.getElementById('difficultyChips');

  groupEl.innerHTML = groups.map(g => `
    <div class="chip${selectedGroups.has(g) ? ' selected' : ''}" onclick="toggleGroup('${g}')">${g}</div>
  `).join('');

  diffEl.innerHTML = diffs.map(d => `
    <div class="chip diff-${d}${selectedDifficulties.has(d) ? ' selected' : ''}" onclick="toggleDifficulty('${d}')">${d}</div>
  `).join('');

  updateFilterCount();
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
  return DECKS[currentDeckName].filter(c => {
    const groupOk = selectedGroups.size === 0      || selectedGroups.has(c.group);
    const diffOk  = selectedDifficulties.size === 0 || selectedDifficulties.has(c.difficulty);
    return groupOk && diffOk;
  });
}

function updateFilterCount() {
  const count = filteredCards().length;
  const total = DECKS[currentDeckName].length;
  const el    = document.getElementById('filterCount');
  const btn   = document.getElementById('startBtn');
  const activeFilters = selectedGroups.size + selectedDifficulties.size;
  el.innerHTML = activeFilters > 0
    ? `<span>${count}</span> of ${total} cards match`
    : `All <span>${total}</span> cards`;
  btn.disabled = count === 0;
}

function startFiltered() {
  deck    = filteredCards();
  ratings = Array(deck.length).fill(null);
  thumbs  = Array(deck.length).fill(null);
  flags   = Array(deck.length).fill(null);
  index   = 0;
  flipped = false;
  show('studyView');
  hide('filterPicker');
  hide('deckPicker');
  document.getElementById('summary').style.display  = 'none';
  document.getElementById('cardArea').style.display = 'block';
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
    card.group      ? `<span class="card-meta-tag">${card.group}</span>` : '',
    card.difficulty ? `<span class="card-meta-tag ${card.difficulty}">${card.difficulty}</span>` : ''
  ].join('');
  document.getElementById('cardMeta').innerHTML = metaTags;

  const done = ratings.filter(r => r !== null).length;
  document.getElementById('pFill').style.width    = Math.round(done / deck.length * 100) + '%';
  document.getElementById('pLabel').textContent   = done + ' / ' + deck.length;
  document.getElementById('deckCount').textContent = currentDeckName + ' · ' + deck.length + ' cards';
  renderThumbs();
}

function renderThumbs() {
  document.getElementById('thumbUp').classList.toggle('active-up',     thumbs[index] === 'up');
  document.getElementById('thumbDown').classList.toggle('active-down', thumbs[index] === 'down');
}

function thumb(direction) {
  if (thumbs[index] === direction) {
    thumbs[index] = null;
    if (direction === 'down') document.getElementById('flagPanel').style.display = 'none';
  } else {
    thumbs[index] = direction;
    if (direction === 'down') {
      document.getElementById('flagPanel').style.display = 'block';
      document.getElementById('flagNote').focus();
    } else {
      document.getElementById('flagPanel').style.display = 'none';
      flags[index] = null;
    }
  }
  renderThumbs();
}

function cancelFlag() {
  thumbs[index] = null;
  flags[index]  = null;
  document.getElementById('flagPanel').style.display = 'none';
  document.getElementById('flagNote').value = '';
  renderThumbs();
}

function submitFlag() {
  flags[index] = document.getElementById('flagNote').value.trim() || '(no note provided)';
  document.getElementById('flagPanel').style.display = 'none';
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
  document.getElementById('cardArea').style.display = 'none';
  document.getElementById('summary').style.display  = 'block';
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
    .map(f => `Deck: ${currentDeckName}\nQuestion: ${f.card.q}\nAnswer: ${f.card.a}\nNote: ${f.note || ''}\n`)
    .join('\n---\n\n');
  const a  = document.createElement('a');
  a.href   = URL.createObjectURL(new Blob([lines], { type: 'text/plain' }));
  a.download = `flagged-${currentDeckName.toLowerCase().replace(/\s+/g, '-')}.txt`;
  a.click();
}

function restart() { startFiltered(); }

function show(id) { document.getElementById(id).style.display = 'block'; }
function hide(id) { document.getElementById(id).style.display = 'none'; }

document.addEventListener('keydown', e => {
  if (document.getElementById('studyView').style.display === 'none') return;
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.code === 'Space')      { e.preventDefault(); flip(); }
  if (e.code === 'ArrowRight') next();
  if (e.code === 'ArrowLeft')  prev();
});
