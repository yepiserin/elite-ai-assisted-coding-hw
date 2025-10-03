import air
from sqlmodel import SQLModel, Session, create_engine
from models import MiceCard
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
            air.H1("Story Builder", class_="text-4xl font-bold mb-4"),
            air.P(
                air.A("API Docs", target="_blank", href="/api/docs", class_="btn btn-primary")
            ),
            class_="card bg-base-100 shadow-xl p-8 max-w-4xl mx-auto"
        )
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
                    air.Div(
                        air.Span("ID:", class_="font-bold"),
                        air.Span(f" {mice_card.id}"),
                        class_="mb-2"
                    ),
                    air.Div(
                        air.Span("Code:", class_="font-bold"),
                        air.Span(f" {mice_card.code}"),
                        class_="mb-2"
                    ),
                    air.Div(
                        air.Span("Opening:", class_="font-bold"),
                        air.Span(f" {mice_card.opening}"),
                        class_="mb-2"
                    ),
                    air.Div(
                        air.Span("Closing:", class_="font-bold"),
                        air.Span(f" {mice_card.closing}"),
                        class_="mb-2"
                    ),
                    air.Div(
                        air.Span("Nesting Level:", class_="font-bold"),
                        air.Span(f" {mice_card.nesting_level}"),
                        class_="mb-2"
                    ),
                    class_="card-body"
                ),
                class_="card bg-base-100 shadow-xl max-w-4xl mx-auto"
            )
        )


