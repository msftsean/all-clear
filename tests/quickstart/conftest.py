"""Shared fixtures/helpers for the quickstart test suite (feature 006).

These tests MUST run in CI with zero Azure credentials. They exercise the
seeder's `--dry-run` mode and the `quickstart.sh --mock` lane only.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

# Repo root = three levels up from this file: tests/quickstart/conftest.py
REPO_ROOT = Path(__file__).resolve().parents[2]

# Canonical seed corpus directory (six-intent AJCU corpus).
SEED_DIR = REPO_ROOT / "infra" / "ai-search" / "seed-articles"

# The literal stdout contract marker for "scenario-ready" (contracts/quickstart-cli.md).
SCENARIO_READY_MARKER = "✅ Scenario-ready"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def seed_dir() -> Path:
    return SEED_DIR


def assert_scenario_ready(stdout: str) -> None:
    """Assert the success-banner stdout contract marker is present."""
    assert SCENARIO_READY_MARKER in stdout, (
        f"expected literal marker {SCENARIO_READY_MARKER!r} in stdout, got:\n{stdout}"
    )


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command from the repo root, capturing text output."""
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        **kwargs,
    )
