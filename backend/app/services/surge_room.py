"""Room surge tally (024-room-surge).

Keeps the live counts for an audience-sourced surge: how many Signals the room
sent, which Incidents they collapsed onto, how many were blocked by content
safety or escalated to a person, and a per-device rate limit.

Bounded authority: this module only *observes* PipelineResults. It never
classifies, routes, deduplicates or mutates Incidents; every audience Signal
goes through the unchanged AllClearPipeline. ``reset`` clears this tally only,
never Incidents, Reports or audit entries.

Privacy: the public snapshot carries machine-derived fields only (Incident id,
severity, queue, category, a PII-redacted and length-capped location). Raw
attendee text is never stored here.

Scope: in-process state. For the event the backend runs on one replica; the
snapshot includes ``replica`` so a split across replicas is visible.
"""

from __future__ import annotations

import os
import socket
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from app.services.pii import redact_pii_text

VALID_CARDS = frozenset({"A", "B", "C", "D", "E", "R"})
_LOCATION_MAX = 40


def normalize_card(card: Optional[str]) -> str:
    """Map a card id from the query string to a known card, else '?'."""
    value = (card or "").strip().upper()[:1]
    return value if value in VALID_CARDS else "?"


def _value(obj: Any) -> Any:
    """Enum -> value; passthrough otherwise."""
    return getattr(obj, "value", obj)


def safe_location(raw: Optional[str]) -> Optional[str]:
    """PII-redact and cap a QueryAgent-extracted location for the public board."""
    if not raw:
        return None
    text = " ".join(str(raw).split())
    text = redact_pii_text(text)
    if len(text) > _LOCATION_MAX:
        text = text[: _LOCATION_MAX - 1].rstrip() + "…"
    return text or None


@dataclass
class _Tile:
    incident_id: str
    severity: str
    queue: str
    category: str
    location: Optional[str]
    escalated: bool
    room_reports: int = 0
    magnitude: int = 1
    first_seen: float = 0.0
    last_seen: float = 0.0


