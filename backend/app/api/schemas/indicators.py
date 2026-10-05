from typing import Self

from pydantic import BaseModel, Field

from app.api.schemas.common import IndexString, MoneyString
from app.domain.evm import CostPerformanceStatus, EvmIndicators, SchedulePerformanceStatus


class CostPerformanceIndexResponse(BaseModel):
    value: IndexString | None = Field(description="EV / AC. Null when AC is 0")
    status: CostPerformanceStatus = Field(
        description="Decided on the unrounded value: above 1 under budget, below 1 over budget"
    )


class SchedulePerformanceIndexResponse(BaseModel):
    value: IndexString | None = Field(description="EV / PV. Null when PV is 0")
    status: SchedulePerformanceStatus = Field(
        description="Decided on the unrounded value: above 1 ahead, below 1 behind schedule"
    )


class IndicatorsResponse(BaseModel):
    """Earned Value indicators, the same shape for an activity and for a project."""

    bac: MoneyString = Field(description="Budget at Completion")
    pv: MoneyString = Field(description="Planned Value = planned % x BAC")
    ev: MoneyString = Field(description="Earned Value = actual % x BAC")
    ac: MoneyString = Field(description="Actual Cost")
    cv: MoneyString = Field(description="Cost Variance = EV - AC")
    sv: MoneyString = Field(description="Schedule Variance = EV - PV")
    cpi: CostPerformanceIndexResponse = Field(description="Cost Performance Index")
    spi: SchedulePerformanceIndexResponse = Field(description="Schedule Performance Index")
    eac: MoneyString | None = Field(
        description="Estimate at Completion = BAC / CPI. Null when CPI is null or 0"
    )
    vac: MoneyString | None = Field(
        description="Variance at Completion = BAC - EAC. Null when EAC is null"
    )

    @classmethod
    def from_indicators(cls, indicators: EvmIndicators) -> Self:
        cpi = indicators.cost_performance_index
        spi = indicators.schedule_performance_index
        return cls(
            bac=indicators.budget_at_completion,
            pv=indicators.planned_value,
            ev=indicators.earned_value,
            ac=indicators.actual_cost,
            cv=indicators.cost_variance,
            sv=indicators.schedule_variance,
            cpi=CostPerformanceIndexResponse(value=cpi.value, status=cpi.status),
            spi=SchedulePerformanceIndexResponse(value=spi.value, status=spi.status),
            eac=indicators.estimate_at_completion,
            vac=indicators.variance_at_completion,
        )
