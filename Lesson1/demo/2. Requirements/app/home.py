"""Home page template for the Story Builder application"""
import air
from typing import List, Dict, Any
from components import (
    theory_card, mice_card_component, try_card_component,
    build_nesting_diagram, build_story_flow
)


def home_page(mice_cards: List[Dict[str, Any]], try_cards: List[Dict[str, Any]]) -> air.Tag:
    """Render the main home page"""
    return air.Html(
        air.Head(
            air.Title("Story Builder - MICE Quotient"),
            air.Link(rel="stylesheet", href="/static/styles.css"),
            air.Script(src="https://unpkg.com/htmx.org@1.9.10"),
            air.Script(src="/static/app.js", defer=True)
        ),
        air.Body(
            air.H1("Story Builder with MICE Quotient"),

            # Top action buttons
            air.Div(
                air.Button("Seed Sample Data", hx_post="/api/seed-data", hx_swap="none", class_="btn-primary"),
                air.Button("Clear All Data", onclick="clearAllData()", class_="btn-danger", style="margin-left: 10px;"),
                air.Button("📚 MICE Theory", onclick="toggleTheoryPanel()", class_="btn-secondary", style="margin-left: 10px;"),
                style="text-align: center; margin-bottom: 20px;"
            ),

            # Theory panel
            theory_panel(),

            # Main content
            air.Div(
                mice_column(mice_cards),
                try_column(try_cards),
                outline_column(mice_cards, try_cards),
                class_="container"
            )
        )
    )


def theory_panel() -> air.Tag:
    """Render the theory panel"""
    return air.Div(
        air.Div(
            air.H2("MICE Quotient Framework"),
            air.P("Stories are built from four fundamental narrative threads that open and close in nested order:"),

            air.Div(
                theory_card("M", "M - Milieu", "Stories about exploring a place or setting",
                          "Character enters a new world", "Character leaves that world",
                          "Lord of the Rings (Frodo enters Middle Earth, leaves the Shire)"),
                theory_card("I", "I - Inquiry", "Stories driven by seeking answers to questions",
                          "A question is raised", "The question is answered",
                          "Murder mysteries (Who did it? → The killer is revealed)"),
                theory_card("C", "C - Character", "Stories about personal transformation",
                          "Character is dissatisfied with their role", "Character accepts or changes their role",
                          "A Christmas Carol (Scrooge is miserly → becomes generous)"),
                theory_card("E", "E - Event", "Stories about external conflicts and actions",
                          "The world falls out of order", "Order is restored (or new order established)",
                          "Die Hard (terrorists take building → hero defeats them)"),
                class_="theory-grid"
            ),

            air.H3("Nesting Concept", style="margin-top: 30px;"),
            air.P("Stories open outside-in (1→2→3→4) and close inside-out (4→3→2→1). The outermost thread frames the entire story, while inner threads create complexity and depth."),

            air.H3("Try/Fail Cycles", style="margin-top: 20px;"),
            air.Div(
                air.Div(
                    air.Strong("Escalation (No, AND):"),
                    air.Span(" Character fails and things get worse"),
                    class_="try-pattern"
                ),
                air.Div(
                    air.Strong("Complication (Yes, BUT):"),
                    air.Span(" Character succeeds but creates new problems"),
                    class_="try-pattern"
                ),
                air.Div(
                    air.Strong("Revelation (No, BUT):"),
                    air.Span(" Character fails but discovers opportunity"),
                    class_="try-pattern"
                ),
                air.Div(
                    air.Strong("Resolution (Yes, AND):"),
                    air.Span(" Character succeeds and builds momentum"),
                    class_="try-pattern"
                ),
                style="display: flex; flex-direction: column; gap: 10px;"
            ),

            class_="theory-content"
        ),
        id="theory-panel",
        class_="theory-panel hidden",
        style="background: white; border: 2px solid #333; border-radius: 8px; padding: 20px; margin-bottom: 20px; max-width: 1200px; margin-left: auto; margin-right: auto;"
    )


