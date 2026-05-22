import aiohttp
from typing import Optional
from ..cache import cache

SCRYFALL_API = "https://api.scryfall.com"

async def fetch_card(name: str) -> Optional[dict]:
    cache_key = f"card:{name}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        async with aiohttp.ClientSession() as session:
            url = f"{SCRYFALL_API}/cards/named?exact={name}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    cache.set(cache_key, data)
                    return data
    except Exception as e:
        print(f"Error fetching {name}: {e}")

    return None

def parse_card_data(card: dict) -> dict:
    colors = card.get("colors", [])
    color_map = {
        "W": "white",
        "U": "blue",
        "B": "black",
        "R": "red",
        "G": "green",
        "C": "colorless"
    }

    return {
        "name": card.get("name"),
        "scryfall_id": card.get("id"),
        "mana_cost": card.get("mana_cost"),
        "cmc": card.get("cmc", 0),
        "colors": [color_map.get(c, c) for c in colors],
        "type_line": card.get("type_line"),
        "oracle_text": card.get("oracle_text", ""),
        "image_uris": card.get("image_uris"),
    }
