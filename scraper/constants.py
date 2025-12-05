from typing import Literal
from scraper.models import Flight


STOP_AFTER_ATTEMPTS: int = 5

RESULTS_SELECTORS: dict[str, str] = {
    "airline": "div.sSHqwe.tPgKwe.ogfYpf",
    "departure_time": 'span[aria-label^="Departure time"]',
    "arrival_time": 'span[aria-label^="Arrival time"]',
    "duration": 'div[aria-label^="Total duration"]',
    "stops": "div.hF6lYb span.rGRiKd",
    "price": "div.FpEdX span",
}

FLIGHTS_PAGE_URL: Literal = "https://www.google.com/flights"
FLIGHTS_AUTOMATIC_MULTI_CITY_SPAWN: int = 2

TICKET_TYPE_SELECTOR: Literal = "div.VfPpkd-TkwUic[jsname='oYxtQd']"
FLIGHT_TYPE_SELECTOR: Literal = "div.TQYpgc[jsname='zkxPxd']"
PASSENGER_BUTTON_SELECTOR: Literal = "div[jsname='QqIbod'] button[jsname='LgbsSe'][aria-haspopup='dialog']"

ADULT_PASSENGERS_SELECTOR: Literal = "div[jsname='mMhAUc']"
CHILDREN_PASSENGERS_SELECTOR: Literal = "div[jsname='LpMIEc']"
INFANTS_SEAT_PASSENGERS_SELECTOR: Literal = "div[jsname='u3Jn2e']"
INFANTS_LAP_PASSENGERS_SELECTOR: Literal = "div[jsname='TwhQhe']"
PASSENGER_INCREMENT_BUTTON: Literal = "button[jsname='TdyTDe']"
PASSENGER_DECREMENT_BUTTON: Literal = "button[jsname='DUGJie']"
PASSENGER_DONE_BUTTON: Literal = "button[jsname='McfNlf']"

FROM_SELECTOR: Literal = "input[aria-label^='Where from?']"
TO_SELECTOR: Literal = "input[aria-label^='Where to?']"
DEPARTURE_DATE_SELECTOR: Literal = "input[aria-label^='Departure']"
RETURN_DATE_SELECTOR: Literal = "input[aria-label^='Return']"

SEARCH_BUTTON_SELECTOR: Literal = "button[aria-label^='Search']"

ADD_FLIGHT_BUTTON_SELECTOR: Literal = "button[jsname='htvI8d']"

ADULT_PER_INFANTS_ON_LAP_ERROR_SELECTOR: Literal = "span[jsname='Ne3sFf']"
NO_FLIGHTS_ERROR_SELECTOR: Literal = "div.lF6CS"

BROWSER_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-web-security",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-site-isolation-trials",
    "--disable-accelerated-2d-canvas",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-software-rasterizer",
    "--disable-dev-tools",
    "--disable-browser-side-navigation",
    "--disable-notifications",
    "--disable-popup-blocking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--disable-ipc-flooding-protection",
    "--disable-hang-monitor",
    "--disable-sync",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--password-store=basic",
    "--use-mock-keychain",
]

BLOCKED_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"
)

BLOCKED_DOMAINS = (
    "analytics", 
    "google-analytics", 
    "googletagmanager", 
    "doubleclick", 
    "facebook", 
    "twitter"
)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


API_DESCRIPTION = """
Perform a real-time flight search using Google Flights.

The endpoint accepts structured search parameters and returns a list of available flights.
It supports:
- **One Way**, **Round Trip**, and **Multi-City** searches
- **Economy**, **Premium Economy**, **Business**, and **First** class
- Multiple passenger types (Adults, Children, Infants)

The scraper will:
1. Launch a headless browser
2. Navigate to Google Flights
3. Input the search parameters
4. Extract flight details from the results
5. Return a structured list of flights
"""

API_RESPONSES = {
    200: {
        "description": "Successfully retrieved flight search results",
        "model": list[Flight],
    },
    422: {
        "description": "Validation Error - Invalid search parameters",
    },
    500: {
        "description": "Server Error - Failed to scrape flight data",
    }
}
