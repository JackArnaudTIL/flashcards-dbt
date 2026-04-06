const DIFFICULTIES = ['Easy', 'Medium', 'Hard'];

let DECKS = {}, deck = [], index = 0, flipped = false, ratings = [];
let thumbs = [], flags = [], currentDeckName = '', currentCert = null;
let selectedCategories = new Set(), selectedGroups = new Set(), selectedDifficulties = new Set();

// ── Global Audio Controller ──────────────────────────────────────────────
let cardAudio = new Audio();

function stopAudio() {
  cardAudio.pause();
  cardAudio.currentTime = 0;
  // Remove existing listeners to prevent memory leaks or logic ghosting
  cardAudio.onloadedmetadata = null;
}

/**
 * Plays audio with an optional start time offset.
 * Waits for metadata to load before seeking to ensure the timestamp is valid.
 */
function playAudio(fileName, startTime = 0) {
  if (!fileName) return;
  stopAudio(); 

  const isCloud = fileName.startsWith('http');
  cardAudio.src = isCloud ? fileName : `./assets/sounds/${fileName}`;
  
  // Logic to handle seeking once the browser knows the file duration
  const seekAndPlay = () => {
    cardAudio.currentTime = startTime;
    cardAudio.play().catch(e => console.log("Playback blocked: Click the card to enable audio."));
  };

  if (cardAudio.readyState >= 1) {
    seekAndPlay();
  } else {
    cardAudio.onloadedmetadata = seekAndPlay;
  }
}

// ── Data Loading ──────────────────────────────────────────────────────────
fetch('cards.json')
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(data => { DECKS = data.decks; buildDeckGrid(); })
  .catch(() => {
    document.getElementById('app').innerHTML =
      '<div class="error">Could not load cards.json — check folder structure.</div>';
  });

// ── Helpers ────────────────────────────────────────────────────────────────
function show(id) { 
  const el = document.getElementById(id);
  if (el) el.style.display = 'block'; 
}
function hide(id) { 
  const el = document.getElementById(id);
  if (el) el.style.display = 'none'; 
}
function showOnly(id) {
  ['deckPicker','certPicker','filterPicker','studyView'].forEach(s => hide(s));
  show(id);
}

// ── Azure API Integration ──────────────────────────────────────────────────
const API_URL = 'https://flashcard-feedback-logging.azurewebsites.net/api/flashcardfeedback';

function sendFeedback(thumbType, noteText = '') {
  const card = deck[index];
  if (!card) return;
  
  const payload = {
    thumb: thumbType,
    deck: currentDeckName,
    certification: currentCert || '',
    category: card.category || '',
    group: Array.isArray(card.group) ? card.group.join(', ') : (card.group || ''),
    difficulty: card.difficulty || '',
    question: card.q,
    answer: card.a,
    note: noteText
  };

  fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(response => {
    if (!response.ok) console.error("Feedback API error:", response.status);
  })
  .catch(err => console.error("Network error sending feedback:", err));
}

// ── Screen 1: Deck picker ──────────────────────────────────────────────────
function buildDeckGrid() {
  const grid = document.getElementById('deckGrid');
  grid.innerHTML = '';

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

    sections[section].sort((a, b) => a.localeCompare(b)).forEach(name => {
      const cards = DECKS[name].cards;
      const tile  = document.createElement('div');
      tile.className = 'deck-tile';
      tile.innerHTML = `
        <div class="deck-tile-name">${name}</div>
        <div class="deck-tile-count">${cards.length} card${cards.length !== 1 ? 's' : ''}</div>
      `;
      tile.addEventListener('click', () => selectDeck(name));
      row.appendChild(tile);
    });
  });
}

function showPicker() { 
  stopAudio();
  showOnly('deckPicker'); 
}

