import httpx

SPELLBOOK_API = "https://backend.commanderspellbook.com"

BRACKET_TAG_MAP = {
    "E": {"base": 1, "label": "Exhibition"},
    "P": {"base": 3, "label": "Upgraded"},
    "R": {"base": 4, "label": "Optimized"},
}

BRACKET_LABELS = {1: "Exhibition", 2: "Core", 3: "Upgraded", 4: "Optimized", 5: "cEDH"}


def estimate_bracket(commander_names: list[str], main_names: list[str], avg_cmc: float) -> dict:
    payload = {
        "commanders": [{"card": name} for name in commander_names],
        "main": [{"card": name} for name in main_names],
    }

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.post(f"{SPELLBOOK_API}/estimate-bracket", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return {"error": str(e), "bracket": None}

    tag = data.get("bracketTag", "E")
    cards = data.get("cards", [])
    combos_raw = data.get("combos", [])

    game_changers = [c["card"]["name"] for c in cards if c.get("gameChanger")]
    mld = [c["card"]["name"] for c in cards if c.get("massLandDenial")]
    extra_turns = [c["card"]["name"] for c in cards if c.get("extraTurn")]
    has_combo = len(combos_raw) > 0

    # Map tag to bracket number
    base = BRACKET_TAG_MAP.get(tag, {}).get("base", 2)
    if tag == "E":
        bracket = 1 if avg_cmc >= 3.2 and not mld and not extra_turns else 2
    elif tag == "R" and has_combo and len(game_changers) >= 6:
        bracket = 5
    else:
        bracket = base

    combos = []
    for entry in combos_raw:
        combo = entry.get("combo", {})
        cards_used = [u["card"]["name"] for u in combo.get("uses", [])]
        produces = [p["feature"]["name"] for p in combo.get("produces", [])]
        combos.append({
            "cards": cards_used,
            "produces": produces,
            "description": combo.get("description", ""),
            "two_card": entry.get("definitelyTwoCard", False),
        })

    return {
        "bracket": bracket,
        "bracket_label": BRACKET_LABELS[bracket],
        "game_changer_count": len(game_changers),
        "game_changers_found": game_changers,
        "mass_land_denial": mld,
        "extra_turns": extra_turns,
        "combos": combos,
    }
