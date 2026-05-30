import re
import httpx
import threading
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Optional

_CACHE_TTL = timedelta(hours=4)
_CACHE_MAX = 500
_cache: "OrderedDict[str, dict]" = OrderedDict()
_cache_lock = threading.Lock()

def _cache_get(key: str):
    with _cache_lock:
        entry = _cache.get(key)
        if not entry:
            return None
        if datetime.now() >= entry['exp']:
            _cache.pop(key, None)
            return None
        _cache.move_to_end(key)
        return entry['data']

def _cache_set(key: str, data: dict):
    with _cache_lock:
        _cache[key] = {'data': data, 'exp': datetime.now() + _CACHE_TTL}
        _cache.move_to_end(key)
        while len(_cache) > _CACHE_MAX:
            _cache.popitem(last=False)
from ..services.spellbook import estimate_bracket
from ..services.speed import analyze_speed
from ..services.wincon import detect_win_conditions
from ..services.interaction import analyze_interaction


class DeckImportError(Exception):
    """Deck-import failure with a user-friendly message and HTTP status."""
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.status_code = status_code


def _wrap_http_error(e: httpx.HTTPStatusError, source: str) -> DeckImportError:
    code = e.response.status_code
    if code == 404:
        return DeckImportError(f"Deck not found on {source}.", status_code=404)
    if code in (401, 403):
        return DeckImportError(f"Deck is private on {source}.", status_code=403)
    return DeckImportError(f"{source} returned an error ({code}). Try again shortly.", status_code=502)


def _wrap_transport_error(source: str) -> DeckImportError:
    return DeckImportError(f"{source} is not responding. Try again in a moment.", status_code=504)

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
    total_nonland_cmc = 0.0
    card_count_processed = 0
    nonland_count = 0
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
            total_nonland_cmc += cmc * qty
            nonland_count += qty
            mana_val = str(int(cmc))
            mana_curve[mana_val] = mana_curve.get(mana_val, 0) + qty

        type_part = type_line.split("—")[0].split("(")[0].split("//")[0].strip()
        type_words = [w for w in type_part.split() if w.lower() not in SUPERTYPES]
        primary_type = type_words[0] if type_words else ""
        if primary_type:
            type_count[primary_type.lower()] = type_count.get(primary_type.lower(), 0) + qty

    avg_cmc = total_cmc / card_count_processed if card_count_processed > 0 else 0
    avg_nonland_cmc = total_nonland_cmc / nonland_count if nonland_count > 0 else 0

    commander_names = [e["name"] for e in entries if e.get("is_commander")]
    main_names = [e["name"] for e in entries if not e.get("is_commander")]
    bracket_result = estimate_bracket(commander_names, main_names, avg_cmc)
    speed_result = analyze_speed(cards_data, avg_nonland_cmc)
    cmd_name = next((e["name"] for e in entries if e.get("is_commander")), None)
    win_conditions, wincon_diag = detect_win_conditions(cards_data, type_count, bracket_result.get("combos", []), cmd_name)
    interaction = analyze_interaction(cards_data)

    diagnostics = {
        "interaction": {
            "removal": interaction.get("removal_cards", []),
            "board_wipes": interaction.get("board_wipe_cards", []),
            "counterspells": interaction.get("counterspell_cards", []),
            "tutors": interaction.get("tutor_cards", []),
        },
        "wincons": wincon_diag,
    }

    return {
        "cards": cards_data,
        "commander": commander,
        "card_count": total_cards,
        "avg_cmc": round(avg_cmc, 2),
        "colors": colors_count,
        "card_types": type_count,
        "mana_curve": mana_curve,
        "bracket": bracket_result,
        "speed": speed_result,
        "win_conditions": win_conditions,
        "interaction": interaction,
        "precon_match": None,
        "_diagnostics": diagnostics,
    }


# --- Moxfield ---

def _extract_moxfield_id(url: str) -> Optional[str]:
    match = re.search(r"moxfield\.com/decks/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def _fetch_moxfield(deck_id: str) -> dict:
    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(
                f"https://api2.moxfield.com/v2/decks/all/{deck_id}",
                headers=MOXFIELD_HEADERS,
            )
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise _wrap_http_error(e, "Moxfield") from e
    except (httpx.TimeoutException, httpx.TransportError):
        raise _wrap_transport_error("Moxfield")


def analyze_from_moxfield(url: str) -> dict:
    deck_id = _extract_moxfield_id(url)
    if not deck_id:
        raise DeckImportError("That doesn't look like a Moxfield deck URL.", status_code=400)

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
    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(
                f"https://archidekt.com/api/decks/{deck_id}/",
                headers=MOXFIELD_HEADERS,
            )
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise _wrap_http_error(e, "Archidekt") from e
    except (httpx.TimeoutException, httpx.TransportError):
        raise _wrap_transport_error("Archidekt")


def analyze_from_archidekt(url: str) -> dict:
    deck_id = _extract_archidekt_id(url)
    if not deck_id:
        raise DeckImportError("That doesn't look like an Archidekt deck URL.", status_code=400)

    data = _fetch_archidekt(deck_id)
    entries = []
    excluded_keywords = ("sideboard", "maybeboard", "considering", "token", "extras", "reference", "cuts")

    for entry in data.get("cards", []):
        categories = entry.get("categories", [])
        if any(any(kw in c.lower() for kw in excluded_keywords) for c in categories):
            continue
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

def analyze_from_url(url: str) -> tuple[dict, bool]:
    """Returns (analysis, cache_hit)."""
    cached = _cache_get(url)
    if cached is not None:
        return cached, True
    if "moxfield.com" in url:
        result = analyze_from_moxfield(url)
    elif "archidekt.com" in url:
        result = analyze_from_archidekt(url)
    else:
        raise DeckImportError("Unsupported site. Use Moxfield or Archidekt.", status_code=400)
    _cache_set(url, result)
    return result, False
