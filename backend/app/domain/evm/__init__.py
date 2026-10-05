"""Earned Value Management engine: pure functions with no framework or database dependencies."""

from app.domain.evm.calculator import (
    calculate_activity_indicators,
    calculate_indicators,
    consolidate_project_indicators,
)
from app.domain.evm.constants import PRESENTATION_ROUNDING
from app.domain.evm.exceptions import InvalidActivityProgressError, ValidationRule
from app.domain.evm.models import (
    ActivityProgress,
    CostPerformanceStatus,
    EarnedValueBase,
    EvmIndicators,
    PerformanceIndex,
    SchedulePerformanceStatus,
)
from app.domain.evm.rounding import round_index, round_money

__all__ = [
    "PRESENTATION_ROUNDING",
    "ActivityProgress",
    "CostPerformanceStatus",
    "EarnedValueBase",
    "EvmIndicators",
    "InvalidActivityProgressError",
    "PerformanceIndex",
    "SchedulePerformanceStatus",
    "ValidationRule",
    "calculate_activity_indicators",
    "calculate_indicators",
    "consolidate_project_indicators",
    "round_index",
    "round_money",
]
