"""T011 — Validation test for the azure.yaml postprovision hook (feature 006).

Asserts the postprovision hook invokes scripts/quickstart.sh and is wrapped in a
non-fatal guard so a seed failure never breaks `azd up` (SC-005). Other hook
phases and the services/infra blocks must remain intact.
"""

from __future__ import annotations

import yaml

from conftest import REPO_ROOT

AZURE_YAML = REPO_ROOT / "azure.yaml"


def _load():
    with open(AZURE_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_postprovision_invokes_quickstart_non_fatal():
    data = _load()
    run = data["hooks"]["postprovision"]["run"]
    assert "scripts/quickstart.sh" in run
    assert "--no-smoke" in run
    # Non-fatal guard: a failure is swallowed so azd still succeeds.
    assert "||" in run
    assert "true" in run


def test_services_and_infra_blocks_intact():
    data = _load()
    assert set(data["services"].keys()) == {"backend", "frontend"}
    assert data["infra"]["provider"] == "bicep"
    assert data["infra"]["module"] == "main"


def test_other_hook_phases_preserved():
    data = _load()
    hooks = data["hooks"]
    assert "preprovision" in hooks
    assert "postdeploy" in hooks
    # postdeploy still surfaces the deployed URLs.
    assert "AZURE_CONTAINERAPP_URL" in hooks["postdeploy"]["run"]
