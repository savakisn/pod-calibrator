REMOVAL = {
    # White
    "Swords to Plowshares", "Path to Exile", "Generous Gift",
    "Oblivion Ring", "Banishing Light", "Grasp of Fate",
    "Fateful Absence", "Heliod's Intervention", "Ossification",
    "Council's Judgment", "Unexpectedly Absent", "Condemn",
    # Blue
    "Reality Shift", "Pongify", "Rapid Hybridization",
    "Imprisoned in the Moon", "Song of the Dryads", "Ravenform",
    "Petty Theft", "Venser, Shaper Savant", "Aether Gust",
    # Black
    "Tragic Slip", "Go for the Throat", "Victim of Night",
    "Murderous Rider", "Doom Blade", "Dismember", "Snuff Out",
    "Infernal Grasp", "Eat to Extinction", "Feed the Swarm",
    "Hero's Downfall", "Vraska's Contempt", "Curtains' Call",
    "Malicious Affliction", "Eliminate", "Disfigure",
    # Red
    "Chaos Warp", "Abrade", "Wild Magic Surge",
    "Kolaghan's Command", "Chaos Defiler",
    # Green
    "Beast Within", "Nature's Claim", "Return to Nature",
    "Reclamation Sage", "Force of Vigor", "Krosan Grip",
    "Naturalize", "Broken Bond", "Voracious Hydra",
    # Multi
    "Anguished Unmaking", "Assassin's Trophy", "Vindicate",
    "Utter End", "Despark", "Price of Fame", "Bedevil",
    "Dreadbore", "Terminate", "Putrefy", "Sultai Charm",
    "Merciless Purge", "Fiend Artisan",
    # Artifacts
    "Spine of Ish Sah",
}

BOARD_WIPES = {
    # White
    "Wrath of God", "Day of Judgment", "Fumigate",
    "Austere Command", "Supreme Verdict", "Cleansing Nova",
    "Mass Calcify", "Hour of Revelation", "Slaughter the Strong",
    "Martial Coup", "Rout", "Sunfall", "Descend upon the Sinful",
    "Urza's Ruinous Blast", "Winds of Abandon",
    # Black
    "Damnation", "Black Sun's Zenith", "In Garruk's Wake",
    "Decree of Pain", "Toxic Deluge", "Massacre Girl",
    "Crux of Fate", "Languish", "Extinction Event",
    "Killing Wave", "Mutilate", "Life's Finale",
    # Red
    "Blasphemous Act", "Chain Reaction", "Star of Extinction",
    "Mizzium Mortars", "Anger of the Gods", "Earthquake",
    "Rolling Earthquake", "Pyrohemia", "Magmaquake",
    "Subterranean Tremors", "Hour of Devastation",
    # Blue
    "Devastation Tide", "Wash Out", "Cyclonic Rift",
    "Flood of Tears", "Evacuation",
    # Green
    "Ezuri's Predation", "Bane of Progress",
    # Multi
    "Merciless Eviction", "Ruinous Ultimatum", "Depopulate",
    "Casualties of War", "Aetherspouts",
    # Artifacts
    "Oblivion Stone", "Nevinyrral's Disk", "Perilous Vault",
    "Ugin, the Spirit Dragon",
}

COUNTERSPELLS = {
    "Force of Will", "Force of Negation", "Pact of Negation",
    "Mana Drain", "Counterspell", "Arcane Denial",
    "Swan Song", "Fierce Guardianship", "Negate",
    "Dispel", "Flusterstorm", "Mental Misstep", "Spell Pierce",
    "Disallow", "Void Shatter", "Mystic Confluence",
    "Cryptic Command", "Absorb", "Render Silent",
    "Dovin's Veto", "Voidslime", "Delay",
    "Deprive", "Memory Lapse", "Remand", "Rewind",
    "Undermine", "Forbid", "Counterbalance",
    "Muddle the Mixture", "Spellstutter Sprite",
    "Tale's End", "Wash Away", "Saw It Coming",
    "An Offer You Can't Refuse", "Miscast",
    "Narset's Reversal", "Abjure",
}

TUTORS = {
    # Black
    "Demonic Tutor", "Vampiric Tutor", "Imperial Seal",
    "Diabolic Tutor", "Diabolic Intent", "Beseech the Queen",
    "Beseech the Mirror", "Grim Tutor", "Dark Petition",
    "Scheming Symmetry", "Wishclaw Talisman", "Mastermind's Acquisition",
    # Green
    "Worldly Tutor", "Natural Order", "Green Sun's Zenith",
    "Finale of Devastation", "Chord of Calling", "Woodland Bellower",
    "Eldritch Evolution", "Fauna Shaman", "Birthing Pod",
    "Fierce Empath", "Defense of the Heart", "Signal the Clans",
    # Blue
    "Mystical Tutor", "Merchant Scroll", "Fabricate",
    "Reshape", "Transmute Artifact", "Spellseeker",
    "Drift of Phantasms", "Dimir Machinations", "Perplex",
    "Tezzeret the Seeker", "Whir of Invention",
    # White
    "Enlightened Tutor", "Idyllic Tutor",
    "Recruiter of the Guard", "Ranger-Captain of Eos",
    "Weathered Wayfarer", "Ranger of Eos",
    # Red
    "Gamble", "Imperial Recruiter",
    # Multi
    "Bring to Light", "Wargate", "Momir Vig, Simic Visionary",
    "Tainted Pact", "Lim-Dul's Vault",
}


def analyze_interaction(cards: list) -> dict:
    names = {c["name"] for c in cards}
    return {
        "removal": len(names & REMOVAL),
        "board_wipes": len(names & BOARD_WIPES),
        "counterspells": len(names & COUNTERSPELLS),
        "tutors": len(names & TUTORS),
    }
