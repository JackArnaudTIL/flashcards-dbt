// Progress storage — localStorage when signed out, Firestore when signed in.
// The rest of the app calls the same sync API either way; Firestore writes
// are fire-and-forget so they never block the UI.
//
// Firestore shape:  /users/{uid}/decks/{deckName}  →  { [cardId]: { attempts, ratings[] } }

import { auth, db } from './firebase.js';
import {
  doc, setDoc, collection, getDocs
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

const STORAGE_KEY = 'fc_progress';

// In-memory cache — null means "not yet populated from Firestore"
let _cache = null;

// Called by auth listener after fetching Firestore data
export function hydrateCache(data) { _cache = data; }

// Called on sign-out
export function clearCache() { _cache = null; }

// ── Local helpers ─────────────────────────────────────────────────────────────
function _loadLocal() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
  catch { return {}; }
}

function _saveLocal(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

function _getAll() {
  return _cache !== null ? _cache : _loadLocal();
}

// ── Public API (synchronous — reads from cache or localStorage) ───────────────
export function getDeckProgress(deckName) {
  return _getAll()[deckName] || {};
}

export function deckStats(deckName, cards) {
  const progress = getDeckProgress(deckName);
  const total = cards.length;
  const attempted = cards.filter(c => progress[c.id]?.attempts > 0).length;
  const allRatings = cards.flatMap(c => progress[c.id]?.ratings || []);
  const goodCount = allRatings.filter(r => r === 'Good').length;
  const successRate = allRatings.length > 0
    ? Math.round((goodCount / allRatings.length) * 100)
    : null;
  return { total, attempted, successRate };
}

export function recordRating(deckName, cardId, rating) {
  const all = _getAll();
  if (!all[deckName]) all[deckName] = {};
  const entry = all[deckName][cardId] || { attempts: 0, ratings: [] };
  entry.attempts += 1;
  entry.ratings.push(rating);
  all[deckName][cardId] = entry;

  if (_cache !== null) _cache = all;
  _saveLocal(all);

  // Fire-and-forget Firestore write
  const user = auth.currentUser;
  if (user) {
    setDoc(
      doc(db, 'users', user.uid, 'decks', deckName),
      { [cardId]: { attempts: entry.attempts, ratings: entry.ratings } },
      { merge: true }
    ).catch(err => console.warn('Firestore write failed:', err));
  }
}

// ── Firestore fetch (called once on sign-in) ──────────────────────────────────
export async function loadUserProgress(uid) {
  const snap = await getDocs(collection(db, 'users', uid, 'decks'));
  const all = {};
  snap.forEach(d => { all[d.id] = d.data(); });
  hydrateCache(all);
  return all;
}

// ── localStorage → Firestore merge (called after sign-in if local data exists) ─
export async function mergeLocalToFirestore(uid) {
  const local = _loadLocal();
  if (Object.keys(local).length === 0) return 0;
  let count = 0;
  for (const [deckName, cards] of Object.entries(local)) {
    await setDoc(doc(db, 'users', uid, 'decks', deckName), cards, { merge: true });
    count += Object.keys(cards).length;
  }
  return count;
}
