from datetime import date, datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.activities import ActivityResponse
from app.api.schemas.indicators import IndicatorsResponse
from app.db.models import DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH
from app.services.results import ProjectInput, ProjectResult


class ProjectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH, examples=["Portal de clientes"])
    description: str | None = Field(default=None, max_length=DESCRIPTION_MAX_LENGTH)
    cutoff_date: date | None = Field(
        default=None, description="Date the progress percentages refer to"
    )

    def to_input(self) -> ProjectInput:
        return ProjectInput(
            name=self.name, description=self.description, cutoff_date=self.cutoff_date
        )


class ProjectSummaryResponse(BaseModel):
    """A project in the list: consolidated indicators without the activity detail."""

    id: int
    name: str
    description: str | None
    cutoff_date: date | None
    activity_count: int
    indicators: IndicatorsResponse = Field(
        description="Consolidated with ratios of summed amounts, never averaged indices"
    )

    @classmethod
    def from_result(cls, result: ProjectResult) -> Self:
        project = result.record
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            cutoff_date=project.cutoff_date,
            activity_count=len(result.activities),
            indicators=IndicatorsResponse.from_indicators(result.indicators),
        )


class ProjectResponse(BaseModel):
    """Everything the dashboard needs in one call: project, activities and consolidation."""

    id: int
    name: str
    description: str | None
    cutoff_date: date | None
    created_at: datetime
    updated_at: datetime
    activities: list[ActivityResponse]
    indicators: IndicatorsResponse = Field(
        description="Consolidated with ratios of summed amounts, never averaged indices"
    )

    @classmethod
    def from_result(cls, result: ProjectResult) -> Self:
        project = result.record
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            cutoff_date=project.cutoff_date,
            created_at=project.created_at,
            updated_at=project.updated_at,
            activities=[ActivityResponse.from_result(item) for item in result.activities],
            indicators=IndicatorsResponse.from_indicators(result.indicators),
        )
