# Voice Input Structured Output Template

This file defines the structure of the output that the voice recognition endpoint should return after processing audio input.

## Output Format

When a user sends audio to the voice endpoint, the AI will:
1. Transcribe the audio using OpenAI Whisper
2. Extract structured information from the transcription
3. Return data in the following format:

```json
{
  "transcription": "Full text of what the user said",
  "summary": "Brief summary of the user's request",
  "extracted_data": {
    "departure": "Departure airport code or city",
    "destination": "Destination airport code or city",
    "departure_date": "Date in YYYY-MM-DD format",
    "return_date": "Return date in YYYY-MM-DD format (if mentioned)",
    "ticket_type": "One Way, Round Trip, or Multi-City",
    "flight_type": "Economy, Premium Economy, Business, or First",
    "city_amount": "Number of cities in the trip (Multi-City only) spawns one when there are more than 2 cities",
    "passengers": {
      "Adult": 1,
      "Children": 0,
      "Infants In Seat": 0,
      "Infants On Lap": 0
    }
  },
  "confidence": "high/medium/low",
  "missing_fields": ["List of required fields that couldn't be extracted"]
}
```

## Field Descriptions

### `transcription`
- The complete, verbatim transcription of the audio input
- Type: `string`

### `summary`
- A concise summary of the user's flight search request
- Type: `string`
- Example: "User wants to book a round trip flight from New York to London for 2 adults in business class"

### `extracted_data`
- Structured flight search parameters extracted from the voice input
- This should match the `SearchParams` model structure where possible
- Fields:
  - **departure**: Airport code or city name (will be normalized)
  - **destination**: Airport code or city name (will be normalized)
  - **departure_date**: Date in YYYY-MM-DD format
  - **return_date**: Optional, only if round trip is mentioned
  - **ticket_type**: "One Way", "Round Trip", or "Multi-City"
  - **flight_type**: "Economy", "Premium Economy", "Business", or "First"
  - **passengers**: Object with passenger counts by type
  - **city_amount**: Number of cities in the trip (Multi-City only) Google Flights spawns 2 selectors when multi-city is selected so it will spawn one when there are more than 2 cities, and it will spawn two when there are more than 3 cities so on and so forth.

### `confidence`
- AI's confidence level in the extraction accuracy
- Values: `"high"`, `"medium"`, `"low"`
- Based on clarity of audio and completeness of information

### `missing_fields`
- Array of field names that are required but couldn't be extracted from the audio
- Type: `array of strings`
- Example: `["return_date", "passengers"]`

## Example User Voice Inputs

### Example 1: Simple One-Way Flight
**User says:** "I need a flight from JFK to London on March 15th, 2026 for one person"

