from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import Engine

from app.db.engine import get_engine, is_database_reachable

router = APIRouter(tags=["health"])


class ServiceStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"


class DependencyStatus(StrEnum):
    UP = "up"
    DOWN = "down"


class HealthResponse(BaseModel):
    status: ServiceStatus
    database: DependencyStatus


@router.get(
    "/health",
    summary="Report service health",
    description="Reports whether the API is running and whether it can reach the database.",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": HealthResponse,
            "description": "The API is running but the database is unreachable.",
        }
    },
)
def read_health(
    response: Response, engine: Annotated[Engine, Depends(get_engine)]
) -> HealthResponse:
    if is_database_reachable(engine):
        return HealthResponse(status=ServiceStatus.OK, database=DependencyStatus.UP)
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(status=ServiceStatus.DEGRADED, database=DependencyStatus.DOWN)
