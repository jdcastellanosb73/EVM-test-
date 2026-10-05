from decimal import Decimal

from fastapi.testclient import TestClient

from tests.integration.conftest import ContractChecker

from .support import (
    ACTIVITY,
    DESIGN_UX,
    PROJECT,
    PROJECTS,
    assert_money_fields_are_strings,
    create_activity,
    create_demo_project,
    create_project,
    decimal_from_json,
    value_and_status,
)


def test_create_project_returns_201_location_and_empty_indicators(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.post(
        PROJECTS, json={"name": "Portal de clientes", "cutoff_date": "2026-10-03"}
    )

    assert response.status_code == 201
    contract.check(response, "post", PROJECTS)
    body = response.json()
    assert response.headers["location"].endswith(f"/api/v1/projects/{body['id']}")
    assert body["cutoff_date"] == "2026-10-03"
    assert body["activities"] == []
    indicators = body["indicators"]
    assert_money_fields_are_strings(indicators)
    assert decimal_from_json(indicators["bac"]) == Decimal(0)
    assert value_and_status(indicators["cpi"]) == {"value": None, "status": "NOT_APPLICABLE"}
    assert value_and_status(indicators["spi"]) == {"value": None, "status": "NOT_APPLICABLE"}
    assert indicators["eac"] is None
    assert indicators["vac"] is None


def test_create_project_with_taken_name_returns_409(
    api_client: TestClient, contract: ContractChecker
) -> None:
    create_project(api_client, "Portal de clientes")

    response = api_client.post(PROJECTS, json={"name": "Portal de clientes"})

    assert response.status_code == 409
    contract.check(response, "post", PROJECTS)
    assert response.json()["code"] == "PROJECT_NAME_TAKEN"


def test_create_project_with_blank_name_returns_422(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.post(PROJECTS, json={"name": "   "})

    assert response.status_code == 422
    contract.check(response, "post", PROJECTS)
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert [detail["field"] for detail in body["details"]] == ["body.name"]


def test_list_projects_returns_consolidated_summaries(
    api_client: TestClient, contract: ContractChecker
) -> None:
    demo = create_demo_project(api_client)
    create_project(api_client, "Proyecto vacío")

    response = api_client.get(PROJECTS)

    assert response.status_code == 200
    contract.check(response, "get", PROJECTS)
    summaries = response.json()
    assert [summary["name"] for summary in summaries] == ["Portal de clientes", "Proyecto vacío"]
    demo_summary = summaries[0]
    assert demo_summary["id"] == demo["id"]
    assert demo_summary["activity_count"] == 3
    assert decimal_from_json(demo_summary["indicators"]["cpi"]["value"]) == Decimal("0.8854")


def test_get_project_consolidates_demo_dataset_with_ratio_of_sums(
    api_client: TestClient, contract: ContractChecker
) -> None:
    project_id = create_demo_project(api_client)["id"]

    response = api_client.get(PROJECT.format(project_id=project_id))

    assert response.status_code == 200
    contract.check(response, "get", PROJECT)
    body = response.json()
    assert [activity["name"] for activity in body["activities"]] == [
        "Diseño UX",
        "Desarrollo backend",
        "Pruebas QA",
    ]
    indicators = body["indicators"]
    assert_money_fields_are_strings(indicators)
    assert decimal_from_json(indicators["bac"]) == Decimal("34000000.00")
    assert decimal_from_json(indicators["pv"]) == Decimal("21200000.00")
    assert decimal_from_json(indicators["ev"]) == Decimal("17000000.00")
    assert decimal_from_json(indicators["ac"]) == Decimal("19200000.00")
    assert decimal_from_json(indicators["cv"]) == Decimal("-2200000.00")
    assert decimal_from_json(indicators["sv"]) == Decimal("-4200000.00")
    assert decimal_from_json(indicators["cpi"]["value"]) == Decimal("0.8854")
    assert indicators["cpi"]["status"] == "OVER_BUDGET"
    assert decimal_from_json(indicators["spi"]["value"]) == Decimal("0.8019")
    assert indicators["spi"]["status"] == "BEHIND_SCHEDULE"
    assert decimal_from_json(indicators["eac"]) == Decimal("38400000.00")
    assert decimal_from_json(indicators["vac"]) == Decimal("-4400000.00")


def test_get_unknown_project_returns_404(api_client: TestClient, contract: ContractChecker) -> None:
    response = api_client.get(PROJECT.format(project_id=999999))

    assert response.status_code == 404
    contract.check(response, "get", PROJECT)
    assert response.json() == {
        "code": "PROJECT_NOT_FOUND",
        "message": "Project 999999 not found",
        "details": [],
    }


def test_get_project_with_non_numeric_id_returns_422(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.get(PROJECT.format(project_id="abc"))

    assert response.status_code == 422
    contract.check(response, "get", PROJECT)
    assert response.json()["details"][0]["field"] == "path.project_id"


def test_update_project_replaces_its_data_and_keeps_activities(
    api_client: TestClient, contract: ContractChecker
) -> None:
    project_id = create_demo_project(api_client)["id"]

    response = api_client.put(
        PROJECT.format(project_id=project_id),
        json={"name": "Portal renovado", "description": "Fase 2", "cutoff_date": "2026-11-01"},
    )

    assert response.status_code == 200
    contract.check(response, "put", PROJECT)
    body = response.json()
    assert (body["name"], body["description"], body["cutoff_date"]) == (
        "Portal renovado",
        "Fase 2",
        "2026-11-01",
    )
    assert len(body["activities"]) == 3


def test_update_unknown_project_returns_404(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.put(PROJECT.format(project_id=999999), json={"name": "Nuevo"})

    assert response.status_code == 404
    contract.check(response, "put", PROJECT)
    assert response.json()["code"] == "PROJECT_NOT_FOUND"


def test_update_project_to_a_taken_name_returns_409(
    api_client: TestClient, contract: ContractChecker
) -> None:
    create_project(api_client, "Existente")
    project_id = create_project(api_client, "Otro")["id"]

    response = api_client.put(PROJECT.format(project_id=project_id), json={"name": "Existente"})

    assert response.status_code == 409
    contract.check(response, "put", PROJECT)
    assert response.json()["code"] == "PROJECT_NAME_TAKEN"


def test_delete_project_returns_204_and_cascades_to_its_activities(
    api_client: TestClient, contract: ContractChecker
) -> None:
    project_id = create_project(api_client)["id"]
    activity_id = create_activity(api_client, project_id, DESIGN_UX)["id"]

    response = api_client.delete(PROJECT.format(project_id=project_id))

    assert response.status_code == 204
    contract.check(response, "delete", PROJECT)
    assert api_client.get(PROJECT.format(project_id=project_id)).status_code == 404
    orphan = api_client.get(ACTIVITY.format(project_id=project_id, activity_id=activity_id))
    assert orphan.status_code == 404


def test_delete_unknown_project_returns_404(
    api_client: TestClient, contract: ContractChecker
) -> None:
    response = api_client.delete(PROJECT.format(project_id=999999))

    assert response.status_code == 404
    contract.check(response, "delete", PROJECT)


def test_unknown_route_uses_the_single_error_format(api_client: TestClient) -> None:
    response = api_client.get("/api/v1/unknown")

    assert response.status_code == 404
    assert response.json() == {"code": "NOT_FOUND", "message": "Not Found", "details": []}


def test_list_projects_through_the_real_session_dependency(client: TestClient) -> None:
    """The other tests replace get_session with a rolled-back transaction; this one does not."""
    response = client.get(PROJECTS)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
