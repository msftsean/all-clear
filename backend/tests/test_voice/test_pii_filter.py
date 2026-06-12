"""Tests for PII filtering in voice tool responses.

T020: PII values in query arguments must not be echoed in tool results.

These tests verify the MockRealtimeService does not parrot back raw user input
that may contain sensitive data (SSN, email, phone number).
"""
from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from app.api.realtime import _append_voice_message
from app.core.dependencies import get_session_store
from app.models.schemas import Session
from app.services.mock.realtime import MockRealtimeService


class TestVoicePiiFilter:
    """PII must not leak through voice tool responses."""

    @pytest.fixture
    def service(self):
        return MockRealtimeService()

    async def test_pii_not_echoed_in_tool_result(self, service):
        """T020a: SSN in query must not appear verbatim in tool result."""
        result = await service.execute_tool(
            call_id="pii-test-1",
            tool_name="analyze_and_route_query",
            arguments={"query": "my SSN is 123-45-6789"},
            session_id="pii-test-session",
        )
        assert result.error is None
        assert "123-45-6789" not in result.result

    async def test_email_not_echoed_in_tool_result(self, service):
        """T020b: Email in query must not appear verbatim in tool result."""
        result = await service.execute_tool(
            call_id="pii-test-2",
            tool_name="analyze_and_route_query",
            arguments={"query": "my email is student@university.edu and I need help"},
            session_id="pii-test-session",
        )
        assert result.error is None
        # Mock response should not echo the raw input query back
        assert "student@university.edu" not in result.result

    async def test_phone_not_echoed_in_tool_result(self, service):
        """T020c: Phone number in query must not appear verbatim in tool result."""
        result = await service.execute_tool(
            call_id="pii-test-3",
            tool_name="search_knowledge_base",
            arguments={"query": "call me at 555-123-4567"},
            session_id="pii-test-session",
        )
        assert result.error is None
        assert "555-123-4567" not in result.result

    async def test_credit_card_not_echoed_in_tool_result(self, service):
        """T020d: Credit card number in query must not appear verbatim in tool result."""
        result = await service.execute_tool(
            call_id="pii-test-4",
            tool_name="analyze_and_route_query",
            arguments={"query": "my card number is 4111-1111-1111-1111"},
            session_id="pii-test-session",
        )
        assert result.error is None
        assert "4111-1111-1111-1111" not in result.result

    async def test_tool_result_is_non_empty_after_pii_query(self, service):
        """T020e: Tool result must still be non-empty when query contains PII."""
        result = await service.execute_tool(
            call_id="pii-test-5",
            tool_name="analyze_and_route_query",
            arguments={"query": "SSN 123-45-6789 I need password help"},
            session_id="pii-test-session",
        )
        assert result.error is None
        assert result.result  # non-empty response

    async def test_ssn_removed_from_voice_tool_input(self, service):
        """T069 layer 1: SSN in tool input is redacted before tool handling."""
        result = await service.execute_tool(
            call_id="pii-test-6",
            tool_name="escalate_to_human",
            arguments={"reason": "my SSN is 123-45-6789 and I need a human"},
            session_id="pii-test-session",
        )
        assert result.error is None
        assert "123-45-6789" not in result.result
        assert "[REDACTED]" in result.result

    async def test_credit_card_removed_from_voice_tool_result(self, service):
        """T069 layer 2: credit card numbers are removed from tool results."""
        result = await service.execute_tool(
            call_id="pii-test-7",
            tool_name="escalate_to_human",
            arguments={"reason": "card 4111-1111-1111-1111 was charged twice"},
            session_id="pii-test-session",
        )
        assert result.error is None
        assert "4111-1111-1111-1111" not in result.result
        assert "[REDACTED]" in result.result

    async def test_phone_removed_from_voice_message_content(self):
        """T069 layer 3: phone numbers are removed before storing VoiceMessage.content."""
        session_id = uuid4()
        now = datetime.now(UTC)
        await get_session_store().create_session(
            Session(
                session_id=session_id,
                student_id_hash="a" * 64,
                created_at=now,
                last_active=now,
                conversation_history=[],
                clarification_attempts=0,
            )
        )

        await _append_voice_message(str(session_id), "Please call me at 555-123-4567")
        stored = await get_session_store().get_session(UUID(str(session_id)))
        assert stored.conversation_history[-1].input_modality == "voice"
        assert "555-123-4567" not in stored.conversation_history[-1].content


class TestPiiStudentIdAndDob:
    """T019: context-anchored student-ID/DOB redaction without ticket-ID false positives."""

    def test_student_id_redacted_when_labeled(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("My student id is 12345678 please help")
        assert "12345678" not in out
        assert "[REDACTED]" in out

    def test_campus_number_redacted(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("campus number: A0098231")
        assert "A0098231" not in out
        assert "[REDACTED]" in out

    def test_dob_redacted_when_labeled(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("date of birth 03/14/2001")
        assert "03/14/2001" not in out
        assert "[REDACTED]" in out

    def test_ticket_id_not_redacted(self):
        """Ticket IDs embed an 8-digit date but must survive — not student PII."""
        from app.services.pii import redact_pii_text

        for tid in ("TKT-IT-20260601-0007", "ESC-MOCK-20260601-0003"):
            out = redact_pii_text(f"Your ticket is {tid}, follow up tomorrow.")
            assert tid in out, f"{tid} was wrongly redacted: {out}"

    def test_bare_number_not_redacted_without_label(self):
        """An unlabeled 8-digit number is left alone (avoids over-redaction)."""
        from app.services.pii import redact_pii_text

        out = redact_pii_text("Order quantity 12345678 units shipped")
        assert "12345678" in out

    def test_student_id_number_phrasing_redacted(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("my student id number is 12345678")
        assert "12345678" not in out

    def test_student_id_with_letter_prefix_and_dash(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("student ID is A-1234567 thanks")
        assert "1234567" not in out

    def test_student_no_dot_phrasing(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("student no. 1234567 please")
        assert "1234567" not in out

    def test_month_name_dob_redacted(self):
        from app.services.pii import redact_pii_text

        out = redact_pii_text("DOB: March 14, 2001")
        assert "March 14, 2001" not in out
        assert "2001" not in out
