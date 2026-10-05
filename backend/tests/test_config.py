import pytest
from pydantic import ValidationError

from app.config import Settings


def test_settings_are_read_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:secret@db:5432/evm")
    monkeypatch.setenv("APP_NAME", "Custom name")

    settings = Settings(_env_file=None)

    assert settings.database_url == "postgresql+psycopg://user:secret@db:5432/evm"
    assert settings.app_name == "Custom name"


def test_settings_require_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
