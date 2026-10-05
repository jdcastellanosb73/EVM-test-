from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException

from app.api.schemas.common import ErrorDetail, ErrorResponse
from app.domain.evm import InvalidActivityProgressError
from app.services.errors import ApplicationError, ConflictError, ErrorCode, NotFoundError

VALIDATION_FAILED_MESSAGE = "Request validation failed"
INTERNAL_ERROR_MESSAGE = "Unexpected server error"
LOCATION_SEPARATOR = "."
BODY_LOCATION = "body"

ExceptionHandler = Callable[[Request, Any], Coroutine[Any, Any, Response]]


def error_response(status_code: int, description: str) -> dict[int | str, dict[str, Any]]:
    """OpenAPI documentation for an error status that uses the single ErrorResponse format."""
    return {status_code: {"model": ErrorResponse, "description": description}}


VALIDATION_ERROR_RESPONSE = error_response(
    status.HTTP_422_UNPROCESSABLE_CONTENT,
    "VALIDATION_ERROR: the request is malformed or breaks a rule "
    "(BAC > 0, percentages 0-100, AC >= 0, name required); details lists each field",
)
PROJECT_NOT_FOUND_RESPONSE = error_response(
    status.HTTP_404_NOT_FOUND, "PROJECT_NOT_FOUND: no project with that id"
)
ACTIVITY_NOT_FOUND_RESPONSE = error_response(
    status.HTTP_404_NOT_FOUND,
    "PROJECT_NOT_FOUND or ACTIVITY_NOT_FOUND: the project does not exist, "
    "or the activity does not belong to it",
)
PROJECT_NAME_TAKEN_RESPONSE = error_response(
    status.HTTP_409_CONFLICT, "PROJECT_NAME_TAKEN: another project already uses that name"
)
ACTIVITY_NAME_TAKEN_RESPONSE = error_response(
    status.HTTP_409_CONFLICT,
    "ACTIVITY_NAME_TAKEN: the project already has an activity with that name",
)
INTERNAL_ERROR_RESPONSE = error_response(
    status.HTTP_500_INTERNAL_SERVER_ERROR,
    "INTERNAL_ERROR: unexpected server failure; the body never exposes internal details",
)


def _application_error(status_code: int) -> ExceptionHandler:
    async def handle(_: Request, error: ApplicationError) -> JSONResponse:
        return _error_json(status_code, ErrorResponse(code=error.code, message=error.message))

    return handle


async def _handle_validation_error(_: Request, error: RequestValidationError) -> JSONResponse:
    details = [
        ErrorDetail(
            field=LOCATION_SEPARATOR.join(str(part) for part in problem["loc"]),
            message=problem["msg"],
        )
        for problem in error.errors()
    ]
    return _validation_error_json(details)


async def _handle_domain_validation_error(
    _: Request, error: InvalidActivityProgressError
) -> JSONResponse:
    field = LOCATION_SEPARATOR.join((BODY_LOCATION, error.field))
    return _validation_error_json([ErrorDetail(field=field, message=str(error.rule))])


async def _handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
    body = ErrorResponse(code=ErrorCode.INTERNAL_ERROR, message=INTERNAL_ERROR_MESSAGE)
    return _error_json(status.HTTP_500_INTERNAL_SERVER_ERROR, body)


def _validation_error_json(details: list[ErrorDetail]) -> JSONResponse:
    body = ErrorResponse(
        code=ErrorCode.VALIDATION_ERROR, message=VALIDATION_FAILED_MESSAGE, details=details
    )
    return _error_json(status.HTTP_422_UNPROCESSABLE_CONTENT, body)


async def _handle_http_exception(_: Request, error: HTTPException) -> JSONResponse:
    body = ErrorResponse(code=HTTPStatus(error.status_code).name, message=str(error.detail))
    return _error_json(error.status_code, body)


def _error_json(status_code: int, body: ErrorResponse) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


EXCEPTION_HANDLERS: dict[int | type[Exception], ExceptionHandler] = {
    NotFoundError: _application_error(status.HTTP_404_NOT_FOUND),
    ConflictError: _application_error(status.HTTP_409_CONFLICT),
    RequestValidationError: _handle_validation_error,
    InvalidActivityProgressError: _handle_domain_validation_error,
    HTTPException: _handle_http_exception,
    Exception: _handle_unexpected_error,
}
