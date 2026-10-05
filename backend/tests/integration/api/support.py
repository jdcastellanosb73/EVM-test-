from decimal import Decimal
from typing import Any

from fastapi.testclient import TestClient

PROJECTS = "/api/v1/projects"
PROJECT = "/api/v1/projects/{project_id}"
ACTIVITIES = "/api/v1/projects/{project_id}/activities"
ACTIVITY = "/api/v1/projects/{project_id}/activities/{activity_id}"

MONEY_FIELDS = ("bac", "pv", "ev", "ac", "cv", "sv", "eac", "vac")

# Demo dataset "Portal de clientes", amounts as strings like any client should send them.
DESIGN_UX = {
    "name": "Diseño UX",
    "budget_at_completion": "8000000.00",
    "planned_percent": "100",
    "actual_percent": "100",
    "actual_cost": "7200000.00",
}
BACKEND_DEVELOPMENT = {
    "name": "Desarrollo backend",
    "budget_at_completion": "20000000.00",
    "planned_percent": "60",
    "actual_percent": "45",
    "actual_cost": "12000000.00",
}
QA_TESTING = {
    "name": "Pruebas QA",
    "budget_at_completion": "6000000.00",
    "planned_percent": "20",
    "actual_percent": "0",
    "actual_cost": "0",
}


def create_project(client: TestClient, name: str = "Portal de clientes") -> dict[str, Any]:
    response = client.post(PROJECTS, json={"name": name, "cutoff_date": "2026-10-03"})
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def create_activity(client: TestClient, project_id: int, payload: dict[str, str]) -> dict[str, Any]:
    response = client.post(ACTIVITIES.format(project_id=project_id), json=payload)
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def create_demo_project(client: TestClient) -> dict[str, Any]:
    project = create_project(client)
    for payload in (DESIGN_UX, BACKEND_DEVELOPMENT, QA_TESTING):
        create_activity(client, project["id"], payload)
    return project


def decimal_from_json(value: Any) -> Decimal:
    """Money and indices must travel as a JSON string; parse it as Decimal, never as float."""
    assert isinstance(value, str), f"expected a decimal string, got {value!r}"
    return Decimal(value)


def assert_money_fields_are_strings(indicators: dict[str, Any]) -> None:
    for field in MONEY_FIELDS:
        value = indicators[field]
        assert value is None or isinstance(value, str), f"{field} = {value!r}"
    for index in ("cpi", "spi"):
        value = indicators[index]["value"]
        assert value is None or isinstance(value, str), f"{index} = {value!r}"


def value_and_status(index: dict[str, Any]) -> dict[str, Any]:
    """The machine-readable part of a CPI/SPI response; the interpretation is tested apart."""
    return {"value": index["value"], "status": index["status"]}
