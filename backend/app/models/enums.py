"""Domain-neutral enums shared by All Clear support services."""

from enum import Enum


class Sentiment(str, Enum):
    """Detected tone of an inbound signal."""

    NEUTRAL = "NEUTRAL"
    FRUSTRATED = "FRUSTRATED"
    URGENT = "URGENT"
    SATISFIED = "SATISFIED"
