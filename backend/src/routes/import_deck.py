import re
import httpx
from typing import Optional

MOXFIELD_API = "https://api2.moxfield.com/v2/decks/all"
MOXFIELD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def extract_moxfield_id(url: str) -> Optional[str]:
    match = re.search(r"moxfield\.com/decks/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def fetch_moxfield_deck(deck_id: str) -> dict:
    with httpx.Client(timeout=15) as client:
        resp = client.get(f"{MOXFIELD_API}/{deck_id}", headers=MOXFIELD_HEADERS)
        resp.raise_for_status()
        return resp.json()


def moxfield_to_decklist(data: dict) -> str:
    """Convert Moxfield API response to plain text decklist."""
    lines = []
    commanders = data.get("commanders", {})
    mainboard = data.get("mainboard", {})

    for entry in commanders.values():
        lines.append(f"{entry['quantity']} {entry['card']['name']}")
    for entry in mainboard.values():
        lines.append(f"{entry['quantity']} {entry['card']['name']}")

    return "\n".join(lines)


def analyze_from_moxfield(url: str) -> dict:
    deck_id = extract_moxfield_id(url)
    if not deck_id:
        raise ValueError("Invalid Moxfield URL")

    data = fetch_moxfield_deck(deck_id)

    # Build card list directly from Moxfield data (no Scryfall needed)
    from collections import Counter

    commanders = data.get("commanders", {})
    mainboard = data.get("mainboard", {})
    all_entries = list(commanders.values()) + list(mainboard.values())

    total_cards = sum(e["quantity"] for e in all_entries)
    colors_count = {}
    type_count = {}
    mana_curve = {}
    total_cmc = 0
    card_count_processed = 0
    cards_data = []
    commander = None

    color_map = {"W": "white", "U": "blue", "B": "black", "R": "red", "G": "green", "C": "colorless"}
    supertypes = {"basic", "legendary", "snow", "world"}

    commander_names = {e["card"]["name"] for e in commanders.values()}

    for entry in all_entries:
        qty = entry["quantity"]
        card = entry["card"]
        name = card["name"]

        color_identity = [color_map.get(c, c) for c in (card.get("color_identity") or [])]
        cmc = card.get("cmc", 0) or 0
        type_line = card.get("type_line", "") or ""
        mana_cost = card.get("mana_cost", "")
        image_uris = card.get("image_uris")

        cards_data.append({
            "name": name,
            "quantity": qty,
            "cmc": cmc,
            "color_identity": color_identity,
            "colors": [color_map.get(c, c) for c in (card.get("colors") or [])],
            "type_line": type_line,
            "mana_cost": mana_cost,
            "image_uris": image_uris,
        })

        if name in commander_names:
            commander = cards_data[-1]

        total_cmc += cmc * qty
        card_count_processed += qty

        if color_identity:
            for color in color_identity:
                colors_count[color] = colors_count.get(color, 0) + qty
        else:
            colors_count["colorless"] = colors_count.get("colorless", 0) + qty

        if "land" not in type_line.lower():
            mana_val = str(int(cmc))
            mana_curve[mana_val] = mana_curve.get(mana_val, 0) + qty

        type_part = type_line.split("—")[0].split("(")[0].split("//")[0].strip()
        type_words = [w for w in type_part.split() if w.lower() not in supertypes]
        primary_type = type_words[0] if type_words else ""
        if primary_type:
            type_count[primary_type.lower()] = type_count.get(primary_type.lower(), 0) + qty

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
