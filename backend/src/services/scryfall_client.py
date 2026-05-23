import httpx
import time
from typing import Optional, Dict, List
from ..cache import cache

SCRYFALL_API = "https://api.scryfall.com"
_last_request_time = 0.0

def fetch_cards_batch(card_names: List[str]) -> List[Optional[Dict]]:
    """Fetch multiple cards using Scryfall's batch endpoint (max 75 cards per request)"""
    global _last_request_time

    # Rate limit before batch request
    elapsed = time.time() - _last_request_time
    if elapsed < 0.1:
        time.sleep(0.1 - elapsed)

    results = [None] * len(card_names)

    # Process in batches of 75 (Scryfall limit)
    for batch_start in range(0, len(card_names), 75):
        batch_end = min(batch_start + 75, len(card_names))
        batch_names = card_names[batch_start:batch_end]

        # Check cache first
        batch_to_fetch = []
        fetch_indices = []
        for i, name in enumerate(batch_names):
            cache_key = f"card:{name}"
            cached = cache.get(cache_key)
            if cached:
                results[batch_start + i] = cached
            else:
                batch_to_fetch.append({"name": name, "fuzzy": name})
                fetch_indices.append(batch_start + i)

        if not batch_to_fetch:
            continue

        try:
            with httpx.Client() as client:
                # Rate limit before each batch request
                elapsed = time.time() - _last_request_time
                if elapsed < 0.1:
                    time.sleep(0.1 - elapsed)

                _last_request_time = time.time()
                url = f"{SCRYFALL_API}/cards/collection"
                resp = client.post(url, json={"identifiers": batch_to_fetch})

                if resp.status_code == 200:
                    data = resp.json()
                    cards = data.get("data", [])

                    # Map results back to original indices
                    for card, orig_idx in zip(cards, fetch_indices):
                        results[orig_idx] = card
                        # Cache the result
                        card_name = batch_names[orig_idx - batch_start]
                        cache.set(f"card:{card_name}", card)
                elif resp.status_code == 429:
                    print(f"Rate limited on batch request")
        except Exception as e:
            print(f"Error fetching batch: {e}")

    return results

def fetch_card_sync(name: str) -> Optional[Dict]:
    global _last_request_time

    cache_key = f"card:{name}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        import sys
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

    # Don't cache failures - they might be due to rate limiting
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
