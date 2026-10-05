"""Errors that the request schemas do not catch still use the single error format."""

from collections.abc import Iterator
from decimal import Decimal

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import Settings
from app.domain.evm import ActivityProgress
from app.main import create_app

DOMAIN_ERROR_PATH = "/domain-error"
UNEXPECTED_ERROR_PATH = "/unexpected-error"
UNPROCESSABLE = 422
INTERNAL_SERVER_ERROR = 500
INTERNAL_DETAIL = "database host db-internal:5432 refused the connection"


def _raise_domain_error() -> None:
    ActivityProgress(
        budget_at_completion=Decimal(0),
        planned_percent=Decimal(0),
        actual_percent=Decimal(0),
        actual_cost=Decimal(0),
    )


def _raise_unexpected_error() -> None:
    raise RuntimeError(INTERNAL_DETAIL)


@pytest.fixture
def failing_app_client(test_settings: Settings) -> Iterator[TestClient]:
    app: FastAPI = create_app(test_settings)
    app.add_api_route(DOMAIN_ERROR_PATH, _raise_domain_error)
    app.add_api_route(UNEXPECTED_ERROR_PATH, _raise_unexpected_error)
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


def test_domain_validation_error_is_a_422_with_the_offending_field(
    failing_app_client: TestClient,
) -> None:
    response = failing_app_client.get(DOMAIN_ERROR_PATH)

    assert response.status_code == UNPROCESSABLE
    assert response.json() == {
        "code": "VALIDATION_ERROR",
        "message": "Request validation failed",
        "details": [{"field": "body.budget_at_completion", "message": "must be greater than 0"}],
    }


def test_unexpected_error_is_a_500_without_internal_details(
    failing_app_client: TestClient,
) -> None:
    response = failing_app_client.get(UNEXPECTED_ERROR_PATH)

    assert response.status_code == INTERNAL_SERVER_ERROR
    assert response.json() == {
        "code": "INTERNAL_ERROR",
        "message": "Unexpected server error",
        "details": [],
    }
    assert INTERNAL_DETAIL not in response.text
