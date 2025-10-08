import air

app = air.Air()

@app.get("/")
async def index():
    return air.layouts.picocss(
        air.H1("Time Zone Converter"),
        air.P("Find the perfect meeting time across time zones")
    )