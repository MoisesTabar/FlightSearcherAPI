import os
import tempfile
from fastapi import APIRouter, UploadFile
from dotenv import load_dotenv

from voice.voice import VoiceRecognitionService
from voice.models import VoiceSearchResponse
from voice.constants import (
    VOICE_RECOGNITION_ENDPOINT_DESCRIPTION,
    VOICE_RECOGNITION_ENDPOINT_RESPONSES,
    VOICE_FLIGHT_SEARCH_ENDPOINT_DESCRIPTION,
    VOICE_FLIGHT_SEARCH_ENDPOINT_RESPONSES
)
from scraper.scraper import search_flights
from scraper.models import SearchParams, Flight

from openai import OpenAI

load_dotenv()

router = APIRouter()

voice_service = VoiceRecognitionService(
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
)

@router.post(
    "/voice/recognition",
    response_model=VoiceSearchResponse,
    responses=VOICE_RECOGNITION_ENDPOINT_RESPONSES,
    description=VOICE_RECOGNITION_ENDPOINT_DESCRIPTION
)
async def voice_recognition(audio: UploadFile) -> VoiceSearchResponse:
    audio_content = await audio.read()
    
    # Create temporary file for audio processing
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f"_{audio.filename}"
    ) as temp_file:
        temp_file.write(audio_content)
        temp_file.flush()
        temp_path = temp_file.name
    
    try:
        with open(temp_path, "rb") as audio_file:
            result = await voice_service.process_audio(
                file=audio_file,
                filename=audio.filename
            )
        
        return VoiceSearchResponse(**result)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@router.post(
    "/voice/search",
    response_model=list[Flight],
    responses=VOICE_FLIGHT_SEARCH_ENDPOINT_RESPONSES,
    description=VOICE_FLIGHT_SEARCH_ENDPOINT_DESCRIPTION
)
async def voice_search(audio: UploadFile) -> list[Flight]:
    audio_content = await audio.read()
    
    # Create temporary file for audio processing
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f"_{audio.filename}"
    ) as temp_file:
        temp_file.write(audio_content)
        temp_file.flush()
        temp_path = temp_file.name
    
    try:
        with open(temp_path, "rb") as audio_file:
            result = await voice_service.process_audio(
                file=audio_file,
                filename=audio.filename
            )

        voice_result = VoiceSearchResponse(**result)
        params = SearchParams(**voice_result.extracted_data.dict())
        flights = await search_flights(params)

        return flights  
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
