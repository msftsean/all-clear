"""Coach load-test coordinator (demo tooling).

Lets a coach trigger a burst of realistic signals at the live pipeline from the
browser (Coach's Runbook) so the ClearBoard fills with deduplicating incidents
and magnitude climbs. The job runs as a *single* background task guarded by a
shared lock so that a second click — or another coach on another machine — does
not start a duplicate run. The guard is idempotent: while a run is active, a
``start`` call simply returns the in-flight job's status.

Cross-replica safety: the container app scales to >1 replica, so the lock cannot
live in process memory. In live mode the lock/state is a single Cosmos document
(partition ``__loadtest__``, id ``__loadtest_job__``) in the existing
``incidents`` container, acquired with optimistic-concurrency (etag). In mock
mode (local/tests, no Cosmos) the same shape is kept in process memory.

Bounded authority: this is demo orchestration only. It submits signals through
the normal pipeline; it never classifies, routes, or mutates incidents itself.
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from app.core.config import get_settings
from app.services.scenario_packs import get_scenario_pack, scenario_signals

# Lock document coordinates: its own logical partition so it is never returned
# by category-scoped dedup queries against real SignalCategory partitions.
_LOCK_PARTITION = "__loadtest__"
_LOCK_ID = "__loadtest_job__"

# A running job older than this is treated as crashed so a new run can take over
# (e.g. the replica that owned it was recycled mid-run).
_STALE_AFTER_S = 300

# Bounds for a single run (keep demo bursts safe and snappy).
_MIN_COUNT = 1
_MAX_COUNT = 150
_DEFAULT_COUNT = 40

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _age_seconds(started_at: Optional[str]) -> float:
    if not started_at:
        return 1e9
    try:
        started = datetime.fromisoformat(started_at)
    except ValueError:
        return 1e9
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - started).total_seconds()


def clamp_count(count: int) -> int:
    return max(_MIN_COUNT, min(_MAX_COUNT, int(count)))


def _public_view(doc: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Strip Cosmos internals and present a stable status shape to the browser."""
    if doc is None:
        return {
            "status": "idle",
            "running": False,
            "total": 0,
            "sent": 0,
            "ok": 0,
            "failed": 0,
            "incidents": 0,
            "max_magnitude": 0,
            "mode": None,
            "started_by": None,
            "started_at": None,
            "finished_at": None,
            "message": "No load run yet.",
        }
    running = doc.get("status") == "running" and _age_seconds(doc.get("started_at")) < _STALE_AFTER_S
    return {
        "status": "running" if running else "idle",
        "running": running,
        "run_id": doc.get("run_id"),
        "total": int(doc.get("total", 0)),
        "sent": int(doc.get("sent", 0)),
        "ok": int(doc.get("ok", 0)),
        "failed": int(doc.get("failed", 0)),
        "incidents": int(doc.get("incidents", 0)),
        "max_magnitude": int(doc.get("max_magnitude", 0)),
        "mode": doc.get("mode"),
        "pack": doc.get("pack"),
        "started_by": doc.get("started_by"),
        "started_at": doc.get("started_at"),
        "finished_at": doc.get("finished_at"),
        "message": doc.get("message", ""),
    }


