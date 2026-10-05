"""The project is consolidated with ratios of sums, never by averaging activity indices."""

from decimal import Decimal
from statistics import fmean

from app.domain.evm import (
    ActivityProgress,
    CostPerformanceStatus,
    EarnedValueBase,
    calculate_activity_indicators,
    calculate_indicators,
    consolidate_project_indicators,
    round_index,
)

# Large activity spending twice what it earns: EV 50, AC 100, CPI 0.50.
LARGE_INEFFICIENT_MIGRATION = ActivityProgress(
    budget_at_completion=Decimal(100),
    planned_percent=Decimal(50),
    actual_percent=Decimal(50),
    actual_cost=Decimal(100),
)
# Small activity earning twice what it spends: EV 2, AC 1, CPI 2.00.
SMALL_EFFICIENT_MANUAL = ActivityProgress(
    budget_at_completion=Decimal(2),
    planned_percent=Decimal(100),
    actual_percent=Decimal(100),
    actual_cost=Decimal(1),
)


def cpi_of(progress: ActivityProgress) -> Decimal:
    cpi = calculate_activity_indicators(progress).cost_performance_index.value
    assert cpi is not None
    return cpi


def test_averaging_cpis_would_invert_the_verdict_but_ratio_of_sums_does_not() -> None:
    activities = [LARGE_INEFFICIENT_MIGRATION, SMALL_EFFICIENT_MANUAL]

    project = consolidate_project_indicators(activities)

    assert fmean(cpi_of(item) for item in activities) == 1.25
    assert project.cost_performance_index.value is not None
    assert round_index(project.cost_performance_index.value) == Decimal("0.5149")
    assert project.cost_performance_index.status is CostPerformanceStatus.OVER_BUDGET
    assert project.cost_variance == Decimal(-49)


def test_project_cpi_is_the_actual_cost_weighted_mean_of_activity_cpis() -> None:
    activities = [LARGE_INEFFICIENT_MIGRATION, SMALL_EFFICIENT_MANUAL]
    weighted_sum = sum(cpi_of(item) * item.actual_cost for item in activities)
    total_cost = sum(item.actual_cost for item in activities)

    project = consolidate_project_indicators(activities)

    assert project.cost_performance_index.value == weighted_sum / total_cost


def test_consolidation_reuses_the_activity_calculation_on_summed_amounts() -> None:
    activities = [LARGE_INEFFICIENT_MIGRATION, SMALL_EFFICIENT_MANUAL]
    summed_base = EarnedValueBase(
        budget_at_completion=Decimal(102),
        planned_value=Decimal(52),
        earned_value=Decimal(52),
        actual_cost=Decimal(101),
    )

    assert consolidate_project_indicators(activities) == calculate_indicators(summed_base)


def test_project_with_one_activity_equals_that_activity() -> None:
    assert consolidate_project_indicators(
        [LARGE_INEFFICIENT_MIGRATION]
    ) == calculate_activity_indicators(LARGE_INEFFICIENT_MIGRATION)


def test_splitting_an_activity_does_not_change_the_project_cpi() -> None:
    half_of_migration = ActivityProgress(
        budget_at_completion=Decimal(50),
        planned_percent=Decimal(50),
        actual_percent=Decimal(50),
        actual_cost=Decimal(50),
    )

    whole_plan = [LARGE_INEFFICIENT_MIGRATION, SMALL_EFFICIENT_MANUAL]
    split_plan = [half_of_migration, half_of_migration, SMALL_EFFICIENT_MANUAL]

    whole = consolidate_project_indicators(whole_plan)
    split = consolidate_project_indicators(split_plan)

    assert split.cost_performance_index == whole.cost_performance_index
    assert fmean(map(cpi_of, whole_plan)) == 1.25
    assert fmean(map(cpi_of, split_plan)) == 1.0
