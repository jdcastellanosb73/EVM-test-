from decimal import ROUND_HALF_UP, Decimal

ZERO = Decimal(0)
PERCENT_SCALE = Decimal(100)
MIN_PERCENT = ZERO
MAX_PERCENT = PERCENT_SCALE

# A performance index of exactly 1 means the work goes exactly as planned.
PERFORMANCE_BASELINE = Decimal(1)

MONEY_QUANTUM = Decimal("0.01")
INDEX_QUANTUM = Decimal("0.0001")
PRESENTATION_ROUNDING = ROUND_HALF_UP
