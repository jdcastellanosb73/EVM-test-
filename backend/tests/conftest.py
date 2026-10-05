import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

DEFAULT_TEST_DATABASE_URL = "postgresql+psycopg://evm:evm@localhost:5433/evm_test"
UNREACHABLE_DATABASE_URL = "postgresql+psycopg://evm:evm@127.0.0.1:1/evm_test?connect_timeout=1"


@pytest.fixture(scope="session")
def test_database_url() -> str:
    return os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DATABASE_URL)


@pytest.fixture
def test_settings(test_database_url: str) -> Settings:
    return Settings(database_url=test_database_url)


@pytest.fixture
def client(test_settings: Settings) -> Iterator[TestClient]:
    with TestClient(create_app(test_settings)) as test_client:
        yield test_client


@pytest.fixture
def client_without_database() -> Iterator[TestClient]:
    settings = Settings(database_url=UNREACHABLE_DATABASE_URL)
    with TestClient(create_app(settings)) as test_client:
        yield test_client
