import json

from dataclasses import dataclass
from pathlib import Path

from openai import (
    OpenAI,
    OpenAIError,
    APIError,
    RateLimitError,
    APIConnectionError
)

from typing import Any
from text.errors import (
    EmptyTextInputError,
    APIError as TextAPIError
)
from text.constants.prompts import BASE_TEXT_EXTRACTION_PROMPT
from utils import build_prompt, load_template
from logging_config import get_logger

logger = get_logger("text")


@dataclass(slots=True)
class TextRecognitionService:
    client: OpenAI

    def extract_structured_data(self, text: str) -> dict[str, Any]:
        if not text or not text.strip():
            error_message = "Text input is empty or contains only whitespace"
            logger.error(error_message)
            raise EmptyTextInputError(error_message)
        
        try:
            template_path = Path(__file__).parent.parent / "text_output_structure.md"
            template_content = load_template(template_path)

            system_prompt = build_prompt(BASE_TEXT_EXTRACTION_PROMPT, template_content)

            logger.info("Structured data extraction from natural text started")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Extract flight search information from this text:\n\n{text}"
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            logger.info("Structured data extraction completed successfully")

            return json.loads(response.choices[0].message.content)["extracted_data"]
        
        except json.JSONDecodeError as e:
            error_message = "Failed to parse extracted data. Please try again."
            logger.error(f"{error_message} - {str(e)}")
            raise TextAPIError(error_message) from e
        
        except (RateLimitError, APIConnectionError, APIError, OpenAIError) as e:
            # Convert OpenAI exceptions to domain exception
            error_messages = {
                RateLimitError: "OpenAI API rate limit exceeded. Please try again later.",
                APIConnectionError: "Failed to connect to OpenAI API. Please check your internet connection.",
            }

            message = error_messages.get(type(e), f"Text extraction failed: {str(e)}")
            logger.error(message)
            raise TextAPIError(message) from e
