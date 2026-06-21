"""
Starter red-to-green test for the GitHub-in-the-lab exercise.

Participants intentionally start with this test failing, implement one bounded
extension, then make it pass by setting ALL_CLEAR_LAB09_COMPLETE=true for their
completed exercise run.
"""

from __future__ import annotations

import os


def test_lab09_starter_red_to_green() -> None:
    assert os.getenv("ALL_CLEAR_LAB09_COMPLETE") == "true", (
        "Starter test is intentionally red. Complete one bounded lab extension "
        "(tool or scenario pack), then re-run with ALL_CLEAR_LAB09_COMPLETE=true."
    )

