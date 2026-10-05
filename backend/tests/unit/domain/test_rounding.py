"""Full Decimal precision internally; rounding only for presentation."""

from decimal import ROUND_HALF_UP, Decimal

from app.domain.evm import (
    PRESENTATION_ROUNDING,
    CostPerformanceStatus,
    EarnedValueBase,
    SchedulePerformanceStatus,
    calculate_indicators,
    round_index,
    round_money,
)


def test_presentation_rounding_mode_is_half_up() -> None:
    assert PRESENTATION_ROUNDING == ROUND_HALF_UP


def test_money_is_presented_with_two_decimals_rounding_half_up() -> None:
    assert str(round_money(Decimal("26666666.665"))) == "26666666.67"
    assert str(round_money(Decimal("-6666666.665"))) == "-6666666.67"
    assert str(round_money(Decimal("8000000"))) == "8000000.00"


def test_indices_are_presented_with_four_decimals_rounding_half_up() -> None:
    assert str(round_index(Decimal("0.66665"))) == "0.6667"
    assert str(round_index(Decimal(1))) == "1.0000"


def test_cpi_status_is_decided_on_the_unrounded_value() -> None:
    indicators = calculate_indicators(
        EarnedValueBase(
            budget_at_completion=Decimal(200000),
            planned_value=Decimal(99996),
            earned_value=Decimal(99996),
            actual_cost=Decimal(100000),
        )
    )
    cpi = indicators.cost_performance_index

    assert cpi.value == Decimal("0.99996")
    assert str(round_index(cpi.value)) == "1.0000"
    assert cpi.status is CostPerformanceStatus.OVER_BUDGET


def test_spi_status_is_decided_on_the_unrounded_value() -> None:
    indicators = calculate_indicators(
        EarnedValueBase(
            budget_at_completion=Decimal(200000),
            planned_value=Decimal(100000),
            earned_value=Decimal(100004),
            actual_cost=Decimal(100004),
        )
    )
    spi = indicators.schedule_performance_index

    assert spi.value == Decimal("1.00004")
    assert str(round_index(spi.value)) == "1.0000"
    assert spi.status is SchedulePerformanceStatus.AHEAD_OF_SCHEDULE


def test_estimate_at_completion_keeps_full_precision_until_presented() -> None:
    indicators = calculate_indicators(
        EarnedValueBase(
            budget_at_completion=Decimal(20000000),
            planned_value=Decimal(12000000),
            earned_value=Decimal(9000000),
            actual_cost=Decimal(12000000),
        )
    )

    assert indicators.estimate_at_completion is not None
    assert indicators.estimate_at_completion != round_money(indicators.estimate_at_completion)
    assert str(round_money(indicators.estimate_at_completion)) == "26666666.67"
