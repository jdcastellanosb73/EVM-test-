from fastapi.testclient import TestClient

from app.config import Settings


def test_swagger_ui_is_served_at_api_docs(client: TestClient) -> None:
    response = client.get("/api-docs")

    assert response.status_code == 200
    assert "swagger-ui" in response.text


def test_openapi_schema_documents_health_endpoint(
    client: TestClient, test_settings: Settings
) -> None:
    schema = client.get("/api-docs/openapi.json").json()

    assert schema["info"]["title"] == test_settings.app_name
    health_responses = schema["paths"]["/health"]["get"]["responses"]
    assert set(health_responses) == {"200", "503"}
