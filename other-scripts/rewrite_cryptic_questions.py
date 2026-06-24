"""
Rewrites cryptic/telegraphic dbt flashcard questions using Claude.
Targets questions under 60 chars that follow the fragment pattern
"Short noun phrase. Question word?" left over from the Scenario: cleanup.
"""

import json
import hashlib
import re
import anthropic

DECK = 'dbt'
BATCH_SIZE = 25

def make_id(deck_name, q, a):
    key = deck_name + '||' + q + '||' + a
    return hashlib.sha1(key.encode('utf-8')).hexdigest()[:8]

def is_cryptic(q):
    """Fragment pattern: ends with '. Short question?' and is under 60 chars."""
    return bool(re.search(r'\.\s+[A-Z][a-zA-Z ]{0,25}\?$', q)) and len(q) < 60

def rewrite_batch(client, cards):
    """Ask Claude to rewrite a batch of cryptic questions."""
    payload = [{"index": i, "q": c["q"], "a": c["a"]} for i, c in cards]

    prompt = f"""You are improving flashcard questions for a dbt (data build tool) study deck.

The questions below are too telegraphic — they were originally written as scenario shorthand
and need rewriting as clear, complete, standalone questions a learner can understand.

Rules:
- One sentence maximum (two if absolutely needed for clarity)
- Must be a complete grammatical question
- Preserve all technical terms exactly (backtick-quoted identifiers, CLI flags, etc.)
- Don't add information not implied by the question + answer together
- Don't start every question with "How do you" — vary the phrasing
- Keep it concise; these are flashcards

Return ONLY a JSON array of objects with "index" and "q" fields. No other text.

Cards to rewrite:
{json.dumps(payload, ensure_ascii=False, indent=2)}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text)


# ── Load cards ────────────────────────────────────────────────────────────────
with open('frontend/cards.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

cards = data['decks'][DECK]['cards']

# ── Identify cryptic cards ───────────────────────────────────────────────────
targets = [(i, c) for i, c in enumerate(cards) if is_cryptic(c['q'])]
print(f"Found {len(targets)} cryptic questions to rewrite")

# ── Process in batches ───────────────────────────────────────────────────────
client = anthropic.Anthropic()
rewrites = {}

for batch_start in range(0, len(targets), BATCH_SIZE):
    batch = targets[batch_start:batch_start + BATCH_SIZE]
    batch_num = batch_start // BATCH_SIZE + 1
    total_batches = (len(targets) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Batch {batch_num}/{total_batches} ({len(batch)} cards)...", end=" ", flush=True)

    try:
        results = rewrite_batch(client, batch)
        for r in results:
            original_card_index = batch[r['index']][0]
            rewrites[original_card_index] = r['q']
        print(f"done ({len(results)} rewritten)")
    except Exception as e:
        print(f"ERROR: {e}")
        # On error, skip this batch and continue
        continue

# ── Apply rewrites ───────────────────────────────────────────────────────────
changed = 0
for card_index, new_q in rewrites.items():
    card = cards[card_index]
    if new_q and new_q != card['q']:
        card['q'] = new_q
        card['id'] = make_id(DECK, card['q'], card['a'])
        changed += 1

print(f"\nApplied {changed} rewrites")

# ── Write back ───────────────────────────────────────────────────────────────
with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

print("Done — cards.json updated.")
