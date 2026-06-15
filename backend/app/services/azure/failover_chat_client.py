"""Model-agnostic chat-client failover (018-model-agnostic-failover).

``FailoverChatClient`` wraps an ordered list of MAF chat clients (a primary plus
one or more fallbacks) behind the standard ``BaseChatClient`` interface used by
the All Clear pipeline's QueryAgent. When the active client raises a
*model-unavailability* error, the wrapper advances to the next client and retries
the same request. If a model is pulled, restricted, or returns
404/403/401/503, triage keeps running on the fallback instead of failing.

What is **not** a failover trigger (by design):

- **Rate limits (HTTP 429).** Handled by ``app.agents.retry.with_rate_limit_retry``;
  a 429 is back-pressure, not an outage.
- **Content-filter / Prompt-Shield blocks.** A guardrail block is a *correct*
  safety outcome (Constitution Art. III); routing around it would be a defect.

The wrapper is transport-only: it adds no tools and no authority, preserves
``response_format`` passthrough so classification stays typed (Art. IV), and is a
no-op when only a single client is supplied (``build_failover_client``).
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from typing import Any

from agent_framework import BaseChatClient

logger = logging.getLogger(__name__)

# Exception *type names* that unambiguously mean "this model/deployment cannot
# serve the request right now" (matched by name to avoid importing openai).
_UNAVAILABLE_TYPE_NAMES = frozenset(
    {"NotFoundError", "PermissionDeniedError", "AuthenticationError", "APIStatusError"}
)

# HTTP status codes that mean the model is unavailable/inaccessible.
_UNAVAILABLE_STATUS = frozenset({401, 403, 404, 503})

# Substrings (lower-cased) that indicate model unavailability.
_UNAVAILABLE_SUBSTRINGS = (
    "deploymentnotfound",
    "deployment not found",
    "model_not_found",
    "model not found",
    "does not exist",
    "service unavailable",
    "serviceunavailable",
    "access denied",
    "permissiondenied",
    "unauthorized",
    "forbidden",
)

# Markers that must NEVER count as a failover trigger.
_RATE_LIMIT_MARKERS = ("ratelimiterror", "429", "too many requests", "too_many_requests")
_CONTENT_FILTER_MARKERS = (
    "content_filter",
    "contentfiltered",
    "responsibleaipolicyviolation",
    "content management policy",
    "jailbreak",
    "prompt shield",
)


def _status_code(exc: BaseException) -> int | None:
    """Best-effort HTTP status code from an openai/httpx-style exception."""
    code = getattr(exc, "status_code", None)
    if code is None:
        response = getattr(exc, "response", None)
        code = getattr(response, "status_code", None)
    return code if isinstance(code, int) else None


def _is_model_unavailable(exc: BaseException) -> bool:
    """True if ``exc`` (or anything in its cause/context chain) means the model
    is unavailable/inaccessible — and is NOT a rate limit or content-filter block.
    """
    seen: set[int] = set()
    cur: BaseException | None = exc
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        name = type(cur).__name__
        text = str(cur).lower()

        # Guardrail and back-pressure signals are never "unavailable".
        if name == "RateLimitError" or any(m in text for m in _RATE_LIMIT_MARKERS):
            return False
        if any(m in text for m in _CONTENT_FILTER_MARKERS):
            return False

        if _status_code(cur) in _UNAVAILABLE_STATUS:
            return True
        if name in _UNAVAILABLE_TYPE_NAMES:
            return True
        if any(m in text for m in _UNAVAILABLE_SUBSTRINGS):
            return True

        cur = cur.__cause__ or cur.__context__
    return False


class FailoverChatClient(BaseChatClient):
    """Ordered failover across a primary chat client and one or more fallbacks."""

    OTEL_PROVIDER_NAME = "allclear.failover"

    def __init__(
        self,
        clients: Sequence[BaseChatClient],
        model_names: Sequence[str],
    ) -> None:
        if not clients:
            raise ValueError("FailoverChatClient requires at least one client")
        if len(clients) != len(model_names):
            raise ValueError("clients and model_names must be the same length")
        super().__init__()
        self._clients: list[BaseChatClient] = list(clients)
        self._model_names: list[str] = list(model_names)
        self._last_used_index: int = 0
        self._last_used_model: str = model_names[0]

    @property
    def model_names(self) -> list[str]:
        return list(self._model_names)

    @property
    def last_used_model(self) -> str:
        return self._last_used_model

    @property
    def last_used_index(self) -> int:
        return self._last_used_index

    @property
    def failover_active(self) -> bool:
        """True if the most recent request was served by a fallback, not the primary."""
        return self._last_used_index > 0

    def _inner_get_response(  # type: ignore[override]
        self,
        *,
        messages: Sequence[Any],
        stream: bool,
        options: Mapping[str, Any],
        **kwargs: Any,
    ) -> Any:
        if stream:
            return self._get_streaming(messages=messages, options=options, kwargs=kwargs)
        return self._get_response(messages=messages, options=options, kwargs=kwargs)

    async def _get_response(
        self,
        *,
        messages: Sequence[Any],
        options: Mapping[str, Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        last_exc: BaseException | None = None
        for index, client in enumerate(self._clients):
            try:
                response = await client.get_response(
                    messages,
                    options=options or None,  # type: ignore[arg-type]
                    client_kwargs=dict(kwargs) or None,
                )
            except Exception as exc:  # noqa: BLE001 - re-raised unless a fallback exists
                last_exc = exc
                if index + 1 < len(self._clients) and _is_model_unavailable(exc):
                    logger.warning(
                        "chat model %r unavailable (%s); failing over to %r",
                        self._model_names[index],
                        type(exc).__name__,
                        self._model_names[index + 1],
                    )
                    continue
                raise
            self._last_used_index = index
            self._last_used_model = self._model_names[index]
            return response
        assert last_exc is not None  # loop only exits via return or raise
        raise last_exc

    def _get_streaming(
        self,
        *,
        messages: Sequence[Any],
        options: Mapping[str, Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        last_exc: BaseException | None = None
        for index, client in enumerate(self._clients):
            try:
                stream = client.get_response(
                    messages,
                    stream=True,
                    options=options or None,  # type: ignore[arg-type]
                    client_kwargs=dict(kwargs) or None,
                )
            except Exception as exc:  # noqa: BLE001 - re-raised unless a fallback exists
                last_exc = exc
                if index + 1 < len(self._clients) and _is_model_unavailable(exc):
                    logger.warning(
                        "chat model %r unavailable on stream open (%s); failing over to %r",
                        self._model_names[index],
                        type(exc).__name__,
                        self._model_names[index + 1],
                    )
                    continue
                raise
            self._last_used_index = index
            self._last_used_model = self._model_names[index]
            return stream
        assert last_exc is not None
        raise last_exc


def build_failover_client(
    clients: Sequence[BaseChatClient],
    model_names: Sequence[str],
) -> BaseChatClient:
    """Return a ``FailoverChatClient`` when a fallback exists, else the bare client.

    A single-element chain is returned unwrapped so the no-fallback path is a true
    no-op (identical behavior to before this feature).
    """
    if len(clients) == 1:
        return clients[0]
    return FailoverChatClient(clients, model_names)
