import air
from sqlmodel import SQLModel, Session, create_engine
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
    return story_builder_layout(
        air.Title("Story Builder"),
        air.Div(
            air.Div(
                air.H2("MICE Cards", class_="text-2xl font-bold mb-4"),
                class_="border border-base-300 p-4"
            ),
            air.Div(
                air.H2("Try/Fail Cycles", class_="text-2xl font-bold mb-4"),
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


