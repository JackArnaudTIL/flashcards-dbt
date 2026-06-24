import json

with open('frontend/cards.json', encoding='utf-8') as f:
    data = json.load(f)

# Perched bird in profile: head, open beak, body, wing fold, legs and feet
bird_svg = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"'
    ' stroke-linecap="round" stroke-linejoin="round">'
    # Head
    '<circle cx="16" cy="8" r="2.5"/>'
    # Beak — upper and lower bill meeting at tip (22, 7.5)
    '<path d="M18.5 6.5L22 7.5"/>'
    '<path d="M18.5 9L22 7.5"/>'
    # Body — back sweeps left and down, belly curves back right to chest
    '<path d="M13.5 6C10 5 6 6 4 8L2 11v3c2 1 6 1 9 0 2-1 2.5-2.5 2.5-4"/>'
    # Wing fold line
    '<path d="M9 12c1-2 3-3.5 5-4.5"/>'
    # Legs
    '<path d="M8 14v4M11 14v4"/>'
    # Feet
    '<path d="M6 18h4M9 18h4"/>'
    '</svg>'
)

data['decks']['Birds of the World']['icon'] = bird_svg

with open('frontend/cards.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done')
