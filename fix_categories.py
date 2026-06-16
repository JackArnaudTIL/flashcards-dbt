"""
Quick-win category renames:
1. dbt 102: "Code → X" → clean topic names; also fixes list-typed group fields
2. Data Engineering Concepts: strip "Section N: " prefix from all categories
"""
import json, re

with open('frontend/cards.json', encoding='utf-8') as f:
    data = json.load(f)

# ── 1. dbt 102 ────────────────────────────────────────────────────────────────
DBT102_MAP = {
    'Code – Config':       'Configuration',
    'Code – Incremental':  'Incremental Models',
    'Code – Jinja':        'Jinja',
    'Code – Macros':       'Macros',
    'Code – Models':       'Models',
    'Code – Snapshots':    'Snapshots',
    'Code – YAML':         'YAML',
}

renamed_dbt = 0
for card in data['decks']['dbt']['cards']:
    if card.get('module') != 'dbt 102':
        continue
    old_cat = card.get('category', '')
    if old_cat in DBT102_MAP:
        new_cat = DBT102_MAP[old_cat]
        card['category'] = new_cat
        # group may be a list or a string
        grp = card.get('group')
        if isinstance(grp, list):
            card['group'] = [DBT102_MAP.get(g, g) for g in grp]
        elif isinstance(grp, str) and grp in DBT102_MAP:
            card['group'] = new_cat
        renamed_dbt += 1

print(f'dbt 102: renamed {renamed_dbt} cards')

# ── 2. Data Engineering Concepts ─────────────────────────────────────────────
section_prefix = re.compile(r'^Section \d+:\s*')

renamed_de = 0
for card in data['decks']['Data Engineering Concepts']['cards']:
    cat = card.get('category', '')
    new_cat = section_prefix.sub('', cat)
    if new_cat != cat:
        card['category'] = new_cat
        # group mirrors category on these cards if set
        if card.get('group') == cat:
            card['group'] = new_cat
        renamed_de += 1

print(f'Data Engineering: renamed {renamed_de} cards')

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done. cards.json updated.')
