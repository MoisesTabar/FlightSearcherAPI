from voice.models import (
    VoiceSearchErrorResponse,
    VoiceSearchResponse
)
from scraper.models import Flight
from voice.constants.settings import (
    MAX_FILE_SIZE_MB,
    SUPPORTED_AUDIO_FORMATS
)


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