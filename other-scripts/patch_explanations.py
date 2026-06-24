"""
Reads all results_NNN.json files from explanation_batches/ and patches
them into frontend/cards.json. Run this after all explanation agents finish.
"""

import json
import shutil
from pathlib import Path

CARDS_PATH = Path(__file__).parent.parent / "frontend" / "cards.json"
BACKUP_PATH = CARDS_PATH.with_suffix(".json.bak")
BATCH_DIR = Path(__file__).parent / "explanation_batches"


def load_all_results() -> dict[str, str]:
    results = {}
    result_files = sorted(BATCH_DIR.glob("results_*.json"))
    if not result_files:
        print("No results files found. Run agents first.")
        return results
    for f in result_files:
        data = json.loads(f.read_text(encoding="utf-8"))
        results.update(data)
    print(f"Loaded {len(results)} explanations from {len(result_files)} result files")
    return results


def main():
    explanations = load_all_results()
    if not explanations:
        return

    print(f"Reading {CARDS_PATH}")
    raw = CARDS_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)

    patched = 0
    skipped_already_has = 0

    for deck in data["decks"].values():
        if not isinstance(deck, dict) or "cards" not in deck:
            continue
        for card in deck["cards"]:
            card_id = card.get("id")
            if card_id in explanations:
                if card.get("explanation"):
                    skipped_already_has += 1
                else:
                    card["explanation"] = explanations[card_id]
                    patched += 1

    print(f"Patched: {patched} cards")
    print(f"Skipped (already had explanation): {skipped_already_has}")
    print(f"Writing backup -> {BACKUP_PATH}")
    shutil.copy2(CARDS_PATH, BACKUP_PATH)
    CARDS_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("Done.")


if __name__ == "__main__":
    main()
