from pydantic import BaseModel, Field
from typing import Literal
from scraper.types import PassengersType, PassengerType


class ExtractedFlightData(BaseModel):
    departure: str | list[str]
    destination: str | list[str]
    departure_date: str | list[str]
    return_date: str | list[str] | None = None
    ticket_type: Literal["One Way", "Round Trip", "Multi-City"] = "One Way"
    flight_type: Literal["Economy", "Premium Economy", "Business", "First"] = "Economy"
    city_amount: int = 0 
    passengers: PassengersType = {PassengerType.adult: 1}


class VoiceSearchResponse(BaseModel):
    transcription: str
    summary: str
    extracted_data: ExtractedFlightData
    confidence: Literal["high", "medium", "low"] = Field(
        description="AI confidence level in the extraction accuracy"
    )
    missing_fields: list[str] = Field(
        default_factory=list,
        description="List of required fields that couldn't be extracted"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "transcription": "I need a flight from JFK to London on March 15th, 2026 for one person",
                "summary": "One-way flight from JFK to London on March 15, 2026 for 1 adult",
                "extracted_data": {
                    "departure": "JFK",
                    "destination": "London",
                    "departure_date": "2026-03-15",
                    "ticket_type": "One Way",
                    "flight_type": "Economy",
                    "passengers": {
                        "Adult": 1,
                        "Children": 0,
                        "Infants In Seat": 0,
                        "Infants On Lap": 0
                    }
                },
                "confidence": "high",
                "missing_fields": []
            }
        }


class VoiceSearchErrorResponse(BaseModel):
    error: str
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "InvalidAudioFormat",
                "detail": "Unsupported audio format: txt. Supported formats: mp3, mp4, mpeg, mpga, m4a, wav, webm"
            }
        }
