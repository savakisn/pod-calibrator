import httpx
from ..services.deck_parser import parse_moxfield_decklist
from ..services.scryfall_client import fetch_card_sync, parse_card_data

def analyze_deck_sync(decklist: str) -> dict:
    cards_list, commander_name = parse_moxfield_decklist(decklist)

    total_cards = sum(qty for qty, _ in cards_list)

    cards_data = []
    commander = None
    colors_count = {}
    type_count = {}
    mana_curve = {}
    total_cmc = 0
    card_count_processed = 0

    for qty, card_name in cards_list:
        scryfall_data = fetch_card_sync(card_name)

        if scryfall_data:
            parsed = parse_card_data(scryfall_data)
            card = {
                "name": card_name,
                "quantity": qty,
                **parsed
            }
            cards_data.append(card)

            if card_name == commander_name:
                commander = card

            cmc = parsed.get("cmc") or 0
            total_cmc += cmc * qty
            card_count_processed += qty

            mana_val = int(cmc)
            mana_curve[str(mana_val)] = mana_curve.get(str(mana_val), 0) + qty

            for color in parsed.get("colors") or []:
                colors_count[color] = colors_count.get(color, 0) + qty

            type_line = parsed.get("type_line") or ""
            card_type_parts = type_line.split("(")[0].strip().split()
            for card_type in card_type_parts:
                card_type_clean = card_type.lower()
                type_count[card_type_clean] = type_count.get(card_type_clean, 0) + qty
        else:
            card = {"name": card_name, "quantity": qty}
            cards_data.append(card)

    avg_cmc = total_cmc / card_count_processed if card_count_processed > 0 else 0

    return {
        "cards": cards_data,
        "commander": commander,
        "card_count": total_cards,
        "avg_cmc": round(avg_cmc, 2),
        "colors": colors_count,
        "card_types": type_count,
        "mana_curve": mana_curve,
        "detected_combos": [],
        "bracket_score": None,
        "power_label": None,
        "precon_match": None,
        "win_conditions": [],
        "speed": None,
    }
