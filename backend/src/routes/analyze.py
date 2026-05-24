import httpx
from ..services.deck_parser import parse_moxfield_decklist
from ..services.scryfall_client import fetch_cards_batch, fetch_card_sync, parse_card_data

def analyze_deck_sync(decklist: str) -> dict:
    cards_list, commander_name = parse_moxfield_decklist(decklist)

    total_cards = sum(qty for qty, _ in cards_list)

    # Fetch all cards in batches from Scryfall (max 75 per request)
    card_names = [name for _, name in cards_list]
    scryfall_results = fetch_cards_batch(card_names)

    cards_data = []
    commander = None
    colors_count = {}
    type_count = {}
    mana_curve = {}
    total_cmc = 0
    card_count_processed = 0

    for (qty, card_name), scryfall_data in zip(cards_list, scryfall_results):
        # Fallback to fuzzy matching for Secret Lair variants and other special names
        if not scryfall_data:
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

            type_line = parsed.get("type_line") or ""
            if type_line and "land" not in type_line.lower():
                mana_val = int(cmc)
                mana_curve[str(mana_val)] = mana_curve.get(str(mana_val), 0) + qty

            colors = parsed.get("colors") or []
            color_identity = parsed.get("color_identity") or []
            has_color = False

            # Use color_identity for lands (includes non-basic lands like Oran-Rief)
            if "land" in type_line.lower():
                for color in color_identity:
                    colors_count[color] = colors_count.get(color, 0) + qty
                    has_color = True
            else:
                # For non-lands, use mana cost colors
                for color in colors:
                    colors_count[color] = colors_count.get(color, 0) + qty
                    has_color = True

            # Fallback for basic lands without color_identity (shouldn't happen, but safe)
            if "basic land" in type_line.lower() and not has_color:
                land_color_map = {
                    "mountain": "red",
                    "forest": "green",
                    "island": "blue",
                    "swamp": "black",
                    "plains": "white",
                }
                land_subtype = type_line.split("—")[-1].strip().split()[0].lower() if "—" in type_line else ""
                color = land_color_map.get(land_subtype)
                if color:
                    colors_count[color] = colors_count.get(color, 0) + qty
                    has_color = True

            # Cards with no color contribution should be counted as colorless
            if not has_color:
                colors_count["colorless"] = colors_count.get("colorless", 0) + qty

            supertypes = {"basic", "legendary", "snow", "world"}
            type_part = type_line.split("—")[0].split("(")[0].split("//")[0].strip()
            type_words = [w for w in type_part.split() if w.lower() not in supertypes]
            primary_type = type_words[0] if type_words else ""
            if primary_type:
                type_count[primary_type.lower()] = type_count.get(primary_type.lower(), 0) + qty
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
