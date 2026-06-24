"""
Assign a stable 8-character hex ID to every card based on SHA1 of (deck + question).
Including the deck name in the hash means identical questions in different decks
get different IDs. Collisions are checked and flagged.
"""
import json, hashlib

with open('frontend/cards.json', encoding='utf-8') as f:
    data = json.load(f)

seen = {}
collisions = 0
total = 0

for deck_name, deck in data['decks'].items():
    for card in deck['cards']:
        key = deck_name + '||' + card.get('q', '') + '||' + card.get('a', '')
        card_id = hashlib.sha1(key.encode('utf-8')).hexdigest()[:8]
        if card_id in seen:
            print(f'COLLISION: {card_id} used by "{seen[card_id]}" and "{card.get("q","")[:60]}"')
            collisions += 1
        seen[card_id] = card.get('q', '')[:60]
        card['id'] = card_id
        total += 1

print(f'Assigned IDs to {total} cards across {len(data["decks"])} decks')
print(f'Collisions: {collisions}')

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done.')
