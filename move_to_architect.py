"""
Two moves:
1. All Domain 8 (Semantic Layer) cards → dbt Architect
2. 17 Mesh-specific Domain 2 cards → dbt Architect
"""
import json

with open('frontend/cards.json', encoding='utf-8') as f:
    data = json.load(f)

dbt = data['decks']['dbt']
cards = dbt['cards']

# ── 1. Domain 8: Semantic Layer → dbt Architect ───────────────────────────────
moved_sl = 0
for card in cards:
    if card.get('module') == 'Developer Cert: Jinja & Cloud' \
       and card.get('category') == 'Domain 8: Semantic Layer':
        card['module'] = 'dbt Architect'
        card['category'] = 'Semantic Layer'
        if card.get('group') == 'Domain 8: Semantic Layer':
            card['group'] = 'Semantic Layer'
        moved_sl += 1

print(f'Semantic Layer: moved {moved_sl} cards to dbt Architect')

# ── 2. Mesh-specific Domain 2 cards → dbt Architect ──────────────────────────
MESH_FRAGMENTS = [
    'Producer in a dbt Mesh setup',
    "Finance' project needs to use the 'Orders' project",
    "Consumer is slow. You realize they are querying a View",
    'prevent any project from referencing your',
    'Consumer build fails because your Producer model changed',
    'two projects: Sales and Inventory',
    "primary role of the 'Architect' in a dbt Mesh",
    'A team is using your public model. You delete the model',
    "Consumer' project referencing a 'Producer' project. Both use Snowflake",
    "Status' of models across 5 different projects",
    "Consumer project is building. It needs the Producer's manifest",
    "designing a Mesh. Where should 'Common Macros' live",
    "producer model has 'enforced: true' for its contract",
    "Cross-Project Lineage' in your local IDE",
    "Cross-project' consumers. Possible in dbt Core",
    "Project Health' across the entire Mesh",
    "Consumer' projects stay updated",
]

moved_mesh = 0
for card in cards:
    if card.get('module') != 'Developer Cert: Governance & Debugging':
        continue
    if card.get('category') != 'Domain 2: Data Governance & Metadata':
        continue
    q = card.get('q', '')
    for fragment in MESH_FRAGMENTS:
        if fragment in q:
            card['module'] = 'dbt Architect'
            card['category'] = 'dbt Mesh & Multi-Project'
            if card.get('group') == 'Domain 2: Data Governance & Metadata':
                card['group'] = 'dbt Mesh & Multi-Project'
            moved_mesh += 1
            break

print(f'Domain 2 Mesh cards: moved {moved_mesh} cards to dbt Architect')

# ── Verify final counts ───────────────────────────────────────────────────────
mods = {}
for c in cards:
    m = c.get('module', '(none)')
    mods[m] = mods.get(m, 0) + 1

print('\nFinal module counts:')
for m, n in sorted(mods.items()):
    print(f'  {n:4d}  {m}')

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('\nDone.')
