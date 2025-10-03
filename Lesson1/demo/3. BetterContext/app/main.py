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
                    "Seed Sample Data",
                    class_="btn btn-secondary mr-2",
                    hx_post="/seed-data",
                    hx_target="body",
                    hx_swap="outerHTML"
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

def _truncate(text: str, max_length: int = 50) -> str:
    return text[:max_length] + "..." if len(text) > max_length else text

def _get_try_color(cycle_type: str) -> str:
    colors = {
        "Success": "bg-green-100 border-green-300",
        "Failure": "bg-red-100 border-red-300",
        "Trade-off": "bg-orange-100 border-orange-300",
        "Moral": "bg-blue-100 border-blue-300"
    }
    return colors.get(cycle_type, "bg-gray-100 border-gray-300")

def _render_try_card(card: TryCard):
    return air.Div(
        air.Div(
            air.Span(f"{card.type} #{card.order_num}", class_="font-bold"),
            class_="mb-2"
        ),
        air.Div(
            air.Span("Attempt: ", class_="font-bold text-xs"),
            air.Span(_truncate(card.attempt, 40), class_="text-xs"),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Failure: ", class_="font-bold text-xs"),
            air.Span(_truncate(card.failure, 40), class_="text-xs"),
            class_="mb-1"
        ),
        air.Div(
            air.Span("Consequence: ", class_="font-bold text-xs"),
            air.Span(_truncate(card.consequence, 40), class_="text-xs"),
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

def _render_mice_card(card: MiceCard):
    def _info_span(icon: str, text: str, extra_class: str = ""):
        return air.Div(
            air.Span(icon, class_="font-bold"),
            air.Span(_truncate(text)),
            class_=f"mb-2 text-sm {extra_class}"
        )

    return air.Div(
        air.Div(
            air.Span(f"{card.code}", class_="text-lg font-bold"),
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
        style="width: 290px; height: 200px;",
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

@app.post("/seed-data")
def seed_data():
    with Session(engine) as session:
        # Clear existing data
        session.exec(select(MiceCard)).all()
        session.exec(select(TryCard)).all()
        for card in session.exec(select(MiceCard)):
            session.delete(card)
        for card in session.exec(select(TryCard)):
            session.delete(card)

        # Create sample MICE cards at different nesting levels
        mice_cards_data = [
            {"code": "M", "opening": "A detective arrives in a mysterious coastal town", "closing": "She leaves, having solved the mystery and found peace", "nesting_level": 1},
            {"code": "I", "opening": "She discovers the town has a dark secret", "closing": "The truth about the town's past is revealed", "nesting_level": 2},
            {"code": "C", "opening": "She meets a reclusive lighthouse keeper", "closing": "The keeper becomes her trusted ally", "nesting_level": 3},
            {"code": "E", "opening": "A storm traps everyone in the town", "closing": "The storm passes, bringing clarity", "nesting_level": 4},
        ]

        for data in mice_cards_data:
            session.add(MiceCard(**data))

        # Create sample Try/Fail cycles
        try_cards_data = [
            {"type": "Success", "order_num": 1, "attempt": "She interviews the townspeople", "failure": "They all give contradictory stories", "consequence": "She realizes someone is lying"},
            {"type": "Failure", "order_num": 2, "attempt": "She searches the lighthouse at night", "failure": "She gets caught in a trap", "consequence": "The keeper rescues her, earning her trust"},
            {"type": "Trade-off", "order_num": 3, "attempt": "She confronts the mayor publicly", "failure": "It causes panic in the town", "consequence": "But it forces the guilty party to make a mistake"},
        ]

        for data in try_cards_data:
            session.add(TryCard(**data))

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
        session.refresh(card)

        return _render_mice_card(card).render()

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

