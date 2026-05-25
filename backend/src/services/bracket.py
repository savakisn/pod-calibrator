GAME_CHANGERS = {
    "Ad Nauseam",
    "Ancient Tomb",
    "Aura Shards",
    "Biorhythm",
    "Bolas's Citadel",
    "Braids, Cabal Minion",
    "Chrome Mox",
    "Coalition Victory",
    "Consecrated Sphinx",
    "Crop Rotation",
    "Cyclonic Rift",
    "Demonic Tutor",
    "Drannith Magistrate",
    "Enlightened Tutor",
    "Farewell",
    "Field of the Dead",
    "Fierce Guardianship",
    "Force of Will",
    "Gaea's Cradle",
    "Gamble",
    "Gifts Ungiven",
    "Glacial Chasm",
    "Grand Arbiter Augustin IV",
    "Grim Monolith",
    "Humility",
    "Imperial Seal",
    "Intuition",
    "Jeska's Will",
    "Lion's Eye Diamond",
    "Mana Vault",
    "Mishra's Workshop",
    "Mox Diamond",
    "Mystical Tutor",
    "Narset, Parter of Veils",
    "Natural Order",
    "Necropotence",
    "Notion Thief",
    "Opposition Agent",
    "Orcish Bowmasters",
    "Panoptic Mirror",
    "Rhystic Study",
    "Seedborn Muse",
    "Serra's Sanctum",
    "Smothering Tithe",
    "Survival of the Fittest",
    "Teferi's Protection",
    "Tergrid, God of Fright // Tergrid's Lantern",
    "Tergrid, God of Fright",
    "Thassa's Oracle",
    "The One Ring",
    "The Tabernacle at Pendrell Vale",
    "Underworld Breach",
    "Vampiric Tutor",
    "Worldly Tutor",
}

MASS_LAND_DENIAL = {
    "Armageddon",
    "Ravages of War",
    "Catastrophe",
    "Jokulhaups",
    "Obliterate",
    "Decree of Annihilation",
    "Wildfire",
    "Sunder",
    "Ruination",
    "Land Equilibrium",
    "Mana Vortex",
    "Boom // Bust",
}

EXTRA_TURNS = {
    "Time Warp",
    "Temporal Manipulation",
    "Capture of Jingzhou",
    "Temporal Trespass",
    "Nexus of Fate",
    "Savor the Moment",
    "Expropriate",
    "Part the Waterveil",
    "Walk the Aeons",
    "Karn's Temporal Sundering",
    "Alrund's Epiphany",
    "Beacon of Tomorrows",
    "Medomai the Ageless",
    "Magistrate's Scepter",
}

BRACKET_LABELS = {
    1: "Exhibition",
    2: "Core",
    3: "Upgraded",
    4: "Optimized",
    5: "cEDH",
}


def score_bracket(cards: list, avg_cmc: float) -> dict:
    """
    cards: list of {name, quantity, ...} dicts from _build_analysis
    Returns bracket score and breakdown.
    """
    game_changers_found = []
    mld_found = []
    extra_turns_found = []

    for card in cards:
        name = card["name"]
        qty = card.get("quantity", 1)

        if name in GAME_CHANGERS:
            game_changers_found.append(name)
        if name in MASS_LAND_DENIAL:
            mld_found.append(name)
        if name in EXTRA_TURNS:
            extra_turns_found.append(name)

    gc_count = len(game_changers_found)
    has_mld = len(mld_found) > 0
    has_extra_turns = len(extra_turns_found) > 0

    if gc_count == 0:
        # Distinguish precon-ish (1) from upgraded-casual (2)
        # High avg CMC + no MLD/ET = closer to precon
        if not has_mld and not has_extra_turns and avg_cmc >= 3.2:
            bracket = 1
        else:
            bracket = 2
    elif gc_count <= 3:
        bracket = 3
    elif gc_count <= 7:
        bracket = 4
    else:
        bracket = 5

    return {
        "bracket": bracket,
        "bracket_label": BRACKET_LABELS[bracket],
        "game_changer_count": gc_count,
        "game_changers_found": game_changers_found,
        "mass_land_denial": mld_found,
        "extra_turns": extra_turns_found,
    }
