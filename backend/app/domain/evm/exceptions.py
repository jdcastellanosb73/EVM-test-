from enum import StrEnum


class ValidationRule(StrEnum):
    MUST_BE_FINITE = "must be a finite number"
    MUST_BE_POSITIVE = "must be greater than 0"
    MUST_BE_PERCENTAGE = "must be between 0 and 100"
    MUST_BE_NON_NEGATIVE = "must be greater than or equal to 0"


class InvalidActivityProgressError(ValueError):
    """An activity value violates a domain rule."""

    def __init__(self, field: str, rule: ValidationRule) -> None:
        self.field = field
        self.rule = rule
        super().__init__(f"{field} {rule}")
