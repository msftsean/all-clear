"""
Escalation Detector - Generated from your-spec.md and your-constitution.md

Feature: Statutory-Clock Escalation Detector
Spec: labs/03-spec-driven-development/your-spec.md
Constitution: labs/03-spec-driven-development/your-constitution.md

This module implements deterministic escalation detection per the specification.
"""

from dataclasses import dataclass, field
from typing import Optional
import json
from pathlib import Path


# FR-006: Support configurable term lists without code changes.
# Terms can be loaded from external JSON config.
DEFAULT_SAFETY_TERMS = {
    "downed power line", "gas leak", "transformer fire", "sparking line",
    "life safety", "injured", "fire", "explosion", "total outage",
}

DEFAULT_POLICY_TERMS = {
    "breach notification", "recall reporting", "regulatory notice",
    "statutory deadline", "legal deadline", "compliance report",
}

# Constitution: Governance Notes - escalate legal, regulatory, PII, and safety signals.
GOVERNANCE_TERMS = {
    "statutory clock", "legal", "lawyer", "attorney", "lawsuit",
    "pii exposure", "personal data exposed", "regulatory", "recall",
    "human request", "escalate to human",
}


def load_keywords_from_config(config_path: Optional[Path] = None) -> tuple[set, set, set]:
    """FR-006: Load configurable escalation terms from external JSON file."""
    if config_path and config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        return (
            set(config.get("safety_terms", DEFAULT_SAFETY_TERMS)),
            set(config.get("policy_terms", DEFAULT_POLICY_TERMS)),
            set(config.get("governance_terms", GOVERNANCE_TERMS)),
        )
    return DEFAULT_SAFETY_TERMS, DEFAULT_POLICY_TERMS, GOVERNANCE_TERMS


@dataclass
class EscalationDecision:
    """
    FR-003: Structured output with escalate, severity, and reasons fields.
    FR-005: Include confidence score and rule hits in decision metadata.
    """
    escalate: bool
    severity: str  # "SEV1", "SEV2", "SEV4"
    reasons: list[str] = field(default_factory=list)
    confidence: float = 0.0
    # FR-004: Preserve original signal text for human reviewers.
    original_text: str = ""
    rule_hits: list[str] = field(default_factory=list)


def detect_escalation(
    user_text: str,
    config_path: Optional[Path] = None,
) -> EscalationDecision:
    """
    Detect escalation triggers in signal text.

    FR-001: Detect safety/statutory terms -> SEV1 escalation.
    FR-002: Detect policy-sensitive terms (breach notification, recall, regulatory notice).
    FR-007: Provide fallback response when confidence is low.

    Constitution Principle 1: Escalation is a safety control.
    Constitution Principle 2: Deterministic behavior - explicit rules.
    Constitution Principle 3: Transparent outputs - reason codes included.
    Constitution Principle 4: Human collaboration - escalate on low confidence.

    Constitution Prohibited: Never suppress SEV1 or statutory-clock indicators.
    """
    # Load configurable terms (FR-006).
    safety_terms, policy_terms, governance_terms = load_keywords_from_config(config_path)

    text = (user_text or "").lower()
    reasons: list[str] = []
    rule_hits: list[str] = []

    # FR-001: Detect safety and statutory-clock terms.
    matched_safety = [term for term in safety_terms if term in text]
    if matched_safety:
        reasons.append("safety_signal")
        rule_hits.extend([f"safety:{term}" for term in matched_safety])

    # FR-002: Detect policy-sensitive terms.
    matched_policy = [term for term in policy_terms if term in text]
    if matched_policy:
        reasons.append("policy_signal")
        rule_hits.extend([f"policy:{term}" for term in matched_policy])

    # Constitution Governance: escalate legal, regulatory, recall, PII, and safety topics.
    matched_governance = [term for term in governance_terms if term in text]
    if matched_governance:
        reasons.append("governance_escalation")
        rule_hits.extend([f"governance:{term}" for term in matched_governance])

    # Determine severity and confidence.
    if reasons:
        # FR-001: Safety signals force SEV1.
        if "safety_signal" in reasons:
            severity = "SEV1"
            confidence = 0.95
        elif "governance_escalation" in reasons:
            severity = "SEV1"  # Constitution requires immediate escalation.
            confidence = 0.90
        else:
            severity = "SEV2"
            confidence = 0.85

        # FR-003, FR-004, FR-005: Return structured decision with all metadata.
        return EscalationDecision(
            escalate=True,
            severity=severity,
            reasons=reasons,
            confidence=confidence,
            original_text=user_text,  # FR-004: Preserve original text.
            rule_hits=rule_hits,  # FR-005: Include rule hits.
        )

    # FR-007: Fallback when no triggers detected.
    # Constitution Principle 4: escalate when the system does not know.
    return EscalationDecision(
        escalate=False,
        severity="SEV4",
        reasons=[],
        confidence=0.4,
        original_text=user_text,
        rule_hits=[],
    )
