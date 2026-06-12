"""T014 — Doc-lint for the Day-0 Head-Start guide (feature 006).

Asserts docs/quickstart/HEADSTART.md exists, documents all three lanes, carries
the "scenario-ready" checklist, and is linked from README.md.
"""

from __future__ import annotations

from conftest import REPO_ROOT

HEADSTART = REPO_ROOT / "docs" / "quickstart" / "HEADSTART.md"
README = REPO_ROOT / "README.md"


def test_headstart_exists():
    assert HEADSTART.exists(), f"missing {HEADSTART}"


def test_headstart_names_all_three_lanes():
    text = HEADSTART.read_text(encoding="utf-8").lower()
    assert "shared backend" in text
    # self-serve azd lane
    assert "azd" in text and "self-serve" in text
    # offline mock lane
    assert "mock" in text


def test_headstart_has_scenario_ready_checklist():
    text = HEADSTART.read_text(encoding="utf-8").lower()
    assert "scenario-ready" in text
    # references the verify/smoke output the checklist is tied to.
    assert "verify" in text or "smoke" in text


def test_headstart_covers_day0_steps():
    text = HEADSTART.read_text(encoding="utf-8").lower()
    assert "codespaces" in text
    assert "copilot" in text
    assert "azd auth login" in text


def test_readme_links_to_headstart():
    text = README.read_text(encoding="utf-8")
    assert "docs/quickstart/HEADSTART.md" in text
