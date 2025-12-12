from scraper.models import Flight

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
