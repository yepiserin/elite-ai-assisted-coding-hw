"""UI components for the Story Builder application"""
import air
from typing import Dict, Any, List

# Constants
MICE_TYPE_NAMES = {'M': 'Milieu', 'I': 'Inquiry', 'C': 'Character', 'E': 'Event'}


def labeled_field(label: str, content: str, field_class: str = "") -> air.Tag:
    """Create a labeled field display"""
    return air.Div(
        air.Strong(f"{label}:"),
        air.Div(content, class_=f"{field_class}-text" if field_class else ""),
        class_=f"{field_class}-field" if field_class else ""
    )


def theory_card(code: str, title: str, description: str, opens: str, closes: str, example: str) -> air.Tag:
    """Create a MICE theory card"""
    return air.Div(
        air.H3(title, class_=f"theory-header {code}"),
        air.P(description),
        air.P(f"Opens: {opens}", style="font-style: italic;"),
        air.P(f"Closes: {closes}", style="font-style: italic;"),
        air.P(f"Example: {example}", style="color: #666;"),
        class_="theory-card"
    )


def mice_card_component(card: Dict[str, Any]) -> air.Tag:
    """Render a MICE card component"""
    return air.Div(
        air.Div(
            f"{card['code']} - {MICE_TYPE_NAMES.get(card['code'], '')}",
            class_=f"mice-type {card['code']}"
        ),
        air.Div(
            labeled_field("Opening", card['opening'], "mice"),
            labeled_field("Closing", card['closing'], "mice"),
            class_="mice-content"
        ),
        air.Div(f"Nesting Level: {card['nesting_level']}", class_="nesting-level"),
        air.Div(
            air.Button("Edit", class_="btn-secondary", onclick=f"editMiceCard({card['id']}, '{card['code']}', `{card['opening']}`, `{card['closing']}`, {card['nesting_level']})"),
            air.Button("Delete", class_="btn-danger", onclick=f"deleteMiceCard({card['id']})"),
            class_="card-actions"
        ),
        class_="card mice-card",
        id=f"mice-card-{card['id']}"
    )


def try_card_component(card: Dict[str, Any]) -> air.Tag:
    """Render a Try/Fail card component"""
    type_class = ""
    for keyword in ['Escalation', 'Complication', 'Revelation', 'Resolution']:
        if keyword in card['type']:
            type_class = keyword.lower()
            break

    return air.Div(
        air.Div(
            f"#{card['order_num']} - {card['type']}",
            class_=f"try-type {type_class}"
        ),
        labeled_field("Attempt", card['attempt'], "try"),
        labeled_field("Outcome", card['failure'], "try"),
        labeled_field("Consequence", card['consequence'], "try"),
        air.Div(
            air.Button("Edit", class_="btn-secondary", onclick=f"editTryCard({card['id']}, '{card['type']}', `{card['attempt']}`, `{card['failure']}`, `{card['consequence']}`, {card['order_num']})"),
            air.Button("Delete", class_="btn-danger", onclick=f"deleteTryCard({card['id']})"),
            class_="card-actions"
        ),
        class_="card try-card",
        id=f"try-card-{card['id']}"
    )


def build_nesting_diagram(mice_cards: List[Dict[str, Any]]) -> air.Tag:
    """Build the nesting diagram visualization"""
    # Group cards by nesting level
    by_level: Dict[int, List[Dict[str, Any]]] = {}
    for card in mice_cards:
        level = card['nesting_level']
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(card)

    max_level = max(by_level.keys()) if by_level else 0

    def build_level_box(level: int) -> air.Tag:
        if level > max_level:
            return air.Span()

        cards_at_level = by_level.get(level, [])
        inner_content = build_level_box(level + 1) if level < max_level else air.Span()

        return air.Div(
            *[air.Div(
                f"↓ {card['code']}: {card['opening'][:30]}...",
                class_=f"nest-item opening {card['code']}"
            ) for card in cards_at_level],
            inner_content if level < max_level else air.Span(),
            *[air.Div(
                f"↑ {card['code']}: {card['closing'][:30]}...",
                class_=f"nest-item closing {card['code']}"
            ) for card in reversed(cards_at_level)],
            class_=f"nest-level level-{level}",
            style=f"margin: 10px; padding: 10px; border: 2px solid #{'ddd' if level % 2 == 0 else 'ccc'}; border-radius: 4px;"
        )

    return build_level_box(1)


def build_story_flow(mice_cards: List[Dict[str, Any]], try_cards: List[Dict[str, Any]]) -> air.Tag:
    """Build the story flow visualization"""
    # Sort MICE cards by nesting level
    sorted_mice = sorted(mice_cards, key=lambda x: x['nesting_level'])

    return air.Div(
        # Act 1
        air.Div(
            air.H4("Act 1: Openings"),
            *[air.Div(
                f"{card['code']}: {card['opening']}",
                class_=f"flow-item {card['code']}"
            ) for card in sorted_mice],
            class_="act act-1",
            style="background-color: #e8f5e9; padding: 10px; border-radius: 4px; margin-bottom: 10px;"
        ),
        # Act 2
        air.Div(
            air.H4("Act 2: Try/Fail Cycles"),
            *[air.Div(
                f"#{card['order_num']}: {card['attempt']} → {card['failure']}",
                class_="flow-item try"
            ) for card in try_cards],
            class_="act act-2",
            style="background-color: #e3f2fd; padding: 10px; border-radius: 4px; margin-bottom: 10px;"
        ) if try_cards else air.Span(),
        # Act 3
        air.Div(
            air.H4("Act 3: Closings"),
            *[air.Div(
                f"{card['code']}: {card['closing']}",
                class_=f"flow-item {card['code']}"
            ) for card in reversed(sorted_mice)],
            class_="act act-3",
            style="background-color: #f3e5f5; padding: 10px; border-radius: 4px;"
        ),
    )
