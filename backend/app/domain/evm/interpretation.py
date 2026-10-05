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


COST_PERFORMANCE_INTERPRETATIONS: dict[CostPerformanceStatus, str] = {
    CostPerformanceStatus.UNDER_BUDGET: (
        "Bajo presupuesto: CPI mayor a 1, el trabajo realizado vale más de lo que ha costado."
    ),
    CostPerformanceStatus.ON_BUDGET: (
        "En presupuesto: CPI igual a 1, el costo corresponde exactamente al trabajo realizado."
    ),
    CostPerformanceStatus.OVER_BUDGET: (
        "Sobre presupuesto: CPI menor a 1, se está gastando más de lo que se avanza."
    ),
    CostPerformanceStatus.NOT_APPLICABLE: (
        "No aplica: sin costo real registrado (AC = 0) no se puede medir la eficiencia en costos."
    ),
}

SCHEDULE_PERFORMANCE_INTERPRETATIONS: dict[SchedulePerformanceStatus, str] = {
    SchedulePerformanceStatus.AHEAD_OF_SCHEDULE: (
        "Adelantado: SPI mayor a 1, se ha avanzado más de lo planificado a la fecha de corte."
    ),
    SchedulePerformanceStatus.ON_SCHEDULE: (
        "A tiempo: SPI igual a 1, el avance coincide con lo planificado a la fecha de corte."
    ),
    SchedulePerformanceStatus.BEHIND_SCHEDULE: (
        "Atrasado: SPI menor a 1, se ha avanzado menos de lo planificado a la fecha de corte."
    ),
    SchedulePerformanceStatus.NOT_APPLICABLE: (
        "No aplica: sin avance planificado a la fecha de corte (PV = 0) no se puede medir "
        "el cronograma."
    ),
}


def interpret_cost_performance(status: CostPerformanceStatus) -> str:
    """Plain-language reading of a CPI status for the project leader."""
    return COST_PERFORMANCE_INTERPRETATIONS[status]


def interpret_schedule_performance(status: SchedulePerformanceStatus) -> str:
    """Plain-language reading of an SPI status for the project leader."""
    return SCHEDULE_PERFORMANCE_INTERPRETATIONS[status]
