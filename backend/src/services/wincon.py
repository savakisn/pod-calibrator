STAX = {
    "Winter Orb", "Static Orb", "Smokestack", "Tangle Wire",
    "Sphere of Resistance", "Trinisphere", "Damping Sphere",
    "Thalia, Guardian of Thraben", "Thalia, Heretic Cathar",
    "Hokori, Dust Drinker", "Eidolon of Rhetoric", "Rule of Law",
    "Archon of Emeria", "Collector Ouphe", "Null Rod",
    "Cursed Totem", "Suppression Field", "Pendrell Mists",
    "Ghostly Prison", "Propaganda", "Sphere of Safety",
    "Meekstone", "Ensnaring Bridge", "Humility",
}

ARISTOCRATS = {
    "Blood Artist", "Zulaport Cutthroat", "Falkenrath Noble",
    "Vindictive Vampire", "Poison-Tip Archer", "Bastion of Remembrance",
    "Cruel Celebrant", "Mayhem Devil",
    "Dictate of Erebos", "Grave Pact", "Butcher of Malakir",
    "Ashnod's Altar", "Phyrexian Altar", "Altar of Dementia",
    "Viscera Seer", "Carrion Feeder", "Goblin Bombardment",
    "Skullclamp", "Pitiless Plunderer", "Pawn of Ulamog",
    "Sifter of Skulls", "Midnight Reaper", "Dark Prophecy",
    "Grim Haruspex", "Erebos's Titan",
}

REANIMATOR = {
    "Animate Dead", "Reanimate", "Necromancy", "Dance of the Dead",
    "Exhume", "Entomb", "Buried Alive", "Unearth",
    "Dread Return", "Victimize", "Living Death", "Living End",
    "Zombify", "Persist", "Rescue from the Underworld",
    "Apprentice Necromancer", "Goryo's Vengeance",
    "Corpse Dance", "Sheoldred, Whispering One",
}

VOLTRON = {
    "Lightning Greaves", "Swiftfoot Boots", "Hammer of Nazahn",
    "Colossus Hammer", "Embercleave", "Umezawa's Jitte",
    "Batterskull", "Loxodon Warhammer", "Blackblade Reforged",
    "Sunforger", "Champion's Helm", "Commander's Plate",
    "Darksteel Plate", "Bloodforged Battle-Axe",
    "Sword of Fire and Ice", "Sword of Feast and Famine",
    "Sword of Light and Shadow", "Sword of War and Peace",
    "Sword of Body and Mind", "Sword of Sinew and Steel",
    "Sword of Truth and Justice", "Sword of the Animist",
    "Sword of Dungeons & Dragons", "Sword of Once and Future",
    "Masterwork of Ingenuity", "Fireshrieker", "Grappling Hook",
    "Rancor", "Ethereal Armor", "Colossification",
}

TOKENS = {
    "Parallel Lives", "Anointed Procession", "Doubling Season",
    "Primal Vigor", "Divine Visitation", "Intangible Virtue",
    "Cathars' Crusade", "Coat of Arms",
    "Avenger of Zendikar", "Tendershoot Dryad", "Mycoloth",
    "Dragon Broodmother", "Goblin Rabblemaster", "Legion Warboss",
    "Monastery Mentor", "Young Pyromancer", "Murmuring Mystic",
    "Talrand, Sky Summoner", "Metallurgic Summonings",
    "Lingering Souls", "Spectral Procession", "Secure the Wastes",
    "Entreat the Angels", "Sylvan Offering", "Rhys the Redeemed",
    "Marrow-Gnawer", "Sliver Queen", "Najeela, the Blade-Blossom",
    "Izoni, Thousand-Eyed",
}

SPELLSLINGER_PAYOFFS = {
    "Talrand, Sky Summoner", "Young Pyromancer", "Monastery Mentor",
    "Guttersnipe", "Murmuring Mystic", "Metallurgic Summonings",
    "Niv-Mizzet, Parun", "Niv-Mizzet, the Firemind",
    "Thousand-Year Storm", "Aria of Flame", "Archmage Ascension",
    "Thing in the Ice", "Crackling Drake", "Sprite Dragon",
    "Erratic Cyclops", "Spellheart Chimera", "Melek, Izzet Paragon",
    "Mizzix of the Izmagnus", "Wavebreak Hippocamp",
}

LIFEGAIN = {
    "Aetherflux Reservoir", "Serra Ascendant", "Crested Sunmare",
    "Archangel of Thune", "Karlov of the Ghost Council",
    "Soul Warden", "Soul's Attendant", "Essence Warden",
    "Sunbond", "Test of Endurance", "Felidar Sovereign",
    "Heliod, Sun-Crowned", "Ajani's Pridemate",
    "Vito, Thorn of the Dusk Rose", "Sanguine Bond",
    "Chalice of Life // Chalice of Death",
}


def detect_win_conditions(cards: list, card_types: dict, combos: list) -> list:
    names = {c["name"] for c in cards}
    wins = []

    if combos:
        wins.append("Combo")

    if len(names & STAX) >= 3:
        wins.append("Stax")

    if len(names & ARISTOCRATS) >= 3:
        wins.append("Aristocrats")

    if len(names & REANIMATOR) >= 3:
        wins.append("Reanimator")

    if len(names & VOLTRON) >= 4:
        wins.append("Voltron")

    if len(names & TOKENS) >= 3:
        wins.append("Tokens")

    if len(names & LIFEGAIN) >= 2:
        wins.append("Lifegain")

    total_nonland = sum(v for k, v in card_types.items() if k != "land")
    spell_ratio = (card_types.get("instant", 0) + card_types.get("sorcery", 0)) / max(total_nonland, 1)
    has_payoff = bool(names & SPELLSLINGER_PAYOFFS)
    if spell_ratio >= 0.35 and has_payoff:
        wins.append("Spellslinger")

    if not wins:
        wins.append("Goodstuff")

    return wins
