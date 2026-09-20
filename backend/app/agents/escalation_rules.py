"""Intent-independent safety detection for the All Clear incident pipeline."""

from __future__ import annotations

import re

_HARM_KEYWORDS = (
    "harm myself",
    "kill myself",
    "end it",
    "end my life",
    "take my life",
    "suicide",
    "want to die",
    "hurt myself",
    "hurt someone",
    "hurt others",
    "cutting myself",
    "cut myself",
    "overdose",
    "better off dead",
    "no reason to live",
    "don't want to live",
    "do not want to live",
)
_WHITESPACE = re.compile(r"\s+")


def contains_harm_signal(message: str) -> bool:
    """Return whether a message requires the crisis escalation safety override."""
    normalized = (message or "").lower()
    if any(keyword in normalized for keyword in _HARM_KEYWORDS):
        return True
    compact = _WHITESPACE.sub("", normalized)
    return any(_WHITESPACE.sub("", keyword) in compact for keyword in _HARM_KEYWORDS)
