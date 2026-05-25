RAMP = {
    # 0-CMC fast mana
    "Mana Crypt", "Chrome Mox", "Mox Diamond", "Lotus Petal",
    # 1-CMC
    "Sol Ring", "Dark Ritual", "Cabal Ritual", "Pyretic Ritual",
    "Desperate Ritual", "Seething Song",
    # 2-CMC rocks
    "Arcane Signet", "Mind Stone", "Thought Vessel", "Fellwar Stone",
    "Talisman of Dominance", "Talisman of Indulgence", "Talisman of Creativity",
    "Talisman of Conviction", "Talisman of Impulse", "Talisman of Progress",
    "Talisman of Unity", "Talisman of Curiosity", "Talisman of Hierarchy",
    "Talisman of Resilience",
    "Azorius Signet", "Dimir Signet", "Rakdos Signet", "Gruul Signet",
    "Selesnya Signet", "Orzhov Signet", "Izzet Signet", "Golgari Signet",
    "Boros Signet", "Simic Signet",
    # 3-CMC rocks
    "Commander's Sphere", "Coalition Relic", "Chromatic Lantern",
    "Worn Powerstone", "Mana Vault", "Grim Monolith", "Basalt Monolith",
    # 4-5-CMC rocks
    "Thran Dynamo", "Gilded Lotus",
    # Land ramp
    "Cultivate", "Kodama's Reach", "Rampant Growth", "Nature's Lore",
    "Three Visits", "Farseek", "Skyshroud Claim", "Explosive Vegetation",
    "Ranger's Path", "Circuitous Route", "Migration Path", "Harrow",
    "Hour of Promise", "Sylvan Scrying", "Crop Rotation",
    # Mana dorks
    "Birds of Paradise", "Llanowar Elves", "Elvish Mystic", "Fyndhorn Elves",
    "Avacyn's Pilgrim", "Noble Hierarch", "Deathrite Shaman", "Sylvan Caryatid",
    "Bloom Tender", "Selvala, Heart of the Wilds", "Selvala, Explorer Returned",
    "Priest of Titania", "Elvish Archdruid", "Somberwald Sage",
    # Enchantment ramp
    "Wild Growth", "Utopia Sprawl", "Fertile Ground", "Carpet of Flowers",
    "Overgrowth",
}

_TIERS = [
    (1.8, "Turbo"),
    (2.4, "Fast"),
    (3.1, "Midrange"),
    (3.7, "Slow"),
    (float("inf"), "Battlecruiser"),
]


def analyze_speed(cards: list, avg_nonland_cmc: float) -> dict:
    ramp_count = sum(1 for c in cards if c["name"] in RAMP)
    adjusted = avg_nonland_cmc - (ramp_count * 0.05)
    label = next(lbl for threshold, lbl in _TIERS if adjusted < threshold)
    return {
        "label": label,
        "avg_nonland_cmc": round(avg_nonland_cmc, 2),
        "ramp_count": ramp_count,
    }