class LoadTestCoordinator:
    """Single-flight load-test runner with a shared (Cosmos or in-memory) lock."""

    def __init__(self, container: Any | None) -> None:
        self._container = container
        # In-memory fallback (mock mode / tests). Cosmos mode ignores these.
        self._mem: Optional[dict[str, Any]] = None
        self._mem_lock = asyncio.Lock()
        # Hold a reference to the running task so it is not garbage collected.
        self._task: Optional[asyncio.Task[Any]] = None

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    async def status(self) -> dict[str, Any]:
        return _public_view(await self._read())

    async def start(
        self,
        count: int = _DEFAULT_COUNT,
        mode: str = "varied",
        started_by: str = "coach",
        pack: str | None = None,
    ) -> dict[str, Any]:
        """Acquire the lock and launch a run, or return the in-flight job.

        Idempotent: if a (non-stale) run is already active, no new run starts and
        the active job's status is returned unchanged.
        """
        count = clamp_count(count)
        mode = "same" if str(mode).lower() == "same" else "varied"
        settings = get_settings()
        resolved_pack = get_scenario_pack(settings, pack).pack_id
        run_id = uuid.uuid4().hex
        new_doc = {
            "id": _LOCK_ID,
            "intent_category": _LOCK_PARTITION,
            "status": "running",
            "run_id": run_id,
            "mode": mode,
            "pack": resolved_pack,
            "total": count,
            "sent": 0,
            "ok": 0,
            "failed": 0,
            "incidents": 0,
            "max_magnitude": 0,
            "started_by": started_by or "coach",
            "started_at": _now_iso(),
            "finished_at": None,
            "message": f"Starting {count} {mode} signals for {resolved_pack}…",
        }

        acquired = await self._try_acquire(new_doc)
        if acquired is None:
            # Someone else holds an active run — return their status, do not start.
            return _public_view(await self._read())

        self._task = asyncio.create_task(self._run(run_id, count, mode, resolved_pack))
        return _public_view(acquired)

    # ------------------------------------------------------------------ #
    # Lock acquisition
    # ------------------------------------------------------------------ #
    async def _try_acquire(self, new_doc: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Return the stamped lock doc if we won the lock, else None."""
        if self._container is None:
            async with self._mem_lock:
                cur = self._mem
                if cur is not None and cur.get("status") == "running" \
                        and _age_seconds(cur.get("started_at")) < _STALE_AFTER_S:
                    return None
                self._mem = dict(new_doc)
                return dict(self._mem)
        return await self._try_acquire_cosmos(new_doc)

    async def _try_acquire_cosmos(self, new_doc: dict[str, Any]) -> Optional[dict[str, Any]]:
        from azure.core import MatchConditions
        from azure.cosmos.exceptions import (
            CosmosAccessConditionFailedError,
            CosmosResourceExistsError,
            CosmosResourceNotFoundError,
        )

        try:
            existing = await self._container.read_item(
                item=_LOCK_ID, partition_key=_LOCK_PARTITION
            )
        except CosmosResourceNotFoundError:
            existing = None

        if existing is None:
            try:
                return await self._container.create_item(dict(new_doc))
            except CosmosResourceExistsError:
                return None  # lost the create race; another run just started

        active = existing.get("status") == "running" and \
            _age_seconds(existing.get("started_at")) < _STALE_AFTER_S
        if active:
            return None

        merged = dict(new_doc)
        try:
            return await self._container.replace_item(
                item=_LOCK_ID,
                body=merged,
                etag=existing.get("_etag"),
                match_condition=MatchConditions.IfNotModified,
            )
        except (CosmosAccessConditionFailedError, CosmosResourceExistsError):
            return None  # lost the takeover race

    # ------------------------------------------------------------------ #
    # Storage helpers
    # ------------------------------------------------------------------ #
    async def _read(self) -> Optional[dict[str, Any]]:
        if self._container is None:
            return dict(self._mem) if self._mem is not None else None
        from azure.cosmos.exceptions import CosmosResourceNotFoundError

        try:
            return await self._container.read_item(
                item=_LOCK_ID, partition_key=_LOCK_PARTITION
            )
        except CosmosResourceNotFoundError:
            return None

    async def _patch(self, run_id: str, **fields: Any) -> bool:
        """Apply ``fields`` to the lock doc iff we still own it (run_id matches).

        Returns False if ownership was lost (another run took over) so the caller
        can abort. Uses etag CAS in Cosmos mode; a small retry covers benign races.
        """
        if self._container is None:
            async with self._mem_lock:
                cur = self._mem
                if cur is None or cur.get("run_id") != run_id:
                    return False
                cur.update(fields)
                return True
        return await self._patch_cosmos(run_id, fields)

    async def _patch_cosmos(self, run_id: str, fields: dict[str, Any]) -> bool:
        from azure.core import MatchConditions
        from azure.cosmos.exceptions import (
            CosmosAccessConditionFailedError,
            CosmosResourceNotFoundError,
        )

        for _ in range(8):
            try:
                doc = await self._container.read_item(
                    item=_LOCK_ID, partition_key=_LOCK_PARTITION
                )
            except CosmosResourceNotFoundError:
                return False
            if doc.get("run_id") != run_id:
                return False  # another run owns the lock now; abort ours
            doc.update(fields)
            try:
                await self._container.replace_item(
                    item=_LOCK_ID,
                    body=doc,
                    etag=doc.get("_etag"),
                    match_condition=MatchConditions.IfNotModified,
                )
                return True
            except CosmosAccessConditionFailedError:
                await asyncio.sleep(0.05)
                continue
        return False

    # ------------------------------------------------------------------ #
    # Background runner
    # ------------------------------------------------------------------ #
    async def _run(self, run_id: str, count: int, mode: str, pack: str) -> None:
        from app.core.dependencies import get_pipeline

        settings = get_settings()
        signals = scenario_signals(settings, pack_id=pack, count=count, mode=mode)
        pipeline = get_pipeline()
        ok = 0
        failed = 0
        incidents: set[str] = set()
        max_mag = 0

        for i, message in enumerate(signals):
            try:
                result = await pipeline.process_signal(
                    text=message, session_id="coach-loadtest", channel="chat"
                )
            except Exception:  # noqa: BLE001 - a blocked/failed signal must not kill the run
                failed += 1
            else:
                ok += 1
                # Metadata extraction must never be counted as a failed signal.
                try:
                    incidents.add(result.action.incident_id)
                    # Magnitude lives on the routing decision (ATTACH path); the
                    # OPEN path leaves it unset, where magnitude is 1.
                    mag = getattr(result.routing, "magnitude", None) or 1
                    max_mag = max(max_mag, int(mag))
                except Exception:  # noqa: BLE001
                    pass

            still_ours = await self._patch(
                run_id,
                sent=i + 1,
                ok=ok,
                failed=failed,
                incidents=len(incidents),
                max_magnitude=max_mag,
                message=(
                    f"Fired {i + 1}/{count} signals ({pack}) → "
                    f"{len(incidents)} incidents (max magnitude {max_mag})."
                ),
            )
            if not still_ours:
                return  # ownership lost (takeover); stop quietly

        await self._patch(
            run_id,
            status="idle",
            finished_at=_now_iso(),
            sent=count,
            ok=ok,
            failed=failed,
            incidents=len(incidents),
            max_magnitude=max_mag,
            message=(
                f"Done: {ok} signals fired → {len(incidents)} incidents, "
                f"max magnitude {max_mag}"
                + (f", {failed} rejected." if failed else ".")
            ),
        )