def mice_column(mice_cards: List[Dict[str, Any]]) -> air.Tag:
    """Render the MICE cards column"""
    return air.Div(
        air.H2("MICE Cards"),
        air.Button("+ Add MICE Card", id="add-mice-btn", class_="btn-primary add-card-btn", onclick="showMiceForm()"),
        air.Div(
            air.Form(
                air.Div(
                    air.Label("MICE Type", for_="code"),
                    air.Select(
                        air.Option("Select type...", value=""),
                        air.Option("M - Milieu (Place/Setting)", value="M"),
                        air.Option("I - Inquiry (Question/Mystery)", value="I"),
                        air.Option("C - Character (Personal Change)", value="C"),
                        air.Option("E - Event (External Conflict)", value="E"),
                        id="code", name="code", required=True
                    ),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Opening (Act 1)", for_="opening"),
                    air.Textarea(id="opening", name="opening", required=True, placeholder="What begins this narrative thread?"),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Closing (Act 3)", for_="closing"),
                    air.Textarea(id="closing", name="closing", required=True, placeholder="How does this thread resolve?"),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Nesting Level", for_="nesting_level"),
                    air.Input(type="number", id="nesting_level", name="nesting_level", min="1", max="10", value="1", required=True),
                    class_="form-group"
                ),
                air.Div(
                    air.Button("Save Card", type="submit", class_="btn-primary"),
                    air.Button("Cancel", type="button", class_="btn-secondary", onclick="hideMiceForm()"),
                    class_="form-actions"
                ),
                id="mice-card-form",
                onsubmit="submitMiceCard(event)"
            ),
            id="mice-form",
            class_="card-form hidden"
        ),
        air.Div(
            *[mice_card_component(card) for card in mice_cards] if mice_cards else [air.Div("No MICE cards yet. Add one to get started!", class_="empty-state")],
            id="mice-cards",
            class_="card-grid"
        ),
        class_="column"
    )


def try_column(try_cards: List[Dict[str, Any]]) -> air.Tag:
    """Render the Try/Fail cards column"""
    return air.Div(
        air.H2("Try/Fail Cycles"),
        air.Button("+ Add Try Card", id="add-try-btn", class_="btn-primary add-card-btn", onclick="showTryForm()"),
        air.Div(
            air.Form(
                air.Div(
                    air.Label("Cycle Type", for_="type"),
                    air.Select(
                        air.Option("Select type...", value=""),
                        air.Option("Escalation (No, AND)", value="Escalation (No, AND)"),
                        air.Option("Complication (Yes, BUT)", value="Complication (Yes, BUT)"),
                        air.Option("Revelation (No, BUT)", value="Revelation (No, BUT)"),
                        air.Option("Resolution (Yes, AND)", value="Resolution (Yes, AND)"),
                        id="type", name="type", required=True
                    ),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Order Number", for_="order_num"),
                    air.Input(type="number", id="order_num", name="order_num", min="1", value=str(len(try_cards) + 1), required=True),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Attempt", for_="attempt"),
                    air.Textarea(id="attempt", name="attempt", required=True, placeholder="What does the character try?"),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Outcome", for_="failure"),
                    air.Textarea(id="failure", name="failure", required=True, placeholder="What actually happens?"),
                    class_="form-group"
                ),
                air.Div(
                    air.Label("Consequence", for_="consequence"),
                    air.Textarea(id="consequence", name="consequence", required=True, placeholder="What is the result or learning?"),
                    class_="form-group"
                ),
                air.Div(
                    air.Button("Save Card", type="submit", class_="btn-primary"),
                    air.Button("Cancel", type="button", class_="btn-secondary", onclick="hideTryForm()"),
                    class_="form-actions"
                ),
                id="try-card-form",
                onsubmit="submitTryCard(event)"
            ),
            id="try-form",
            class_="card-form hidden"
        ),
        air.Div(
            *[try_card_component(card) for card in try_cards] if try_cards else [air.Div("No Try/Fail cycles yet. Add one to build your Act 2!", class_="empty-state")],
            id="try-cards",
            class_="card-grid"
        ),
        class_="column"
    )


def outline_column(mice_cards: List[Dict[str, Any]], try_cards: List[Dict[str, Any]]) -> air.Tag:
    """Render the story outline column"""
    return air.Div(
        air.H2("Story Outline"),
        air.Div(
            air.H3("Nesting Structure"),
            build_nesting_diagram(mice_cards) if mice_cards else air.Div("Add MICE cards to see structure", class_="empty-state"),
            class_="nesting-diagram"
        ),
        air.Div(
            air.H3("Story Flow"),
            build_story_flow(mice_cards, try_cards) if mice_cards or try_cards else air.Div("Add cards to see story flow", class_="empty-state"),
            class_="story-flow"
        ),
        class_="column"
    )
