"""
Pipeline envelopes for All Clear (001-maf-rehost).

Plain dataclasses that carry a signal through the QueryAgent -> RouterExecutor ->
ActionAgent workflow. Kept free of any model/LLM client import so the RouterExecutor
(Constitution Art. II: deterministic, zero LLM calls) can import them safely.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.agents.schemas import RoutingDecision, SignalClassification


@dataclass
class ClassifiedSignal:
    """QueryAgent output paired with the raw signal text (RouterExecutor input)."""

    signal_text: str
    classification: SignalClassification
    session_id: str | None = None
    channel: str | None = None


@dataclass
class RoutedSignal:
    """RouterExecutor output: the decision plus everything ActionAgent needs.

    ``embedding`` is the signal vector the RouterExecutor already computed during
    dedup; it is carried forward so the OPEN_INCIDENT path can persist it with the
    new incident without recomputing (and without ActionAgent importing an
    embedding client).
    """

    signal_text: str
    classification: SignalClassification
    routing: RoutingDecision
    embedding: list[float] = field(default_factory=list)
    session_id: str | None = None
    channel: str | None = None
