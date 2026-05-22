import re
from typing import List, Tuple

def parse_moxfield_decklist(decklist: str) -> Tuple[List[Tuple[int, str]], str]:
    """Parse Moxfield format. Returns (cards, commander)

    Format: quantity card name
    Examples:
        1x Urza, Lord High Artificer
        2 Lightning Bolt
    """
    cards = []
    commander = None

    lines = decklist.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"):
            continue

        match = re.match(r"^(\d+)[x\s]+(.+)$", line)
        if not match:
            continue

        quantity = int(match.group(1))
        card_name = match.group(2).strip()

        if not commander and quantity == 1:
            candidate = card_name
            cards.append((quantity, card_name))
            if len(cards) == 1:
                commander = candidate
        else:
            cards.append((quantity, card_name))

    return cards, commander

def extract_unique_cards(cards: List[Tuple[int, str]]) -> List[str]:
    """Get unique card names from card list."""
    seen = set()
    unique = []
    for qty, name in cards:
        if name not in seen:
            unique.append(name)
            seen.add(name)
    return unique
