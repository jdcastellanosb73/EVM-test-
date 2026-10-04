from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.common import MoneyString, PercentString
from app.api.schemas.indicators import IndicatorsResponse
from app.db.models import DECIMAL_SCALE, MONEY_PRECISION, NAME_MAX_LENGTH, PERCENT_PRECISION
from app.domain.evm import ActivityProgress
from app.domain.evm.constants import MAX_PERCENT, MIN_PERCENT, ZERO
from app.services.results import ActivityInput, ActivityResult


class ActivityRequest(BaseModel):
    """Send amounts as strings (e.g. "20000000.00") to keep them exact."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH, examples=["Desarrollo backend"])
    budget_at_completion: Decimal = Field(
        gt=ZERO,
        max_digits=MONEY_PRECISION,
        decimal_places=DECIMAL_SCALE,
        description="BAC: total planned budget. Must be greater than 0",
        examples=["20000000.00"],
    )
    planned_percent: Decimal = Field(
        ge=MIN_PERCENT,
        le=MAX_PERCENT,
        max_digits=PERCENT_PRECISION,
        decimal_places=DECIMAL_SCALE,
        description="Planned progress at the cutoff date, 0-100",
        examples=["60.00"],
    )
    actual_percent: Decimal = Field(
        ge=MIN_PERCENT,
        le=MAX_PERCENT,
        max_digits=PERCENT_PRECISION,
        decimal_places=DECIMAL_SCALE,
        description="Actual progress completed, 0-100",
        examples=["45.00"],
    )
    actual_cost: Decimal = Field(
        ge=ZERO,
        max_digits=MONEY_PRECISION,
        decimal_places=DECIMAL_SCALE,
        description="AC: cost incurred to date. Must be 0 or greater",
        examples=["12000000.00"],
    )

    def to_input(self) -> ActivityInput:
        return ActivityInput(
            name=self.name,
            progress=ActivityProgress(
                budget_at_completion=self.budget_at_completion,
                planned_percent=self.planned_percent,
                actual_percent=self.actual_percent,
                actual_cost=self.actual_cost,
            ),
        )


class ActivityResponse(BaseModel):
    id: int
    project_id: int
    name: str
    budget_at_completion: MoneyString
    planned_percent: PercentString
    actual_percent: PercentString
    actual_cost: MoneyString
    created_at: datetime
    updated_at: datetime
    indicators: IndicatorsResponse

    @classmethod
    def from_result(cls, result: ActivityResult) -> Self:
        activity = result.record
        return cls(
            id=activity.id,
            project_id=activity.project_id,
            name=activity.name,
            budget_at_completion=activity.budget_at_completion,
            planned_percent=activity.planned_percent,
            actual_percent=activity.actual_percent,
            actual_cost=activity.actual_cost,
            created_at=activity.created_at,
            updated_at=activity.updated_at,
            indicators=IndicatorsResponse.from_indicators(result.indicators),
        )
