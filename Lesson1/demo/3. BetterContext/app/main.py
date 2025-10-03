import air
from fastapi import Form, Response
from sqlmodel import SQLModel, Session, create_engine, select
from models import MiceCard, TryCard
from layouts import story_builder_layout

# Database setup
DATABASE_URL = "sqlite:///story_builder.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

# Initialize database on startup
init_db()

app = air.Air()

@app.get("/")
def index():
    with Session(engine) as session:
        mice_cards = session.exec(select(MiceCard)).all()
        try_cards = session.exec(select(TryCard).order_by(TryCard.order_num)).all()

        return story_builder_layout(
            air.Title("Story Builder"),
            air.Div(
                air.Button(
                    "Templates",
                    class_="btn btn-info mr-2",
                    onclick="document.getElementById('templates-modal').showModal()"
                ),
                air.Button(
                    "Clear All Data",
                    class_="btn btn-error",
                    hx_post="/clear-data",
                    hx_target="body",
                    hx_swap="outerHTML",
                    hx_confirm="Are you sure you want to delete all cards? This cannot be undone."
                ),
                class_="mb-4"
            ),
            air.Dialog(
                air.Div(
                    air.H3("Story Templates", class_="text-2xl font-bold mb-4"),
                    air.P("Choose a template to get started with a pre-built story structure:", class_="mb-4"),
                    air.Div(
                        air.Button(
                            air.H4("🔍 Mystery", class_="text-xl font-bold mb-2"),
                            air.P("A detective investigates a murder in a small town", class_="text-sm"),
                            class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
                            hx_post="/load-template/mystery",
                            hx_target="body",
                            hx_swap="outerHTML",
                            onclick="document.getElementById('templates-modal').close()"
                        ),
                        air.Button(
                            air.H4("🗺️ Adventure", class_="text-xl font-bold mb-2"),
                            air.P("A hero embarks on a quest to save their homeland", class_="text-sm"),
                            class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
                            hx_post="/load-template/adventure",
                            hx_target="body",
                            hx_swap="outerHTML",
                            onclick="document.getElementById('templates-modal').close()"
                        ),
                        air.Button(
                            air.H4("💕 Romance", class_="text-xl font-bold mb-2"),
                            air.P("Two people find love against all odds", class_="text-sm"),
                            class_="btn btn-outline w-full text-left h-auto py-4 mb-3",
                            hx_post="/load-template/romance",
                            hx_target="body",
                            hx_swap="outerHTML",
                            onclick="document.getElementById('templates-modal').close()"
                        ),
                    ),
                    air.Button(
                        "Cancel",
                        class_="btn btn-ghost mt-2",
                        onclick="document.getElementById('templates-modal').close()"
                    ),
                    class_="modal-box"
                ),
                id="templates-modal",
                class_="modal"
            ),
            air.Div(
                air.Div(
                    air.Button(
                        "📚 What is MICE Quotient?",
                        class_="btn btn-sm btn-outline w-full text-left",
                        onclick="const el = document.getElementById('mice-help'); el.style.display = el.style.display === 'none' ? 'block' : 'none';"
                    ),
                    class_="mb-2"
                ),
                air.Div(
                    air.H3("MICE Quotient Story Structure", class_="text-xl font-bold mb-3"),
                    air.P("The MICE Quotient is a plotting technique by Orson Scott Card, enhanced by Mary Robinette Kowal. Each letter represents a promise you make to your reader:", class_="mb-3"),
                    air.Div(
                        air.Div(
                            air.H4("M - Milieu", class_="font-bold text-lg mb-1 text-blue-700"),
                            air.P("Environment, setting, atmosphere", class_="text-sm mb-1"),
                            air.P("Example: Character enters a new world → explores → leaves", class_="text-xs italic text-gray-600"),
                            class_="bg-blue-100 border-l-4 border-blue-300 p-3 rounded"
                        ),
                        air.Div(
                            air.H4("I - Idea", class_="font-bold text-lg mb-1 text-green-700"),
                            air.P("Question, mystery", class_="text-sm mb-1"),
                            air.P("Example: A question is posed → investigated → answered", class_="text-xs italic text-gray-600"),
                            class_="bg-green-100 border-l-4 border-green-300 p-3 rounded"
                        ),
                        air.Div(
                            air.H4("C - Character", class_="font-bold text-lg mb-1 text-yellow-700"),
                            air.P("Internal problems, goals, change", class_="text-sm mb-1"),
                            air.P("Example: Character is dissatisfied → struggles → transforms", class_="text-xs italic text-gray-600"),
                            class_="bg-yellow-100 border-l-4 border-yellow-300 p-3 rounded"
                        ),
                        air.Div(
                            air.H4("E - Event", class_="font-bold text-lg mb-1 text-purple-700"),
                            air.P("External problems, catastrophes", class_="text-sm mb-1"),
                            air.P("Example: World order disrupted → crisis → new order restored", class_="text-xs italic text-gray-600"),
                            class_="bg-purple-100 border-l-4 border-purple-300 p-3 rounded"
                        ),
                        class_="grid grid-cols-2 gap-3 mb-4"
                    ),
                    air.H4("Nesting Structure", class_="font-bold text-lg mb-2"),
                    air.P("Act 1 mirrors Act 3 in opposite order - like boxes within boxes. Open them in order 1→2→3→4, then close them in reverse 4→3→2→1. This creates satisfying symmetry!", class_="mb-3 text-sm"),
                    air.H4("Try/Fail Cycles (Act 2)", class_="font-bold text-lg mb-2"),
                    air.P("Between setup and resolution, your character tries to achieve their goal and fails repeatedly. Each failure raises tension and makes the eventual success more satisfying. Common types:", class_="mb-2 text-sm"),
                    air.Ul(
                        air.Li("Success: Small win, but problem isn't solved", class_="text-sm"),
                        air.Li("Failure: Clear setback", class_="text-sm"),
                        air.Li("Trade-off: Win something, lose something else", class_="text-sm"),
                        air.Li("Moral: Success but at a cost to character's values", class_="text-sm"),
                        class_="list-disc list-inside mb-3"
                    ),
                    id="mice-help",
                    class_="bg-base-200 p-4 rounded mb-4",
                    style="display: none;"
                ),
                class_="mb-4"
            ),
            air.Div(
                air.Div(
                    air.H2("MICE Cards", class_="text-2xl font-bold mb-4"),
                    air.Button(
                        "Add MICE Card",
                        class_="btn btn-primary mb-3",
                        hx_get="/mice-form",
                        hx_target="#mice-form-container",
                        hx_swap="innerHTML"
                    ),
                    air.Div(id="mice-form-container"),
                    air.Div(
                        *[_render_mice_card(card) for card in mice_cards],
                        class_="flex flex-col gap-3",
                        id="mice-cards-list"
                    ),
                    class_="border border-base-300 p-4"
                ),
                air.Div(
                    air.H2("Try/Fail Cycles", class_="text-2xl font-bold mb-4"),
                    air.Button(
                        "Add Try Card",
                        class_="btn btn-primary mb-3",
                        hx_get="/try-form",
                        hx_target="#try-form-container",
                        hx_swap="innerHTML"
                    ),
                    air.Div(id="try-form-container"),
                    air.Div(
                        *[_render_try_card(card) for card in try_cards],
                        class_="flex flex-col gap-3",
                        id="try-cards-list"
                    ),
                    class_="border border-base-300 p-4"
                ),
                air.Div(
                    air.H2("Generated Outline", class_="text-2xl font-bold mb-4"),
                    air.H3("Nesting Structure", class_="text-lg font-semibold mb-2"),
                    _render_nesting_diagram(mice_cards),
                    air.H3("Story Timeline", class_="text-lg font-semibold mb-2 mt-6"),
                    _render_story_timeline(mice_cards, try_cards),
                    class_="border border-base-300 p-4"
                ),
                class_="grid grid-cols-3 gap-4 w-full"
            )
        )

