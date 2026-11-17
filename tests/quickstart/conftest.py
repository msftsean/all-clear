"""Shared fixtures/helpers for the quickstart test suite (feature 006).

These tests MUST run in CI with zero Azure credentials. They exercise the
seeder's `--dry-run` mode and the `quickstart.sh --mock` lane only.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

# Repo root = three levels up from this file: tests/quickstart/conftest.py
REPO_ROOT = Path(__file__).resolve().parents[2]

# Canonical All Clear incident-response seed corpus directory.
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


def _resolve_bash() -> str:
    if os.name != "nt":
        return shutil.which("bash") or "bash"

    git_executable = shutil.which("git")
    git_roots = (
        [parent for parent in Path(git_executable).resolve().parents if parent.name.lower() == "git"]
        if git_executable
        else []
    )
    for variable in ("ProgramFiles", "ProgramFiles(x86)"):
        program_files = os.environ.get(variable)
        if program_files:
            git_roots.append(Path(program_files) / "Git")

    for git_root in git_roots:
        for candidate in (
            git_root / "usr" / "bin" / "bash.exe",
            git_root / "bin" / "bash.exe",
        ):
            if candidate.is_file():
                return str(candidate)

    raise RuntimeError("Git Bash was not found; install Git for Windows to run quickstart tests.")


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command from the repo root, capturing text output."""
    if cmd and Path(cmd[0]).name.lower() in {"bash", "bash.exe"}:
        cmd = [_resolve_bash(), *cmd[1:]]
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        **kwargs,
    )
