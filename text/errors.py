class TextRecognitionError(Exception):
    """Base exception for text recognition errors"""
    pass


class EmptyTextInputError(TextRecognitionError):
    """Raised when text input is empty or contains only whitespace"""
    pass


class APIError(TextRecognitionError):
    """Raised when OpenAI API call fails"""
    pass