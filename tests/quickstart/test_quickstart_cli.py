"""T006/T008 — Contract tests for scripts/quickstart.sh (feature 006).

Per contracts/quickstart-cli.md. All cases run with ZERO Azure credentials:
  - `--help` exits 0
  - live lane with missing env exits 2, names the missing vars, prints no values
  - `--mock` exits 0 and emits the literal `✅ Scenario-ready` marker
"""

from __future__ import annotations

import os

from conftest import REPO_ROOT, assert_scenario_ready, run

QUICKSTART = str(REPO_ROOT / "scripts" / "quickstart.sh")

# Env stripped of all live-lane Azure vars (forces the fail-closed path).
LIVE_ENV_VARS = [
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_API_KEY",
    "AZURE_SEARCH_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
]


def _clean_env() -> dict:
    env = dict(os.environ)
    for var in LIVE_ENV_VARS:
        env.pop(var, None)
    return env


def test_help_exits_zero():
    result = run(["bash", QUICKSTART, "--help"])
    assert result.returncode == 0
    assert "quickstart.sh" in (result.stdout + result.stderr)
    assert "--mock" in (result.stdout + result.stderr)


def test_missing_live_env_exits_2_and_names_vars_without_values():
    env = _clean_env()
    # Inject sentinel secret values that must NEVER be echoed.
    secret = "SUPER-SECRET-VALUE-DO-NOT-PRINT"
    env["AZURE_SEARCH_API_KEY"] = secret  # set one, leave others missing
    env.pop("AZURE_SEARCH_ENDPOINT", None)
    result = run(["bash", QUICKSTART], env=env)
    assert result.returncode == 2
    combined = result.stdout + result.stderr
    # Names at least one missing required var.
    assert "AZURE_SEARCH_ENDPOINT" in combined
    # Never prints secret values.
    assert secret not in combined


def test_mock_lane_exits_zero_and_is_scenario_ready():
    env = _clean_env()  # zero Azure credentials
    result = run(["bash", QUICKSTART, "--mock"], env=env)
    assert result.returncode == 0, (
        f"--mock should exit 0; got {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    assert_scenario_ready(result.stdout)
