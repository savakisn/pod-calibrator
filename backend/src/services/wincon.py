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
    "Cruel Celebrant", "Mayhem Devil", "Judith, the Scourge Diva",
    "Dictate of Erebos", "Grave Pact", "Butcher of Malakir",
    "Ashnod's Altar", "Phyrexian Altar", "Altar of Dementia",
    "Viscera Seer", "Carrion Feeder", "Goblin Bombardment",
    "Skullclamp", "Pitiless Plunderer", "Pawn of Ulamog",
    "Sifter of Skulls", "Midnight Reaper", "Dark Prophecy",
    "Grim Haruspex", "Champion of the Perished", "Teysa Karlov",
    "Savra, Queen of the Golgari", "Butcher of the Horde",
    "Bolas's Citadel",
}

REANIMATOR = {
    "Animate Dead", "Reanimate", "Necromancy", "Dance of the Dead",
    "Exhume", "Entomb", "Buried Alive", "Unearth",
    "Dread Return", "Victimize", "Living Death", "Living End",
    "Zombify", "Persist", "Rescue from the Underworld",
    "Apprentice Necromancer", "Goryo's Vengeance", "Corpse Dance",
    "Sheoldred, Whispering One", "Debtor's Knell", "Patriarch's Bidding",
    "Haunting Voyage", "Ever After", "Hell's Caretaker",
    "Twilight's Call", "Stitch Together",
}

VOLTRON = {
    "Lightning Greaves", "Swiftfoot Boots", "Hammer of Nazahn",
    "Colossus Hammer", "Embercleave", "Umezawa's Jitte",
    "Batterskull", "Loxodon Warhammer", "Blackblade Reforged",
    "Sunforger", "Champion's Helm", "Commander's Plate",
    "Darksteel Plate", "Bloodforged Battle-Axe", "Fireshrieker",
    "Grappling Hook", "Masterwork of Ingenuity",
    "Sword of Fire and Ice", "Sword of Feast and Famine",
    "Sword of Light and Shadow", "Sword of War and Peace",
    "Sword of Body and Mind", "Sword of Sinew and Steel",
    "Sword of Truth and Justice", "Sword of the Animist",
    "Sword of Dungeons & Dragons", "Sword of Once and Future",
    "Rancor", "Ethereal Armor", "Colossification",
    "Eldrazi Conscription", "Corrupted Conscience",
    "Auramancer's Guise", "Sage's Reverie",
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
    "Izoni, Thousand-Eyed", "Chatterfang, Squirrel General",
    "Lathril, Blade of the Elves", "Jetmir, Nexus of Revels",
    "Adrix and Nev, Twincasters", "Jinnie Fay, Jetmir's Second",
    "Rampaging Baloths", "Titania, Protector of Argoth",
    "Sporemound", "Verdant Force", "Bramble Sovereign",
    "Saproling Migration", "Fungal Plots", "Spore Flower",
    "Slimefoot, the Stowaway", "Thalisse, Reverent Medium",
    "Ghave, Guru of Spores",
}

LIFEGAIN = {
    "Aetherflux Reservoir", "Serra Ascendant", "Crested Sunmare",
    "Archangel of Thune", "Karlov of the Ghost Council",
    "Soul Warden", "Soul's Attendant", "Essence Warden",
    "Sunbond", "Test of Endurance", "Felidar Sovereign",
    "Heliod, Sun-Crowned", "Ajani's Pridemate",
    "Vito, Thorn of the Dusk Rose", "Sanguine Bond",
    "Chalice of Life // Chalice of Death", "Oloro, Ageless Ascetic",
    "Lathiel, the Bounteous Dawn", "Willowdusk, Essence Seer",
    "Dina, Soul Steeper", "Speaker of the Heavens",
}

SPELLSLINGER_PAYOFFS = {
    "Talrand, Sky Summoner", "Young Pyromancer", "Monastery Mentor",
    "Guttersnipe", "Murmuring Mystic", "Metallurgic Summonings",
    "Niv-Mizzet, Parun", "Niv-Mizzet, the Firemind",
    "Thousand-Year Storm", "Aria of Flame", "Archmage Ascension",
    "Thing in the Ice", "Crackling Drake", "Sprite Dragon",
    "Erratic Cyclops", "Spellheart Chimera", "Melek, Izzet Paragon",
    "Mizzix of the Izmagnus", "Wavebreak Hippocamp", "Kalamax, the Stormsire",
    "Veyran, Voice of Duality", "Galazeth Prismari",
}

