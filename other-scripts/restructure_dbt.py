"""
Two structural changes to the dbt deck:
1. dbt SQL Basics — assign meaningful sub-categories to all 50 cards
2. Exam Prep — split into 3 thematic cert-prep modules
"""
import json

with open('frontend/cards.json', encoding='utf-8') as f:
    data = json.load(f)

dbt = data['decks']['dbt']
cards = dbt['cards']

# ── 1. dbt SQL Basics — categorise by question keyword ───────────────────────
# Maps a keyword fragment (found in the question text) to the new category.
# Ordered so the first match wins.
SQL_RULES = [
    # SQL & CTEs
    ('Write a basic `SELECT` statement',                     'SQL & CTEs'),
    ('pulls the `id` and `amount`',                         'SQL & CTEs'),
    ('standard CTE wrapper',                                'SQL & CTEs'),
    ('self-referential variable',                           'SQL & CTEs'),

    # dbt Utils
    ('dbt_utils.star',                                      'dbt Utils'),
    ('dbt_utils.generate_surrogate_key',                    'dbt Utils'),
    ('dbt_utils.pivot',                                     'dbt Utils'),
    ('dbt_utils.union_relations',                           'dbt Utils'),

    # Macros
    ('basic structure to define a macro',                   'Macros'),
    ('Call a macro',                                        'Macros'),
    ('return a specific Python object',                     'Macros'),
    ('custom generic test macro',                           'Macros'),

    # dbt Variables & Context
    ('global dbt project variable',                        'Variables & Context'),
    ('providing a default value',                          'Variables & Context'),
    ('timestamp when the current dbt invocation started',  'Variables & Context'),
    ('unique UUID for the current dbt run',                'Variables & Context'),

    # Adapters & Execution
    ('print `\'Hello World\'` to the dbt terminal logs',   'Adapters & Execution'),
    ('target environment name',                            'Adapters & Execution'),
    ('adapter type',                                       'Adapters & Execution'),
    ('run_query',                                          'Adapters & Execution'),
    ('only runs during the execution phase',               'Adapters & Execution'),
    ('correctly quote the reserved keyword',               'Adapters & Execution'),
    ('fetch a list of column objects',                     'Adapters & Execution'),

    # Materializations & Config  (broad — runs after more specific rules)
    ('materialize a model',                                'Materializations & Config'),
    ('alias',                                              'Materializations & Config'),
    ('custom schema',                                      'Materializations & Config'),
    ('tags',                                               'Materializations & Config'),
    ('ephemeral',                                          'Materializations & Config'),
    ('unique_key',                                         'Materializations & Config'),
    ('filter for new rows in an incremental model',        'Materializations & Config'),
    ('append` strategy',                                   'Materializations & Config'),
    ('snapshot block',                                     'Materializations & Config'),
    ('post_hook',                                          'Materializations & Config'),
    ('pre_hook',                                           'Materializations & Config'),
    ('store the failing rows',                             'Materializations & Config'),

    # Jinja Fundamentals (broad — runs last within this group)
    ('environment variable',                               'Jinja Fundamentals'),
    ('comment that will',                                  'Jinja Fundamentals'),
    ('Jinja variable',                                     'Jinja Fundamentals'),
    ('`for` loop',                                        'Jinja Fundamentals'),
    ('whitespace control',                                 'Jinja Fundamentals'),
    ('Jinja list',                                        'Jinja Fundamentals'),
    ('Jinja dictionary',                                   'Jinja Fundamentals'),
    ('Jinja filter',                                      'Jinja Fundamentals'),
    ('join a list',                                       'Jinja Fundamentals'),
    ('add a comma',                                        'Jinja Fundamentals'),
    ('1-based index',                                      'Jinja Fundamentals'),
    ('length (count of items)',                            'Jinja Fundamentals'),
]

changed_sql = 0
for card in cards:
    if card.get('module') != 'dbt SQL Basics':
        continue
    q = card.get('q', '')
    for fragment, cat in SQL_RULES:
        if fragment in q:
            card['category'] = cat
            card['group'] = cat
            changed_sql += 1
            break
    else:
        print(f'  UNMATCHED: {q[:80]}')

print(f'dbt SQL Basics: categorised {changed_sql} cards')

# ── 2. Exam Prep → 3 thematic modules ────────────────────────────────────────
CERT_MODULE_MAP = {
    'Domain 1: Developing dbt Models':   'Developer Cert: Modeling & Testing',
    'Domain 3: Implementing dbt Tests':  'Developer Cert: Modeling & Testing',
    'Domain 4: Managing Data Pipelines': 'Developer Cert: Modeling & Testing',
    'Domain 2: Data Governance & Metadata':    'Developer Cert: Governance & Debugging',
    'Domain 5: Debugging & Troubleshooting':   'Developer Cert: Governance & Debugging',
    'Domain 6: Jinja & Macros':          'Developer Cert: Jinja & Cloud',
    'Domain 7: dbt Cloud & Deployment':  'Developer Cert: Jinja & Cloud',
    'Domain 8: Semantic Layer':          'Developer Cert: Jinja & Cloud',
}

changed_ep = 0
for card in cards:
    if card.get('module') != 'Exam Prep':
        continue
    cat = card.get('category', '')
    new_mod = CERT_MODULE_MAP.get(cat)
    if new_mod:
        card['module'] = new_mod
        changed_ep += 1
    else:
        print(f'  UNMAPPED Exam Prep category: {cat!r}')

print(f'Exam Prep: reassigned {changed_ep} cards to 3 modules')

# Update modules_ordered — replace 'Exam Prep' with the 3 new modules
old_mods = dbt['modules_ordered']
new_mods = []
for m in old_mods:
    if m == 'Exam Prep':
        new_mods += [
            'Developer Cert: Modeling & Testing',
            'Developer Cert: Governance & Debugging',
            'Developer Cert: Jinja & Cloud',
        ]
    else:
        new_mods.append(m)
dbt['modules_ordered'] = new_mods
print(f'modules_ordered: {new_mods}')

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done.')
