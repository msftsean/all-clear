"""Test fakes for FailoverChatClient (018-model-agnostic-failover)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from agent_framework import BaseChatClient, ChatResponse, Message


class FakeError(Exception):
    """An exception carrying an optional HTTP-style status code, used to mimic
    openai/httpx errors (e.g. NotFoundError 404) by name and status."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def make_named_error(type_name: str, message: str, status_code: int | None = None) -> Exception:
    """Build an exception whose ``type(...).__name__`` is ``type_name`` (e.g.
    'NotFoundError', 'RateLimitError') so the detector's name checks are exercised."""
    cls = type(type_name, (FakeError,), {})
    return cls(message, status_code)


class RaisingChatClient(BaseChatClient):
    """A chat client that always raises a configured exception."""

    OTEL_PROVIDER_NAME = "test.raising"

    def __init__(self, exc: BaseException) -> None:
        super().__init__()
        self.exc = exc
        self.calls = 0

    def _inner_get_response(  # type: ignore[override]
        self,
        *,
        messages: Sequence[Message],
        stream: bool,
        options: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        async def _raise() -> ChatResponse:
            self.calls += 1
            raise self.exc

        return _raise()


class RecordingChatClient(BaseChatClient):
    """A chat client that records calls and returns a fixed text response."""

    OTEL_PROVIDER_NAME = "test.recording"

    def __init__(self, text: str = "fallback-response") -> None:
        super().__init__()
        self.text = text
        self.calls = 0

    def _inner_get_response(  # type: ignore[override]
        self,
        *,
        messages: Sequence[Message],
        stream: bool,
        options: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        async def _respond() -> ChatResponse:
            self.calls += 1
            return ChatResponse(messages=[Message("assistant", [self.text])])

        return _respond()
