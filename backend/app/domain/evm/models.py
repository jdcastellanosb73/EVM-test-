from dataclasses import dataclass, fields
from decimal import Decimal
from enum import StrEnum
from typing import Self

from app.domain.evm.constants import MAX_PERCENT, MIN_PERCENT, PERCENT_SCALE, ZERO
from app.domain.evm.exceptions import InvalidActivityProgressError, ValidationRule


@dataclass(frozen=True, slots=True)
class ActivityProgress:
    """What a project leader records for an activity at the cutoff date.

    Percentages use the 0-100 scale. Invalid values cannot be constructed.
    """

    budget_at_completion: Decimal
    planned_percent: Decimal
    actual_percent: Decimal
    actual_cost: Decimal

    def __post_init__(self) -> None:
        for field in fields(self):
            if not getattr(self, field.name).is_finite():
                raise InvalidActivityProgressError(field.name, ValidationRule.MUST_BE_FINITE)
        if self.budget_at_completion <= ZERO:
            raise InvalidActivityProgressError(
                "budget_at_completion", ValidationRule.MUST_BE_POSITIVE
            )
        _require_percentage("planned_percent", self.planned_percent)
        _require_percentage("actual_percent", self.actual_percent)
        if self.actual_cost < ZERO:
            raise InvalidActivityProgressError("actual_cost", ValidationRule.MUST_BE_NON_NEGATIVE)


def _require_percentage(field_name: str, value: Decimal) -> None:
    if not MIN_PERCENT <= value <= MAX_PERCENT:
        raise InvalidActivityProgressError(field_name, ValidationRule.MUST_BE_PERCENTAGE)


@dataclass(frozen=True, slots=True)
class EarnedValueBase:
    """The four amounts every EVM indicator derives from.

    Activities and projects share this shape: a project base is the sum of its activity bases.
    """

    budget_at_completion: Decimal
    planned_value: Decimal
    earned_value: Decimal
    actual_cost: Decimal

    @classmethod
    def from_activity(cls, progress: ActivityProgress) -> Self:
        budget = progress.budget_at_completion
        return cls(
            budget_at_completion=budget,
            planned_value=budget * progress.planned_percent / PERCENT_SCALE,
            earned_value=budget * progress.actual_percent / PERCENT_SCALE,
            actual_cost=progress.actual_cost,
        )

    def __add__(self, other: Self) -> Self:
        return type(self)(
            budget_at_completion=self.budget_at_completion + other.budget_at_completion,
            planned_value=self.planned_value + other.planned_value,
            earned_value=self.earned_value + other.earned_value,
            actual_cost=self.actual_cost + other.actual_cost,
        )


EMPTY_BASE = EarnedValueBase(
    budget_at_completion=ZERO, planned_value=ZERO, earned_value=ZERO, actual_cost=ZERO
)


class CostPerformanceStatus(StrEnum):
    UNDER_BUDGET = "UNDER_BUDGET"
    ON_BUDGET = "ON_BUDGET"
    OVER_BUDGET = "OVER_BUDGET"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SchedulePerformanceStatus(StrEnum):
    AHEAD_OF_SCHEDULE = "AHEAD_OF_SCHEDULE"
    ON_SCHEDULE = "ON_SCHEDULE"
    BEHIND_SCHEDULE = "BEHIND_SCHEDULE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class PerformanceIndex[StatusT: StrEnum]:
    """An index value (None when undefined) and its interpretation."""

    value: Decimal | None
    status: StatusT


@dataclass(frozen=True, slots=True)
class EvmIndicators:
    budget_at_completion: Decimal
    planned_value: Decimal
    earned_value: Decimal
    actual_cost: Decimal
    cost_variance: Decimal
    schedule_variance: Decimal
    cost_performance_index: PerformanceIndex[CostPerformanceStatus]
    schedule_performance_index: PerformanceIndex[SchedulePerformanceStatus]
    estimate_at_completion: Decimal | None
    variance_at_completion: Decimal | None
