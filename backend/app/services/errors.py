from enum import StrEnum


class ErrorCode(StrEnum):
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    ACTIVITY_NOT_FOUND = "ACTIVITY_NOT_FOUND"
    PROJECT_NAME_TAKEN = "PROJECT_NAME_TAKEN"
    ACTIVITY_NAME_TAKEN = "ACTIVITY_NAME_TAKEN"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ApplicationError(Exception):
    """A business error with a stable code that clients can rely on."""

    def __init__(self, code: ErrorCode, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class NotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass
