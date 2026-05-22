import httpx
from typing import Optional, Dict
from ..cache import cache

SCRYFALL_API = "https://api.scryfall.com"

def fetch_card_sync(name: str) -> Optional[Dict]:
    cache_key = f"card:{name}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        with httpx.Client() as client:
            url = f"{SCRYFALL_API}/cards/named?exact={name}"
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data)
                return data
    except Exception as e:
        print(f"Error fetching {name}: {e}")

    return None

def parse_card_data(card: Dict) -> Dict:
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
        "scryfall_id": card.get("id"),
        "mana_cost": card.get("mana_cost"),
        "cmc": card.get("cmc", 0),
        "colors": [color_map.get(c, c) for c in colors],
        "type_line": card.get("type_line"),
        "oracle_text": card.get("oracle_text", ""),
        "image_uris": card.get("image_uris"),
    }
