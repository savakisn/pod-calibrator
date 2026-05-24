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

        # Build mapping of unique card names to all their indices in this batch
        name_to_indices = {}
        unique_names_to_fetch = []

        for i, name in enumerate(batch_names):
            cache_key = f"card:{name}"
            cached = cache.get(cache_key)
            if cached:
                # Replicate cached result to all indices with this name
                if name not in name_to_indices:
                    name_to_indices[name] = []
                name_to_indices[name].append((batch_start + i, cached))
                results[batch_start + i] = cached
            else:
                # Track unique names to fetch
                if name not in name_to_indices:
                    name_to_indices[name] = []
                    unique_names_to_fetch.append({"name": name, "fuzzy": name})
                name_to_indices[name].append(batch_start + i)

        if not unique_names_to_fetch:
            continue

        try:
            with httpx.Client() as client:
                # Rate limit before each batch request
                elapsed = time.time() - _last_request_time
                if elapsed < 0.1:
                    time.sleep(0.1 - elapsed)

                _last_request_time = time.time()
                url = f"{SCRYFALL_API}/cards/collection"
                resp = client.post(url, json={"identifiers": unique_names_to_fetch})

                if resp.status_code == 200:
                    data = resp.json()
                    cards = data.get("data", [])

                    # Map each fetched card to all indices where it appears
                    for card in cards:
                        card_name = card.get("name")
                        if card_name in name_to_indices:
                            # Replicate this card to all indices with this name
                            for idx in name_to_indices[card_name]:
                                if isinstance(idx, tuple):  # Already cached, skip
                                    continue
                                results[idx] = card
                            # Cache it
                            cache.set(f"card:{card_name}", card)
                elif resp.status_code == 429:
                    print(f"Rate limited on batch request")
        except Exception as e:
            print(f"Error fetching batch: {e}")

    return results

def fetch_card_sync(name: str, retry_count: int = 0, max_retries: int = 2) -> Optional[Dict]:
    global _last_request_time

    cache_key = f"card:{name}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        with httpx.Client() as client:
            # Rate limit: 100ms between requests (same as batch)
            elapsed = time.time() - _last_request_time
            if elapsed < 0.1:
                time.sleep(0.1 - elapsed)

            # Try exact match first
            url = f"{SCRYFALL_API}/cards/named?exact={name}"
            _last_request_time = time.time()
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data)
                return data
            elif resp.status_code == 429:
                # Retry with exponential backoff on rate limit
                if retry_count < max_retries:
                    wait_time = 0.5 * (2 ** retry_count)
                    time.sleep(wait_time)
                    return fetch_card_sync(name, retry_count + 1, max_retries)
                return None

            # Rate limit before second request
            elapsed = time.time() - _last_request_time
            if elapsed < 0.1:
                time.sleep(0.1 - elapsed)

            # Fall back to fuzzy match if exact fails
            url = f"{SCRYFALL_API}/cards/named?fuzzy={name}"
            _last_request_time = time.time()
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data)
                return data
            elif resp.status_code == 429:
                # Retry with exponential backoff on rate limit
                if retry_count < max_retries:
                    wait_time = 0.5 * (2 ** retry_count)
                    time.sleep(wait_time)
                    return fetch_card_sync(name, retry_count + 1, max_retries)
                return None
    except Exception as e:
        print(f"Error fetching {name}: {e}")

    return None

def parse_card_data(card: Dict) -> Dict:
    colors = card.get("colors", [])
    color_identity = card.get("color_identity", [])
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
        "color_identity": [color_map.get(c, c) for c in color_identity],
        "type_line": card.get("type_line"),
        "oracle_text": card.get("oracle_text", ""),
        "image_uris": card.get("image_uris"),
    }
