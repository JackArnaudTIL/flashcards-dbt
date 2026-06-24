"""
Rewrites low-quality flashcard formats in cards.json.

Pass 1 (this script, no API key needed):
  - Strips "Scenario: " prefix from questions → natural question phrasing
  - Splits "Action: X | Error: Y" answers → clean answer + explanation field

Pass 2 (separate, requires ANTHROPIC_API_KEY):
  - Generates fuller explanations for cards still missing them
"""

import json
import re
import shutil
from pathlib import Path

CARDS_PATH = Path(__file__).parent.parent / "frontend" / "cards.json"
BACKUP_PATH = CARDS_PATH.with_suffix(".json.bak")


def clean_question(q: str) -> str:
    """Remove 'Scenario: ' prefix and tidy the question."""
    q = q.strip()
    if q.startswith("Scenario: "):
        q = q[len("Scenario: "):]
    # Ensure the question doesn't start with lowercase after stripping
    if q and q[0].islower():
        q = q[0].upper() + q[1:]
    return q


def split_action_error(a: str) -> tuple[str, str]:
    """
    Split 'Action: X | Error: Y' into (answer, error_context).
    Returns (original, "") if the pattern doesn't match.
    """
    a = a.strip()
    if not a.startswith("Action:"):
        return a, ""

    # Split on ' | Error:' (with possible whitespace)
    parts = re.split(r"\s*\|\s*Error:\s*", a, maxsplit=1)
    action = parts[0].replace("Action:", "", 1).strip()
    error = parts[1].strip() if len(parts) > 1 else ""
    return action, error


def build_explanation(question: str, answer: str, error: str) -> str:
    """Build a structured explanation from the action + error parts."""
    lines = []
    if error:
        lines.append(f"Common mistake: {error}")
    return "\n\n".join(lines) if lines else ""


def transform_card(card: dict) -> dict:
    q = card.get("q", "")
    a = card.get("a", "")

    if not q.startswith("Scenario:"):
        return card  # not a Scenario-format card, leave it alone

    new_q = clean_question(q)
    answer, error = split_action_error(a)
    explanation = build_explanation(new_q, answer, error)

    updated = dict(card)
    updated["q"] = new_q
    updated["a"] = answer

    # Only set explanation if the card doesn't already have one
    if explanation and not card.get("explanation"):
        updated["explanation"] = explanation

    return updated


def main():
    print(f"Reading {CARDS_PATH}")
    raw = CARDS_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)

    decks = data["decks"]
    total_transformed = 0

    for deck_name, deck in decks.items():
        if not isinstance(deck, dict) or "cards" not in deck:
            continue
        cards = deck["cards"]
        new_cards = []
        transformed = 0
        for card in cards:
            new_card = transform_card(card)
            if new_card is not card:
                transformed += 1
            new_cards.append(new_card)
        deck["cards"] = new_cards
        if transformed:
            print(f"  {deck_name}: transformed {transformed} cards")
            total_transformed += transformed

    print(f"\nTotal cards transformed: {total_transformed}")
    print(f"Writing backup → {BACKUP_PATH}")
    shutil.copy2(CARDS_PATH, BACKUP_PATH)

    print(f"Writing updated cards.json")
    CARDS_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("Done.")


if __name__ == "__main__":
    main()
