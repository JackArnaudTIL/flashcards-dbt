const DIFFICULTIES = ['Easy', 'Medium', 'Hard'];
const DECK_SIZES = [10, 20, 50, 100];

let DECKS = {}, deck = [], index = 0, flipped = false, ratings = [];
let thumbs = [], flags = [], currentDeckName = '', currentCert = null;
let selectedCategories = new Set(), selectedGroups = new Set(), selectedDifficulties = new Set();
let selectedDeckSize = 50; 

// ── Global IDE & Audio Controllers ───────────────────────────────────────
let codeEditor;
let cardAudio = new Audio();

document.addEventListener("DOMContentLoaded", () => {
  const textArea = document.getElementById('userCodeInput');
  if (textArea) {
    // Initialize CodeMirror IDE
    codeEditor = CodeMirror.fromTextArea(textArea, {
      lineNumbers: true,
      theme: "dracula",
      mode: "text/x-sql",
      indentUnit: 4,
      matchBrackets: true,
      extraKeys: {
        "Cmd-Enter": function() { submitCode(); },
        "Ctrl-Enter": function() { submitCode(); }
      }
    });
  }
});

function stopAudio() {
  cardAudio.pause();
  cardAudio.currentTime = 0;
  cardAudio.onloadedmetadata = null;
}

function playAudio(fileName, startTime = 0) {
  if (!fileName) return;
  stopAudio(); 

  const isCloud = fileName.startsWith('http');
  cardAudio.src = isCloud ? fileName : `./assets/sounds/${fileName}`;
  
  const seekAndPlay = () => {
    cardAudio.currentTime = startTime;
    cardAudio.play().catch(e => console.log("Playback blocked: Interaction required."));
  };

  if (cardAudio.readyState >= 1) {
    seekAndPlay();
  } else {
    cardAudio.onloadedmetadata = seekAndPlay;
  }
}

function getImagePath(fileName) {
  if (!fileName) return '';
  const isCloud = fileName.startsWith('http');
  return isCloud ? fileName : `./assets/images/${fileName}`;
}

/**
 * Formats text content to support Markdown-style code blocks and inline code
 */
function formatContent(text) {
  if (text === null || text === undefined) return '';

  let escaped = String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Multi-line Blocks: ```language \n code ``` -> <pre><code class="language">code</code></pre>
  escaped = escaped.replace(/\`\`\`([a-z]+)?\n?([\s\S]*?)\`\`\`/g, (match, lang, code) => {
    const langClass = lang ? `language-${lang}` : '';
    return `<pre><code class="${langClass}">${code}</code></pre>`;
  });

  // Inline Code: `code` -> <code>code</code>
  escaped = escaped.replace(/\`([^\`]+)\`/g, '<code>$1</code>');

  return escaped.replace(/\n/g, '<br>');
}

// ── Data Loading ──────────────────────────────────────────────────────────
fetch('cards.json')
  .then(r => { 
    if (!r.ok) throw new Error("Could not fetch cards.json file."); 
    return r.json(); 
  })
  .then(data => { 
    if (!data || !data.decks) throw new Error("cards.json is missing the 'decks' object.");
    DECKS = data.decks; 
    buildDeckGrid(); 
  })
  .catch((err) => {
    console.error("Initialization Error:", err);
    const container = document.getElementById('app') || document.body;
    container.innerHTML = `
      <div class="error" style="text-align: center; margin-top: 3rem; color: var(--red, #dc2626);">
        <h2 style="margin-bottom: 1rem;">⚠️ Application Error</h2>
        <p>${err.message}</p>
      </div>`;
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
  }).catch(err => console.error("Feedback error:", err));
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
    return ai === -1 ? 1 : bi === -1 ? -1 : ai - bi;
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
        <div class="deck-tile-count">${cards.length} cards</div>
      `;
      tile.onclick = () => selectDeck(name);
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
  selectedCategories.clear(); 
  selectedGroups.clear(); 
  selectedDifficulties.clear();
  selectedDeckSize = 50; 

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
    const tile  = document.createElement('div');
    tile.className = 'cert-tile';
    tile.innerHTML = `<div class="cert-tile-name">${cert}</div>`;
    tile.onclick = () => {
        currentCert = cert;
        showFilterPicker();
    };
    grid.appendChild(tile);
  });

  showOnly('certPicker');
}

