import sys
import urllib.error

import pytest

from scripts import surge_rehearsal as rehearsal


@pytest.fixture
def run_rehearsal(monkeypatch, capsys):
    state = {
        "signals": 43, "incidents": 7, "blocked": 2,
        "escalated_to_person": 0, "failed": 0, "replica": "test",
    }
    calls = []

    def run(change=None, *, failed=0, key_env=None):
        state["failed"] = failed
        monkeypatch.setattr(rehearsal, "_get", lambda *_: state)
        if key_env:
            monkeypatch.setenv("TEST_SURGE_SECRET", key_env)

        def post(_base, path, body, key=None):
            calls.append((path, key))
            if path.endswith("/control"):
                return 200, {}, 0.1
            card = body["card"]
            if card == "R":
                result = {"accepted": False, "outcome": "blocked"}
            else:
                incident = f"old-{card}"
                if card == "E":
                    incident += f"-{rehearsal.PARAPHRASES[card].index(body['message'])}"
                result = {"accepted": True, "outcome": "joined", "incident_id": incident}
            response = (200, result, 0.2)
            return change(card, body, response) if change else response

        monkeypatch.setattr(rehearsal, "_post", post)
        monkeypatch.setattr(sys, "argv", ["surge_rehearsal.py", "--base", "https://example.invalid",
                                         "--key-env", "TEST_SURGE_SECRET"])
        code = rehearsal.main()
        return code, capsys.readouterr().out

    return run, calls


def test_distinct_existing_incidents_pass_and_key_stays_private(run_rehearsal):
    run, calls = run_rehearsal
    code, output = run(key_env="secret-value")
    assert code == 0
    assert "secret-value" not in output
    assert [key for path, key in calls if path.endswith("/control")] == ["secret-value"] * 2
    assert all(key is None for path, key in calls if path.endswith("/report"))
    assert "45/45" in output and "R1: blocked, R2: blocked" in output


def test_all_blocked_events_fail(run_rehearsal):
    run, _ = run_rehearsal
    code, output = run(lambda card, body, response:
                       (200, {"accepted": False, "outcome": "blocked"}, 0.2) if card in "ABCD" else response)
    assert code == 1
    assert "SC-001" in output and "FAIL" in output


def test_cross_event_merge_and_e_merge_fail(run_rehearsal):
    run, _ = run_rehearsal
    for merged_card in ("B", "E"):
        def merge(card, body, response):
            if card == merged_card:
                return 200, {"accepted": True, "outcome": "joined", "incident_id": "old-A"}, 0.2
            return response
        assert run(merge)[0] == 1


def test_red_cards_report_individual_live_outcomes_without_forcing_blocks(run_rehearsal):
    run, _ = run_rehearsal

    def change(card, body, response):
        if card == "R" and body["message"] == rehearsal.PARAPHRASES["R"][0]:
            return 200, {"accepted": True, "outcome": "received"}, 0.1
        return response

    code, output = run(change)
    assert code == 0
    assert "R1: received, R2: blocked" in output


@pytest.mark.parametrize("kind", ["slow", "http", "timeout", "unknown", "room-failed"])
def test_failures_never_pass(run_rehearsal, kind):
    run, _ = run_rehearsal

    def change(card, body, response):
        if kind == "slow":
            return response[0], response[1], 8.0
        if card == "R" and body["message"] == rehearsal.PARAPHRASES["R"][0]:
            if kind == "http":
                return 503, {}, 0.1
            if kind == "timeout":
                raise urllib.error.URLError("timeout")
            if kind == "unknown":
                return 200, {"accepted": False, "outcome": "error"}, 0.1
        return response

    code, output = run(change, failed=int(kind == "room-failed"))
    assert code == 1
    assert "FAIL" in output


def test_no_redirects():
    assert rehearsal._NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.invalid") is None


def test_control_timeout_fails_without_exposing_key(monkeypatch, capsys):
    monkeypatch.setenv("SURGE_COACH_KEY", "secret-value")
    monkeypatch.setattr(sys, "argv", ["surge_rehearsal.py", "--base", "https://example.invalid"])

    def fail(*args):
        raise TimeoutError("secret-value")

    monkeypatch.setattr(rehearsal, "_post", fail)
    assert rehearsal.main() == 1
    output = capsys.readouterr().out
    assert "transport" in output and "secret-value" not in output
