import air

app = air.Air()

# Time zone options with city names and IANA time zone identifiers
TIME_ZONES = {
    "America/Los_Angeles": "San Francisco",
    "America/Chicago": "Chicago",
    "America/New_York": "Washington D.C.",
    "Europe/London": "London",
    "Europe/Paris": "Paris",
    "Europe/Berlin": "Berlin",
    "Asia/Manila": "Manila",
    "Asia/Tokyo": "Tokyo",
    "Asia/Singapore": "Singapore",
    "Australia/Sydney": "Sydney",
}

@app.get("/")
async def index(source_tz: str = "America/New_York"):
    # Get the city name for the selected timezone
    source_city = TIME_ZONES.get(source_tz, "Washington D.C.")
    
    return air.layouts.picocss(
        air.H1("Time Zone Converter"),
        air.P("Find the perfect meeting time across time zones"),
        air.Hr(),
        air.Form(
            air.Label(
                "Source Time Zone:",
                air.Select(
                    *[air.Option(city, value=tz, selected=(tz == source_tz)) for tz, city in TIME_ZONES.items()],
                    name="source_tz",
                    onchange="this.form.submit()"
                )
            ),
            method="get"
        ),
        air.P(f"Selected time zone: {source_city} ({source_tz})")
    )