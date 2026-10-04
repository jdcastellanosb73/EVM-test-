"""Invariants that must hold for any valid input. Each strategy is bounded to where its
invariant is defined; the undefined zones (AC = 0, PV = 0, EV = 0) are covered by
test_edge_cases.py with fixed values."""

from decimal import Decimal

from hypothesis import given
from hypothesis import strategies as st

from app.domain.evm import ActivityProgress, calculate_activity_indicators

BASELINE = Decimal(1)
MIN_MONEY = Decimal("0.01")
MAX_MONEY = Decimal(1_000_000_000)
MIN_POSITIVE_PERCENT = Decimal("0.01")
MAX_PERCENT = Decimal(100)
RELATIVE_TOLERANCE = Decimal("1e-20")

positive_money = st.decimals(min_value=MIN_MONEY, max_value=MAX_MONEY, places=2)
percent = st.decimals(min_value=Decimal(0), max_value=MAX_PERCENT, places=2)
positive_percent = st.decimals(min_value=MIN_POSITIVE_PERCENT, max_value=MAX_PERCENT, places=2)


def sign(value: Decimal) -> int:
    return (value > 0) - (value < 0)


def progress(bac: Decimal, planned: Decimal, actual: Decimal, cost: Decimal) -> ActivityProgress:
    return ActivityProgress(
        budget_at_completion=bac, planned_percent=planned, actual_percent=actual, actual_cost=cost
    )


@given(bac=positive_money, planned=percent, actual=percent, cost=positive_money)
def test_cost_variance_sign_matches_cpi_against_one(
    bac: Decimal, planned: Decimal, actual: Decimal, cost: Decimal
) -> None:
    indicators = calculate_activity_indicators(progress(bac, planned, actual, cost))
    cpi = indicators.cost_performance_index.value

    assert cpi is not None
    assert sign(indicators.cost_variance) == sign(cpi - BASELINE)


@given(bac=positive_money, planned=positive_percent, actual=percent, cost=positive_money)
def test_schedule_variance_sign_matches_spi_against_one(
    bac: Decimal, planned: Decimal, actual: Decimal, cost: Decimal
) -> None:
    indicators = calculate_activity_indicators(progress(bac, planned, actual, cost))
    spi = indicators.schedule_performance_index.value

    assert spi is not None
    assert sign(indicators.schedule_variance) == sign(spi - BASELINE)


@given(bac=positive_money, planned=percent, actual=positive_percent, cost=positive_money)
def test_estimate_at_completion_is_consistent_with_cpi_and_cost_variance(
    bac: Decimal, planned: Decimal, actual: Decimal, cost: Decimal
) -> None:
    indicators = calculate_activity_indicators(progress(bac, planned, actual, cost))
    cpi = indicators.cost_performance_index.value
    eac = indicators.estimate_at_completion
    vac = indicators.variance_at_completion

    assert cpi is not None
    assert eac is not None
    assert vac is not None
    assert abs(eac * cpi - bac) <= bac * RELATIVE_TOLERANCE
    assert sign(vac) == sign(indicators.cost_variance)
