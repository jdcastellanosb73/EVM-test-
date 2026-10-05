"""Every CPI and SPI status has a reading that names the verdict the enunciado asks for."""

import pytest

from app.domain.evm import (
    CostPerformanceStatus,
    SchedulePerformanceStatus,
    interpret_cost_performance,
    interpret_schedule_performance,
)


@pytest.mark.parametrize(
    ("status", "verdict"),
    [
        (CostPerformanceStatus.UNDER_BUDGET, "Bajo presupuesto"),
        (CostPerformanceStatus.ON_BUDGET, "En presupuesto"),
        (CostPerformanceStatus.OVER_BUDGET, "Sobre presupuesto"),
        (CostPerformanceStatus.NOT_APPLICABLE, "No aplica"),
    ],
)
def test_cost_interpretation_starts_with_its_verdict(
    status: CostPerformanceStatus, verdict: str
) -> None:
    assert interpret_cost_performance(status).startswith(verdict)


@pytest.mark.parametrize(
    ("status", "verdict"),
    [
        (SchedulePerformanceStatus.AHEAD_OF_SCHEDULE, "Adelantado"),
        (SchedulePerformanceStatus.ON_SCHEDULE, "A tiempo"),
        (SchedulePerformanceStatus.BEHIND_SCHEDULE, "Atrasado"),
        (SchedulePerformanceStatus.NOT_APPLICABLE, "No aplica"),
    ],
)
def test_schedule_interpretation_starts_with_its_verdict(
    status: SchedulePerformanceStatus, verdict: str
) -> None:
    assert interpret_schedule_performance(status).startswith(verdict)