// ── Screen 2: Certification picker ────────────────────────────────────────
function selectDeck(name) {
  currentDeckName = name;
  currentCert     = null;
  selectedCategories   = new Set();
  selectedGroups       = new Set();
  selectedDifficulties = new Set();
  selectedDeckSize     = null;

  stopAudio();

  const cards = DECKS[name].cards;
  const certs = [...new Set(cards.map(c => c.certification).filter(Boolean))];

  if (certs.length === 0) {
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
  const label = currentCert ? `${currentDeckName} · ${currentCert}` : currentDeckName;
  document.getElementById('filterDeckTitle').textContent = label;
  buildFilterChips();
  showOnly('filterPicker');
}

function cardGroups(card) {
  if (!card.group) return [];
  return Array.isArray(card.group) ? card.group : [card.group];
}

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

  // Calculate unique values
  const categories = [...new Set(cards.map(c => c.category).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));

  const activeCards = selectedCategories.size > 0
    ? cards.filter(c => selectedCategories.has(c.category))
    : cards;
    
  const groupCounts = {};
  activeCards.forEach(c => cardGroups(c).forEach(g => { groupCounts[g] = (groupCounts[g] || 0) + 1; }));
  const groups = [...new Set(activeCards.flatMap(c => cardGroups(c)))]
    .sort((a, b) => (groupCounts[b] || 0) - (groupCounts[a] || 0));

  const diffs = DIFFICULTIES.filter(d => cards.some(c => d === c.difficulty));

  // Identify sections
  const catSection   = document.getElementById('categorySection');
  const groupSection = document.getElementById('groupSection');
  const diffSection  = document.getElementById('difficultySection'); 
  const groupHint    = document.getElementById('groupHint');
  const groupChips   = document.getElementById('groupChips');

  // Logic: Hide sections if only 1 option exists
  if (catSection) catSection.style.display = categories.length > 1 ? 'block' : 'none';

  const categorySelected = selectedCategories.size > 0;
  if (groupSection) {
    groupSection.style.display = (groups.length > 1 || categorySelected) ? 'block' : 'none';
    if (groupHint) groupHint.style.display = categorySelected ? 'none' : 'block';
    if (groupChips) groupChips.style.display = categorySelected ? 'grid' : 'none';
  }

  if (diffSection) diffSection.style.display = diffs.length > 1 ? 'block' : 'none';

  // Render chips
  document.getElementById('categoryChips').innerHTML = categories.map(cat => `
    <div class="chip${selectedCategories.has(cat) ? ' selected' : ''}" onclick="toggleCategory('${CSS.escape(cat)}')">${categoryLabel(cat)}</div>
  `).join('');

  groupChips.innerHTML = groups.map(g => `
    <div class="chip${selectedGroups.has(g) ? ' selected' : ''}" onclick="toggleGroup('${CSS.escape(g)}')">
      ${g} <span class="chip-count">${groupCounts[g] || 0}</span>
    </div>
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
let selectedDeckSize = null;

function updateFilterCount() {
  const count  = filteredCards().length;
  const total  = certCards().length;
  const active = selectedCategories.size + selectedGroups.size + selectedDifficulties.size;
  const el     = document.getElementById('filterCount');
  el.innerHTML = active > 0
    ? `<span>${count}</span> of ${total} cards match`
    : `All <span>${total}</span> cards`;

  if (selectedDeckSize !== null && selectedDeckSize > count) selectedDeckSize = null;

  const sizeSection    = document.getElementById('deckSizeSection');
  const row            = document.getElementById('deckSizeRow');
  const availableSizes = DECK_SIZES.filter(s => s < count);
  row.innerHTML = '';

  if (availableSizes.length > 0) {
    sizeSection.style.display = 'block';
    const allTile = document.createElement('div');
    allTile.className = 'size-tile' + (selectedDeckSize === null ? ' selected' : '');
    allTile.innerHTML = `All <span class="size-tile-sub">${count} cards</span>`;
    allTile.onclick = () => selectSize(null);
    row.appendChild(allTile);

    availableSizes.forEach(s => {
      const tile = document.createElement('div');
      tile.className = 'size-tile' + (selectedDeckSize === s ? ' selected' : '');
      tile.innerHTML = `${s} <span class="size-tile-sub">cards</span>`;
      tile.onclick = () => selectSize(s);
      row.appendChild(tile);
    });
  } else {
    sizeSection.style.display = 'none';
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
  stopAudio(); 

  document.getElementById('cardInner').classList.remove('flipped');
  flipped = false;
  const card = deck[index];
  
  // Play Question Sound immediately
  if (card.q_sound) {
    playAudio(card.q_sound, card.q_sound_start || 0);
  }

  document.getElementById('frontText').textContent   = card.q;
  document.getElementById('backText').textContent    = card.a;
  document.getElementById('cardNum').textContent     = (index + 1) + ' of ' + deck.length;
  document.getElementById('prevBtn').disabled        = index === 0;
  document.getElementById('nextBtn').disabled        = index === deck.length - 1;
  document.getElementById('hintText').textContent = 'Click the card to reveal the answer';
  document.getElementById('hintText').className   = 'hint';
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
      sendFeedback('up');
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
  const noteText = document.getElementById('flagNote').value.trim();
  flags[index] = noteText || '(no note provided)';
  hide('flagPanel');
  sendFeedback('down', noteText);
}

function flip() {
  flipped = !flipped;
  document.getElementById('cardInner').classList.toggle('flipped', flipped);
  
  const card = deck[index];
  const deckConfig = DECKS[currentDeckName];

  if (flipped) {
    if (card.a_sound) {
      playAudio(card.a_sound, card.a_sound_start || 0);
    } 
    else if (deckConfig.a_sound) {
      playAudio(deckConfig.a_sound, deckConfig.a_sound_start || 0);
    }
  } else {
    stopAudio();
    if (card.q_sound) playAudio(card.q_sound, card.q_sound_start || 0);
  }

  const hint = document.getElementById('hintText');
  if (flipped) {
    hint.textContent = 'How did you do?';
    hint.className = 'hint answered';
    document.getElementById('ratingRow').style.display = 'flex';
  } else {
    hint.textContent = 'Click the card to reveal the answer';
    hint.className = 'hint';
    document.getElementById('ratingRow').style.display = 'none';
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
  stopAudio();
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