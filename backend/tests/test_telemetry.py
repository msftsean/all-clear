"""Verify telemetry stays opt-in and never uses local export buffers."""

import sys
from types import ModuleType
from unittest.mock import Mock

import pytest

from app.main import create_app


@pytest.mark.parametrize("enabled", [False, True])
def test_azure_monitor_is_opt_in(
    monkeypatch: pytest.MonkeyPatch, enabled: bool
) -> None:
    configure = Mock()
    module = ModuleType("azure.monitor.opentelemetry")
    module.configure_azure_monitor = configure
    monkeypatch.setitem(sys.modules, "azure.monitor.opentelemetry", module)
    if enabled:
        monkeypatch.setenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "nonsecret-test-value")
    else:
        monkeypatch.delenv("APPLICATIONINSIGHTS_CONNECTION_STRING", raising=False)

    create_app()

    if enabled:
        configure.assert_called_once_with(
            logger_name="allclear",
            enable_live_metrics=False,
            disable_offline_storage=True,
        )
    else:
        configure.assert_not_called()
