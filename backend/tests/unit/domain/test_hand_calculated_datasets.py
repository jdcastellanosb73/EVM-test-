"""Expected values were calculated by hand before writing the engine (see AI_PROCESS.md)."""

from decimal import Decimal

import pytest

from app.domain.evm import (
    ActivityProgress,
    CostPerformanceStatus,
    SchedulePerformanceStatus,
    calculate_activity_indicators,
    consolidate_project_indicators,
)

from .helpers import present

UNDER = CostPerformanceStatus.UNDER_BUDGET
OVER = CostPerformanceStatus.OVER_BUDGET
COST_NA = CostPerformanceStatus.NOT_APPLICABLE
AHEAD = SchedulePerformanceStatus.AHEAD_OF_SCHEDULE
ON_TIME = SchedulePerformanceStatus.ON_SCHEDULE
BEHIND = SchedulePerformanceStatus.BEHIND_SCHEDULE
SCHEDULE_NA = SchedulePerformanceStatus.NOT_APPLICABLE


def activity(bac: str, planned: str, actual: str, cost: str) -> ActivityProgress:
    return ActivityProgress(
        budget_at_completion=Decimal(bac),
        planned_percent=Decimal(planned),
        actual_percent=Decimal(actual),
        actual_cost=Decimal(cost),
    )


# Demo seed "Portal de clientes" (db/init/02_seed.sql).
DESIGN_UX = activity("8000000", "100", "100", "7200000")
BACKEND_DEVELOPMENT = activity("20000000", "60", "45", "12000000")
QA_TESTING = activity("6000000", "20", "0", "0")

# Hand exercise A-D used to learn EVM before coding.
EXERCISE_DESIGN = activity("20000000", "100", "100", "18000000")
EXERCISE_DEVELOPMENT = activity("50000000", "60", "40", "25000000")
EXERCISE_TESTING = activity("10000000", "20", "30", "2000000")
EXERCISE_DEPLOYMENT = activity("8000000", "0", "0", "0")


@pytest.mark.parametrize(
    ("progress", "expected"),
    [
        pytest.param(
            DESIGN_UX,
            {
                "bac": "8000000.00", "pv": "8000000.00", "ev": "8000000.00", "ac": "7200000.00",
                "cv": "800000.00", "sv": "0.00",
                "cpi": "1.1111", "cpi_status": UNDER, "spi": "1.0000", "spi_status": ON_TIME,
                "eac": "7200000.00", "vac": "800000.00",
            },
            id="demo-design-ux",
        ),
        pytest.param(
            BACKEND_DEVELOPMENT,
            {
                "bac": "20000000.00", "pv": "12000000.00", "ev": "9000000.00",
                "ac": "12000000.00", "cv": "-3000000.00", "sv": "-3000000.00",
                "cpi": "0.7500", "cpi_status": OVER, "spi": "0.7500", "spi_status": BEHIND,
                "eac": "26666666.67", "vac": "-6666666.67",
            },
            id="demo-backend-development",
        ),
        pytest.param(
            QA_TESTING,
            {
                "bac": "6000000.00", "pv": "1200000.00", "ev": "0.00", "ac": "0.00",
                "cv": "0.00", "sv": "-1200000.00",
                "cpi": None, "cpi_status": COST_NA, "spi": "0.0000", "spi_status": BEHIND,
                "eac": None, "vac": None,
            },
            id="demo-qa-testing-not-started-but-planned",
        ),
        pytest.param(
            EXERCISE_DESIGN,
            {
                "bac": "20000000.00", "pv": "20000000.00", "ev": "20000000.00",
                "ac": "18000000.00", "cv": "2000000.00", "sv": "0.00",
                "cpi": "1.1111", "cpi_status": UNDER, "spi": "1.0000", "spi_status": ON_TIME,
                "eac": "18000000.00", "vac": "2000000.00",
            },
            id="exercise-a-design",
        ),
        pytest.param(
            EXERCISE_DEVELOPMENT,
            {
                "bac": "50000000.00", "pv": "30000000.00", "ev": "20000000.00",
                "ac": "25000000.00", "cv": "-5000000.00", "sv": "-10000000.00",
                "cpi": "0.8000", "cpi_status": OVER, "spi": "0.6667", "spi_status": BEHIND,
                "eac": "62500000.00", "vac": "-12500000.00",
            },
            id="exercise-b-development",
        ),
        pytest.param(
            EXERCISE_TESTING,
            {
                "bac": "10000000.00", "pv": "2000000.00", "ev": "3000000.00",
                "ac": "2000000.00", "cv": "1000000.00", "sv": "1000000.00",
                "cpi": "1.5000", "cpi_status": UNDER, "spi": "1.5000", "spi_status": AHEAD,
                "eac": "6666666.67", "vac": "3333333.33",
            },
            id="exercise-c-testing",
        ),
        pytest.param(
            EXERCISE_DEPLOYMENT,
            {
                "bac": "8000000.00", "pv": "0.00", "ev": "0.00", "ac": "0.00",
                "cv": "0.00", "sv": "0.00",
                "cpi": None, "cpi_status": COST_NA, "spi": None, "spi_status": SCHEDULE_NA,
                "eac": None, "vac": None,
            },
            id="exercise-d-deployment-not-started",
        ),
    ],
)  # fmt: skip
def test_activity_indicators_match_hand_calculation(
    progress: ActivityProgress, expected: dict[str, object]
) -> None:
    assert present(calculate_activity_indicators(progress)) == expected


def test_demo_project_consolidation_matches_hand_calculation() -> None:
    indicators = consolidate_project_indicators([DESIGN_UX, BACKEND_DEVELOPMENT, QA_TESTING])

    assert present(indicators) == {
        "bac": "34000000.00", "pv": "21200000.00", "ev": "17000000.00", "ac": "19200000.00",
        "cv": "-2200000.00", "sv": "-4200000.00",
        "cpi": "0.8854", "cpi_status": OVER, "spi": "0.8019", "spi_status": BEHIND,
        "eac": "38400000.00", "vac": "-4400000.00",
    }  # fmt: skip


def test_exercise_project_consolidation_matches_hand_calculation() -> None:
    indicators = consolidate_project_indicators(
        [EXERCISE_DESIGN, EXERCISE_DEVELOPMENT, EXERCISE_TESTING, EXERCISE_DEPLOYMENT]
    )

    assert present(indicators) == {
        "bac": "88000000.00", "pv": "52000000.00", "ev": "43000000.00", "ac": "45000000.00",
        "cv": "-2000000.00", "sv": "-9000000.00",
        "cpi": "0.9556", "cpi_status": OVER, "spi": "0.8269", "spi_status": BEHIND,
        "eac": "92093023.26", "vac": "-4093023.26",
    }  # fmt: skip


def test_brief_example_spent_sixty_percent_with_forty_percent_done() -> None:
    """The brief's warning sign: 60% of the budget spent with only 40% of the work done."""
    indicators = calculate_activity_indicators(activity("100000000", "40", "40", "60000000"))

    shown = present(indicators)
    assert shown["cv"] == "-20000000.00"
    assert shown["cpi"] == "0.6667"
    assert shown["cpi_status"] == OVER
    assert shown["eac"] == "150000000.00"
    assert shown["vac"] == "-50000000.00"