// ── Screen 3: Filter picker ──────────────────────────────────
function filterBack() {
  const certs = [...new Set(DECKS[currentDeckName].cards.map(c => c.certification).filter(Boolean))];
  certs.length > 0 ? showOnly('certPicker') : showOnly('deckPicker');
}

function showFilterPicker() {
  const label = currentCert ? `${currentDeckName} · ${currentCert}` : currentDeckName;
  document.getElementById('filterDeckTitle').textContent = label;
  document.getElementById('customizationPanel').style.display = 'none';
  document.getElementById('customChevron').classList.remove('rotated');
  buildFilterChips();
  showOnly('filterPicker');
}

function toggleCustomization() {
  const panel = document.getElementById('customizationPanel');
  const chevron = document.getElementById('customChevron');
  const isHidden = panel.style.display === 'none';
  panel.style.display = isHidden ? 'block' : 'none';
  chevron.classList.toggle('rotated', isHidden);
}

function categoryLabel(cat) {
  const match = cat.match(/^[^:]+:\s*(.+)$/);
  return match ? match[1].trim() : cat;
}

function buildFilterChips() {
  const cards = currentCert ? DECKS[currentDeckName].cards.filter(c => c.certification === currentCert) : DECKS[currentDeckName].cards;
  const categories = [...new Set(cards.map(c => c.category).filter(Boolean))].sort();
  const activeCards = selectedCategories.size > 0 ? cards.filter(c => selectedCategories.has(c.category)) : cards;
  
  const groupCounts = {}; 
  activeCards.forEach(c => (Array.isArray(c.group) ? c.group : [c.group]).filter(Boolean).forEach(g => groupCounts[g] = (groupCounts[g] || 0) + 1));
  const groups = Object.keys(groupCounts).sort((a,b) => groupCounts[b] - groupCounts[a]);
  const diffs = DIFFICULTIES.filter(d => cards.some(c => c.difficulty === d));

  document.getElementById('categoryChips').innerHTML = categories.map(cat => `
    <div class="chip${selectedCategories.has(cat) ? ' selected' : ''}" onclick="toggleCategory('${CSS.escape(cat)}')">${categoryLabel(cat)}</div>
  `).join('');
  
  const grpSec = document.getElementById('groupSection');
  if (selectedCategories.size > 0 && groups.length > 1) {
    grpSec.style.display = 'block';
    document.getElementById('groupChips').innerHTML = groups.map(g => `
      <div class="chip${selectedGroups.has(g) ? ' selected' : ''}" onclick="toggleGroup('${CSS.escape(g)}')">${g} <span class="chip-count">${groupCounts[g]}</span></div>
    `).join('');
  } else { 
    grpSec.style.display = 'none'; 
  }

  document.getElementById('difficultyChips').innerHTML = diffs.map(d => `
    <div class="chip diff-${d}${selectedDifficulties.has(d) ? ' selected' : ''}" onclick="toggleDifficulty('${CSS.escape(d)}')">${d}</div>
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

function updateFilterCount() {
  const all = currentCert ? DECKS[currentDeckName].cards.filter(c => c.certification === currentCert) : DECKS[currentDeckName].cards;
  const filtered = all.filter(c => {
    const catOk = selectedCategories.size === 0 || selectedCategories.has(c.category);
    const grpOk = selectedGroups.size === 0 || (Array.isArray(c.group) ? c.group : [c.group]).some(g => selectedGroups.has(g));
    const diffOk = selectedDifficulties.size === 0 || selectedDifficulties.has(c.difficulty);
    return catOk && grpOk && diffOk;
  });
  
  const count = filtered.length;
  document.getElementById('heroCountDisplay').textContent = `${selectedDeckSize !== null && selectedDeckSize < count ? selectedDeckSize : count} cards`;
  document.getElementById('filterCount').innerHTML = `<span>${count}</span> of ${all.length} cards match filters`;
  
  const row = document.getElementById('deckSizeRow'); row.innerHTML = '';
  [null, 10, 20, 50, 100].filter(s => s === null || s < count).forEach(s => {
    const tile = document.createElement('div'); 
    tile.className = `size-tile ${selectedDeckSize === s ? 'selected' : ''}`;
    tile.innerHTML = s === null ? `All <span class="size-tile-sub">${count}</span>` : s;
    tile.onclick = () => { selectedDeckSize = s; updateFilterCount(); };
    row.appendChild(tile);
  });
  document.getElementById('startBtn').disabled = count === 0;
}

function selectSize(s) {
  selectedDeckSize = s;
  updateFilterCount();
}

// ── Screen 4: Study view ───────────────────────────────────────────────────
function startFiltered() {
  const all = currentCert ? DECKS[currentDeckName].cards.filter(c => c.certification === currentCert) : DECKS[currentDeckName].cards;
  const filtered = all.filter(c => {
    const catOk = selectedCategories.size === 0 || selectedCategories.has(c.category);
    const grpOk = selectedGroups.size === 0 || (Array.isArray(c.group) ? c.group : [c.group]).some(g => selectedGroups.has(g));
    const diffOk = selectedDifficulties.size === 0 || selectedDifficulties.has(c.difficulty);
    return catOk && grpOk && diffOk;
  });
  
  deck = filtered.sort(() => Math.random() - 0.5).slice(0, selectedDeckSize || filtered.length);
  ratings = Array(deck.length).fill(null); 
  thumbs = Array(deck.length).fill(null); 
  flags = Array(deck.length).fill(null);
  index = 0; 
  flipped = false; 
  
  showOnly('studyView'); 
  render();
}

function render() {
  stopAudio();
  const card = deck[index];
  const deckConfig = DECKS[currentDeckName];

  // ── Code IDE Handle ──
  const codeContainer = document.getElementById('codeInputContainer');
  const compareBtn = document.getElementById('compareBtn');
  
  if (codeEditor) { 
    codeEditor.setValue(''); 
    codeEditor.setOption('readOnly', false); 
    
    // Auto-detect language mode from the answer markdown for the IDE
    let mode = "javascript";
    if (card.a && card.a.includes('```sql')) mode = "text/x-sql";
    if (card.a && card.a.includes('```python')) mode = "python";
    if (card.a && card.a.includes('```jinja')) mode = "jinja2";
    codeEditor.setOption('mode', mode);
  }
  
  if (compareBtn) { 
    compareBtn.style.display = 'inline-block'; 
  }
  
  if (codeContainer) { 
    if (card.requires_code) {
      codeContainer.style.display = 'block'; 
      // CodeMirror needs a manual refresh when its container becomes visible
      setTimeout(() => codeEditor.refresh(), 10); 
    } else {
      codeContainer.style.display = 'none'; 
    }
  }

  document.getElementById('cardInner').classList.remove('flipped');
  flipped = false;
  
  if (card.q_sound || deckConfig.q_sound) {
    playAudio(card.q_sound || deckConfig.q_sound, card.q_sound_start || deckConfig.q_sound_start || 0);
  }

  // ── Image Clear Fix ──
  const fImg = document.getElementById('frontImage'); 
  const bImg = document.getElementById('backImage');
  fImg.removeAttribute('src'); 
  bImg.removeAttribute('src');
  
  if (card.q_image || deckConfig.q_image) { 
    fImg.src = getImagePath(card.q_image || deckConfig.q_image); 
    fImg.style.display = 'block'; 
  } else { 
    fImg.style.display = 'none'; 
  }
  
  if (card.a_image || deckConfig.a_image) { 
    bImg.src = getImagePath(card.a_image || deckConfig.a_image); 
    bImg.style.display = 'block'; 
  } else { 
    bImg.style.display = 'none'; 
  }

  document.getElementById('frontText').innerHTML = formatContent(card.q);
  document.getElementById('backText').innerHTML  = formatContent(card.a);
  
  // Apply Highlight.js to any code blocks in the flashcard answers
  if (window.hljs) {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightElement(block);
    });
  }

  document.getElementById('cardNum').textContent = `${index + 1} of ${deck.length}`;
  document.getElementById('prevBtn').disabled = index === 0;
  document.getElementById('nextBtn').disabled = index === deck.length - 1;
  document.getElementById('ratingRow').style.display = 'none';
  document.getElementById('hintText').textContent = 'Click the card or "Submit" to reveal the answer';
  document.getElementById('hintText').className = 'hint';

  document.getElementById('cardMeta').innerHTML = [
    card.category ? `<span class="card-meta-tag">${categoryLabel(card.category)}</span>` : '',
    ...(Array.isArray(card.group) ? card.group : [card.group]).filter(Boolean).map(g => `<span class="card-meta-tag">${g}</span>`),
    card.difficulty ? `<span class="card-meta-tag ${card.difficulty}">${card.difficulty}</span>` : ''
  ].join('');

  const att = ratings.filter(r => r !== null).length;
  document.getElementById('pFill').style.width = Math.round((att / deck.length) * 100) + '%';
  document.getElementById('pLabel').textContent = `${att} / ${deck.length} attempted`;
  document.getElementById('pBreakdown').textContent = att > 0 ? `${ratings.filter(r=>r==='Good').length} Got it · ${ratings.filter(r=>r==='Ok').length} Ok · ${ratings.filter(r=>r==='Hard').length} Hard` : '';
  
  renderThumbs();
}

