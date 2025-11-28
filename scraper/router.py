from scraper.scraper import search_flights
from scraper.models import SearchParams, Flight
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

from scraper.constants import API_DESCRIPTION, API_RESPONSES

router = APIRouter()

load_dotenv()


@router.post(
    "/search", 
    response_model=list[Flight],
    description=API_DESCRIPTION,
    responses=API_RESPONSES,
)
async def search_flight(params: SearchParams) -> list[Flight]:
    return await search_flights(params)