def _info_row(label, value):
    return air.Div(
        air.Span(label, class_="font-bold"),
        air.Span(f" {value}"),
        class_="mb-2"
    )

def _get_mice_color(code: str) -> str:
    colors = {
        "M": "bg-blue-100 border-blue-300",
        "I": "bg-green-100 border-green-300",
        "C": "bg-yellow-100 border-yellow-300",
        "E": "bg-purple-100 border-purple-300"
    }
    return colors.get(code, "bg-gray-100 border-gray-300")


def _get_try_color(cycle_type: str) -> str:
    colors = {
        "Success": "bg-green-100 border-green-300",
        "Failure": "bg-red-100 border-red-300",
        "Trade-off": "bg-orange-100 border-orange-300",
        "Moral": "bg-blue-100 border-blue-300"
    }
    return colors.get(cycle_type, "bg-gray-100 border-gray-300")

def _render_nesting_diagram(mice_cards):
    """Render nested boxes showing MICE card structure by nesting level."""
    if not mice_cards:
        return air.Div("No MICE cards to display", class_="text-gray-500 italic")

    # Sort by nesting level
    sorted_cards = sorted(mice_cards, key=lambda c: c.nesting_level)

    def render_nested_card(card, level):
        """Render a single card with appropriate nesting indentation."""
        indent = (level - 1) * 20  # 20px per level
        return air.Div(
            air.Div(
                air.Span(f"{card.code}", class_=f"font-bold mr-2"),
                air.Span(f"Level {card.nesting_level}", class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("↓ ", class_="text-green-600 font-bold"),
                air.Span(card.opening, class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("↑ ", class_="text-purple-600 font-bold"),
                air.Span(card.closing, class_="text-xs"),
            ),
            class_=f"border-l-4 pl-2 mb-2 {_get_mice_color(card.code).replace('bg-', 'border-')}",
            style=f"margin-left: {indent}px;"
        )

    return air.Div(
        *[render_nested_card(card, card.nesting_level) for card in sorted_cards],
        class_="bg-base-100 p-3 rounded"
    )

def _render_story_timeline(mice_cards, try_cards):
    """Render three-act story timeline."""
    sorted_mice = sorted(mice_cards, key=lambda c: c.nesting_level)
    sorted_tries = sorted(try_cards, key=lambda c: c.order_num)

    # Act 1: MICE openings in nesting order
    act1_items = [
        air.Li(
            air.Span(f"{card.code}: ", class_="font-bold"),
            air.Span(card.opening, class_="text-sm")
        )
        for card in sorted_mice
    ]

    # Act 2: Try/Fail cycles with all fields
    act2_items = [
        air.Li(
            air.Div(
                air.Span(f"{card.type} #{card.order_num}", class_="font-bold text-sm"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Attempt: ", class_="font-bold text-xs"),
                air.Span(card.attempt, class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Failure: ", class_="font-bold text-xs"),
                air.Span(card.failure, class_="text-xs"),
                class_="mb-1"
            ),
            air.Div(
                air.Span("Consequence: ", class_="font-bold text-xs"),
                air.Span(card.consequence, class_="text-xs")
            ),
            class_="mb-3"
        )
        for card in sorted_tries
    ]

    # Act 3: MICE closings in reverse order
    act3_items = [
        air.Li(
            air.Span(f"{card.code}: ", class_="font-bold"),
            air.Span(card.closing, class_="text-sm")
        )
        for card in reversed(sorted_mice)
    ]

    return air.Div(
        air.Div(
            air.H4("Act 1: Setup", class_="font-bold text-green-700 mb-2"),
            air.Ul(*act1_items, class_="list-disc list-inside space-y-1") if act1_items else air.P("No openings", class_="text-gray-500 italic text-sm"),
            class_="bg-green-50 p-3 rounded mb-3"
        ),
        air.Div(
            air.H4("Act 2: Confrontation", class_="font-bold text-blue-700 mb-2"),
            air.Ul(*act2_items, class_="list-disc list-inside space-y-1") if act2_items else air.P("No try/fail cycles", class_="text-gray-500 italic text-sm"),
            class_="bg-blue-50 p-3 rounded mb-3"
        ),
        air.Div(
            air.H4("Act 3: Resolution", class_="font-bold text-purple-700 mb-2"),
            air.Ul(*act3_items, class_="list-disc list-inside space-y-1") if act3_items else air.P("No closings", class_="text-gray-500 italic text-sm"),
            class_="bg-purple-50 p-3 rounded"
        ),
        class_="mt-4"
    )

def _get_try_tooltip(cycle_type: str) -> str:
    """Get tooltip text for Try/Fail card type."""
    tooltips = {
        "Success": "Yes, but... - Character succeeds at immediate goal but the larger problem persists. Example: Hero defeats minion but villain escapes.",
        "Failure": "No, and... - Character fails and situation worsens. Example: Detective's suspect has alibi AND another murder occurs.",
        "Trade-off": "Yes, but at a cost - Character wins something but loses something else. Example: Hero saves city but loses their powers.",
        "Moral": "Success with ethical compromise - Character succeeds but violates their values. Example: Detective catches killer by breaking the law."
    }
    return tooltips.get(cycle_type, "")

def _render_try_card(card: TryCard):
    return air.Div(
        air.Div(
            air.Span(f"{card.type} #{card.order_num}", class_="font-bold tooltip", data_tip=_get_try_tooltip(card.type)),
            class_="mb-2"
        ),
        air.Div(
            air.Span("Attempt: ", class_="font-bold text-xs"),
            air.Span(card.attempt, class_="text-xs"),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Failure: ", class_="font-bold text-xs"),
            air.Span(card.failure, class_="text-xs"),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Consequence: ", class_="font-bold text-xs"),
            air.Span(card.consequence, class_="text-xs"),
            class_="mb-2"
        ),
        air.Div(
            air.Button(
                "Edit",
                class_="btn btn-xs btn-primary mr-2",
                hx_get=f"/try-edit/{card.id}",
                hx_target=f"#try-card-{card.id}",
                hx_swap="outerHTML"
            ),
            air.Button(
                "Delete",
                class_="btn btn-xs btn-error",
                hx_delete=f"/try-cards/{card.id}",
                hx_target="body",
                hx_swap="outerHTML",
                hx_confirm="Are you sure you want to delete this Try card?"
            ),
            class_="flex gap-2"
        ),
        class_=f"card border-2 p-3 {_get_try_color(card.type)}",
        style="height: auto; max-height: 250px; overflow-auto;",
        id=f"try-card-{card.id}"
    )

def _get_mice_tooltip(code: str) -> str:
    """Get tooltip text for MICE card type."""
    tooltips = {
        "M": "Milieu: Story about a place/environment. Character enters → explores → leaves. Example: Alice falls down rabbit hole, explores Wonderland, returns home.",
        "I": "Idea: Story about a question/mystery. Question posed → investigated → answered. Example: Whodunit mystery starts with murder, detective investigates, reveals killer.",
        "C": "Character: Story about internal change. Character dissatisfied → struggles → transforms. Example: Scrooge is miserly, faces ghosts, becomes generous.",
        "E": "Event: Story about external problem. World order disrupted → crisis → new order. Example: Alien invasion threatens Earth, heroes fight back, peace restored."
    }
    return tooltips.get(code, "")

def _render_mice_card(card: MiceCard):
    def _info_span(icon: str, text: str, extra_class: str = ""):
        return air.Div(
            air.Span(icon, class_="font-bold"),
            air.Span(text),
            class_=f"mb-2 text-sm {extra_class}"
        )

    return air.Div(
        air.Div(
            air.Span(f"{card.code}", class_="text-lg font-bold tooltip tooltip-right", data_tip=_get_mice_tooltip(card.code)),
            air.Span(f" Level {card.nesting_level}", class_="text-sm"),
            class_="mb-2"
        ),
        _info_span("↓ ", card.opening),
        _info_span("↑ ", card.closing),
        air.Div(
            air.Button(
                "Edit",
                class_="btn btn-xs btn-primary mr-1",
                hx_get=f"/mice-edit/{card.id}",
                hx_target=f"#mice-card-{card.id}",
                hx_swap="outerHTML"
            ),
            air.Button(
                "Delete",
                class_="btn btn-xs btn-error",
                hx_delete=f"/mice-cards/{card.id}",
                hx_target=f"#mice-card-{card.id}",
                hx_swap="outerHTML"
            ),
            class_="mt-2"
        ),
        class_=f"card border-2 p-3 {_get_mice_color(card.code)}",
        style="height: auto; min-height: 200px;",
        id=f"mice-card-{card.id}"
    )

@app.get("/mice-form")
def mice_form():
    return air.Form(
        air.Div(
            air.Label("Type:", class_="label"),
            air.Select(
                air.Option("Milieu", value="M"),
                air.Option("Idea", value="I"),
                air.Option("Character", value="C"),
                air.Option("Event", value="E"),
                name="code",
                class_="select select-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Opening:", class_="label"),
            air.Textarea(
                name="opening",
                class_="textarea textarea-bordered w-full mb-2",
                rows="3"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Closing:", class_="label"),
            air.Textarea(
                name="closing",
                class_="textarea textarea-bordered w-full mb-2",
                rows="3"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Nesting Level:", class_="label"),
            air.Input(
                type="number",
                name="nesting_level",
                value="1",
                class_="input input-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Button(
            "Save",
            type="submit",
            class_="btn btn-success mr-2"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_="btn btn-ghost",
            hx_get="/clear-form",
            hx_target="#mice-form-container",
            hx_swap="innerHTML"
        ),
        hx_post="/mice-cards",
        hx_target="body",
        hx_swap="outerHTML",
        class_="card bg-base-100 shadow-lg p-4 mb-3"
    )

@app.get("/clear-form")
def clear_form():
    return ""

@app.get("/try-form")
def try_form():
    return air.Form(
        air.Div(
            air.Label("Cycle Type:", class_="label"),
            air.Select(
                air.Option("Success", value="Success"),
                air.Option("Failure", value="Failure"),
                air.Option("Trade-off", value="Trade-off"),
                air.Option("Moral", value="Moral"),
                name="type",
                class_="select select-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Order Number:", class_="label"),
            air.Input(
                type="number",
                name="order_num",
                value="1",
                class_="input input-bordered w-full mb-2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Attempt:", class_="label"),
            air.Textarea(
                name="attempt",
                class_="textarea textarea-bordered w-full mb-2",
                rows="2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Failure:", class_="label"),
            air.Textarea(
                name="failure",
                class_="textarea textarea-bordered w-full mb-2",
                rows="2"
            ),
            class_="form-control"
        ),
        air.Div(
            air.Label("Consequence:", class_="label"),
            air.Textarea(
                name="consequence",
                class_="textarea textarea-bordered w-full mb-2",
                rows="2"
            ),
            class_="form-control"
        ),
        air.Button(
            "Save",
            type="submit",
            class_="btn btn-success mr-2"
        ),
        air.Button(
            "Cancel",
            type="button",
            class_="btn btn-ghost",
            hx_get="/clear-try-form",
            hx_target="#try-form-container",
            hx_swap="innerHTML"
        ),
        hx_post="/try-cards",
        hx_target="body",
        hx_swap="outerHTML",
        class_="card bg-base-100 shadow-lg p-4 mb-3"
    )

@app.get("/clear-try-form")
def clear_try_form():
    return ""

@app.post("/try-cards")
def create_try_card(
    type: str = Form(...),
    order_num: int = Form(...),
    attempt: str = Form(...),
    failure: str = Form(...),
    consequence: str = Form(...)
):
    with Session(engine) as session:
        try_card = TryCard(
            type=type,
            order_num=order_num,
            attempt=attempt,
            failure=failure,
            consequence=consequence
        )
        session.add(try_card)
        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})


@app.post("/clear-data")
def clear_data():
    with Session(engine) as session:
        # Delete all MICE cards
        for card in session.exec(select(MiceCard)):
            session.delete(card)
        # Delete all Try cards
        for card in session.exec(select(TryCard)):
            session.delete(card)
        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.post("/load-template/mystery")
def load_template_mystery():
    with Session(engine) as session:
        # Clear existing data
        for card in session.exec(select(MiceCard)):
            session.delete(card)
        for card in session.exec(select(TryCard)):
            session.delete(card)

        # Create Mystery template MICE cards
        mice_cards_data = [
            {"code": "M", "opening": "Detective arrives in fog-shrouded coastal town where everyone seems suspicious", "closing": "Detective leaves the town, now peaceful and welcoming, mystery solved", "nesting_level": 1},
            {"code": "I", "opening": "Who killed the wealthy lighthouse keeper? Why was the body moved?", "closing": "The killer was the keeper's business partner, hiding embezzlement scheme", "nesting_level": 2},
            {"code": "C", "opening": "Detective haunted by unsolved case from her past, struggles to trust her instincts", "closing": "Detective learns to trust herself again, finds closure on both cases", "nesting_level": 3},
            {"code": "E", "opening": "Hurricane warning issued - all evidence must be gathered before evacuation", "closing": "Hurricane passes, evidence preserved, arrest made just in time", "nesting_level": 4},
        ]

        for data in mice_cards_data:
            session.add(MiceCard(**data))

        # Create Mystery template Try/Fail cycles
        try_cards_data = [
            {"type": "Success", "order_num": 1, "attempt": "Detective interviews all townspeople for alibis", "failure": "Everyone has an alibi, but stories have inconsistencies", "consequence": "Realizes someone is lying, narrows suspects to three people"},
            {"type": "Failure", "order_num": 2, "attempt": "Searches lighthouse for physical evidence before storm", "failure": "Storm hits early, evidence washed away by flooding", "consequence": "Must rely on testimonies and deduction instead of forensics"},
            {"type": "Trade-off", "order_num": 3, "attempt": "Confronts prime suspect publicly to force confession", "failure": "Suspect denies everything, town turns against detective", "consequence": "Gains access to suspect's financial records in the chaos"},
        ]

        for data in try_cards_data:
            session.add(TryCard(**data))

        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.post("/load-template/adventure")
def load_template_adventure():
    with Session(engine) as session:
        # Clear existing data
        for card in session.exec(select(MiceCard)):
            session.delete(card)
        for card in session.exec(select(TryCard)):
            session.delete(card)

        # Create Adventure template MICE cards
        mice_cards_data = [
            {"code": "M", "opening": "Hero leaves peaceful village to journey through dangerous enchanted forest", "closing": "Hero returns home victorious, village saved and celebrating", "nesting_level": 1},
            {"code": "I", "opening": "What ancient artifact can defeat the dragon threatening the kingdom?", "closing": "The artifact is the hero's family heirloom - a dragon-forged blade", "nesting_level": 2},
            {"code": "C", "opening": "Reluctant hero doubts their worthiness, fears they'll fail like their father", "closing": "Hero accepts their destiny, realizes courage isn't absence of fear", "nesting_level": 3},
            {"code": "E", "opening": "Dragon awakens early, attacks begin - kingdom will fall in seven days", "closing": "Dragon defeated, ancient threat ended, peace restored to the land", "nesting_level": 4},
        ]

        for data in mice_cards_data:
            session.add(MiceCard(**data))

        # Create Adventure template Try/Fail cycles
        try_cards_data = [
            {"type": "Success", "order_num": 1, "attempt": "Hero seeks wise hermit's guidance on finding the artifact", "failure": "Hermit speaks only in riddles, no clear answer given", "consequence": "Hero deciphers one clue - must seek the mountain temple"},
            {"type": "Failure", "order_num": 2, "attempt": "Climbs treacherous mountain to reach ancient temple", "failure": "Avalanche destroys path, temple guardian refuses entry", "consequence": "Forced to prove worth through dangerous trial by combat"},
            {"type": "Trade-off", "order_num": 3, "attempt": "Makes bargain with forest spirits for magical protection", "failure": "Protection works but hero owes the spirits a future favor", "consequence": "Gains power needed but at unknown cost to be paid later"},
        ]

        for data in try_cards_data:
            session.add(TryCard(**data))

        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.post("/load-template/romance")
def load_template_romance():
    with Session(engine) as session:
        # Clear existing data
        for card in session.exec(select(MiceCard)):
            session.delete(card)
        for card in session.exec(select(TryCard)):
            session.delete(card)

        # Create Romance template MICE cards
        mice_cards_data = [
            {"code": "M", "opening": "City lawyer forced to spend summer in small coastal town for work", "closing": "Lawyer chooses to stay in the town, makes it her permanent home", "nesting_level": 1},
            {"code": "I", "opening": "Can two people from completely different worlds find common ground?", "closing": "Love transcends backgrounds - they complement each other perfectly", "nesting_level": 2},
            {"code": "C", "opening": "Guarded workaholic afraid to open her heart after painful divorce", "closing": "Learns to trust again, opens herself to love and vulnerability", "nesting_level": 3},
            {"code": "E", "opening": "Town's beloved community center faces demolition - she must defend it", "closing": "Community center saved through partnership, becomes symbol of their love", "nesting_level": 4},
        ]

        for data in mice_cards_data:
            session.add(MiceCard(**data))

        # Create Romance template Try/Fail cycles
        try_cards_data = [
            {"type": "Success", "order_num": 1, "attempt": "She agrees to coffee with handsome local boat captain", "failure": "They argue about city vs. small-town life constantly", "consequence": "Realizes their debates are actually playful chemistry, not conflict"},
            {"type": "Failure", "order_num": 2, "attempt": "Plans romantic beach picnic to show she's changing", "failure": "Storm ruins picnic, she loses composure and pushes him away", "consequence": "He sees her vulnerability for first time, understands her fear"},
            {"type": "Moral", "order_num": 3, "attempt": "Uses legal loophole to save community center temporarily", "failure": "Wins case but betrays town's trust by using manipulative tactics", "consequence": "Must choose between winning and being the person he fell for"},
        ]

        for data in try_cards_data:
            session.add(TryCard(**data))

        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.get("/mice-edit/{card_id}")
def mice_edit(card_id: int):
    with Session(engine) as session:
        card = session.get(MiceCard, card_id)
        if not card:
            return ""

        def _form_field(label, input_element):
            return air.Div(
            air.Label(label, class_="label"),
            input_element,
            class_="form-control"
            )

        return air.Form(
            _form_field(
            "Type:",
            air.Select(
                air.Option("Milieu", value="M", selected=(card.code == "M")),
                air.Option("Idea", value="I", selected=(card.code == "I")),
                air.Option("Character", value="C", selected=(card.code == "C")),
                air.Option("Event", value="E", selected=(card.code == "E")),
                name="code",
                class_="select select-bordered w-full mb-1"
            )
            ),
            _form_field(
            "Opening:",
            air.Textarea(
                card.opening,
                name="opening",
                class_="textarea textarea-bordered w-full mb-1",
                rows="2"
            )
            ),
            _form_field(
            "Closing:",
            air.Textarea(
                card.closing,
                name="closing",
                class_="textarea textarea-bordered w-full mb-1",
                rows="2"
            )
            ),
            _form_field(
            "Nesting Level:",
            air.Input(
                type="number",
                name="nesting_level",
                value=str(card.nesting_level),
                class_="input input-bordered w-full mb-1"
            )
            ),
            air.Button(
            "Save",
            type="submit",
            class_="btn btn-success btn-xs mr-2"
            ),
            air.Button(
            "Cancel",
            type="button",
            class_="btn btn-ghost btn-xs",
            hx_get=f"/mice-card/{card_id}",
            hx_target=f"#mice-card-{card_id}",
            hx_swap="outerHTML"
            ),
            hx_put=f"/mice-cards/{card_id}",
            hx_target=f"#mice-card-{card_id}",
            hx_swap="outerHTML",
            class_=f"card border-2 p-3 {_get_mice_color(card.code)} overflow-auto",
            style="width: 290px; height: auto; max-height: 400px;",
            id=f"mice-card-{card_id}"
        )

@app.get("/mice-card/{card_id}")
def mice_card(card_id: int):
    with Session(engine) as session:
        card = session.get(MiceCard, card_id)
        if not card:
            return ""
        return _render_mice_card(card)

@app.put("/mice-cards/{card_id}")
def update_mice_card(
    card_id: int,
    code: str = Form(...),
    opening: str = Form(...),
    closing: str = Form(...),
    nesting_level: int = Form(...)
):
    with Session(engine) as session:
        card = session.get(MiceCard, card_id)
        if not card:
            return ""

        card.code = code
        card.opening = opening
        card.closing = closing
        card.nesting_level = nesting_level
        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.delete("/mice-cards/{card_id}")
def delete_mice_card(card_id: int):
    with Session(engine) as session:
        card = session.get(MiceCard, card_id)
        if card:
            session.delete(card)
            session.commit()
    return ""

@app.post("/mice-cards")
def create_mice_card(
    code: str = Form(...),
    opening: str = Form(...),
    closing: str = Form(...),
    nesting_level: int = Form(...)
):
    with Session(engine) as session:
        mice_card = MiceCard(
            code=code,
            opening=opening,
            closing=closing,
            nesting_level=nesting_level
        )
        session.add(mice_card)
        session.commit()

    return Response(status_code=200, headers={"HX-Redirect": "/"})

@app.get("/add-sample-mice")
def add_sample_mice():
    with Session(engine) as session:
        mice_card = MiceCard(
            code="M",
            opening="A young girl arrives at summer camp",
            closing="She leaves camp with new friends and confidence",
            nesting_level=1
        )
        session.add(mice_card)
        session.commit()
        session.refresh(mice_card)
        return story_builder_layout(
            air.Title("Sample MICE Card Added"),
            air.Div(
                air.Div(
                    air.H2("Sample MICE Card Added", class_="card-title text-2xl"),
                    class_="card-body"
                ),
                air.Div(
                    _info_row("ID:", mice_card.id),
                    _info_row("Code:", mice_card.code),
                    _info_row("Opening:", mice_card.opening),
                    _info_row("Closing:", mice_card.closing),
                    _info_row("Nesting Level:", mice_card.nesting_level),
                    class_="card-body"
                ),
                class_="card bg-base-100 shadow-xl max-w-4xl mx-auto"
            )
        )

@app.get("/add-sample-try")
def add_sample_try():
    with Session(engine) as session:
        try_card = TryCard(
            type="Success",
            attempt="She tries out for the camp talent show",
            failure="She freezes on stage and forgets her lines",
            consequence="Her cabinmates rally around her and help her practice",
            order_num=1
        )
        session.add(try_card)
        session.commit()
        session.refresh(try_card)


        return story_builder_layout(
            air.Title("Sample Try Card Added"),
            air.Div(
            air.Div(
                air.H2("Sample Try Card Added", class_="card-title text-2xl"),
                class_="card-body"
            ),
            air.Div(
                _info_row("ID:", try_card.id),
                _info_row("Type:", try_card.type),
                _info_row("Attempt:", try_card.attempt),
                _info_row("Failure:", try_card.failure),
                _info_row("Consequence:", try_card.consequence),
                _info_row("Order Number:", try_card.order_num),
                class_="card-body"
            ),
            class_="card bg-base-100 shadow-xl max-w-4xl mx-auto"
            )
        )

@app.get("/try-edit/{card_id}")
def try_edit(card_id: int):
    with Session(engine) as session:
        card = session.get(TryCard, card_id)
        if not card:
            return ""

        def _form_field(label, input_element):
            return air.Div(
                air.Label(label, class_="label"),
                input_element,
                class_="form-control"
            )

        return air.Form(
            _form_field(
                "Type:",
                air.Select(
                    air.Option("Success", value="Success", selected=(card.type == "Success")),
                    air.Option("Failure", value="Failure", selected=(card.type == "Failure")),
                    air.Option("Trade-off", value="Trade-off", selected=(card.type == "Trade-off")),
                    air.Option("Moral", value="Moral", selected=(card.type == "Moral")),
                    name="type",
                    class_="select select-bordered select-sm w-full"
                )
            ),
            _form_field(
                "Order #:",
                air.Input(
                    type="number",
                    name="order_num",
                    value=str(card.order_num),
                    class_="input input-bordered input-sm w-full"
                )
            ),
            _form_field(
                "Attempt:",
                air.Textarea(
                    card.attempt,
                    name="attempt",
                    class_="textarea textarea-bordered textarea-sm w-full",
                    rows="1"
                )
            ),
            _form_field(
                "Failure:",
                air.Textarea(
                    card.failure,
                    name="failure",
                    class_="textarea textarea-bordered textarea-sm w-full",
                    rows="1"
                )
            ),
            _form_field(
                "Consequence:",
                air.Textarea(
                    card.consequence,
                    name="consequence",
                    class_="textarea textarea-bordered textarea-sm w-full",
                    rows="1"
                )
            ),
            air.Div(
                air.Button(
                    "Save",
                    type="submit",
                    class_="btn btn-success btn-xs mr-2"
                ),
                air.Button(
                    "Cancel",
                    type="button",
                    class_="btn btn-ghost btn-xs",
                    hx_get=f"/try-card/{card.id}",
                    hx_target=f"#try-card-{card.id}",
                    hx_swap="outerHTML"
                ),
                class_="mt-2"
            ),
            hx_put=f"/try-cards/{card.id}",
            hx_target=f"#try-card-{card.id}",
            hx_swap="outerHTML",
            class_="card bg-base-100 shadow-lg p-2",
            style="height: auto;",
            id=f"try-card-{card.id}"
        )

@app.get("/try-card/{card_id}")
def get_try_card(card_id: int):
    with Session(engine) as session:
        card = session.get(TryCard, card_id)
        if not card:
            return ""
        return _render_try_card(card)

@app.put("/try-cards/{card_id}")
def update_try_card(
    card_id: int,
    type: str = Form(...),
    order_num: int = Form(...),
    attempt: str = Form(...),
    failure: str = Form(...),
    consequence: str = Form(...)
):
    with Session(engine) as session:
        card = session.get(TryCard, card_id)
        if card:
            card.type = type
            card.order_num = order_num
            card.attempt = attempt
            card.failure = failure
            card.consequence = consequence
            session.add(card)
            session.commit()
            session.refresh(card)
            return _render_try_card(card).render()
    return ""

@app.delete("/try-cards/{card_id}")
def delete_try_card(card_id: int):
    with Session(engine) as session:
        card = session.get(TryCard, card_id)
        if card:
            session.delete(card)
            session.commit()
    return Response(status_code=200, headers={"HX-Redirect": "/"})

