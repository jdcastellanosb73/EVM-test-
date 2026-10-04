from fastapi.testclient import TestClient


def test_health_reports_ok_when_database_is_reachable(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up"}


def test_health_reports_degraded_when_database_is_unreachable(
    client_without_database: TestClient,
) -> None:
    response = client_without_database.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "down"}
