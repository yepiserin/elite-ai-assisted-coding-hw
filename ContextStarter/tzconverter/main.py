import air
from datetime import datetime, timedelta

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

def generate_time_options():
    """Generate time options in 12-hour format with 30-minute increments"""
    times = []
    start = datetime.strptime("12:00 AM", "%I:%M %p")
    for i in range(48):  # 24 hours * 2 (30-min increments)
        time_str = start.strftime("%I:%M %p").lstrip("0")  # Remove leading zero
        times.append(time_str)
        start += timedelta(minutes=30)
    return times

@app.get("/")
async def index(source_tz: str = "America/New_York", selected_time: str = "9:00 AM"):
    # Get the city name for the selected timezone
    source_city = TIME_ZONES.get(source_tz, "Washington D.C.")
    
    # Generate all time options
    time_options = generate_time_options()
    
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
            air.Label(
                "Time:",
                air.Select(
                    *[air.Option(time, value=time, selected=(time == selected_time)) for time in time_options],
                    name="selected_time",
                    onchange="this.form.submit()"
                )
            ),
            method="get"
        ),
        air.P(f"Selected time zone: {source_city} ({source_tz})"),
        air.P(f"Selected time: {selected_time}")
    )