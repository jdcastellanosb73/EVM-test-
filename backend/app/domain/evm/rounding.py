"""Presentation rounding. The domain keeps full precision; only the edges call these."""

from decimal import Decimal

from app.domain.evm.constants import INDEX_QUANTUM, MONEY_QUANTUM, PRESENTATION_ROUNDING


def round_money(amount: Decimal) -> Decimal:
    return amount.quantize(MONEY_QUANTUM, rounding=PRESENTATION_ROUNDING)


def round_index(index: Decimal) -> Decimal:
    return index.quantize(INDEX_QUANTUM, rounding=PRESENTATION_ROUNDING)
