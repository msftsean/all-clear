"""Verifiers for the room-surge tally (024-room-surge).

Pure unit tests over SurgeRoom: rate limit, tally, privacy of the public
snapshot, and reset semantics. No pipeline, no network.
"""

from __future__ import annotations

from types import SimpleNamespace

from app.services.surge_room import SurgeRoom, normalize_card, safe_location


class _Clock:
    def __init__(self) -> None:
        self.t = 1000.0

    def __call__(self) -> float:
        return self.t


def _result(incident_id, outcome="OPEN_INCIDENT", magnitude=None, location="Wilson Blvd",
            severity="SEV2", escalated=False, text="RAW ATTENDEE TEXT 555-123-4567"):
    sev = SimpleNamespace(value=severity)
    return SimpleNamespace(
        signal_text=text,
        action=SimpleNamespace(
            incident_id=incident_id,
            severity=sev,
            queue=SimpleNamespace(value="field-operations"),
            escalated=escalated,
            user_message="ack",
        ),
        routing=SimpleNamespace(outcome=SimpleNamespace(value=outcome), magnitude=magnitude),
        classification=SimpleNamespace(
            intent_category=SimpleNamespace(value="FIELD_HAZARD"),
            entities=SimpleNamespace(location=location),
        ),
    )


def test_normalize_card() -> None:
    assert normalize_card("a") == "A"
    assert normalize_card("R") == "R"
    assert normalize_card("Z") == "?"
    assert normalize_card(None) == "?"
    assert normalize_card("<script>") == "?"


def test_rate_limit_sliding_window() -> None:
    clock = _Clock()
    room = SurgeRoom(reports_per_window=3, window_seconds=60, clock=clock)
    assert all(room.admit("device-0001") for _ in range(3))
    assert room.admit("device-0001") is False
    assert room.rate_limited == 1
    assert room.admit("device-0002") is True  # other devices unaffected
    clock.t += 60
    assert room.admit("device-0001") is True
    assert room.snapshot()["devices"] == 2


def test_tally_collapses_reports_onto_incidents() -> None:
    room = SurgeRoom()
    room.open()
    first = room.record_result("A", _result("AC-0001"))
    assert first == {"outcome": "opened", "incident_id": "AC-0001", "room_reports": 1}
    for m in range(2, 6):
        out = room.record_result("A", _result("AC-0001", "ATTACH_TO_INCIDENT", magnitude=m))
    assert out["outcome"] == "joined" and out["room_reports"] == 5
    room.record_result("B", _result("AC-0002", severity="SEV1"))
    snap = room.snapshot()
    assert snap["signals"] == 6
    assert snap["incidents"] == 2
    assert snap["ratio"] == 3.0
    assert snap["tiles"][0]["incident_id"] == "AC-0001"  # biggest first
    assert snap["tiles"][0]["room_reports"] == 5
    assert snap["tiles"][0]["magnitude"] == 5
    assert snap["by_card"] == {"A": 5, "B": 1}


def test_crisis_path_counts_as_escalated_without_tile() -> None:
    room = SurgeRoom()
    out = room.record_result("R", _result(None, escalated=True))
    assert out["outcome"] == "escalated"
    snap = room.snapshot()
    assert snap["escalated_to_person"] == 1
    assert snap["incidents"] == 0
    assert snap["signals"] == 1


def test_snapshot_never_contains_raw_text_and_redacts_location() -> None:
    room = SurgeRoom()
    room.record_result("A", _result("AC-0009", location="call me at 555-123-4567 on Wilson"))
    room.record_blocked("R")
    snap_text = repr(room.snapshot())
    assert "RAW ATTENDEE TEXT" not in snap_text
    assert "555-123-4567" not in snap_text
    assert room.snapshot()["blocked"] == 1


def test_safe_location_caps_length() -> None:
    long = "x" * 200
    capped = safe_location(long)
    assert capped is not None and len(capped) <= 40
    assert safe_location(None) is None
    assert safe_location("   ") is None


def test_reset_clears_tally_and_closes() -> None:
    room = SurgeRoom()
    room.open()
    room.admit("device-0001")
    room.record_result("A", _result("AC-0001"))
    room.record_blocked("R")
    room.reset()
    snap = room.snapshot()
    assert snap["open"] is False
    assert snap["signals"] == snap["incidents"] == snap["blocked"] == snap["devices"] == 0
    assert snap["tiles"] == []
