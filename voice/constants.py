from voice.models import (
    VoiceSearchErrorResponse,
    VoiceSearchResponse
)
from scraper.models import Flight

SUPPORTED_AUDIO_FORMATS = {
    "mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"
}

MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

BASE_EXTRACTION_PROMPT = """
You are an AI assistant that extracts structured flight search information from voice transcriptions.

Your task is to:
1. Analyze the transcription carefully
2. Extract relevant flight search parameters
3. Return a JSON object with the exact structure specified below

CRITICAL REQUIREMENTS:
- Always return valid JSON
- Use the exact field names and structure shown in the examples
- Infer reasonable defaults for unspecified fields
- Mark fields as null or omit them if not mentioned
- Set confidence based on information completeness:
  * "high" - All key information present and clear
  * "medium" - Some ambiguity or missing optional fields
  * "low" - Missing critical information or unclear intent
- List any required fields that couldn't be extracted in missing_fields

For ticket_type, determine based on context:
- "One Way" - Only departure mentioned, no return
- "Round Trip" - Both departure and return dates mentioned
- "Multi-City" - Multiple destinations/segments mentioned

For flight_type, use context clues:
- "Economy" - Default if not specified
- "Premium Economy", "Business", "First" - If explicitly mentioned

For passengers, default to {"Adult": 1} if not specified.

For dates:
- Convert relative dates (e.g., "next month", "March 15th") to YYYY-MM-DD format
- Assume year 2026 if not specified
- Return null if date cannot be determined

Output JSON structure:
{
  "transcription": "exact transcription text",
  "summary": "brief summary of the request",
  "extracted_data": {
    "departure": "airport code or city" or ["city1", "city2"] for multi-city,
    "destination": "airport code or city" or ["city1", "city2"] for multi-city,
    "departure_date": "YYYY-MM-DD" or ["YYYY-MM-DD", "YYYY-MM-DD"] for multi-city,
    "return_date": "YYYY-MM-DD" or null,
    "ticket_type": "One Way" | "Round Trip" | "Multi-City",
    "flight_type": "Economy" | "Premium Economy" | "Business" | "First",
    "city_amount": number (only for multi-city),
    "passengers": {
      "Adult": number,
      "Children": number,
      "Infants In Seat": number,
      "Infants On Lap": number
    }
  },
  "confidence": "high" | "medium" | "low",
  "missing_fields": ["field1", "field2"] or []
}

"""

VOICE_RECOGNITION_ENDPOINT_DESCRIPTION = f"""
Upload an audio file containing a flight search request.

The endpoint will:
1. Transcribe the audio using OpenAI Whisper
2. Extract structured flight search parameters using GPT-4
3. Return the transcription, summary, and structured data

**Supported audio formats:** {', '.join(SUPPORTED_AUDIO_FORMATS)}

**Maximum file size:** {MAX_FILE_SIZE_MB}MB

**Example voice input:** "I need a round trip flight from New York to London, 
leaving March 15th and returning March 22nd for two adults in business class"
"""

VOICE_RECOGNITION_ENDPOINT_RESPONSES = {
  200: {
    "description": "Successfully processed audio and extracted flight search data",
    "model": VoiceSearchResponse
  },
  400: {
    "description": "Invalid audio format or file too large",
    "model": VoiceSearchErrorResponse
  },
  500: {
    "description": "Server error or OpenAI API error",
    "model": VoiceSearchErrorResponse
  }
}

VOICE_FLIGHT_SEARCH_ENDPOINT_DESCRIPTION = f"""
Upload an audio file containing a flight search request and get actual flight results.

This endpoint combines voice recognition with real-time flight search:
1. Transcribes the audio using OpenAI Whisper
2. Extracts structured flight search parameters using GPT-4
3. Performs a real-time Google Flights search with the extracted parameters
4. Returns a list of available flights

**Supported audio formats:** {', '.join(SUPPORTED_AUDIO_FORMATS)}

**Maximum file size:** {MAX_FILE_SIZE_MB}MB

**Example voice input:** "I need a round trip flight from New York to London, 
leaving March 15th and returning March 22nd for two adults in business class"

The endpoint supports:
- **One Way**, **Round Trip**, and **Multi-City** searches
- **Economy**, **Premium Economy**, **Business**, and **First** class
- Multiple passenger types (Adults, Children, Infants)
"""

VOICE_FLIGHT_SEARCH_ENDPOINT_RESPONSES = {
    200: {
        "description": "Successfully processed audio and retrieved flight search results",
        "model": list[Flight],
    },
    400: {
        "description": "Invalid audio format or file too large",
        "model": VoiceSearchErrorResponse,
    },
    422: {
        "description": "Validation Error - Invalid search parameters extracted from audio",
    },
    500: {
        "description": "Server Error - OpenAI API error or failed to scrape flight data",
    }
}