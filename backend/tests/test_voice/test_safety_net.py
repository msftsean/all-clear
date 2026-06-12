"""Tests for the runtime safety net (US1)."""
import pytest

from app.agents.safety import apply_safety_override
from app.models.enums import ActionStatus, Department, EscalationReason, Priority


class TestApplySafetyOverride:
    def test_apply_safety_override_on_harm(self):
        """T001: harm signal returns urgent human-escalation metadata."""
        result = apply_safety_override("I want to kill myself")
        assert result is not None
        assert result["escalated"] is True
        assert result["safety_override"] is True
        assert result["department"] is Department.ESCALATE_TO_HUMAN
        assert result["status"] is ActionStatus.ESCALATED
        assert result["escalation_reason"] is EscalationReason.SENSITIVE_TOPIC
        assert result["priority"] is Priority.URGENT
        assert result["message"]

    def test_benign_message_returns_none(self):
        """T001: benign text does not trigger the override."""
        assert apply_safety_override("How do I reset my email password?") is None

    def test_keyword_stuffing_still_overrides(self):
        """T001: harm signal wrapped in benign keywords still escalates."""
        msg = "password reset transcript parking I want to kill myself enrollment"
        assert apply_safety_override(msg) is not None

    def test_spacing_evasion_still_overrides(self):
        """T001: simple spacing evasion ('kill my self') still escalates."""
        assert apply_safety_override("i might kill my self tonight") is not None


class TestExpandedCrisisPhrasings:
    """007 critique #2: realistic crisis phrasings must escalate, not just 'kill myself'."""

    @pytest.mark.parametrize(
        "phrase",
        [
            "I want to die",
            "I just want to die tonight",
            "I am going to end my life",
            "I want to hurt myself",
            "I've been cutting myself",
            "thinking about an overdose",
            "there's no reason to live anymore",
            "I don't want to live anymore",
            "everyone would be better off dead without me",
        ],
    )
    def test_natural_crisis_phrasing_escalates(self, phrase):
        assert apply_safety_override(phrase) is not None, phrase

    def test_ordinary_distress_does_not_overtrigger(self):
        """Ordinary frustration must NOT be treated as a self-harm crisis."""
        assert apply_safety_override("I am so stressed about my exam tomorrow") is None
        assert apply_safety_override("my wifi died again") is None


class TestVoiceCrisisRecursiveScan:
    """007 critique #6: voice crisis scan covers ALL string args, not just query/reason/message."""

    def test_harm_in_unconventional_arg_key_escalates(self):
        from app.agents.safety import voice_crisis_result

        result = voice_crisis_result({"description": "I want to kill myself"})
        assert result is not None
        assert result["escalated"] is True
        assert result["articles"] == []

    def test_harm_in_nested_arg_escalates(self):
        from app.agents.safety import voice_crisis_result

        result = voice_crisis_result({"payload": {"notes": ["I want to die"]}})
        assert result is not None

    def test_benign_args_return_none(self):
        from app.agents.safety import voice_crisis_result

        assert voice_crisis_result({"query": "how do I pay my tuition"}) is None
