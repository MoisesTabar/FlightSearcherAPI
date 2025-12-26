import os

from typing import Annotated
from fastapi import APIRouter, Body
from text.text import TextRecognitionService
from dotenv import load_dotenv

from openai import OpenAI

from scraper.scraper import search_flights
from scraper.models import SearchParams, Flight

load_dotenv()

router = APIRouter()


text_service = TextRecognitionService(
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
)


@router.post("/text/search")
async def text_search(text: Annotated[str, Body(..., embed=True)]) -> list[Flight]:
    result = text_service.extract_structured_data(text)
    params = SearchParams(**result)
    flights = await search_flights(params)
    return flights
