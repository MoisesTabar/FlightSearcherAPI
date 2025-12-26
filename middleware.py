import logging
from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from voice.errors import (
    InvalidAudioFormatError,
    AudioFileTooLargeError,
    TranscriptionError,
    StructuredExtractionError,
    VoiceRecognitionError,
)

from text.errors import EmptyTextInputError
from scraper.errors import (
    NoFlightsFoundError,
    AdultPerInfantsOnLapError,
)

logger = logging.getLogger(__name__)


def create_error_handler(
    error_name: str,
    status_code: int,
    log_message: str,
    log_level: str = "error"
) -> Callable:
    """
    Factory function to create error handlers with consistent structure.
    
    Args:
        error_name: The error type name to include in the response
        status_code: HTTP status code to return
        log_message: Message template for logging (will be formatted with exception)
        log_level: Logging level to use ("warning", "error", or "exception")
    
    Returns:
        An async error handler function
    """
    async def error_handler(request: Request, exc: Exception) -> JSONResponse:
        log_func = getattr(logger, log_level)
        log_func(f"{log_message}: {str(exc)}")
        
        return JSONResponse(
            status_code=status_code,
            content={
                "error": error_name,
                "detail": str(exc)
            }
        )
    
    return error_handler


invalid_audio_format_handler = create_error_handler(
    error_name="InvalidAudioFormat",
    status_code=status.HTTP_400_BAD_REQUEST,
    log_message="Invalid audio format",
    log_level="warning"
)

audio_file_too_large_handler = create_error_handler(
    error_name="AudioFileTooLarge",
    status_code=status.HTTP_400_BAD_REQUEST,
    log_message="Audio file too large",
    log_level="warning"
)

transcription_error_handler = create_error_handler(
    error_name="TranscriptionError",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    log_message="Transcription error",
    log_level="error"
)

structured_extraction_error_handler = create_error_handler(
    error_name="StructuredExtractionError",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    log_message="Structured extraction error",
    log_level="error"
)

voice_recognition_error_handler = create_error_handler(
    error_name="VoiceRecognitionError",
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    log_message="Voice recognition error",
    log_level="error"
)

no_flights_found_error_handler = create_error_handler(
    error_name="NoFlightsFound",
    status_code=status.HTTP_404_NOT_FOUND,
    log_message="No flights found",
    log_level="error"
)

adult_per_infants_on_lap_error_handler = create_error_handler(
    error_name="AdultPerInfantsOnLapError",
    status_code=status.HTTP_400_BAD_REQUEST,
    log_message="Adult per infants on lap error",
    log_level="error"
)


empty_text_input_error_handler = create_error_handler(
    error_name="EmptyTextInputError",
    status_code=status.HTTP_400_BAD_REQUEST,
    log_message="Empty text input",
    log_level="warning"
)


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": f"An unexpected error occurred: {str(exc)}"
        }
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidAudioFormatError, invalid_audio_format_handler)
    app.add_exception_handler(AudioFileTooLargeError, audio_file_too_large_handler)
    app.add_exception_handler(TranscriptionError, transcription_error_handler)
    app.add_exception_handler(StructuredExtractionError, structured_extraction_error_handler)
    app.add_exception_handler(VoiceRecognitionError, voice_recognition_error_handler)
    app.add_exception_handler(NoFlightsFoundError, no_flights_found_error_handler)
    app.add_exception_handler(AdultPerInfantsOnLapError, adult_per_infants_on_lap_error_handler)
    app.add_exception_handler(EmptyTextInputError, empty_text_input_error_handler)

    app.add_exception_handler(Exception, general_exception_handler)
