import os
import json
from pathlib import Path
from typing import BinaryIO, Any
from openai import (
    OpenAI,
    OpenAIError,
    APIError,
    RateLimitError,
    APIConnectionError
)

from voice.errors import (
    VoiceRecognitionError,
    InvalidAudioFormatError,
    AudioFileTooLargeError,
    TranscriptionError,
    StructuredExtractionError,
)

from voice.utils import build_extraction_prompt, load_template

from voice.constants import (
    SUPPORTED_AUDIO_FORMATS,
    MAX_FILE_SIZE_MB,
    MAX_FILE_SIZE_BYTES,
)

from dataclasses import dataclass


@dataclass(slots=True)
class VoiceRecognitionService:
    client: OpenAI

    def validate_audio_file(self, file: BinaryIO, filename: str) -> None:
        file_extension = Path(filename).suffix.lower().lstrip(".")
        
        if file_extension not in SUPPORTED_AUDIO_FORMATS:
            raise InvalidAudioFormatError(
                f"Unsupported audio format: {file_extension}. "
                f"Supported formats: {', '.join(SUPPORTED_AUDIO_FORMATS)}"
            )
        
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE_BYTES:
            total_size = file_size / 1024 / 1024
            raise AudioFileTooLargeError(
                f"Audio file size ({total_size:.2f}MB) exceeds "
                f"maximum allowed size ({MAX_FILE_SIZE_MB}MB)"
            )

    def transcribe_audio(self, file: BinaryIO, filename: str) -> str:
        try:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=(filename, file),
                response_format="text"
            )
            return response.strip() if isinstance(response, str) else response
        except (RateLimitError, APIConnectionError, APIError, OpenAIError) as e:
            # Convert OpenAI exceptions to domain exception
            error_messages = {
                RateLimitError: "OpenAI API rate limit exceeded. Please try again later.",
                APIConnectionError: "Failed to connect to OpenAI API. Please check your internet connection.",
            }
            message = error_messages.get(type(e), f"Transcription failed: {str(e)}")
            raise TranscriptionError(message) from e

    def extract_structured_data(self, transcription: str) -> dict[str, Any]:
        try:
            template_path = Path(__file__).parent.parent / "voice_output_structure.md"
            template_content = load_template(template_path)

            system_prompt = build_extraction_prompt(template_content)
        
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": system_prompt
                    },
                    {
                        "role": "user", 
                        "content": f"Extract flight search information from this transcription:\n\n{transcription}"
                    }
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if "transcription" not in result:
                result["transcription"] = transcription
            
            return result
            
        except json.JSONDecodeError as e:
            raise StructuredExtractionError(
                "Failed to parse extracted data. Please try again."
            ) from e
        except (RateLimitError, APIConnectionError, APIError, OpenAIError) as e:
            error_messages = {
                RateLimitError: "OpenAI API rate limit exceeded. Please try again later.",
                APIConnectionError: "Failed to connect to OpenAI API. Please check your internet connection.",
            }
            message = error_messages.get(type(e), f"Structured extraction failed: {str(e)}")
            raise StructuredExtractionError(message) from e

    async def process_audio(
        self, 
        file: BinaryIO, 
        filename: str,
        validate: bool = True
    ) -> dict[str, Any]:
        if validate:
            self.validate_audio_file(file, filename)
        
        transcription = self.transcribe_audio(file, filename)
        structured_data = self.extract_structured_data(transcription)
        
        return structured_data
