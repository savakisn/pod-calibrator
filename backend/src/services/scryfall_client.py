import httpx
import time
from typing import Optional, Dict
from ..cache import cache

SCRYFALL_API = "https://api.scryfall.com"
_last_request_time = 0.0

def fetch_card_sync(name: str) -> Optional[Dict]:
    global _last_request_time

    cache_key = f"card:{name}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached if cached != "NOT_FOUND" else None

    try:
        with httpx.Client() as client:
            # Rate limit: 200ms between requests (safe margin below 10 req/sec)
            elapsed = time.time() - _last_request_time
            if elapsed < 0.2:
                time.sleep(0.2 - elapsed)

            # Try exact match first
            url = f"{SCRYFALL_API}/cards/named?exact={name}"
            _last_request_time = time.time()
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data)
                return data
            elif resp.status_code == 429:
                print(f"Rate limited fetching {name}: {resp.status_code}")
                return None

            # Rate limit before second request
            elapsed = time.time() - _last_request_time
            if elapsed < 0.2:
                time.sleep(0.2 - elapsed)

            # Fall back to fuzzy match if exact fails
            url = f"{SCRYFALL_API}/cards/named?fuzzy={name}"
            _last_request_time = time.time()
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data)
                return data
            elif resp.status_code == 429:
                print(f"Rate limited fetching {name} (fuzzy): {resp.status_code}")
                return None
    except Exception as e:
        print(f"Error fetching {name}: {e}")

    # Cache the fact that this card wasn't found
    cache.set(cache_key, "NOT_FOUND")
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