function submitCode() { 
  if (!flipped) {
    flip(); 
  }
}

function flip() {
  flipped = !flipped;
  const card = deck[index];
  const deckConfig = DECKS[currentDeckName];
  document.getElementById('cardInner').classList.toggle('flipped', flipped);
  
  const compareBtn = document.getElementById('compareBtn');
  
  if (card.requires_code) {
    if (codeEditor) {
      codeEditor.setOption('readOnly', flipped ? 'nocursor' : false);
    }
    if (compareBtn) {
      compareBtn.style.display = flipped ? 'none' : 'inline-block';
    }
  }

  if (flipped) {
    if (card.a_sound || deckConfig.a_sound) {
      playAudio(card.a_sound || deckConfig.a_sound, card.a_sound_start || deckConfig.a_sound_start || 0);
    }
    document.getElementById('hintText').textContent = 'How did you do?';
    document.getElementById('hintText').className = 'hint answered';
    document.getElementById('ratingRow').style.display = 'flex';
  } else {
    stopAudio(); 
    document.getElementById('ratingRow').style.display = 'none';
  }
}

function rate(r) {
  ratings[index] = r;
  if (index < deck.length - 1) { 
    index++; 
    render(); 
  } else { 
    showSummary(); 
  }
}

function prev() { 
  if (index > 0) { 
    index--; 
    render(); 
  } 
}