# Maps commander name to a list of strategy labels it definitively implies.
COMMANDER_STRATEGIES: dict[str, list[str]] = {
    # Aristocrats
    "Edgar Markov": ["Aristocrats", "Tribal"],
    "Wilhelt, the Rotcleaver": ["Aristocrats", "Tribal"],
    "Meren of Clan Nel Toth": ["Aristocrats", "Reanimator"],
    "Prossh, Skyraider of Kher": ["Aristocrats", "Combo"],
    "Judith, the Scourge Diva": ["Aristocrats"],
    "Korvold, Fae-Cursed King": ["Aristocrats"],
    "Teysa Karlov": ["Aristocrats"],
    "Karador, Ghost Chieftain": ["Aristocrats", "Reanimator"],
    "Savra, Queen of the Golgari": ["Aristocrats"],
    "Ayli, Eternal Pilgrim": ["Aristocrats", "Lifegain"],
    "Ghave, Guru of Spores": ["Aristocrats", "Tokens", "Combo"],
    "Slimefoot, the Stowaway": ["Aristocrats", "Tokens"],
    # Tokens
    "Rhys the Redeemed": ["Tokens"],
    "Najeela, the Blade-Blossom": ["Tokens", "Combo"],
    "Chatterfang, Squirrel General": ["Tokens"],
    "Lathril, Blade of the Elves": ["Tokens", "Tribal"],
    "Jetmir, Nexus of Revels": ["Tokens"],
    "Adrix and Nev, Twincasters": ["Tokens"],
    "Jinnie Fay, Jetmir's Second": ["Tokens"],
    "Thalisse, Reverent Medium": ["Tokens"],
    "Kykar, Wind's Fury": ["Tokens", "Spellslinger"],
    # Voltron
    "Rafiq of the Many": ["Voltron"],
    "Shu Yun, the Silent Tempest": ["Voltron", "Spellslinger"],
    "Nazahn, Revered Bladesmith": ["Voltron"],
    "Galea, Kindler of Hope": ["Voltron"],
    "Sigarda, Host of Herons": ["Voltron"],
    "Ardenn, Intrepid Archaeologist": ["Voltron"],
    "Light-Paws, Emperor's Voice": ["Voltron"],
    "Godo, Bandit Warlord": ["Voltron", "Combo"],
    "Rograkh, Son of Rohgahh": ["Voltron"],
    "Siona, Captain of the Pyleas": ["Voltron", "Combo"],
    # Stax
    "Urza, Lord High Artificer": ["Stax", "Combo"],
    "Grand Arbiter Augustin IV": ["Stax"],
    "Hokori, Dust Drinker": ["Stax"],
    "Derevi, Empyrial Tactician": ["Stax"],
    "Brago, King Eternal": ["Stax"],
    "Teferi, Temporal Archmage": ["Stax", "Combo"],
    "Zur the Enchanter": ["Stax", "Combo"],
    # Reanimator
    "Kaalia of the Vast": ["Reanimator"],
    "The Scarab God": ["Reanimator", "Tribal"],
    "Muldrotha, the Gravetide": ["Reanimator"],
    "Chainer, Nightmare Adept": ["Reanimator"],
    "Nethroi, Apex of Death": ["Reanimator", "Combo"],
    "Sedris, the Traitor King": ["Reanimator"],
    "Sefris of the Hidden Ways": ["Reanimator"],
    "Alesha, Who Smiles at Death": ["Reanimator"],
    # Spellslinger
    "Niv-Mizzet, Parun": ["Spellslinger", "Combo"],
    "Niv-Mizzet, the Firemind": ["Spellslinger", "Combo"],
    "Mizzix of the Izmagnus": ["Spellslinger"],
    "Talrand, Sky Summoner": ["Spellslinger", "Tokens"],
    "Kalamax, the Stormsire": ["Spellslinger"],
    "Veyran, Voice of Duality": ["Spellslinger"],
    "Melek, Izzet Paragon": ["Spellslinger"],
    "Galazeth Prismari": ["Spellslinger"],
    # Lifegain
    "Oloro, Ageless Ascetic": ["Lifegain"],
    "Karlov of the Ghost Council": ["Lifegain", "Voltron"],
    "Lathiel, the Bounteous Dawn": ["Lifegain"],
    "Dina, Soul Steeper": ["Lifegain", "Combo"],
    "Willowdusk, Essence Seer": ["Lifegain", "Combo"],
    "Heliod, Sun-Crowned": ["Lifegain", "Combo"],
    # Combo / Goodstuff
    "Kenrith, the Returned King": ["Combo"],
    "Thrasios, Triton Hero": ["Combo"],
    "Yisan, the Wanderer Bard": ["Combo"],
    "Selvala, Heart of the Wilds": ["Combo"],
    "The Gitrog Monster": ["Combo", "Lands"],
    "Tymna the Weaver": ["Combo"],
    "Kraum, Ludevic's Opus": ["Combo"],
    "Ishai, Ojutai Dragonspeaker": ["Combo"],
    "Food Chain": ["Combo"],
    # Superfriends / Proliferate
    "Atraxa, Praetors' Voice": ["Superfriends"],
    "Djeru, With Eyes Open": ["Superfriends"],
    "Carth the Lion": ["Superfriends"],
    # Tribal
    "The Ur-Dragon": ["Tribal"],
    "Animar, Soul of Elements": ["Tribal", "Combo"],
    "Sliver Overlord": ["Tribal", "Combo"],
    "Sliver Legion": ["Tribal"],
    "Inalla, Archmage Ritualist": ["Tribal", "Combo"],
    "Yuriko, the Tiger's Shadow": ["Tribal"],
    "Scion of the Ur-Dragon": ["Tribal", "Combo"],
    "Tiamat": ["Tribal"],
    # Landfall / Lands
    "Aesi, Tyrant of Gyre Strait": ["Landfall"],
    "Omnath, Locus of Creation": ["Landfall"],
    "Omnath, Locus of Rage": ["Landfall", "Tokens"],
    "Tatyova, Benthic Druid": ["Landfall"],
    "Lord Windgrace": ["Landfall", "Reanimator"],
    "Titania, Protector of Argoth": ["Landfall", "Tokens"],
    "Kodama of the East Tree": ["Landfall"],
}


