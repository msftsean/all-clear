"""A bounded Lab 09 extension artifact.

Participants may replace the message policy, but this module must remain a
pure formatter: it creates no records, changes severity, or bypasses routing.
"""

EXTENSION_NAME = "operator_note"


def build_operator_note(incident_id: str, note: str) -> str:
    """Format a safe operator note without changing incident authority."""
    if not incident_id.startswith("AC-"):
        raise ValueError("incident_id must use the AC- prefix")
    cleaned = " ".join(note.split())
    if not cleaned:
        raise ValueError("note must not be empty")
    return f"[{incident_id}] {cleaned}"