function next() { 
  if (index < deck.length - 1) { 
    index++; 
    render(); 
  } 
}

function thumb(dir) {
  thumbs[index] = (thumbs[index] === dir) ? null : dir;
  if (dir === 'down' && thumbs[index]) {
    show('flagPanel');
  } else { 
    hide('flagPanel'); 
    if (dir === 'up') {
      sendFeedback('up'); 
    }
  }
  renderThumbs();
}

function renderThumbs() {
  document.getElementById('thumbUp').classList.toggle('active-up', thumbs[index] === 'up');
  document.getElementById('thumbDown').classList.toggle('active-down', thumbs[index] === 'down');
}

function submitFlag() {
  const note = document.getElementById('flagNote').value.trim();
  flags[index] = note || '(no note)';
  hide('flagPanel'); 
  sendFeedback('down', note);
}

function showSummary() {
  stopAudio(); 
  hide('cardArea'); 
  show('summary');
  
  document.getElementById('sGood').textContent = ratings.filter(r => r === 'Good').length;
  document.getElementById('sOk').textContent = ratings.filter(r => r === 'Ok').length;
  document.getElementById('sHard').textContent = ratings.filter(r => r === 'Hard').length;
}

function restart() { 
  startFiltered(); 
}

document.addEventListener('keydown', e => {
  if (document.getElementById('studyView').style.display === 'none') return;
  
  // Ignore keydowns if user is typing in a textarea, input, OR our new CodeMirror IDE
  if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT' || e.target.closest('.CodeMirror')) return;
  
  if (e.code === 'Space') { 
    e.preventDefault(); 
    flip(); 
  }
  if (e.code === 'ArrowRight') next();
  if (e.code === 'ArrowLeft') prev();
});