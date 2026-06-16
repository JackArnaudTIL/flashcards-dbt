"""
Merge all dbt-* decks into a single "dbt" deck.
Each card gains a `module` field (the old deck name).
The deck gains `modules_ordered` for UI chip ordering.
"""
import json
import copy

with open('frontend/cards.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Old deck name → module label (display name in UI chips)
MODULE_MAP = {
    "dbt 101":        "dbt 101",
    "dbt 102":        "dbt 102",
    "dbt SQL Basics": "dbt SQL Basics",
    "dbt":            "Exam Prep",      # the original big exam prep deck
    "dbt Architect":  "dbt Architect",
    "dbt Modeling":   "dbt Modeling",
}

MODULES_ORDERED = [
    "dbt 101",
    "dbt 102",
    "dbt SQL Basics",
    "dbt Modeling",
    "Exam Prep",
    "dbt Architect",
]

merged_cards = []

for deck_name, module_label in MODULE_MAP.items():
    if deck_name not in data['decks']:
        print(f"  WARNING: deck '{deck_name}' not found, skipping")
        continue
    deck_cards = data['decks'][deck_name]['cards']
    for card in deck_cards:
        c = copy.deepcopy(card)
        c['module'] = module_label
        merged_cards.append(c)
    print(f"  {len(deck_cards):4}  {deck_name}  ->  module: '{module_label}'")

# Remove the old individual dbt decks
for dk in list(MODULE_MAP.keys()):
    if dk in data['decks']:
        del data['decks'][dk]

# Insert the merged deck at the same position as the old "dbt" entry would have been
# (just append to Professional Development section — order is preserved by dict insertion)
data['decks']['dbt'] = {
    "section": "Professional Development",
    "modules_ordered": MODULES_ORDERED,
    "cards": merged_cards,
}

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Summary
total = sum(len(d['cards']) for d in data['decks'].values())
code  = sum(1 for d in data['decks'].values() for c in d['cards'] if c.get('requires_code'))
print(f"\nMerged dbt deck: {len(merged_cards)} cards")
print(f"Grand total across all decks: {total} cards ({code} code cards)")
print(f"\nDecks remaining: {list(data['decks'].keys())}")
