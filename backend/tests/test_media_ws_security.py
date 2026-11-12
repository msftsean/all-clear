import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect


def test_acs_media_rejects_connections_without_verified_ingress(monkeypatch):
    from unittest.mock import AsyncMock

    import app.api.media_ws as media_ws
    from app.main import app

    monkeypatch.setattr(
        media_ws._token_mgr,
        "get_token",
        AsyncMock(side_effect=AssertionError("must reject before Azure auth")),
    )

    with pytest.raises(WebSocketDisconnect) as exc:
        with TestClient(app).websocket_connect("/ws/acs-media") as websocket:
            websocket.receive_text()

    assert exc.value.code == 1008
    assert "Authenticated ACS ingress" in exc.value.reason
