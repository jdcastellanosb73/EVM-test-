from collections.abc import Callable
from dataclasses import dataclass, field, fields
from decimal import Decimal
from enum import StrEnum
from typing import Self

from app.domain.evm.constants import MAX_PERCENT, MIN_PERCENT, PERCENT_SCALE, ZERO
from app.domain.evm.exceptions import InvalidActivityProgressError, ValidationRule

RULE_METADATA_KEY = "rule"
RULE_CHECKS: dict[ValidationRule, Callable[[Decimal], bool]] = {
    ValidationRule.MUST_BE_POSITIVE: lambda value: value > ZERO,
    ValidationRule.MUST_BE_PERCENTAGE: lambda value: MIN_PERCENT <= value <= MAX_PERCENT,
    ValidationRule.MUST_BE_NON_NEGATIVE: lambda value: value >= ZERO,
}


@dataclass(frozen=True, slots=True)
class ActivityProgress:
    """What a project leader records for an activity at the cutoff date.

    Percentages use the 0-100 scale. Invalid values cannot be constructed.
    """

    budget_at_completion: Decimal = field(
        metadata={RULE_METADATA_KEY: ValidationRule.MUST_BE_POSITIVE}
    )
    planned_percent: Decimal = field(
        metadata={RULE_METADATA_KEY: ValidationRule.MUST_BE_PERCENTAGE}
    )
    actual_percent: Decimal = field(metadata={RULE_METADATA_KEY: ValidationRule.MUST_BE_PERCENTAGE})
    actual_cost: Decimal = field(metadata={RULE_METADATA_KEY: ValidationRule.MUST_BE_NON_NEGATIVE})

    def __post_init__(self) -> None:
        values = [
            (item.name, getattr(self, item.name), item.metadata[RULE_METADATA_KEY])
            for item in fields(self)
        ]
        for field_name, value, _ in values:
            if not value.is_finite():
                raise InvalidActivityProgressError(field_name, ValidationRule.MUST_BE_FINITE)
        for field_name, value, rule in values:
            if not RULE_CHECKS[rule](value):
                raise InvalidActivityProgressError(field_name, rule)


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