@dataclass
class SurgeRoom:
    """In-memory room tally with a per-device sliding-window rate limit."""

    reports_per_window: int = 3
    window_seconds: float = 60.0
    clock: Callable[[], float] = time.monotonic
    wall: Callable[[], float] = time.time

    is_open: bool = False
    opened_at: Optional[float] = None
    closed_at: Optional[float] = None
    signals: int = 0
    blocked: int = 0
    escalated_to_person: int = 0
    rate_limited: int = 0
    failed: int = 0
    _generation: int = field(default=0, init=False, repr=False)
    by_card: dict[str, int] = field(default_factory=dict)
    _tiles: dict[str, _Tile] = field(default_factory=dict)
    _devices: set[str] = field(default_factory=set)
    _recent: dict[str, deque] = field(default_factory=dict)

    @property
    def generation(self) -> int:
        """Current room epoch used to discard completions admitted before reset."""
        return self._generation

    # ------------------------------------------------------------------ control
    def open(self) -> None:
        self.is_open = True
        self.opened_at = self.wall()
        self.closed_at = None

    def close(self) -> None:
        self.is_open = False
        self.closed_at = self.wall()

    def reset(self) -> None:
        """Clear the room tally (never Incidents/Reports/audit). Leaves it closed."""
        self._generation += 1
        self.is_open = False
        self.opened_at = None
        self.closed_at = None
        self.signals = 0
        self.blocked = 0
        self.escalated_to_person = 0
        self.rate_limited = 0
        self.failed = 0
        self.by_card = {}
        self._tiles = {}
        self._devices = set()
        self._recent = {}

    # --------------------------------------------------------------- admission
    def admit(self, device_id: str) -> bool:
        """Record an attempt for ``device_id``; False if over the rate limit."""
        now = self.clock()
        window = self._recent.setdefault(device_id, deque())
        while window and now - window[0] >= self.window_seconds:
            window.popleft()
        if len(window) >= self.reports_per_window:
            self.rate_limited += 1
            return False
        window.append(now)
        self._devices.add(device_id)
        return True

    # --------------------------------------------------------------- recording
    def _count_card(self, card: str) -> None:
        self.by_card[card] = self.by_card.get(card, 0) + 1

    def record_result(
        self, card: str, result: Any, *, generation: int | None = None
    ) -> dict[str, Any]:
        """Tally a PipelineResult. Returns the reporter-facing summary."""
        action = result.action
        routing = result.routing
        incident_id = getattr(action, "incident_id", None)
        outcome = str(_value(getattr(routing, "outcome", "")))
        if generation is not None and generation != self.generation:
            return {
                "outcome": (
                    "escalated" if not incident_id and getattr(action, "escalated", False)
                    else "received" if not incident_id
                    else "joined" if outcome == "ATTACH_TO_INCIDENT"
                    else "opened"
                ),
                "incident_id": incident_id,
                "room_reports": 0,
                "room_counted": False,
            }

        self.signals += 1
        self._count_card(card)

        if not incident_id:
            # Crisis safety net (or any path without an Incident): a person handles it.
            if getattr(action, "escalated", False):
                self.escalated_to_person += 1
            summary = {
                "outcome": "escalated" if getattr(action, "escalated", False) else "received",
                "incident_id": None,
                "room_reports": 0,
            }
            if generation is not None:
                summary["room_counted"] = True
            return summary

        now = self.wall()
        tile = self._tiles.get(incident_id)
        if tile is None:
            classification = result.classification
            entities = getattr(classification, "entities", None)
            tile = _Tile(
                incident_id=incident_id,
                severity=str(_value(action.severity)),
                queue=str(_value(action.queue)),
                category=str(_value(getattr(classification, "intent_category", ""))),
                location=safe_location(getattr(entities, "location", None)),
                escalated=bool(getattr(action, "escalated", False)),
                first_seen=now,
            )
            self._tiles[incident_id] = tile
        tile.room_reports += 1
        tile.last_seen = now
        tile.escalated = tile.escalated or bool(getattr(action, "escalated", False))
        magnitude = getattr(routing, "magnitude", None)
        if isinstance(magnitude, int) and magnitude > tile.magnitude:
            tile.magnitude = magnitude

        summary = {
            "outcome": "joined" if outcome == "ATTACH_TO_INCIDENT" else "opened",
            "incident_id": incident_id,
            "room_reports": tile.room_reports,
        }
        if generation is not None:
            summary["room_counted"] = True
        return summary

    def record_blocked(self, card: str, *, generation: int | None = None) -> bool:
        if generation is not None and generation != self.generation:
            return False
        self.blocked += 1
        self._count_card(card)
        return True

    def record_failed(self, *, generation: int | None = None) -> bool:
        if generation is not None and generation != self.generation:
            return False
        self.failed += 1
        return True

    # ---------------------------------------------------------------- snapshot
    def snapshot(self) -> dict[str, Any]:
        tiles = sorted(
            self._tiles.values(), key=lambda t: (-t.room_reports, t.first_seen)
        )
        incidents = len(tiles)
        return {
            "open": self.is_open,
            "opened_at": self.opened_at,
            "closed_at": self.closed_at,
            "signals": self.signals,
            "incidents": incidents,
            "ratio": round(self.signals / incidents, 1) if incidents else None,
            "devices": len(self._devices),
            "blocked": self.blocked,
            "escalated_to_person": self.escalated_to_person,
            "rate_limited": self.rate_limited,
            "failed": self.failed,
            "by_card": dict(sorted(self.by_card.items())),
            "replica": _replica_id(),
            "tiles": [
                {
                    "incident_id": t.incident_id,
                    "severity": t.severity,
                    "queue": t.queue,
                    "category": t.category,
                    "location": t.location,
                    "escalated": t.escalated,
                    "room_reports": t.room_reports,
                    "magnitude": t.magnitude,
                }
                for t in tiles
            ],
        }


def _replica_id() -> str:
    return os.environ.get("CONTAINER_APP_REPLICA_NAME") or socket.gethostname()
