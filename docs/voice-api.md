# Voice Realtime API

Canonical OpenAPI contract: [`specs/002-voice-interaction/contracts/voice-api.yaml`](../specs/002-voice-interaction/contracts/voice-api.yaml).

The realtime router is mounted in `backend/app/main.py` with `prefix=f"{settings.api_prefix}/realtime"`; `settings.api_prefix` defaults to `/api`. The implemented public paths are therefore `/api/realtime/session`, `/api/realtime/ws`, and `/api/realtime/health`.

## POST `/api/realtime/session`

Creates an ephemeral Azure OpenAI Realtime session token. The handler is `create_realtime_session()` in `backend/app/api/realtime.py` and uses `RealtimeSessionRequest` / `RealtimeSessionResponse` from `backend/app/models/voice_schemas.py`.

### Request body

| Field | Type | Required | Notes |
|---|---|---:|---|
| `session_id` | string or null | No | Existing session ID. If omitted or null, the backend generates a UUID. |
| `voice` | string | No | Defaults to `alloy` in the Pydantic model. |
| `instructions` | string or null | No | Optional system prompt override, max 2000 characters. |

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "voice": "shimmer",
  "instructions": "Speak concisely and focus on IT support."
}
```

Minimal request:

```json
{
  "voice": "alloy"
}
```

### Success response: `200 OK`

| Field | Type | Notes |
|---|---|---|
| `session_id` | string | Matches the request value or the generated UUID. |
| `token` | string | Short-lived ephemeral credential. |
| `expires_at` | string, date-time | Token expiry timestamp. |
| `endpoint` | string | Azure OpenAI Realtime API WebRTC endpoint URL. |
| `deployment` | string | Realtime model deployment name. |

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eph_abc123...",
  "expires_at": "2026-05-31T12:01:00Z",
  "endpoint": "https://your-instance.openai.azure.com",
  "deployment": "gpt-realtime"
}
```

### Voice unavailable response: `503 Service Unavailable`

```json
{
  "detail": {
    "error": "voice_unavailable",
    "message": "Azure OpenAI Realtime API is not configured"
  }
}
```

## WS `/api/realtime/ws`

WebSocket relay for tool calls. The handler is `websocket_tool_relay()` in `backend/app/api/realtime.py`. It requires both query parameters and accepts/sends JSON frames matching `ToolCallRequest` and `ToolCallResponse` in `backend/app/models/voice_schemas.py`.

### Connection

```text
ws://localhost:8000/api/realtime/ws?session_id=550e8400-e29b-41d4-a716-446655440000&token=eph_abc123...
```

| Query parameter | Type | Required | Notes |
|---|---|---:|---|
| `session_id` | string | Yes | Session ID used for tool execution context. |
| `token` | string | Yes | Ephemeral token from `POST /api/realtime/session`; the current handler rejects empty or very short tokens. |

### Inbound frame: `ToolCallRequest`

```json
{
  "call_id": "call_001",
  "tool_name": "analyze_and_route_query",
  "arguments": {
    "query": "I forgot my password"
  }
}
```

| Field | Type | Required | Notes |
|---|---|---:|---|
| `call_id` | string | Yes | Unique tool call identifier. |
| `tool_name` | string | Yes | Tool name to invoke. |
| `arguments` | object | No | Defaults to `{}` in the Pydantic model. |

### Outbound frame: `ToolCallResponse`

```json
{
  "call_id": "call_001",
  "result": "{\"intent\": \"general_question\", \"department\": \"IT\", \"ticket_id\": \"TKT-IT-MOCK-12345678\"}",
  "error": null
}
```

On validation or execution errors, the handler sends the same shape with `result` set to an empty string and `error` containing a message.

```json
{
  "call_id": "call_001",
  "result": "",
  "error": "Unknown tool: unsupported_tool"
}
```

### Close codes

| Code | Meaning |
|---:|---|
| `1000` | Normal closure. |
| `4001` | Invalid token. |
| `4002` | Session not found. |
| `1011` | Server error. |

## GET `/api/realtime/health`

Returns voice subsystem availability from `realtime_health()` in `backend/app/api/realtime.py`.

### Success response: `200 OK`

| Field | Type | Notes |
|---|---|---|
| `realtime_available` | boolean | Mirrors `settings.voice_enabled`. |
| `mock_mode` | boolean | Mirrors `settings.mock_mode`. |
| `voice_enabled` | boolean | Mirrors `settings.voice_enabled`. |

```json
{
  "realtime_available": true,
  "mock_mode": true,
  "voice_enabled": true
}
```
