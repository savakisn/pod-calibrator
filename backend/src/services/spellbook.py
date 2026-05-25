import httpx

SPELLBOOK_API = "https://backend.commanderspellbook.com"
BRACKET_LABELS = {1: "Exhibition", 2: "Core", 3: "Upgraded", 4: "Optimized", 5: "cEDH"}


def _bracket_from_counts(gc_count: int, has_combo: bool, avg_cmc: float, has_mld: bool, has_et: bool) -> int:
    if gc_count == 0 and not has_combo:
        return 1 if (avg_cmc >= 3.2 and not has_mld and not has_et) else 2
    if gc_count <= 3:
        return 3
    if gc_count <= 6:
        return 4
    return 5


def _group_combos(combos_raw: list) -> list:
    """Group combos by what they produce. Each group shows all card combinations."""
    groups = {}
    for entry in combos_raw:
        combo = entry.get("combo", {})
        cards_used = sorted(u["card"]["name"] for u in combo.get("uses", []))
        produces = sorted(p["feature"]["name"] for p in combo.get("produces", []))
        key = tuple(produces)
        if key not in groups:
            groups[key] = {"produces": list(produces), "lines": []}
        groups[key]["lines"].append(cards_used)

    return [{"produces": g["produces"], "lines": g["lines"]} for g in groups.values()]


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

    cards = data.get("cards", [])
    combos_raw = data.get("combos", [])

    game_changers = [c["card"]["name"] for c in cards if c.get("gameChanger")]
    mld = [c["card"]["name"] for c in cards if c.get("massLandDenial")]
    extra_turns = [c["card"]["name"] for c in cards if c.get("extraTurn")]
    has_combo = len(combos_raw) > 0

    bracket = _bracket_from_counts(len(game_changers), has_combo, avg_cmc, bool(mld), bool(extra_turns))
    combos = _group_combos(combos_raw)

    return {
        "bracket": bracket,
        "bracket_label": BRACKET_LABELS[bracket],
        "game_changer_count": len(game_changers),
        "game_changers_found": game_changers,
        "mass_land_denial": mld,
        "extra_turns": extra_turns,
        "combos": combos,
    }
