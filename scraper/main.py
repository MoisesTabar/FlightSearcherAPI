from scraper.scraper import search_flights
from scraper.models import SearchParams, Flight
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.post("/flights/search", response_model=list[Flight])
async def search_flight(params: SearchParams) -> list[Flight]:
    return await search_flights(params)
