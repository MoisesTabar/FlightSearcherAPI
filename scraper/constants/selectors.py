

RESULTS_SELECTORS: dict[str, str] = {
    "airline": "div.sSHqwe.tPgKwe.ogfYpf",
    "departure_time": 'span[aria-label^="Departure time"]',
    "arrival_time": 'span[aria-label^="Arrival time"]',
    "duration": 'div[aria-label^="Total duration"]',
    "stops": "div.hF6lYb span.rGRiKd",
    "price": "div.FpEdX span",
}

FLIGHTS_PAGE_URL = "https://www.google.com/flights"
FLIGHTS_AUTOMATIC_MULTI_CITY_SPAWN = 2

TICKET_TYPE_SELECTOR = "div.VfPpkd-TkwUic[jsname='oYxtQd']"
FLIGHT_TYPE_SELECTOR = "div.TQYpgc[jsname='zkxPxd']"
PASSENGER_BUTTON_SELECTOR = "div[jsname='QqIbod'] button[jsname='LgbsSe'][aria-haspopup='dialog']"

ADULT_PASSENGERS_SELECTOR = "div[jsname='mMhAUc']"
CHILDREN_PASSENGERS_SELECTOR = "div[jsname='LpMIEc']"
INFANTS_SEAT_PASSENGERS_SELECTOR = "div[jsname='u3Jn2e']"
INFANTS_LAP_PASSENGERS_SELECTOR = "div[jsname='TwhQhe']"
PASSENGER_INCREMENT_BUTTON = "button[jsname='TdyTDe']"
PASSENGER_DECREMENT_BUTTON = "button[jsname='DUGJie']"
PASSENGER_DONE_BUTTON = "button[jsname='McfNlf']"

FROM_SELECTOR = "input[aria-label^='Where from?']"
TO_SELECTOR = "input[aria-label^='Where to?']"
DEPARTURE_DATE_SELECTOR = "input[aria-label^='Departure']"
RETURN_DATE_SELECTOR = "input[aria-label^='Return']"

SEARCH_BUTTON_SELECTOR = "button[aria-label^='Search']"

ADD_FLIGHT_BUTTON_SELECTOR = "button[jsname='htvI8d']"

ADULT_PER_INFANTS_ON_LAP_ERROR_SELECTOR = "span[jsname='Ne3sFf']"
NO_FLIGHTS_ERROR_SELECTOR = "div.lF6CS"

FLIGHTS_SELECTOR = "li.pIav2d"