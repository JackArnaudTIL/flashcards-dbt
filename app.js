let DECKS = {}, deck = [], index = 0, flipped = false, ratings = [], currentDeckName = '';

fetch('cards.json')
  .then(r => { if (!r.ok) throw new Error(); return r.json(); })
  .then(data => {
    DECKS = data;
    buildDeckGrid();
  })
  .catch(() => {
    document.getElementById('app').innerHTML =
      '<div class="error">Could not load cards.json — make sure it is in the same folder as index.html.</div>';
  });

function buildDeckGrid() {
  const grid = document.getElementById('deckGrid');
  grid.innerHTML = '';
  Object.keys(DECKS).forEach(name => {
    const count = DECKS[name].length;
    const tile = document.createElement('div');
    tile.className = 'deck-tile';
    tile.innerHTML = `<div class="deck-tile-name">${name}</div><div class="deck-tile-count">${count} card${count !== 1 ? 's' : ''}</div>`;
    tile.addEventListener('click', () => startDeck(name));
    grid.appendChild(tile);
  });
}

function showPicker() {
  document.getElementById('deckPicker').style.display = 'block';
  document.getElementById('studyView').style.display  = 'none';
}

function startDeck(name) {
  currentDeckName = name;
  deck    = DECKS[name];
  ratings = Array(deck.length).fill(null);
  index   = 0;
  flipped = false;
  document.getElementById('deckPicker').style.display = 'none';
  document.getElementById('studyView').style.display  = 'block';
  document.getElementById('summary').style.display    = 'none';
  document.getElementById('cardArea').style.display   = 'block';
  render();
}

function render() {
  document.getElementById('cardInner').classList.remove('flipped');
  flipped = false;
  document.getElementById('frontText').textContent   = deck[index].q;
  document.getElementById('backText').textContent    = deck[index].a;
  document.getElementById('cardNum').textContent     = (index + 1) + ' of ' + deck.length;
  document.getElementById('prevBtn').disabled        = index === 0;
  document.getElementById('nextBtn').disabled        = index === deck.length - 1;
  document.getElementById('hintText').textContent    = 'Click the card to reveal the answer';
  document.getElementById('ratingRow').style.display = 'none';
  const done = ratings.filter(r => r !== null).length;
  document.getElementById('pFill').style.width   = Math.round(done / deck.length * 100) + '%';
  document.getElementById('pLabel').textContent  = done + ' / ' + deck.length;
  document.getElementById('deckCount').textContent = currentDeckName + ' · ' + deck.length + ' cards';
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
}

function restart() { startDeck(currentDeckName); }

document.addEventListener('keydown', e => {
  if (document.getElementById('studyView').style.display === 'none') return;
  if (e.code === 'Space')      { e.preventDefault(); flip(); }
  if (e.code === 'ArrowRight') next();
  if (e.code === 'ArrowLeft')  prev();
});
