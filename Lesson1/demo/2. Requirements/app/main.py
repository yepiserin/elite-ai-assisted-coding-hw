import air
from fastapi import Form, FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import database
from typing import Dict, Any, List
import google.generativeai as genai
import os
import markdown

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

def build_nesting_diagram(mice_cards: List[Dict[str, Any]]) -> air.Tag:
    type_names = {'M': 'Milieu', 'I': 'Inquiry', 'C': 'Character', 'E': 'Event'}

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
    type_names = {'M': 'Milieu', 'I': 'Inquiry', 'C': 'Character', 'E': 'Event'}

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

def try_card_component(card: Dict[str, Any], total_cards: int) -> air.Tag:
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
            air.Span(
                air.Button("↑", class_="btn-move", hx_post=f"/api/try-cards/{card['id']}/move-up", hx_swap="none", hx_trigger="click", disabled=card['order_num'] == 1) if card['order_num'] > 1 else air.Span(""),
                air.Button("↓", class_="btn-move", hx_post=f"/api/try-cards/{card['id']}/move-down", hx_swap="none", hx_trigger="click", disabled=card['order_num'] == total_cards) if card['order_num'] < total_cards else air.Span(""),
                class_="move-controls"
            ),
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
        air.Div(
            air.Button("Edit", class_="btn-secondary", onclick=f"editTryCard({card['id']}, '{card['type']}', `{card['attempt']}`, `{card['failure']}`, `{card['consequence']}`, {card['order_num']})"),
            air.Button("Delete", class_="btn-danger", onclick=f"deleteTryCard({card['id']})"),
            class_="card-actions"
        ),
        class_="card try-card",
        id=f"try-card-{card['id']}"
    )

