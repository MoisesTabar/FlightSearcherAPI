# FlightScraper 

A FastAPI-based flight search API that scrapes flight information from Google Flights using Playwright automation.

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FlightScraper
```

2. **Install dependencies using uv**
```bash
uv sync
```

3. **Install Playwright browsers**
```bash
uv run playwright install
```

### Running the Application

Start the development server:

```bash
uv run fastapi dev main.py
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoint

### `POST /flights/search`

Search for flights based on your travel requirements.

**URL:** `http://localhost:8000/flights/search`

## 💼 Request Examples

### One-Way Flight

Search for a one-way flight between two airports:

```json
{
    "departure": "STI",
    "destination": "JFK",
    "departure_date": "2026-03-01",
    "flight_type": "First",
    "passengers": {
        "Adult": 2
    }
}
```

### Round Trip Flight

Search for a round-trip flight with departure and return dates:

```json
{
    "departure": "STI",
    "destination": "JFK",
    "departure_date": "2026-05-01",
    "return_date": "2026-05-15",
    "ticket_type": "Round Trip",
    "flight_type": "Economy",
    "passengers": {
        "Adult": 2
    }
}
```

### Multi-City Flight

Search for flights across multiple destinations:

```json
{
    "departure": ["STI", "ATL", "JFK"],
    "destination": ["ATL", "JFK", "STI"],
    "departure_date": ["2026-05-01", "2026-05-10", "2026-05-15"],
    "ticket_type": "Multi-City",
    "flight_type": "Premium Economy",
    "city_amount": 1,
    "passengers": {
        "Adult": 2,
        "Children": 1,
        "Infants On Lap": 1
    }
}
```

## 🎫 Request Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `departure` | string or array | Departure airport code(s). Use string for one-way/round-trip, array for multi-city |
| `destination` | string or array | Destination airport code(s). Use string for one-way/round-trip, array for multi-city |
| `departure_date` | string or array | Departure date(s) in YYYY-MM-DD format. Use string for one-way/round-trip, array for multi-city |

### Optional Parameters (with defaults)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticket_type` | string | `"One Way"` | Type of ticket: `"One Way"`, `"Round Trip"`, or `"Multi-City"` |
| `flight_type` | string | `"Economy"` | Class of service: `"Economy"`, `"Premium Economy"`, `"Business"`, or `"First"` |
| `passengers` | object | `{"Adult": 1}` | Number of passengers by type |
| `return_date` | string | `null` | Return date in YYYY-MM-DD format. **Required** when `ticket_type` is `"Round Trip"` |
| `city_amount` | integer | `null` | Number of cities. **Required** when `ticket_type` is `"Multi-City"` |

### Passenger Types

You can specify any combination of the following passenger types:

- `"Adult"` - Adults (12+ years)
- `"Children"` - Children (2-11 years)
- `"Infants In Seat"` - Infants with their own seat
- `"Infants On Lap"` - Infants under 2 years old (no seat)

### Flight Classes

- `"Economy"` - Standard economy class (default)
- `"Premium Economy"` - Premium economy with extra legroom
- `"Business"` - Business class
- `"First"` - First class

## 📝 Example Usage

Using **curl**:

```bash
curl -X POST http://localhost:8000/flights/search \
  -H "Content-Type: application/json" \
  -d '{
    "departure": "STI",
    "destination": "JFK",
    "departure_date": "2026-03-01",
    "flight_type": "Economy",
    "passengers": {"Adult": 2}
  }'
```

Using **Python**:

```python
import requests

response = requests.post(
    "http://localhost:8000/flights/search",
    json={
        "departure": "STI",
        "destination": "JFK",
        "departure_date": "2026-03-01",
        "flight_type": "Economy",
        "passengers": {"Adult": 2}
    }
)

flights = response.json()
print(flights)
```

## 🛠️ Development

### Project Structure

```
FlightScraper/
├── main.py              # FastAPI application entry point
├── scraper/             # Core scraper package
│   ├── scraper.py       # Main scraping logic
│   ├── models.py        # Pydantic models
│   ├── types.py         # Type definitions
│   ├── forms.py         # Form handling
│   ├── browser.py       # Browser automation
│   ├── validators.py    # Input validation
│   ├── utils.py         # Utility functions
│   └── constants.py     # Application constants
└── pyproject.toml       # Project dependencies
```

## 📦 Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Playwright** - Browser automation for web scraping
- **Pydantic** - Data validation using Python type annotations
- **Tenacity** - Retry logic for robust scraping

## 📄 License

This project is for educational and personal use only.
