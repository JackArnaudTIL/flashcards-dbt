import json
import hashlib
import re

def make_id(deck_name, q, a):
    key = deck_name + '||' + q + '||' + a
    return hashlib.sha1(key.encode('utf-8')).hexdigest()[:8]

def reformat_answer(answer):
    """
    Convert 'Action: X | Error: Y' to clean markdown.
    Handles cases where the action or error themselves contain pipes.
    """
    if 'Action:' not in answer or '| Error:' not in answer:
        return answer

    # Split on the literal '| Error:' separator
    idx = answer.find('| Error:')
    if idx == -1:
        return answer

    action = answer[:idx].replace('Action:', '', 1).strip().rstrip('|').strip()
    error  = answer[idx:].replace('| Error:', '', 1).strip()

    # Clean up trailing periods before appending watch-out
    action = action.rstrip('.')

    # Backtick-wrap obvious code tokens (single-quoted identifiers and CLI commands)
    def backtick_single_quotes(text):
        return re.sub(r"'([^']+)'", r'`\1`', text)

    action = backtick_single_quotes(action)
    error  = backtick_single_quotes(error)

    return f"{action}\n\n**Watch out:** {error}"


def clean_question(question):
    """Remove 'Scenario: ' prefix and expand common abbreviations."""
    q = question
    if q.startswith('Scenario: '):
        q = q[len('Scenario: '):]
    return q


with open('frontend/cards.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

deck_name = 'dbt'
cards = data['decks'][deck_name]['cards']

fixed_q   = 0
fixed_a   = 0
fixed_ids = 0

seen_questions = {}   # for dedup reporting only

for card in cards:
    orig_q = card['q']
    orig_a = card['a']

    new_q = clean_question(orig_q)
    new_a = reformat_answer(orig_a)

    changed = False
    if new_q != orig_q:
        card['q'] = new_q
        fixed_q += 1
        changed = True
    if new_a != orig_a:
        card['a'] = new_a
        fixed_a += 1
        changed = True
    if changed:
        card['id'] = make_id(deck_name, card['q'], card['a'])
        fixed_ids += 1

    # Track duplicates for reporting
    key = card['q'].strip().lower()
    seen_questions.setdefault(key, []).append(card['id'])

dupes = {k: v for k, v in seen_questions.items() if len(v) > 1}

print(f"Questions cleaned : {fixed_q}")
print(f"Answers reformatted: {fixed_a}")
print(f"IDs regenerated   : {fixed_ids}")
print(f"Duplicate questions: {len(dupes)}")
if dupes:
    print("  Examples:")
    for k, ids in list(dupes.items())[:5]:
        print(f"    '{k[:80]}' ({len(ids)} copies)")

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

print("\nDone — cards.json updated.")