def detect_win_conditions(
    cards: list,
    card_types: dict,
    combos: list,
    commander_name: str | None = None,
) -> list:
    names = {c["name"] for c in cards}
    wins: list[str] = []

    # Commander lookup goes first - highest confidence signal
    if commander_name:
        for strategy in COMMANDER_STRATEGIES.get(commander_name, []):
            if strategy not in wins:
                wins.append(strategy)

    if combos and "Combo" not in wins:
        wins.append("Combo")

    # Card-based detection: lower threshold to 2 when commander already confirms the strategy
    def threshold(strategy: str, default: int) -> int:
        return max(1, default - 1) if strategy in wins else default

    if len(names & STAX) >= threshold("Stax", 3):
        if "Stax" not in wins:
            wins.append("Stax")

    if len(names & ARISTOCRATS) >= threshold("Aristocrats", 3):
        if "Aristocrats" not in wins:
            wins.append("Aristocrats")

    if len(names & REANIMATOR) >= threshold("Reanimator", 3):
        if "Reanimator" not in wins:
            wins.append("Reanimator")

    if len(names & VOLTRON) >= threshold("Voltron", 4):
        if "Voltron" not in wins:
            wins.append("Voltron")

    if len(names & TOKENS) >= threshold("Tokens", 3):
        if "Tokens" not in wins:
            wins.append("Tokens")

    if len(names & LIFEGAIN) >= threshold("Lifegain", 2):
        if "Lifegain" not in wins:
            wins.append("Lifegain")

    total_nonland = sum(v for k, v in card_types.items() if k != "land")
    spell_ratio = (card_types.get("instant", 0) + card_types.get("sorcery", 0)) / max(total_nonland, 1)
    has_payoff = bool(names & SPELLSLINGER_PAYOFFS)
    if spell_ratio >= 0.35 and has_payoff and "Spellslinger" not in wins:
        wins.append("Spellslinger")

    if not wins:
        wins.append("Goodstuff")

    return wins
