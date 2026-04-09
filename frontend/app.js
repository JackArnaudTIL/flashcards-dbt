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
      mode: "text/plain",
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
 * Wraps code blocks in a Gemini-style header layout.
 */
function formatContent(text) {
  if (text === null || text === undefined) return '';

  // 1. Escaping HTML
  let escaped = String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // 2. Extract multi-line Blocks: ```language \n code ```
  // We extract them first so we don't accidentally inject <br> tags into the code body
  const codeBlocks = [];
  escaped = escaped.replace(/\`\`\`([a-z0-9]+)?\n?([\s\S]*?)\`\`\`/gi, (match, lang, code) => {
    const langClass = lang ? `language-${lang.toLowerCase()}` : '';
    const langLabel = lang ? lang.toLowerCase() : 'text';
    
    codeBlocks.push(`
      <div class="gemini-code-wrapper">
        <div class="gemini-code-header">
          <span class="gemini-code-lang">${langLabel}</span>
          <button class="gemini-code-copy" onclick="copyCode(this)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            Copy
          </button>
        </div>
        <pre><code class="${langClass}">${code}</code></pre>
      </div>
    `);
    
    return `___CODE_BLOCK_${codeBlocks.length - 1}___`;
  });

  // 3. Inline Code: `code` -> <code>code</code>
  escaped = escaped.replace(/\`([^\`]+)\`/g, '<code>$1</code>');

  // 4. Preserve standard line breaks for non-code text
  escaped = escaped.replace(/\n/g, '<br>');

  // 5. Restore the fully formatted code blocks
  codeBlocks.forEach((block, i) => {
    escaped = escaped.replace(`___CODE_BLOCK_${i}___`, block);
  });

  return escaped;
}

// ── Copy Code Logic ───────────────────────────────────────────────────────
window.copyCode = function(btn) {
  const codeEl = btn.closest('.gemini-code-wrapper').querySelector('code');
  
  // Decode HTML entities back to raw text for the clipboard
  const textToCopy = codeEl.innerHTML
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&");

  const copyFallback = (str) => {
    const textArea = document.createElement("textarea");
    textArea.value = str;
    document.body.appendChild(textArea);
    textArea.select();
    try { document.execCommand('copy'); } catch (err) { console.error('Copy failed', err); }
    document.body.removeChild(textArea);
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(textToCopy).catch(() => copyFallback(textToCopy));
  } else {
    copyFallback(textToCopy);
  }

  // Update UI to show success
  const originalHtml = btn.innerHTML;
  btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> <span style="color:#059669">Copied!</span>`;
  setTimeout(() => { btn.innerHTML = originalHtml; }, 2000);
};

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
    const count = cards.filter(c => c.certification === cert).length;
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

function toggleCategory(cat) { selectedCategories.has(cat) ? selectedCategories.delete(cat) : selectedCategories.add(cat); buildFilterChips(); }
function toggleGroup(g) { selectedGroups.has(g) ? selectedGroups.delete(g) : selectedGroups.add(g); buildFilterChips(); }
function toggleDifficulty(d) { selectedDifficulties.has(d) ? selectedDifficulties.delete(d) : selectedDifficulties.add(d); buildFilterChips(); }

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
    const tile = document.createElement('div'); tile.className = `size-tile ${selectedDeckSize === s ? 'selected' : ''}`;
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
  const resultEl = document.getElementById('comparisonResult');
  
  if (codeEditor) { 
    codeEditor.setValue(''); 
    codeEditor.setOption('readOnly', false); 
    
    // Auto-detect language mode from the answer markdown for the IDE
    let mode = "text/plain";
    let label = "text";
    if (card.a && card.a.includes('```sql')) { mode = "text/x-sql"; label = "sql"; }
    else if (card.a && card.a.includes('```python')) { mode = "python"; label = "python"; }
    else if (card.a && card.a.includes('```jinja')) { mode = "jinja2"; label = "jinja"; }
    
    codeEditor.setOption('mode', mode);
    
    const langLabelEl = document.getElementById('draftingLangLabel');
    if (langLabelEl) langLabelEl.textContent = label;
  }
  
  if (compareBtn) { 
    compareBtn.style.display = 'inline-block'; 
  }
  
  if (resultEl) {
    resultEl.style.display = 'none';
    resultEl.className = 'comparison-result';
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
  
  const cardInner = document.getElementById('cardInner');
  if (flipped) {
    cardInner.classList.add('flipped');
  } else {
    cardInner.classList.remove('flipped');
  }
  
  const card = deck[index];
  const deckConfig = DECKS[currentDeckName];
  
  const codeBox = document.getElementById('userCodeInput');
  const compareBtn = document.getElementById('compareBtn');
  const resultEl = document.getElementById('comparisonResult');
  
  if (card.requires_code) {
    if (codeEditor) {
      codeEditor.setOption('readOnly', flipped ? 'nocursor' : false);
    }
    
    if (compareBtn) {
      compareBtn.style.display = flipped ? 'none' : 'inline-block';
    }

    // Code comparison logic
    if (flipped && resultEl) {
      const userCode = codeEditor ? codeEditor.getValue() : codeBox.value;
      
      // Extract code from markdown wrapper
      const expectedMatch = card.a.match(/```[a-z0-9]*\n([\s\S]*?)```/i);
      const expectedCode = expectedMatch ? expectedMatch[1] : card.a;
      
      // Normalize to handle formatting/spacing differences safely
      const normUser = userCode.replace(/\r\n/g, '\n').split('\n').map(l => l.trimEnd()).join('\n').trim();
      const normExpected = expectedCode.replace(/\r\n/g, '\n').split('\n').map(l => l.trimEnd()).join('\n').trim();
      
      if (normUser === normExpected) {
        resultEl.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px; vertical-align:text-bottom"><polyline points="20 6 9 17 4 12"></polyline></svg> Perfect Match!';
        resultEl.className = 'comparison-result match';
      } else {
        resultEl.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px; vertical-align:text-bottom"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg> Code Differs';
        resultEl.className = 'comparison-result mismatch';
      }
      resultEl.style.display = 'inline-flex';
    } else if (resultEl) {
      resultEl.style.display = 'none';
    }
  }

  const hint = document.getElementById('hintText');
  const ratingRow = document.getElementById('ratingRow');

  if (flipped) {
    const finalASound = card.a_sound || deckConfig.a_sound;
    if (finalASound) {
      playAudio(finalASound, card.a_sound_start || deckConfig.a_sound_start || 0);
    } 
    
    hint.textContent = 'How did you do?';
    hint.className = 'hint answered';
    ratingRow.style.display = 'flex';
  } else {
    stopAudio();
    
    const finalQSound = card.q_sound || deckConfig.q_sound;
    if (finalQSound) {
        playAudio(finalQSound, card.q_sound_start || deckConfig.q_sound_start || 0);
    }
    
    hint.textContent = 'Click the card to reveal the answer';
    hint.className = 'hint';
    ratingRow.style.display = 'none';
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
  const thumbUpBtn = document.getElementById('thumbUp');
  const thumbDownBtn = document.getElementById('thumbDown');
  
  if (thumbs[index] === 'up') {
    thumbUpBtn.classList.add('active-up');
  } else {
    thumbUpBtn.classList.remove('active-up');
  }
  
  if (thumbs[index] === 'down') {
    thumbDownBtn.classList.add('active-down');
  } else {
    thumbDownBtn.classList.remove('active-down');
  }
}

function cancelFlag() {
  thumbs[index] = null;
  flags[index]  = null;
  hide('flagPanel');
  document.getElementById('flagNote').value = '';
  renderThumbs();
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
  
  const gotItCount = ratings.filter(r => r === 'Good').length;
  const okCount = ratings.filter(r => r === 'Ok').length;
  const hardCount = ratings.filter(r => r === 'Hard').length;
  
  document.getElementById('sGood').textContent = gotItCount;
  document.getElementById('sOk').textContent   = okCount;
  document.getElementById('sHard').textContent = hardCount;
  
  const flagged = deck.filter((_, i) => thumbs[i] === 'down');
  const flagSummary = document.getElementById('flagSummary');
  
  if (flagged.length > 0) {
    flagSummary.style.display = 'block';
    document.getElementById('flagCount').textContent = flagged.length;
  } else {
    flagSummary.style.display = 'none';
  }
}

function exportFlags() {
  const lines = deck
    .map((card, i) => {
      return { card: card, thumb: thumbs[i], note: flags[i] };
    })
    .filter(item => item.thumb === 'down')
    .map(f => `Deck: ${currentDeckName}\nCertification: ${currentCert || 'n/a'}\nQuestion: ${f.card.q}\nAnswer: ${f.card.a}\nNote: ${f.note || ''}\n`)
    .join('\n---\n\n');
    
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([lines], { type: 'text/plain' }));
  a.download = `flagged-${(currentCert || currentDeckName).toLowerCase().replace(/\s+/g, '-')}.txt`;
  a.click();
}

function restart() { 
  startFiltered(); 
}

document.addEventListener('keydown', e => {
  const studyView = document.getElementById('studyView');
  if (!studyView || studyView.style.display === 'none') return;
  
  // Allow Cmd+Enter or Ctrl+Enter to submit code from the textarea
  if (e.target.tagName === 'TEXTAREA' || e.target.closest('.CodeMirror')) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      submitCode();
      return;
    }
    return; // Don't flip with space while typing
  }
  
  if (e.code === 'Space') { 
    e.preventDefault(); 
    flip(); 
  }
  
  if (e.code === 'ArrowRight') {
    next();
  }
  
  if (e.code === 'ArrowLeft') {
    prev();
  }
});