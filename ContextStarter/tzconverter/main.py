import air

app = air.Air()

@app.get("/")
async def index():
    return air.layouts.mvpcss(
        air.H1("Hello, Air!"),
        air.P("Breathe it in.")
    )