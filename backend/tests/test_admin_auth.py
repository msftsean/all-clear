from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import create_app


def test_admin_routes_fail_closed_when_secret_unset() -> None:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(mock_mode=True, admin_api_token="")
    with TestClient(app) as client:
        response = client.get("/api/admin/tickets")
    assert response.status_code == 503
    assert "Admin API token is not configured" in response.json()["detail"]


def test_admin_routes_reject_invalid_secret() -> None:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(mock_mode=True, admin_api_token="secret")
    with TestClient(app) as client:
        response = client.get("/api/admin/tickets", headers={"X-Admin-Token": "wrong"})
    assert response.status_code == 401


def test_admin_routes_accept_configured_secret() -> None:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(mock_mode=True, admin_api_token="secret")
    with TestClient(app) as client:
        response = client.get("/api/admin/tickets", headers={"X-Admin-Token": "secret"})
    assert response.status_code == 200
