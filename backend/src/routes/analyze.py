from fastapi import APIRouter
from ..models.deck import DeckAnalysisRequest, DeckAnalysis, Card
from ..services.deck_parser import parse_moxfield_decklist, extract_unique_cards
from ..services.scryfall_client import fetch_card, parse_card_data

router = APIRouter()

@router.post("/analyze")
async def analyze_deck(request: DeckAnalysisRequest) -> DeckAnalysis:
    cards_list, commander_name = parse_moxfield_decklist(request.decklist)

    total_cards = sum(qty for qty, _ in cards_list)
    unique_cards = extract_unique_cards(cards_list)

    cards_data = []
    commander = None
    colors_count = {}
    type_count = {}
    mana_curve = {}
    total_cmc = 0
    card_count_processed = 0

    for qty, card_name in cards_list:
        scryfall_data = await fetch_card(card_name)

        if scryfall_data:
            parsed = parse_card_data(scryfall_data)
            card = Card(
                name=card_name,
                quantity=qty,
                **parsed
            )
            cards_data.append(card)

            if card_name == commander_name:
                commander = card

            cmc = card.cmc or 0
            total_cmc += cmc * qty
            card_count_processed += qty

            mana_val = int(cmc)
            mana_curve[mana_val] = mana_curve.get(mana_val, 0) + qty

            for color in card.colors or []:
                colors_count[color] = colors_count.get(color, 0) + qty

            card_type_parts = (card.type_line or "").split("(")[0].strip().split()
            for card_type in card_type_parts:
                card_type_clean = card_type.lower()
                type_count[card_type_clean] = type_count.get(card_type_clean, 0) + qty
        else:
            card = Card(name=card_name, quantity=qty)
            cards_data.append(card)

    avg_cmc = total_cmc / card_count_processed if card_count_processed > 0 else 0

    return DeckAnalysis(
        cards=cards_data,
        commander=commander,
        card_count=total_cards,
        avg_cmc=round(avg_cmc, 2),
        colors=colors_count,
        card_types=type_count,
        mana_curve=mana_curve,
    )
