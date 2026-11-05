"""Completion gate for the bounded GitHub-in-the-lab extension."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_lab09_extension_exists_and_passes_own_tests() -> None:
    lab_dir = Path(__file__).parent
    extension_dir = lab_dir / "participant_extension"
    extension = extension_dir / "extension.py"
    extension_tests = extension_dir / "test_extension.py"
    assert extension.exists(), "Add participant_extension/extension.py"
    assert extension_tests.exists(), "Add participant_extension/test_extension.py"

    env = os.environ.copy()
    env.pop("ALL_CLEAR_LAB09_COMPLETE", None)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(extension_tests)],
        cwd=extension_dir,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