@app.get("/")
def index():
    mice_cards = database.get_mice_cards()
    try_cards = database.get_try_cards()

    return air.Html(
        air.Head(
            air.Title("Story Builder - MICE Quotient"),
            air.Link(rel="stylesheet", href="/static/styles.css"),
            air.Script(src="https://unpkg.com/htmx.org@1.9.10"),
            air.Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3/dist/zero-md.min.js"),
            air.Script(src="/static/app.js", defer=True)
        ),
        air.Body(
            air.H1("Story Builder with MICE Quotient"),
            air.Div(
                air.Button("Seed Sample Data", hx_post="/api/seed-data", hx_swap="none", class_="btn-primary"),
                air.Button("Clear All Data", onclick="clearAllData()", class_="btn-danger", style="margin-left: 10px;"),
                air.Button("📚 MICE Theory", onclick="toggleTheoryPanel()", class_="btn-secondary", style="margin-left: 10px;"),
                style="text-align: center; margin-bottom: 20px;"
            ),
            air.Div(
                air.Div(
                    air.H2("MICE Quotient Framework"),
                    air.P("Stories are built from four fundamental narrative threads that open and close in nested order:"),

                    air.Div(
                        air.Div(
                            air.H3("M - Milieu", class_="theory-header M"),
                            air.P("Stories about exploring a place or setting"),
                            air.P("Opens: Character enters a new world", style="font-style: italic;"),
                            air.P("Closes: Character leaves that world", style="font-style: italic;"),
                            air.P("Example: Lord of the Rings (Frodo enters Middle Earth, leaves the Shire)", style="color: #666;"),
                            class_="theory-card"
                        ),
                        air.Div(
                            air.H3("I - Inquiry", class_="theory-header I"),
                            air.P("Stories driven by seeking answers to questions"),
                            air.P("Opens: A question is raised", style="font-style: italic;"),
                            air.P("Closes: The question is answered", style="font-style: italic;"),
                            air.P("Example: Murder mysteries (Who did it? → The killer is revealed)", style="color: #666;"),
                            class_="theory-card"
                        ),
                        air.Div(
                            air.H3("C - Character", class_="theory-header C"),
                            air.P("Stories about personal transformation"),
                            air.P("Opens: Character is dissatisfied with their role", style="font-style: italic;"),
                            air.P("Closes: Character accepts or changes their role", style="font-style: italic;"),
                            air.P("Example: A Christmas Carol (Scrooge is miserly → becomes generous)", style="color: #666;"),
                            class_="theory-card"
                        ),
                        air.Div(
                            air.H3("E - Event", class_="theory-header E"),
                            air.P("Stories about external conflicts and actions"),
                            air.P("Opens: The world falls out of order", style="font-style: italic;"),
                            air.P("Closes: Order is restored (or new order established)", style="font-style: italic;"),
                            air.P("Example: Die Hard (terrorists take building → hero defeats them)", style="color: #666;"),
                            class_="theory-card"
                        ),
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
            ),
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
                        *[try_card_component(card, len(try_cards)) for card in try_cards] if try_cards else [air.Div("No Try/Fail cycles yet. Add one to build your Act 2!", class_="empty-state")],
                        id="try-cards",
                        class_="card-grid"
                    ),
                    class_="column"
                ),
                # Right Column: Story Outline
                air.Div(
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
                ),
                class_="container"
            ),
            # AI-Generated Outline (full width below)
            air.Div(
                air.H2("AI-Generated Outline"),
                air.Button("Generate Outline", hx_post="/api/generate-outline", hx_target="#ai-outline-content", hx_swap="innerHTML", class_="btn-primary", style="margin-bottom: 15px;"),
                air.Div(id="ai-outline-content", class_="empty-state", content="Click 'Generate Outline' to create a prose outline"),
                style="max-width: 1800px; margin: 30px auto; background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
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

@app.put("/api/mice-cards/{card_id}")
def update_mice_card(
    card_id: int,
    code: str = Form(...),
    opening: str = Form(...),
    closing: str = Form(...),
    nesting_level: int = Form(...)
):
    database.update_mice_card(card_id, code, opening, closing, nesting_level)
    return {"success": True}

@app.delete("/api/mice-cards/{card_id}")
def delete_mice_card(card_id: int):
    database.delete_mice_card(card_id)
    return {"success": True}

@app.post("/api/try-cards")
def create_try_card(
    type: str = Form(...),
    attempt: str = Form(...),
    failure: str = Form(...),
    consequence: str = Form(...),
    order_num: int = Form(...)
):
    card_id = database.add_try_card(type, attempt, failure, consequence, order_num)
    return {"id": card_id, "success": True}

@app.put("/api/try-cards/{card_id}")
def update_try_card(
    card_id: int,
    type: str = Form(...),
    attempt: str = Form(...),
    failure: str = Form(...),
    consequence: str = Form(...),
    order_num: int = Form(...)
):
    database.update_try_card(card_id, type, attempt, failure, consequence, order_num)
    return {"success": True}

@app.delete("/api/try-cards/{card_id}")
def delete_try_card(card_id: int):
    database.delete_try_card(card_id)
    return {"success": True}

@app.post("/api/try-cards/{card_id}/move-up")
def move_try_card_up(card_id: int):
    conn = database.get_db()
    cursor = conn.cursor()

    # Get current card
    cursor.execute("SELECT order_num FROM try_cards WHERE id = ?", (card_id,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return {"success": False}

    current_order = result[0]

    # Swap with card above
    cursor.execute("SELECT id FROM try_cards WHERE order_num = ?", (current_order - 1,))
    above_card = cursor.fetchone()

    if above_card:
        cursor.execute("UPDATE try_cards SET order_num = ? WHERE id = ?", (current_order, above_card[0]))
        cursor.execute("UPDATE try_cards SET order_num = ? WHERE id = ?", (current_order - 1, card_id))
        conn.commit()

    conn.close()
    return air.Script("window.location.reload()")

@app.post("/api/try-cards/{card_id}/move-down")
def move_try_card_down(card_id: int):
    conn = database.get_db()
    cursor = conn.cursor()

    # Get current card
    cursor.execute("SELECT order_num FROM try_cards WHERE id = ?", (card_id,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return {"success": False}

    current_order = result[0]

    # Swap with card below
    cursor.execute("SELECT id FROM try_cards WHERE order_num = ?", (current_order + 1,))
    below_card = cursor.fetchone()

    if below_card:
        cursor.execute("UPDATE try_cards SET order_num = ? WHERE id = ?", (current_order, below_card[0]))
        cursor.execute("UPDATE try_cards SET order_num = ? WHERE id = ?", (current_order + 1, card_id))
        conn.commit()

    conn.close()
    return air.Script("window.location.reload()")

@app.post("/api/seed-data")
def seed_sample_data():
    database.clear_all_data()

    # Sample MICE cards
    database.add_mice_card("M", "Emma arrives at Camp Pinewood for the first time", "Emma leaves camp, confident in her new friendships", 1)
    database.add_mice_card("C", "Emma is shy and struggles to make friends", "Emma has grown into a confident, outgoing person", 2)
    database.add_mice_card("I", "How will Emma overcome her fear of speaking up?", "Emma discovers that vulnerability creates connection", 3)

    # Sample Try/Fail cycles
    database.add_try_card("Escalation (No, AND)", "Emma tries to join a group activity but freezes up", "She backs away and the other kids notice her awkwardness", "Emma feels even more isolated and considers calling her parents", 1)
    database.add_try_card("Complication (Yes, BUT)", "Emma forces herself to sit with others at lunch", "They accept her but the conversation is superficial", "Emma realizes she needs to be authentic, not just present", 2)
    database.add_try_card("Resolution (Yes, AND)", "Emma shares her honest feelings during campfire", "The other kids open up too, creating real bonds", "Emma discovers the power of vulnerability and connection", 3)

    return air.Script("window.location.reload()")

@app.post("/api/clear-data")
def clear_data():
    database.clear_all_data()
    return {"success": True}

@app.post("/api/generate-outline")
def generate_outline():
    mice_cards = database.get_mice_cards()
    try_cards = database.get_try_cards()

    if not mice_cards and not try_cards:
        return air.Div("Please add some cards first before generating an outline.", class_="empty-state")

    # Configure Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return air.Div("Error: GEMINI_API_KEY environment variable not set", style="color: red; padding: 15px;")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")

    # Build prompt
    prompt = "You are a story writing assistant. Generate a detailed prose outline based on the following MICE Quotient structure:\n\n"

    if mice_cards:
        prompt += "MICE CARDS:\n"
        for card in sorted(mice_cards, key=lambda x: x['nesting_level']):
            prompt += f"- Level {card['nesting_level']} {card['code']}: Opens with '{card['opening']}' and closes with '{card['closing']}'\n"

    if try_cards:
        prompt += "\nTRY/FAIL CYCLES:\n"
        for card in sorted(try_cards, key=lambda x: x['order_num']):
            prompt += f"- #{card['order_num']} ({card['type']}): {card['attempt']} → {card['failure']} → {card['consequence']}\n"

    prompt += "\nGenerate a cohesive story outline in prose format that weaves these elements together. Structure it with Act 1 (openings), Act 2 (try/fail cycles), and Act 3 (closings). Make it compelling and narrative."

    # Generate response
    response = model.generate_content(prompt)

    # Convert markdown to HTML
    html_content = markdown.markdown(response.text)

    # Return HTML using Raw to render the HTML string
    return air.Div(
        air.Raw(html_content),
        style="background: #f9f9f9; padding: 15px; border-radius: 6px; border: 1px solid #ddd; line-height: 1.6;"
    )