**Expected Output:**
```json
{
  "transcription": "I need a flight from JFK to London on March 15th, 2026 for one person",
  "summary": "One-way flight from JFK to London on March 15, 2026 for 1 adult",
  "extracted_data": {
    "departure": "JFK",
    "destination": "London",
    "departure_date": "2026-03-15",
    "ticket_type": "One Way",
    "flight_type": "Economy",
    "passengers": {
      "Adult": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 2: Round Trip with Multiple Passengers
**User says:** "Book a round trip from Miami to Paris, leaving May 1st and returning May 15th for two adults and one child in business class"

**Expected Output:**
```json
{
  "transcription": "Book a round trip from Miami to Paris, leaving May 1st and returning May 15th for two adults and one child in business class",
  "summary": "Round trip from Miami to Paris (May 1-15, 2026) for 2 adults and 1 child in business class",
  "extracted_data": {
    "departure": "Miami",
    "destination": "Paris",
    "departure_date": "2026-05-01",
    "return_date": "2026-05-15",
    "ticket_type": "Round Trip",
    "flight_type": "Business",
    "passengers": {
      "Adult": 2,
      "Children": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 3: Incomplete Information
**User says:** "I want to fly to Tokyo sometime next month"

**Expected Output:**
```json
{
  "transcription": "I want to fly to Tokyo sometime next month",
  "summary": "Flight to Tokyo, specific dates and departure location not specified",
  "extracted_data": {
    "destination": "Tokyo",
    "ticket_type": "One Way",
    "flight_type": "Economy",
    "passengers": {
      "Adult": 1
    }
  },
  "confidence": "low",
  "missing_fields": ["departure", "departure_date"]
}
```

### Example 4: Multi-City
**User says:** "I want to fly to Tokyo and then to Paris for two adults, one child and one infant on lap in premium economy class on the 15th of March to the 25th of March"

**Expected Output:**
```json
{
  "transcription": "I want to fly to Tokyo and then to Paris for two adults, one child and one infant on lap in premium economy class on the 15th of March to the 25th of March",
  "summary": "Flight to Tokyo and then to Paris for two adults, one child and one infant in lap in premium economy class on the 15th of March to the 25th of March",
  "extracted_data": {
    "departure": ["Tokyo", "Paris"],
    "destination": ["Paris", "Tokyo"],
    "departure_date": ["2026-03-15", "2026-03-25"],
    "ticket_type": "Multi-City",
    "flight_type": "Premium Economy",
    "passengers": {
        "Adult": 2,
        "Children": 1,
        "Infants On Lap": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 5: Multi-City
**User says:** "Search me a multi-city flight from New York to Paris and back one adult and one child in First class
From april 1st to april 15th 2026"

**Expected Output:**
```json
{
  "transcription": "Search me a multi-city flight from New York to Paris and back one adult and one child in First class From april 1st to april 15th 2026",
  "summary": "Flight to New York and then to Paris for one adult and one child in First class on the 1st of April to the 15th of April 2026", 
  "extracted_data": {
    "departure": ["New York", "Paris"],
    "destination": ["Paris", "New York"],
    "departure_date": ["2026-04-01", "2026-04-15"],
    "ticket_type": "Multi-City",
    "flight_type": "First",
    "passengers": {
        "Adult": 1,
        "Children": 1
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

### Example 6: Multi-City
**User says:** "Search me a multi-city flight from New York to Paris and to Santo Domingo one adult and two infants on lap in Economy class from january 1st, january 8th, january 15th 2026"

**Expected Output:**
```json
{
  "transcription": "Search me a multi-city flight from New York to Paris and to Santo Domingo one adult and two infants on lap in Economy class from january 1st, january 8th, january 15th 2026",
  "summary": "Flight to New York and then to Paris and then to Santo Domingo for one adult and two infants on lap in Economy class from january 1st, january 8th, january 15th 2026",
  "extracted_data": {
    "departure": ["New York", "Paris", "Santo Domingo"],
    "destination": ["Paris", "Santo Domingo", "New York"],
    "departure_date": ["2026-01-01", "2026-01-08", "2026-01-15"],
    "ticket_type": "Multi-City",
    "flight_type": "Economy",
    "city_amount": 1,
    "passengers": {
      "Adult": 1,
      "Infants On Lap": 2
    }
  },
  "confidence": "high",
  "missing_fields": []
}
```

---

## Customization Instructions

You can modify this template to change:
1. **Output fields**: Add or remove fields from `extracted_data`
2. **Field types**: Change data types or add validation rules
3. **Examples**: Add more examples to guide the AI's extraction logic
4. **Confidence criteria**: Define what constitutes high/medium/low confidence
5. **Passenger types**: If provided with "Infants_In_Lap" or "Infants_In_Seat", convert to "Infants In Lap" or "Infants In Seat" in the output JSON,
6. **Children specification**: If provided with "Children In / On Lap" or "Children In / On Seat", convert to "Infants On Lap" or "Infants In Seat" in the output JSON

Save this file and the voice endpoint will use it as a reference for structuring the AI's output.
