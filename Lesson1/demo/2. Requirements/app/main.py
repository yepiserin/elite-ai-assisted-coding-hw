import air
from fastapi import Form, FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import database
from typing import Dict, Any

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = air.Air(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def mice_card_component(card: Dict[str, Any]) -> air.Tag:
    type_names = {'M': 'Milieu', 'I': 'Inquiry', 'C': 'Character', 'E': 'Event'}
    return air.Div(
        air.Div(
            f"{card['code']} - {type_names.get(card['code'], '')}",
            class_=f"mice-type {card['code']}"
        ),
        air.Div(
            air.Div(
                air.Strong("Opening:"),
                air.Div(card['opening'], class_="mice-text"),
                class_="mice-opening"
            ),
            air.Div(
                air.Strong("Closing:"),
                air.Div(card['closing'], class_="mice-text"),
                class_="mice-closing"
            ),
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
    type_class = ""
    if 'Escalation' in card['type']:
        type_class = "escalation"
    elif 'Complication' in card['type']:
        type_class = "complication"
    elif 'Revelation' in card['type']:
        type_class = "revelation"
    elif 'Resolution' in card['type']:
        type_class = "resolution"

    return air.Div(
        air.Div(
            f"#{card['order_num']} - {card['type']}",
            class_=f"try-type {type_class}"
        ),
        air.Div(
            air.Strong("Attempt:"),
            air.Div(card['attempt'], class_="try-text"),
            class_="try-field"
        ),
        air.Div(
            air.Strong("Outcome:"),
            air.Div(card['failure'], class_="try-text"),
            class_="try-field"
        ),
        air.Div(
            air.Strong("Consequence:"),
            air.Div(card['consequence'], class_="try-text"),
            class_="try-field"
        ),
        class_="card try-card"
    )

@app.get("/")
def index():
    mice_cards = database.get_mice_cards()
    try_cards = database.get_try_cards()

    return air.Html(
        air.Head(
            air.Title("Story Builder - MICE Quotient"),
            air.Link(rel="stylesheet", href="/static/styles.css"),
            air.Script(src="/static/app.js", defer=True)
        ),
        air.Body(
            air.H1("Story Builder with MICE Quotient"),
            air.Div(
                # Left Column: MICE Cards
                air.Div(
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
                ),
                # Center Column: Try/Fail Cycles
                air.Div(
                    air.H2("Try/Fail Cycles"),
                    air.Div(
                        *[try_card_component(card) for card in try_cards] if try_cards else [air.Div("No Try/Fail cycles yet. Add one to build your Act 2!", class_="empty-state")],
                        id="try-cards",
                        class_="card-grid"
                    ),
                    class_="column"
                ),
                # Right Column: Generated Outline
                air.Div(
                    air.H2("Story Outline"),
                    air.Div("Outline visualization will appear here", class_="empty-state"),
                    class_="column"
                ),
                class_="container"
            )
        )
    )

@app.post("/api/mice-cards")
def create_mice_card(
    code: str = Form(...),
    opening: str = Form(...),
    closing: str = Form(...),
    nesting_level: int = Form(...)
):
    card_id = database.add_mice_card(code, opening, closing, nesting_level)
    return {"id": card_id, "success": True}


