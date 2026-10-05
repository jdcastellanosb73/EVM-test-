from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import health
from app.config import Settings, get_settings
from app.db.engine import create_db_engine

API_DOCS_PATH = "/api-docs"
OPENAPI_SCHEMA_PATH = f"{API_DOCS_PATH}/openapi.json"


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the application. Used by uvicorn with --factory and by the tests."""
    resolved_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.engine = create_db_engine(resolved_settings.database_url)
        yield
        app.state.engine.dispose()

    app = FastAPI(
        title=resolved_settings.app_name,
        version=resolved_settings.app_version,
        docs_url=API_DOCS_PATH,
        openapi_url=OPENAPI_SCHEMA_PATH,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.include_router(health.router)
    return app
