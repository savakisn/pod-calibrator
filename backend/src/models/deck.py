from pydantic import BaseModel
from typing import Optional, List, Dict

class Card(BaseModel):
    name: str
    quantity: int
    scryfall_id: Optional[str] = None
    mana_cost: Optional[str] = None
    cmc: Optional[float] = None
    colors: Optional[List[str]] = None
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    image_uris: Optional[Dict] = None

class DeckAnalysisRequest(BaseModel):
    decklist: str

class DeckAnalysis(BaseModel):
    cards: List[Card]
    commander: Optional[Card] = None
    card_count: int
    avg_cmc: float
    colors: Dict[str, int]
    card_types: Dict[str, int]
    mana_curve: Dict[int, int]
    detected_combos: List[Dict] = []
    bracket_score: Optional[int] = None
    power_label: Optional[str] = None
    precon_match: Optional[str] = None
    win_conditions: List[str] = []
    speed: Optional[float] = None
