from collections.abc import Iterable
from decimal import Decimal

from app.domain.evm.constants import ZERO
from app.domain.evm.interpretation import (
    classify_cost_performance,
    classify_schedule_performance,
)
from app.domain.evm.models import (
    EMPTY_BASE,
    ActivityProgress,
    EarnedValueBase,
    EvmIndicators,
    PerformanceIndex,
)


def calculate_indicators(base: EarnedValueBase) -> EvmIndicators:
    """Compute every EVM indicator from the four base amounts, with full Decimal precision."""
    cpi = _ratio(base.earned_value, base.actual_cost)
    spi = _ratio(base.earned_value, base.planned_value)
    estimate_at_completion = _estimate_at_completion(base)
    return EvmIndicators(
        budget_at_completion=base.budget_at_completion,
        planned_value=base.planned_value,
        earned_value=base.earned_value,
        actual_cost=base.actual_cost,
        cost_variance=base.earned_value - base.actual_cost,
        schedule_variance=base.earned_value - base.planned_value,
        cost_performance_index=PerformanceIndex(cpi, classify_cost_performance(cpi)),
        schedule_performance_index=PerformanceIndex(spi, classify_schedule_performance(spi)),
        estimate_at_completion=estimate_at_completion,
        variance_at_completion=(
            None
            if estimate_at_completion is None
            else base.budget_at_completion - estimate_at_completion
        ),
    )


def calculate_activity_indicators(progress: ActivityProgress) -> EvmIndicators:
    return calculate_indicators(EarnedValueBase.from_activity(progress))


def consolidate_project_indicators(activities: Iterable[ActivityProgress]) -> EvmIndicators:
    """Sum the activity amounts and compute the indices on those sums (never average indices)."""
    project_base = sum(
        (EarnedValueBase.from_activity(progress) for progress in activities), start=EMPTY_BASE
    )
    return calculate_indicators(project_base)


def _ratio(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    return None if denominator == ZERO else numerator / denominator


def _estimate_at_completion(base: EarnedValueBase) -> Decimal | None:
    """EAC = BAC / CPI, written as BAC * AC / EV to avoid dividing by an already divided ratio.

    Undefined when AC = 0 (no CPI) or EV = 0 (CPI = 0, division by zero).
    """
    if ZERO in (base.actual_cost, base.earned_value):
        return None
    return base.budget_at_completion * base.actual_cost / base.earned_value
