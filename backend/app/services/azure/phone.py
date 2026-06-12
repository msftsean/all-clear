"""
Azure Communication Services Call Automation service.
Handles inbound PSTN calls and bridges them to the Azure OpenAI Realtime API,
reusing the same GPT realtime deployment and tool pipeline as browser voice.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from azure.core.credentials import AccessToken

from app.services.interfaces import PhoneServiceInterface

logger = logging.getLogger(__name__)

PHONE_SYSTEM_PROMPT = """You are All Clear, an emergency and incident-triage assistant taking a call on the operations line. The caller may be a member of the public, a customer, or a field crew reporting something happening right now.

You're speaking with someone on a phone, not a computer, so keep your responses brief and easy to follow by ear.

Your job on the call:
- Quickly understand what is happening and where.
- Classify the situation (power outage, downed or sparking line, gas leak, fire, water main break, flooding, blocked road, billing or account question, status check, or a request for a person) and route it to the right queue.
- Open a new incident or attach the report to an existing one, and give the caller the incident reference.
- For any life-safety situation (fire, gas, downed/sparking line, someone injured or trapped, carbon monoxide), tell the caller to get to safety and call 911 first, then escalate immediately.

Phone-specific instructions:
- Speak concisely and naturally. Do not use markdown formatting, bullet points, or numbered lists.
- Keep answers to two or three sentences whenever possible — callers cannot scroll back.
- Spell out incident and ticket IDs character by character (e.g., "I-N-C dash one zero two four").
- Do NOT repeat any personal identifying information the caller provides (SSN, account number, email, phone).
- Acknowledge the caller's situation before giving instructions, and stay calm and reassuring.
- Ask only one short clarifying question at a time, prioritizing location and whether anyone is in danger.
- Never promise a restoration time, credit, or outcome that the operations team has not confirmed.
- Drafts and public statements always need human approval before they go out.
"""


class PhoneUnavailableError(Exception):
    """Raised when Azure Communication Services is unavailable."""
    pass


class AzurePhoneService(PhoneServiceInterface):
    """
    Production implementation using Azure Communication Services Call Automation.
    Answers inbound PSTN calls and connects audio to the Azure OpenAI Realtime API
    via WebSocket media streaming, reusing the same gpt-realtime deployment.
    """

    def __init__(
        self,
        acs_endpoint: str,
        openai_endpoint: str,
        openai_deployment: str,
        connection_string: Optional[str] = None,
        api_key: Optional[str] = None,
        credential: Optional[object] = None,
    ) -> None:
        self.acs_endpoint = acs_endpoint.rstrip("/")
        self.openai_endpoint = openai_endpoint.rstrip("/")
        self.openai_deployment = openai_deployment
        self.connection_string = connection_string
        self.api_key = api_key
        self.credential = credential
        self._client = None
        self._client_lock = asyncio.Lock()
        self._token: Optional[AccessToken] = None
        self._credential_lock = asyncio.Lock()

    async def _get_client(self):
        """Get or create the CallAutomationClient (lazy init with double-checked locking)."""
        if self._client is not None:
            return self._client

        async with self._client_lock:
            if self._client is not None:
                return self._client

            try:
                from azure.communication.callautomation import CallAutomationClient

                if self.connection_string:
                    logger.info("Phone auth: using ACS connection string")
                    self._client = CallAutomationClient.from_connection_string(
                        self.connection_string
                    )
                else:
                    logger.info("Phone auth: using managed identity")
                    if not self.credential:
                        from azure.identity.aio import ManagedIdentityCredential
                        self.credential = ManagedIdentityCredential()
                        logger.info("Phone auth: created ManagedIdentityCredential")
                    self._client = CallAutomationClient(self.acs_endpoint, self.credential)

                logger.info("Phone: CallAutomationClient initialized")
            except ImportError as exc:
                raise PhoneUnavailableError(
                    "azure-communication-callautomation is not installed. "
                    "Run: pip install azure-communication-callautomation>=1.4.0"
                ) from exc
            except Exception as exc:
                raise PhoneUnavailableError(
                    f"Failed to initialize CallAutomationClient: {exc}"
                ) from exc

        return self._client

    async def handle_incoming_call(
        self,
        incoming_call_context: str,
        caller_id: str,
        callback_url: str,
    ) -> dict:
        """Answer an incoming PSTN call and connect audio to the AI agent.

        Uses ACS Call Automation to answer the call and start media streaming
        to the Azure OpenAI Realtime API WebSocket endpoint.
        """
        client = await self._get_client()

        # Media streaming URL — route through the backend's WebSocket bridge
        # so the bridge can authenticate to Azure OpenAI with managed identity.
        # Derive the WebSocket URL from the callback URL (same host).
        ws_base = callback_url.rsplit("/api/phone/", 1)[0]
        media_ws_url = (
            ws_base
            .replace("https://", "wss://")
            .replace("http://", "ws://")
            + "/ws/acs-media"
        )

        logger.info(
            f"Phone: answering call from {caller_id}, "
            f"media_ws={media_ws_url}"
        )

        try:
            from azure.communication.callautomation import (
                AudioFormat,
                MediaStreamingOptions,
                StreamingTransportType,
                MediaStreamingContentType,
                MediaStreamingAudioChannelType,
            )

            media_streaming = MediaStreamingOptions(
                transport_url=media_ws_url,
                transport_type=StreamingTransportType.WEBSOCKET,
                content_type=MediaStreamingContentType.AUDIO,
                audio_channel_type=MediaStreamingAudioChannelType.MIXED,
                start_media_streaming=True,
                enable_bidirectional=True,
                audio_format=AudioFormat.PCM24_K_MONO,
            )

            answer_result = client.answer_call(
                incoming_call_context=incoming_call_context,
                callback_url=callback_url,
                media_streaming=media_streaming,
            )

            call_connection_id = answer_result.call_connection_id
            logger.info(f"Phone: call answered, connection_id={call_connection_id}")

            return {
                "call_connection_id": call_connection_id,
                "status": "connecting",
                "caller_id": caller_id,
            }

        except PhoneUnavailableError:
            raise
        except Exception as exc:
            logger.error(f"Phone: failed to answer call from {caller_id}: {exc}")
            raise PhoneUnavailableError(
                f"Failed to answer incoming call: {exc}"
            ) from exc

    async def handle_call_event(
        self,
        event_type: str,
        event_data: dict,
    ) -> dict:
        """Handle a Call Automation callback event.

        Routes lifecycle events to the appropriate handler and returns
        a summary of the action taken.
        """
        call_connection_id = event_data.get("callConnectionId", "unknown")

        # Strip namespace prefix if present (e.g. "Microsoft.Communication.CallConnected")
        short_type = event_type.split(".")[-1] if "." in event_type else event_type

        logger.info(f"Phone: event={short_type}, call_id={call_connection_id}")

        if short_type == "CallConnected":
            return await self._on_call_connected(call_connection_id, event_data)
        elif short_type == "CallDisconnected":
            return await self._on_call_disconnected(call_connection_id, event_data)
        elif short_type == "MediaStreamingStarted":
            logger.info(f"Phone: media streaming started, call_id={call_connection_id}")
            return {"action": "media_streaming_started", "call_connection_id": call_connection_id}
        elif short_type == "MediaStreamingStopped":
            logger.info(f"Phone: media streaming stopped, call_id={call_connection_id}")
            return {"action": "media_streaming_stopped", "call_connection_id": call_connection_id}
        elif short_type == "MediaStreamingFailed":
            result_info = event_data.get("resultInformation", {})
            logger.error(
                f"Phone: media streaming failed, call_id={call_connection_id}, "
                f"code={result_info.get('code')}, message={result_info.get('message')}"
            )
            return {
                "action": "media_streaming_failed",
                "call_connection_id": call_connection_id,
                "error": result_info.get("message", "Unknown error"),
            }
        else:
            logger.debug(f"Phone: unhandled event type={short_type}")
            return {"action": "unhandled", "event_type": short_type, "call_connection_id": call_connection_id}

    async def _on_call_connected(self, call_connection_id: str, event_data: dict) -> dict:
        """Call is connected — log and confirm media streaming should begin."""
        logger.info(f"Phone: call connected, call_id={call_connection_id}")
        return {
            "action": "call_connected",
            "call_connection_id": call_connection_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }

    async def _on_call_disconnected(self, call_connection_id: str, event_data: dict) -> dict:
        """Call ended — log and clean up."""
        logger.info(f"Phone: call disconnected, call_id={call_connection_id}")
        return {
            "action": "call_disconnected",
            "call_connection_id": call_connection_id,
            "ended_at": datetime.now(timezone.utc).isoformat(),
        }

    async def health_check(self) -> tuple[bool, Optional[int], Optional[str]]:
        """Check ACS connectivity by verifying the client can be initialized."""
        import time
        start = time.monotonic()
        try:
            await self._get_client()
            latency_ms = int((time.monotonic() - start) * 1000)
            return True, latency_ms, None
        except PhoneUnavailableError as exc:
            latency_ms = int((time.monotonic() - start) * 1000)
            return False, latency_ms, str(exc)
        except Exception as exc:
            latency_ms = int((time.monotonic() - start) * 1000)
            return False, latency_ms, f"Unexpected error: {exc}"

    async def close(self) -> None:
        """Close the ACS client and credential."""
        self._client = None
        if hasattr(self.credential, "close"):
            await self.credential.close()
