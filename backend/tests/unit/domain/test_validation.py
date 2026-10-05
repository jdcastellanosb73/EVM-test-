from decimal import Decimal

import pytest

from app.domain.evm import ActivityProgress, InvalidActivityProgressError, ValidationRule

VALID_FIELDS = {
    "budget_at_completion": Decimal(1000),
    "planned_percent": Decimal(50),
    "actual_percent": Decimal(40),
    "actual_cost": Decimal(300),
}


def build(**overrides: Decimal) -> ActivityProgress:
    return ActivityProgress(**{**VALID_FIELDS, **overrides})


@pytest.mark.parametrize(
    ("field", "value", "rule"),
    [
        ("budget_at_completion", Decimal(0), ValidationRule.MUST_BE_POSITIVE),
        ("budget_at_completion", Decimal("-0.01"), ValidationRule.MUST_BE_POSITIVE),
        ("planned_percent", Decimal("-0.01"), ValidationRule.MUST_BE_PERCENTAGE),
        ("planned_percent", Decimal("100.01"), ValidationRule.MUST_BE_PERCENTAGE),
        ("actual_percent", Decimal("-0.01"), ValidationRule.MUST_BE_PERCENTAGE),
        ("actual_percent", Decimal("100.01"), ValidationRule.MUST_BE_PERCENTAGE),
        ("actual_cost", Decimal("-0.01"), ValidationRule.MUST_BE_NON_NEGATIVE),
        ("actual_cost", Decimal("NaN"), ValidationRule.MUST_BE_FINITE),
        ("budget_at_completion", Decimal("Infinity"), ValidationRule.MUST_BE_FINITE),
    ],
)
def test_invalid_activity_progress_is_rejected(
    field: str, value: Decimal, rule: ValidationRule
) -> None:
    with pytest.raises(InvalidActivityProgressError) as error:
        build(**{field: value})

    assert error.value.field == field
    assert error.value.rule is rule
    assert field in str(error.value)


@pytest.mark.parametrize(
    "overrides",
    [
        {"planned_percent": Decimal(0), "actual_percent": Decimal(0)},
        {"planned_percent": Decimal(100), "actual_percent": Decimal(100)},
        {"actual_cost": Decimal(0)},
        {"budget_at_completion": Decimal("0.01")},
    ],
)
def test_boundary_values_are_accepted(overrides: dict[str, Decimal]) -> None:
    progress = build(**overrides)

    for field, value in overrides.items():
        assert getattr(progress, field) == value


def test_cost_without_progress_is_accepted_because_it_is_the_alert_evm_must_show() -> None:
    progress = build(actual_percent=Decimal(0), actual_cost=Decimal(500))

    assert progress.actual_cost == Decimal(500)
