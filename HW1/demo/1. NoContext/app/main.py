import air
from air.requests import Request
from fastapi import FastAPI
from pydantic import BaseModel

app = air.Air()

# Air's JinjaRenderer is a shortcut for using Jinja templates
jinja = air.JinjaRenderer(directory="templates")

# Data model for MICE narrative structure
class StoryOutline(BaseModel):
    title: str
    milieu_hook: str
    milieu_resolution: str
    inquiry_question: str
    inquiry_answer: str
    character_development: str
    character_change: str
    event_catalyst: str
    event_conclusion: str

@app.get("/")
def index(request: Request):
    return jinja(request, name="home.html")

@app.get("/create")
def create_form(request: Request):
    return jinja(request, name="create.html")

@app.post("/create")
async def create_outline(request: Request, outline: StoryOutline):
    return jinja(request, name="outline.html", outline=outline)


