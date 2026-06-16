"""
One-time script to pre-generate code explanations for all requires_code cards.
Stores the explanation in each card as card['explanation'] in cards.json.

Usage:
    ANTHROPIC_API_KEY=sk-... python generate_explanations.py

Cards that already have a non-empty 'explanation' are skipped (safe to rerun).
"""

import json
import os
import re
import time

import anthropic

CARDS_PATH = "frontend/cards.json"
MODEL = "claude-haiku-4-5"

SYSTEM = (
    "You are a technical educator for a dbt/SQL flashcard app. "
    "Given a code snippet that is the correct answer to a flashcard question, "
    "write a concise explanation of how the code works. "
    "Break it down construct by construct — explain what each key part does "
    "and WHY it is written that way. "
    "Be specific to the language/tool (dbt, Jinja, YAML, SQL). "
    "Write 3-6 sentences in plain prose — no bullet points, no markdown headers. "
    "Do not repeat the question or say 'this code' — just explain directly."
)


def strip_code_fence(text: str) -> str:
    """Extract the code inside the first markdown code fence."""
    match = re.search(r"```[^\n]*\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def detect_language(answer: str) -> str:
    match = re.match(r"```(\w+)", answer.strip())
    return match.group(1) if match else "code"


def generate_explanation(client: anthropic.Anthropic, question: str, answer: str) -> str:
    language = detect_language(answer)
    code = strip_code_fence(answer)
    prompt = f"Question: {question}\n\nLanguage: {language}\n\nCode:\n```\n{code}\n```"
    msg = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY environment variable is not set.")

    client = anthropic.Anthropic(api_key=api_key)

    with open(CARDS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = 0
    skipped = 0
    generated = 0

    for deck_name, deck in data["decks"].items():
        for card in deck["cards"]:
            if not card.get("requires_code"):
                continue
            total += 1
            if card.get("explanation", "").strip():
                skipped += 1
                continue

            print(f"[{deck_name}] {card['q'][:70]}…", end=" ", flush=True)
            try:
                explanation = generate_explanation(client, card["q"], card["a"])
                card["explanation"] = explanation
                generated += 1
                print("done")
            except Exception as e:
                print(f"ERROR: {e}")
                card["explanation"] = ""

            # Avoid rate limits
            time.sleep(0.3)

    with open(CARDS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {total} code cards total | {skipped} already had explanations | {generated} newly generated.")


if __name__ == "__main__":
    main()
