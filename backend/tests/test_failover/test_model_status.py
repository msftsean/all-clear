"""US2 verifiers: model-status surface (018-model-agnostic-failover)."""

from __future__ import annotations

from app.core.dependencies import get_model_status
from app.services.azure.failover_chat_client import FailoverChatClient

from ._fakes import RaisingChatClient, RecordingChatClient, make_named_error

_USER = ["downed line at 5th & Main"]


# --- T016: status reports the active model + fallback chain (mock mode) -------

def test_model_status_reports_chain_in_mock_mode() -> None:
    status = get_model_status()

    assert status["mock_mode"] is True
    assert status["active"] == "mock-classifier"
    assert status["fallback_chain"] == []
    assert status["last_served"] == status["active"]
    assert status["failover_active"] is False


# --- T017: a FailoverChatClient reflects the last-served model ----------------

async def test_failover_client_reflects_last_served() -> None:
    primary = RaisingChatClient(make_named_error("NotFoundError", "DeploymentNotFound", 404))
    fallback = RecordingChatClient()
    client = FailoverChatClient([primary, fallback], ["gpt-primary", "gpt-fallback"])

    # Before any call: defaults to the primary.
    assert client.last_used_model == "gpt-primary"
    assert client.failover_active is False
    assert client.model_names == ["gpt-primary", "gpt-fallback"]

    await client.get_response(_USER)

    # After a forced failover: reports the fallback as last-served.
    assert client.last_used_model == "gpt-fallback"
    assert client.failover_active is True
