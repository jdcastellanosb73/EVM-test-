from decimal import Decimal
from enum import StrEnum

from app.domain.evm.constants import PERFORMANCE_BASELINE
from app.domain.evm.models import CostPerformanceStatus, SchedulePerformanceStatus


def classify_cost_performance(cpi: Decimal | None) -> CostPerformanceStatus:
    return _classify(
        cpi,
        above=CostPerformanceStatus.UNDER_BUDGET,
        at=CostPerformanceStatus.ON_BUDGET,
        below=CostPerformanceStatus.OVER_BUDGET,
        undefined=CostPerformanceStatus.NOT_APPLICABLE,
    )


def classify_schedule_performance(spi: Decimal | None) -> SchedulePerformanceStatus:
    return _classify(
        spi,
        above=SchedulePerformanceStatus.AHEAD_OF_SCHEDULE,
        at=SchedulePerformanceStatus.ON_SCHEDULE,
        below=SchedulePerformanceStatus.BEHIND_SCHEDULE,
        undefined=SchedulePerformanceStatus.NOT_APPLICABLE,
    )


def _classify[StatusT: StrEnum](
    index: Decimal | None, *, above: StatusT, at: StatusT, below: StatusT, undefined: StatusT
) -> StatusT:
    """Compare the unrounded index with 1, so 0.99996 is still below even if shown as 1.0000."""
    if index is None:
        return undefined
    if index > PERFORMANCE_BASELINE:
        return above
    if index < PERFORMANCE_BASELINE:
        return below
    return at
