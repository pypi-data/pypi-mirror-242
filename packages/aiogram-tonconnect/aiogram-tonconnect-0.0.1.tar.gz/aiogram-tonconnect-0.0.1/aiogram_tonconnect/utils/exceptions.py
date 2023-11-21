class AiogramTonconnectException(Exception):
    """
    Base exception class for Aiogram AiogramTonConnect custom exceptions.
    """
    pass


class LanguageCodeNotSupported(AiogramTonconnectException):
    """
    Exception raised when an unsupported language code is encountered.
    """
    pass


# List of error messages related to editing messages
MESSAGE_EDIT_ERRORS = [
    "message can't be edited",
    "message is not modified",
    "message to edit not found",
]

# List of error messages related to deleting messages
MESSAGE_DELETE_ERRORS = [
    "message can't be deleted",
    "message to delete not found",
]
