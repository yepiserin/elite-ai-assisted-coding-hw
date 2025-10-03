import air
from fastapi import Form, FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import database
from home import home_page

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = air.Air(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    mice_cards = database.get_mice_cards()
    try_cards = database.get_try_cards()
    return home_page(mice_cards, try_cards)

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


