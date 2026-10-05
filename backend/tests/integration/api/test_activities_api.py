from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from tests.integration.conftest import ContractChecker

from .support import (
    ACTIVITIES,
    ACTIVITY,
    BACKEND_DEVELOPMENT,
    DESIGN_UX,
    PROJECT,
    QA_TESTING,
    assert_money_fields_are_strings,
    create_activity,
    create_project,
    decimal_from_json,
    value_and_status,
)


@pytest.fixture
def project_id(api_client: TestClient) -> int:
    project_id: int = create_project(api_client)["id"]
    return project_id


def test_create_activity_returns_201_with_hand_calculated_indicators(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    response = api_client.post(ACTIVITIES.format(project_id=project_id), json=BACKEND_DEVELOPMENT)

    assert response.status_code == 201
    contract.check(response, "post", ACTIVITIES)
    body = response.json()
    assert response.headers["location"].endswith(
        f"/api/v1/projects/{project_id}/activities/{body['id']}"
    )
    assert body["project_id"] == project_id
    assert decimal_from_json(body["budget_at_completion"]) == Decimal("20000000.00")
    assert decimal_from_json(body["planned_percent"]) == Decimal(60)
    indicators = body["indicators"]
    assert_money_fields_are_strings(indicators)
    assert decimal_from_json(indicators["pv"]) == Decimal("12000000.00")
    assert decimal_from_json(indicators["ev"]) == Decimal("9000000.00")
    assert decimal_from_json(indicators["cv"]) == Decimal("-3000000.00")
    assert decimal_from_json(indicators["sv"]) == Decimal("-3000000.00")
    assert value_and_status(indicators["cpi"]) == {"value": "0.7500", "status": "OVER_BUDGET"}
    assert value_and_status(indicators["spi"]) == {"value": "0.7500", "status": "BEHIND_SCHEDULE"}
    assert indicators["cpi"]["interpretation"].startswith("Sobre presupuesto")
    assert indicators["spi"]["interpretation"].startswith("Atrasado")
    assert decimal_from_json(indicators["eac"]) == Decimal("26666666.67")
    assert decimal_from_json(indicators["vac"]) == Decimal("-6666666.67")


def test_activity_without_cost_has_not_applicable_cpi_and_no_estimate(
    api_client: TestClient, project_id: int
) -> None:
    indicators = create_activity(api_client, project_id, QA_TESTING)["indicators"]

    assert value_and_status(indicators["cpi"]) == {"value": None, "status": "NOT_APPLICABLE"}
    assert value_and_status(indicators["spi"]) == {"value": "0.0000", "status": "BEHIND_SCHEDULE"}
    assert indicators["eac"] is None
    assert indicators["vac"] is None


def test_create_activity_in_unknown_project_returns_404(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.post(ACTIVITIES.format(project_id=999999), json=DESIGN_UX)

    assert response.status_code == 404
    contract.check(response, "post", ACTIVITIES)
    assert response.json()["code"] == "PROJECT_NOT_FOUND"


def test_create_activity_with_taken_name_returns_409(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    create_activity(api_client, project_id, DESIGN_UX)

    response = api_client.post(ACTIVITIES.format(project_id=project_id), json=DESIGN_UX)

    assert response.status_code == 409
    contract.check(response, "post", ACTIVITIES)
    assert response.json()["code"] == "ACTIVITY_NAME_TAKEN"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("budget_at_completion", "0", id="bac-zero"),
        pytest.param("budget_at_completion", "-1000.00", id="bac-negative"),
        pytest.param("planned_percent", "-0.01", id="planned-below-0"),
        pytest.param("planned_percent", "100.01", id="planned-above-100"),
        pytest.param("actual_percent", "-1", id="actual-below-0"),
        pytest.param("actual_percent", "101", id="actual-above-100"),
        pytest.param("actual_cost", "-0.01", id="ac-negative"),
    ],
)
def test_create_activity_with_out_of_range_value_returns_422(
    api_client: TestClient, contract: ContractChecker, project_id: int, field: str, value: str
) -> None:
    response = api_client.post(
        ACTIVITIES.format(project_id=project_id), json={**DESIGN_UX, field: value}
    )

    assert response.status_code == 422
    contract.check(response, "post", ACTIVITIES)
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert [detail["field"] for detail in body["details"]] == [f"body.{field}"]


def test_list_activities_returns_them_in_creation_order(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    for payload in (DESIGN_UX, BACKEND_DEVELOPMENT, QA_TESTING):
        create_activity(api_client, project_id, payload)

    response = api_client.get(ACTIVITIES.format(project_id=project_id))

    assert response.status_code == 200
    contract.check(response, "get", ACTIVITIES)
    activities = response.json()
    assert [activity["name"] for activity in activities] == [
        "Diseño UX",
        "Desarrollo backend",
        "Pruebas QA",
    ]
    assert decimal_from_json(activities[0]["indicators"]["cpi"]["value"]) == Decimal("1.1111")


def test_list_activities_of_unknown_project_returns_404(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.get(ACTIVITIES.format(project_id=999999))

    assert response.status_code == 404
    contract.check(response, "get", ACTIVITIES)


def test_get_activity_returns_it_with_indicators(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    activity_id = create_activity(api_client, project_id, DESIGN_UX)["id"]

    response = api_client.get(ACTIVITY.format(project_id=project_id, activity_id=activity_id))

    assert response.status_code == 200
    contract.check(response, "get", ACTIVITY)
    indicators = response.json()["indicators"]
    assert value_and_status(indicators["cpi"]) == {"value": "1.1111", "status": "UNDER_BUDGET"}
    assert value_and_status(indicators["spi"]) == {"value": "1.0000", "status": "ON_SCHEDULE"}
    assert decimal_from_json(indicators["eac"]) == Decimal("7200000.00")


def test_get_unknown_activity_returns_404(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    response = api_client.get(ACTIVITY.format(project_id=project_id, activity_id=999999))

    assert response.status_code == 404
    contract.check(response, "get", ACTIVITY)
    assert response.json()["code"] == "ACTIVITY_NOT_FOUND"


def test_activity_is_not_reachable_through_another_project(
    api_client: TestClient, project_id: int
) -> None:
    activity_id = create_activity(api_client, project_id, DESIGN_UX)["id"]
    other_project_id = create_project(api_client, "Otro proyecto")["id"]

    response = api_client.get(ACTIVITY.format(project_id=other_project_id, activity_id=activity_id))

    assert response.status_code == 404
    assert response.json()["code"] == "ACTIVITY_NOT_FOUND"


def test_update_activity_recalculates_activity_and_project_indicators(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    activity_id = create_activity(api_client, project_id, BACKEND_DEVELOPMENT)["id"]
    on_track = {**BACKEND_DEVELOPMENT, "actual_percent": "60", "actual_cost": "12000000.00"}

    response = api_client.put(
        ACTIVITY.format(project_id=project_id, activity_id=activity_id), json=on_track
    )

    assert response.status_code == 200
    contract.check(response, "put", ACTIVITY)
    assert value_and_status(response.json()["indicators"]["cpi"]) == {
        "value": "1.0000",
        "status": "ON_BUDGET",
    }
    project = api_client.get(PROJECT.format(project_id=project_id)).json()
    assert value_and_status(project["indicators"]["spi"]) == {
        "value": "1.0000",
        "status": "ON_SCHEDULE",
    }


def test_update_unknown_activity_returns_404(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    response = api_client.put(
        ACTIVITY.format(project_id=project_id, activity_id=999999), json=DESIGN_UX
    )

    assert response.status_code == 404
    contract.check(response, "put", ACTIVITY)


def test_update_activity_with_negative_cost_returns_422(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    activity_id = create_activity(api_client, project_id, DESIGN_UX)["id"]

    response = api_client.put(
        ACTIVITY.format(project_id=project_id, activity_id=activity_id),
        json={**DESIGN_UX, "actual_cost": "-1"},
    )

    assert response.status_code == 422
    contract.check(response, "put", ACTIVITY)


def test_update_activity_to_a_taken_name_returns_409(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    create_activity(api_client, project_id, DESIGN_UX)
    activity_id = create_activity(api_client, project_id, QA_TESTING)["id"]

    response = api_client.put(
        ACTIVITY.format(project_id=project_id, activity_id=activity_id),
        json={**QA_TESTING, "name": DESIGN_UX["name"]},
    )

    assert response.status_code == 409
    contract.check(response, "put", ACTIVITY)
    assert response.json()["code"] == "ACTIVITY_NAME_TAKEN"


def test_delete_activity_returns_204_and_updates_the_consolidation(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    create_activity(api_client, project_id, DESIGN_UX)
    activity_id = create_activity(api_client, project_id, BACKEND_DEVELOPMENT)["id"]

    response = api_client.delete(ACTIVITY.format(project_id=project_id, activity_id=activity_id))

    assert response.status_code == 204
    contract.check(response, "delete", ACTIVITY)
    indicators = api_client.get(PROJECT.format(project_id=project_id)).json()["indicators"]
    assert decimal_from_json(indicators["bac"]) == Decimal("8000000.00")
    assert indicators["cpi"]["value"] == "1.1111"


def test_delete_unknown_activity_returns_404(
    api_client: TestClient, contract: ContractChecker, project_id: int
) -> None:
    response = api_client.delete(ACTIVITY.format(project_id=project_id, activity_id=999999))

    assert response.status_code == 404
    contract.check(response, "delete", ACTIVITY)
