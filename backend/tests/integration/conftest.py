"""Integration fixtures against the isolated db-test database.

Each test runs inside a transaction that is rolled back at the end, so tests never see each
other's data. Services still call commit(): it only releases a SAVEPOINT.
"""

from collections.abc import Iterator
from typing import Any

import httpx2 as httpx
import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import Session

from app.config import Settings
from app.db.engine import create_db_engine
from app.db.session import get_session
from app.main import create_app

NO_CONTENT = 204


@pytest.fixture(scope="session")
def database_engine(test_database_url: str) -> Iterator[Engine]:
    engine = create_db_engine(test_database_url)
    yield engine
    engine.dispose()


@pytest.fixture
def database_connection(database_engine: Engine) -> Iterator[Connection]:
    with database_engine.connect() as connection:
        transaction = connection.begin()
        yield connection
        transaction.rollback()


@pytest.fixture
def api_client(test_settings: Settings, database_connection: Connection) -> Iterator[TestClient]:
    app = create_app(test_settings)

    def session_in_test_transaction() -> Iterator[Session]:
        with Session(bind=database_connection, join_transaction_mode="create_savepoint") as session:
            yield session

    app.dependency_overrides[get_session] = session_in_test_transaction
    with TestClient(app) as client:
        yield client


class ContractChecker:
    """Validates a response against the schema the API itself publishes in OpenAPI."""

    def __init__(self, openapi: dict[str, Any]) -> None:
        self._openapi = openapi

    def check(self, response: httpx.Response, method: str, path: str) -> None:
        operation = self._openapi["paths"][path][method.lower()]
        documented = operation["responses"].get(str(response.status_code))
        assert documented is not None, f"{response.status_code} is not documented for {path}"
        if response.status_code == NO_CONTENT:
            assert response.content == b""
            return
        schema = documented["content"]["application/json"]["schema"]
        validator = Draft202012Validator({**schema, "components": self._openapi["components"]})
        validator.validate(response.json())


@pytest.fixture
def contract(api_client: TestClient) -> ContractChecker:
    return ContractChecker(api_client.app.openapi())  # type: ignore[attr-defined]
