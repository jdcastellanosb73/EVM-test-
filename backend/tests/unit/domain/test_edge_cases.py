"""Business rules for indicators that cannot be computed (division by zero)."""

from decimal import Decimal

from app.domain.evm import (
    CostPerformanceStatus,
    EarnedValueBase,
    SchedulePerformanceStatus,
    calculate_indicators,
    consolidate_project_indicators,
)

ZERO = Decimal(0)


def base(bac: str, pv: str, ev: str, ac: str) -> EarnedValueBase:
    return EarnedValueBase(
        budget_at_completion=Decimal(bac),
        planned_value=Decimal(pv),
        earned_value=Decimal(ev),
        actual_cost=Decimal(ac),
    )


def test_zero_actual_cost_with_progress_makes_cpi_eac_and_vac_not_applicable() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="500", ev="400", ac="0"))

    assert indicators.cost_performance_index.value is None
    assert indicators.cost_performance_index.status is CostPerformanceStatus.NOT_APPLICABLE
    assert indicators.estimate_at_completion is None
    assert indicators.variance_at_completion is None
    assert indicators.cost_variance == Decimal(400)


def test_zero_actual_cost_without_progress_makes_cpi_eac_and_vac_not_applicable() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="500", ev="0", ac="0"))

    assert indicators.cost_performance_index.value is None
    assert indicators.cost_performance_index.status is CostPerformanceStatus.NOT_APPLICABLE
    assert indicators.estimate_at_completion is None
    assert indicators.variance_at_completion is None


def test_zero_earned_value_with_cost_is_a_real_zero_cpi_over_budget() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="500", ev="0", ac="300"))

    assert indicators.cost_performance_index.value == ZERO
    assert indicators.cost_performance_index.status is CostPerformanceStatus.OVER_BUDGET
    assert indicators.estimate_at_completion is None
    assert indicators.variance_at_completion is None
    assert indicators.cost_variance == Decimal(-300)


def test_zero_earned_value_with_planned_value_is_a_real_zero_spi_behind_schedule() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="500", ev="0", ac="300"))

    assert indicators.schedule_performance_index.value == ZERO
    assert indicators.schedule_performance_index.status is SchedulePerformanceStatus.BEHIND_SCHEDULE


def test_zero_planned_value_with_progress_makes_spi_not_applicable() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="0", ev="100", ac="100"))

    assert indicators.schedule_performance_index.value is None
    assert indicators.schedule_performance_index.status is SchedulePerformanceStatus.NOT_APPLICABLE
    assert indicators.schedule_variance == Decimal(100)


def test_zero_planned_value_without_progress_makes_spi_not_applicable() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="0", ev="0", ac="0"))

    assert indicators.schedule_performance_index.value is None
    assert indicators.schedule_performance_index.status is SchedulePerformanceStatus.NOT_APPLICABLE


def test_project_without_activities_has_zero_totals_and_no_indices() -> None:
    indicators = consolidate_project_indicators([])

    assert indicators.budget_at_completion == ZERO
    assert indicators.planned_value == ZERO
    assert indicators.earned_value == ZERO
    assert indicators.actual_cost == ZERO
    assert indicators.cost_variance == ZERO
    assert indicators.schedule_variance == ZERO
    assert indicators.cost_performance_index.value is None
    assert indicators.cost_performance_index.status is CostPerformanceStatus.NOT_APPLICABLE
    assert indicators.schedule_performance_index.value is None
    assert indicators.schedule_performance_index.status is SchedulePerformanceStatus.NOT_APPLICABLE
    assert indicators.estimate_at_completion is None
    assert indicators.variance_at_completion is None


def test_earned_value_equal_to_actual_cost_is_on_budget() -> None:
    indicators = calculate_indicators(base(bac="1000", pv="400", ev="400", ac="400"))

    assert indicators.cost_performance_index.value == Decimal(1)
    assert indicators.cost_performance_index.status is CostPerformanceStatus.ON_BUDGET
    assert indicators.estimate_at_completion == Decimal(1000)
    assert indicators.variance_at_completion == ZERO
