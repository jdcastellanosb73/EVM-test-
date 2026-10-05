from decimal import Decimal

from app.domain.evm import EvmIndicators, round_index, round_money


def present(indicators: EvmIndicators) -> dict[str, object]:
    """Indicators as shown to a user: money to 2 decimals, indices to 4, plus each status."""

    def money(amount: Decimal | None) -> str | None:
        return None if amount is None else str(round_money(amount))

    def index(value: Decimal | None) -> str | None:
        return None if value is None else str(round_index(value))

    cpi = indicators.cost_performance_index
    spi = indicators.schedule_performance_index
    return {
        "bac": money(indicators.budget_at_completion),
        "pv": money(indicators.planned_value),
        "ev": money(indicators.earned_value),
        "ac": money(indicators.actual_cost),
        "cv": money(indicators.cost_variance),
        "sv": money(indicators.schedule_variance),
        "cpi": index(cpi.value),
        "cpi_status": cpi.status,
        "spi": index(spi.value),
        "spi_status": spi.status,
        "eac": money(indicators.estimate_at_completion),
        "vac": money(indicators.variance_at_completion),
    }
