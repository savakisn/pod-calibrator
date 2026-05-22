from pydantic import BaseModel
from typing import Optional

class Card(BaseModel):
    name: str
    quantity: int
    scryfall_id: Optional[str] = None
    mana_cost: Optional[str] = None
    cmc: Optional[float] = None
    colors: Optional[list[str]] = None
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    image_uris: Optional[dict] = None

class DeckAnalysisRequest(BaseModel):
    decklist: str

class DeckAnalysis(BaseModel):
    cards: list[Card]
    commander: Optional[Card] = None
    card_count: int
    avg_cmc: float
    colors: dict[str, int]
    card_types: dict[str, int]
    mana_curve: dict[int, int]
    detected_combos: list[dict] = []
    bracket_score: Optional[int] = None
    power_label: Optional[str] = None
    precon_match: Optional[str] = None
    win_conditions: list[str] = []
    speed: Optional[float] = None
