from extension import build_operator_note


def test_operator_note_is_bounded_and_deterministic() -> None:
    assert build_operator_note("AC-0042", "  crew   en route  ") == "[AC-0042] crew en route"


def test_operator_note_rejects_invalid_incident() -> None:
    try:
        build_operator_note("TKT-42", "status")
    except ValueError as exc:
        assert "AC-" in str(exc)
    else:
        raise AssertionError("invalid incident id should be rejected")
