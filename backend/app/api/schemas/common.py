"""Shared contract types. Money, percentages and indices travel as JSON strings so that
clients never lose precision by parsing them as binary floating point numbers."""

from decimal import Decimal
from typing import Annotated, Any

from fastapi import Path
from pydantic import BaseModel, Field, PlainSerializer, WithJsonSchema

from app.domain.evm import round_index, round_money


def _decimal_string_schema(description: str, example: str) -> WithJsonSchema:
    schema: dict[str, Any] = {
        "type": "string",
        "format": "decimal",
        "description": description,
        "examples": [example],
    }
    return WithJsonSchema(schema, mode="serialization")


def _money_to_string(amount: Decimal) -> str:
    return str(round_money(amount))


def _index_to_string(index: Decimal) -> str:
    return str(round_index(index))


MoneyString = Annotated[
    Decimal,
    PlainSerializer(_money_to_string, return_type=str),
    _decimal_string_schema("Amount rounded half up to 2 decimals", "20000000.00"),
]
IndexString = Annotated[
    Decimal,
    PlainSerializer(_index_to_string, return_type=str),
    _decimal_string_schema("Performance index rounded half up to 4 decimals", "0.7500"),
]
PercentString = Annotated[
    Decimal,
    PlainSerializer(str, return_type=str),
    _decimal_string_schema("Percentage on the 0-100 scale", "60.00"),
]

ProjectId = Annotated[int, Path(gt=0, description="Project identifier")]
ActivityId = Annotated[int, Path(gt=0, description="Activity identifier")]


class ErrorDetail(BaseModel):
    field: str | None = Field(
        description="Location of the invalid value, e.g. body.budget_at_completion",
        examples=["body.budget_at_completion"],
    )
    message: str = Field(examples=["Input should be greater than 0"])


class ErrorResponse(BaseModel):
    """Single error format for every 4xx response."""

    code: str = Field(
        description=(
            "Stable machine-readable code: PROJECT_NOT_FOUND, ACTIVITY_NOT_FOUND, "
            "PROJECT_NAME_TAKEN, ACTIVITY_NAME_TAKEN, VALIDATION_ERROR, or the HTTP status "
            "name (e.g. NOT_FOUND) for unknown routes"
        ),
        examples=["PROJECT_NOT_FOUND"],
    )
    message: str = Field(examples=["Project 42 not found"])
    details: list[ErrorDetail] = Field(
        default_factory=list,
        description="Per-field problems; empty unless code is VALIDATION_ERROR",
    )
