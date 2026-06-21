"""In-memory capstone lead capture store (SPEC-1, mock-mode safe)."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from io import StringIO


@dataclass(frozen=True)
class CapstoneLeadEntry:
    entry_id: str
    name: str
    agency: str
    surge: str
    signal_flood: str
    incident_underneath: str
    created_at: str


class CapstoneLeadStore:
    """Simple append-only lead store for deterministic demos and tests."""

    def __init__(self) -> None:
        self._entries: list[CapstoneLeadEntry] = []
        self._next_id = 1

    def create(
        self,
        *,
        name: str,
        agency: str,
        surge: str,
        signal_flood: str,
        incident_underneath: str,
    ) -> dict[str, str]:
        entry = CapstoneLeadEntry(
            entry_id=f"lead-{self._next_id:04d}",
            name=name,
            agency=agency,
            surge=surge,
            signal_flood=signal_flood,
            incident_underneath=incident_underneath,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._entries.append(entry)
        self._next_id += 1
        return asdict(entry)

    def list_entries(self) -> list[dict[str, str]]:
        return [asdict(entry) for entry in self._entries]

    def export_csv(self) -> str:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "entry_id",
                "name",
                "agency",
                "surge",
                "signal_flood",
                "incident_underneath",
                "created_at",
            ],
        )
        writer.writeheader()
        writer.writerows(self.list_entries())
        return output.getvalue()
