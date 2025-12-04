from pydantic import BaseModel, field_validator, model_validator
import unicodedata
import re
from scraper.types import (
    SearchParamsType, 
    TicketType, 
    FlightType, 
    PassengersType, 
    PassengerType,
)
from scraper.validators import ensure_list_with_min_len


class SearchParams(BaseModel):
    departure: SearchParamsType
    destination: SearchParamsType
    departure_date: SearchParamsType
    return_date: SearchParamsType | None = None
    city_amount: int = 0 
    ticket_type: TicketType = TicketType.one_way
    flight_type: FlightType = FlightType.economy
    passengers: PassengersType = {PassengerType.adult: 1}

    @model_validator(mode="after")
    def validate_ticket_constraints(self) -> "SearchParams":
        if self.ticket_type == TicketType.multi_city:
            ensure_list_with_min_len(self.departure, "departure")
            ensure_list_with_min_len(self.destination, "destination")
            ensure_list_with_min_len(self.departure_date, "departure date")

        if self.ticket_type == TicketType.round_trip:
            if self.return_date is None:
                raise ValueError("A return date must be specified for round trip tickets")

        return self


class Flight(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    duration: str
    stops: str
    price: str

    @staticmethod
    def _sanitize_text(value: str) -> str:
        normalized = unicodedata.normalize("NFKC", value)
        # Replace narrow no-break space and NBSP with a regular space
        normalized = normalized.replace("\u202f", " ").replace("\xa0", " ")
        # Collapse any repeated whitespace
        normalized = " ".join(normalized.split())
        return normalized.strip()

    @field_validator("airline", "departure_time", "duration", "stops", "price", mode="before")
    @classmethod
    def _sanitize_general(cls, v: str) -> str:
        return cls._sanitize_text(v)

    @field_validator("arrival_time", mode="before")
    @classmethod
    def _sanitize_arrival_time(cls, v: str) -> str:
        normalized = cls._sanitize_text(v)
        # Remove trailing +N day offset if present
        normalized = re.sub(r"\s*\+\d+\s*$", "", normalized)
        return normalized
