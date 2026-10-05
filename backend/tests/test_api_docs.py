from typing import Any

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


API_PREFIX = "/api/v1"
METHODS_WITH_BODY = {"post", "put"}
DEFAULT_SUCCESS_DESCRIPTION = "Successful Response"
SUCCESS_STATUS_PREFIX = "2"
VALIDATION_STATUS = "422"
INTERNAL_ERROR_STATUS = "500"
ERROR_SCHEMA_REF = "#/components/schemas/ErrorResponse"


def _api_operations(schema: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    return [
        (path, method, operation)
        for path, operations in schema["paths"].items()
        if path.startswith(API_PREFIX)
        for method, operation in operations.items()
    ]


def test_every_api_operation_documents_description_schemas_and_errors(
    client: TestClient,
) -> None:
    operations = _api_operations(client.get("/api-docs/openapi.json").json())

    assert operations
    for path, method, operation in operations:
        name = f"{method.upper()} {path}"
        assert operation.get("description"), name
        if method in METHODS_WITH_BODY:
            assert "requestBody" in operation, name
        responses = operation["responses"]
        success = [code for code in responses if code.startswith(SUCCESS_STATUS_PREFIX)]
        assert success, name
        for code in success:
            assert responses[code]["description"] != DEFAULT_SUCCESS_DESCRIPTION, name
        takes_input = "parameters" in operation or "requestBody" in operation
        error_codes = [INTERNAL_ERROR_STATUS, *([VALIDATION_STATUS] if takes_input else [])]
        for code in error_codes:
            error_schema = responses[code]["content"]["application/json"]["schema"]
            assert error_schema["$ref"] == ERROR_SCHEMA_REF, f"{name} {code}"
