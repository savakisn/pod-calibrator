import re
import httpx
from typing import Optional
from ..services.spellbook import estimate_bracket

MOXFIELD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

SUPERTYPES = {"basic", "legendary", "snow", "world"}
MOXFIELD_COLOR_MAP = {"W": "white", "U": "blue", "B": "black", "R": "red", "G": "green", "C": "colorless"}
ARCHIDEKT_COLOR_MAP = {"White": "white", "Blue": "blue", "Black": "black", "Red": "red", "Green": "green", "Colorless": "colorless"}


def _build_analysis(entries: list) -> dict:
    """
    entries: list of dicts with keys:
      name, qty, color_identity (list of lowercase color names),
      cmc, type_line, mana_cost, image_uris, is_commander
    """
    total_cards = sum(e["qty"] for e in entries)
    colors_count = {}
    type_count = {}
    mana_curve = {}
    total_cmc = 0.0
    card_count_processed = 0
    cards_data = []
    commander = None

    for e in entries:
        qty = e["qty"]
        name = e["name"]
        color_identity = e["color_identity"]
        cmc = e["cmc"] or 0
        type_line = e["type_line"] or ""

        card_out = {
            "name": name,
            "quantity": qty,
            "cmc": cmc,
            "color_identity": color_identity,
            "type_line": type_line,
            "mana_cost": e.get("mana_cost", ""),
            "image_uris": e.get("image_uris"),
        }
        cards_data.append(card_out)

        if e.get("is_commander"):
            commander = card_out

        total_cmc += cmc * qty
        card_count_processed += qty

        if color_identity:
            for color in color_identity:
                colors_count[color] = colors_count.get(color, 0) + qty
        else:
            colors_count["colorless"] = colors_count.get("colorless", 0) + qty

        is_land = "land" in type_line.lower()
        if not is_land:
            mana_val = str(int(cmc))
            mana_curve[mana_val] = mana_curve.get(mana_val, 0) + qty

        type_part = type_line.split("—")[0].split("(")[0].split("//")[0].strip()
        type_words = [w for w in type_part.split() if w.lower() not in SUPERTYPES]
        primary_type = type_words[0] if type_words else ""
        if primary_type:
            type_count[primary_type.lower()] = type_count.get(primary_type.lower(), 0) + qty

    avg_cmc = total_cmc / card_count_processed if card_count_processed > 0 else 0

    commander_names = [e["name"] for e in entries if e.get("is_commander")]
    main_names = [e["name"] for e in entries if not e.get("is_commander")]
    bracket_result = estimate_bracket(commander_names, main_names, avg_cmc)

    return {
        "cards": cards_data,
        "commander": commander,
        "card_count": total_cards,
        "avg_cmc": round(avg_cmc, 2),
        "colors": colors_count,
        "card_types": type_count,
        "mana_curve": mana_curve,
        "bracket": bracket_result,
        "precon_match": None,
    }


# --- Moxfield ---

def _extract_moxfield_id(url: str) -> Optional[str]:
    match = re.search(r"moxfield\.com/decks/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def _fetch_moxfield(deck_id: str) -> dict:
    with httpx.Client(timeout=15) as client:
        resp = client.get(
            f"https://api2.moxfield.com/v2/decks/all/{deck_id}",
            headers=MOXFIELD_HEADERS,
        )
        resp.raise_for_status()
        return resp.json()


def analyze_from_moxfield(url: str) -> dict:
    deck_id = _extract_moxfield_id(url)
    if not deck_id:
        raise ValueError("Invalid Moxfield URL")

    data = _fetch_moxfield(deck_id)
    commanders = data.get("commanders", {})
    mainboard = data.get("mainboard", {})
    commander_names = {e["card"]["name"] for e in commanders.values()}

    entries = []
    for entry in list(commanders.values()) + list(mainboard.values()):
        card = entry["card"]
        name = card["name"]
        color_identity = [MOXFIELD_COLOR_MAP.get(c, c.lower()) for c in (card.get("color_identity") or [])]
        type_line = card.get("type_line", "") or ""
        entries.append({
            "name": name,
            "qty": entry["quantity"],
            "color_identity": color_identity,
            "cmc": card.get("cmc", 0) or 0,
            "type_line": type_line,
            "mana_cost": card.get("mana_cost", ""),
            "image_uris": card.get("image_uris"),
            "is_commander": name in commander_names,
        })

    return _build_analysis(entries)


# --- Archidekt ---

def _extract_archidekt_id(url: str) -> Optional[str]:
    match = re.search(r"archidekt\.com/decks/(\d+)", url)
    return match.group(1) if match else None


def _fetch_archidekt(deck_id: str) -> dict:
    with httpx.Client(timeout=15) as client:
        resp = client.get(
            f"https://archidekt.com/api/decks/{deck_id}/",
            headers=MOXFIELD_HEADERS,
        )
        resp.raise_for_status()
        return resp.json()


def analyze_from_archidekt(url: str) -> dict:
    deck_id = _extract_archidekt_id(url)
    if not deck_id:
        raise ValueError("Invalid Archidekt URL")

    data = _fetch_archidekt(deck_id)
    entries = []

    for entry in data.get("cards", []):
        categories = entry.get("categories", [])
        oracle = entry["card"]["oracleCard"]
        name = oracle["name"]

        color_identity = [ARCHIDEKT_COLOR_MAP.get(c, c.lower()) for c in (oracle.get("colorIdentity") or [])]
        types = oracle.get("types", [])
        supertypes = oracle.get("superTypes", [])
        type_line = " ".join(supertypes + types)

        entries.append({
            "name": name,
            "qty": entry["quantity"],
            "color_identity": color_identity,
            "cmc": oracle.get("cmc", 0) or 0,
            "type_line": type_line,
            "mana_cost": oracle.get("manaCost", ""),
            "image_uris": None,
            "is_commander": "Commander" in categories,
        })

    return _build_analysis(entries)


# --- Generic dispatcher ---

def analyze_from_url(url: str) -> dict:
    if "moxfield.com" in url:
        return analyze_from_moxfield(url)
    if "archidekt.com" in url:
        return analyze_from_archidekt(url)
    raise ValueError("Unsupported site. Supported: Moxfield, Archidekt")
