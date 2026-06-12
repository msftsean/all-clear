# 🚀 Voice Feature — Developer Quickstart

> **Feature branch**: `002-voice-interaction` | **Spec**: [spec.md](./spec.md) | **API contract**: [contracts/voice-api.yaml](./contracts/voice-api.yaml)

The voice feature adds a real-time spoken conversation channel to the 47 Doors Support Agent using the Azure OpenAI GPT Realtime API over WebRTC (browser) or direct WebSocket (phone bridge via Azure Communication Services). Audio travels **directly** from the browser to Azure — nothing audio-related passes through the backend. The backend exposes realtime session, health, and tool-call relay endpoints under `/api/realtime`. For phone calls to +1 (913) 217-1946, audio flows through an ACS media streaming bridge at `backend/app/api/media_ws.py`.

---

## 1. Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11+ |
| Node.js | 18+ |
| npm | 9+ |
| Browser | Chrome 90+, Firefox 85+, Edge 90+, or Safari 15+ (WebRTC required) |
| Azure OpenAI | Only needed for live mode — see [Mock Mode](#2-mock-mode-no-azure-required) |

For **live mode** you additionally need an Azure OpenAI resource with a `gpt-realtime` deployment. Supported regions: `eastus2`, `swedencentral`, `westus3`.

---

## 2. Mock Mode (No Azure Required)

Mock mode is the **default**. It simulates the Realtime API session and tool execution using the existing text pipeline and returns deterministic text responses. The current frontend still initializes WebRTC and requests microphone permission when starting voice.

```bash
# ── Terminal 1: Backend ──────────────────────────────────────────────────────
cd backend
cp .env.example .env      # MOCK_MODE=true is already set in .env.example
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# ── Terminal 2: Frontend ─────────────────────────────────────────────────────
cd frontend
npm install
npm run dev               # Vite proxy forwards /api → http://127.0.0.1:8000
```

Open `http://localhost:5173` — the 🎤 microphone button appears in the chat input area.

> **What mock mode does**
> - `GET /api/realtime/health` returns `{ "realtime_available": true, "mock_mode": true, "voice_enabled": true }` in the default mock configuration
> - `POST /api/realtime/session` returns a synthetic token (never leaves the backend)
> - Tool calls route through the real 3-agent pipeline; responses are delivered as text
> - The mic button shows all visual states (listening → processing → responding) with simulated timing
> - Great for UI work, demos, and running CI without Azure credentials

---

## 3. Live Mode (Azure Required)

### 3.1 Environment Variables

Add these to `backend/.env` (do **not** commit secrets):

```dotenv
# Switch to live mode
MOCK_MODE=false

# Azure OpenAI — existing deployment (used by text chat)
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4.1

# Realtime API — gpt-realtime deployment
AZURE_OPENAI_REALTIME_DEPLOYMENT=gpt-realtime
```

> ⚠️ **Managed Identity (Azure Container Apps)**: When deployed to Azure Container Apps via `azd up`, the backend uses `ManagedIdentityCredential` — no API key is needed. The Container App's system-assigned managed identity must have the `Cognitive Services OpenAI User` role on the Azure OpenAI resource. API key auth is disabled by Azure subscription policy (`disableLocalAuth: true`).
>
> **Local development**: For local development, set `AZURE_OPENAI_API_KEY` in `.env` if your Azure OpenAI resource allows API key auth. The current `AzureRealtimeService` uses `ManagedIdentityCredential` which only works in Azure Container Apps — for local dev, use mock mode (`MOCK_MODE=true`).
>
> **Docker**: Ensure `backend/.dockerignore` excludes `.env` to prevent secrets from being baked into container images.

### 3.2 Required Azure Deployment

The Realtime API requires a separate model deployment. Supported regions:

| Region | Status |
|---|---|
| `eastus2` | GA |
| `swedencentral` | GA |
| `westus3` | GA |

Provision via Bicep (see `infra/`) or the Azure Portal → Azure OpenAI → Model deployments → Add → `gpt-realtime`.

### 3.3 Start

```bash
# Backend (same as mock mode)
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (same as mock mode)
cd frontend && npm run dev
```

The microphone button is now backed by the real Realtime API. A WebRTC peer connection is established between the browser and Azure OpenAI directly.

---

## 4. Codespaces Notes

Vite proxies `/api` to the backend automatically — **do not set `VITE_API_BASE_URL` to a localhost URL** inside Codespaces (leave it as empty string or unset).

```dotenv
# frontend/.env.local inside Codespaces — leave this blank
VITE_API_BASE_URL=
```

| Port | Service | Forward? |
|---|---|---|
| `5173` | Vite dev server (frontend) | ✅ Yes |
| `8000` | uvicorn (backend) | ✅ Yes |

WebRTC works in Codespaces — the browser handles the peer connection to Azure OpenAI directly. The backend WebSocket endpoint (`/api/realtime/ws`) is available through the Vite proxy for relay clients and tests; the current browser hook uses the Realtime API data channel for Azure events.

---

## 5. Key Files

### Backend

| File | Purpose |
|---|---|
| `backend/app/api/realtime.py` | `POST /api/realtime/session`, `WS /api/realtime/ws`, `GET /api/realtime/health` |
| `backend/app/services/interfaces.py` | `RealtimeServiceInterface` — implemented by both mock and Azure services |
| `backend/app/services/mock/realtime.py` | Mock realtime service (simulates tool calls) |
| `backend/app/services/azure/realtime.py` | Azure OpenAI Realtime API integration |
| `backend/app/models/voice_schemas.py` | `VoiceMessage`, `RealtimeSessionRequest`, `RealtimeSessionResponse`, `ToolDefinition`, `ToolCallRequest`, `ToolCallResponse` |
| `backend/app/core/config.py` | Voice config fields (`voice_enabled`, `azure_openai_realtime_deployment`, etc.) |

### Frontend

| File | Purpose |
|---|---|
| `frontend/src/hooks/useVoice.ts` | WebRTC state machine, Realtime API data channel, and transcript handling hook |
| `frontend/src/components/VoiceMicButton.tsx` | Mic toggle with 6 visual states |
| `frontend/src/components/VoiceTranscript.tsx` | Real-time transcript bubbles in chat thread |
| `frontend/src/components/VoiceStatusIndicator.tsx` | Connection status banner |
| `frontend/src/types/voice.ts` | `VoiceUIState`, `VoiceMessage`, `RealtimeSessionResponse`, `VoiceHealthResponse` types |
| `frontend/src/components/ChatContainer.tsx` | Integrates voice components into the chat UI |

### Config & Infra

| File | Purpose |
|---|---|
| `backend/.env.example` | Environment variable template |
| `infra/` | Bicep templates — includes `gpt-realtime` deployment |
| `specs/002-voice-interaction/contracts/voice-api.yaml` | OpenAPI 3.1 contract for all voice endpoints |

---

## 6. API Quick Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/realtime/health` | GET | Reports voice availability (`realtime_available`, `mock_mode`, `voice_enabled`) |
| `/api/realtime/session` | POST | Get an ephemeral token (TTL ≤ 60 s) for WebRTC auth |
| `/api/realtime/ws` | WS | Tool call relay (connect with `?session_id=…&token=…`) |

Full schema: [`contracts/voice-api.yaml`](./contracts/voice-api.yaml)

---

## 7. Running Tests

```bash
# ── Backend voice tests ───────────────────────────────────────────────────────
cd backend
python -m pytest tests/test_voice/ -v

# Run all backend tests (voice + existing, excluding GPT-4.1 evals)
python -m pytest -x --ignore=tests/test_gpt4o_evals.py

# ── GPT-4.1 model evals (requires az login) ────────────────────────────────────
az login                              # authenticate with DefaultAzureCredential
python -m pytest tests/test_gpt4o_evals.py -v   # 97 tests: intent, PII, sentiment, entities, urgency, e2e

# Run ALL backend tests (338 unit/mock + 97 GPT-4.1 evals)
python -m pytest -x

# ── Frontend voice tests ──────────────────────────────────────────────────────
cd frontend
npm test -- --run src/components/VoiceMicButton.test.tsx src/hooks/useVoice.test.ts

# E2E (requires both backend and frontend running)
npx playwright test tests/e2e/voice-e2e.spec.ts
```

Backend test coverage areas:

| Test file | What it covers |
|---|---|
| `test_config.py` | Voice config fields, `voice_enabled` flag, mock-mode defaults |
| `test_models.py` | `VoiceMessage`, `RealtimeSessionResponse` Pydantic validation |
| `test_mock_service.py` | Mock Realtime service tool call simulation |
| `test_endpoints.py` | `POST /api/realtime/session`, WS handshake for `/api/realtime/ws` |
| `test_pii_filter.py` | PII scrubbing of transcripts before persistence |
| `test_evals.py` | 74 mock-based eval tests (intent routing, PII, sentiment, entities, urgency) |
| `test_gpt4o_evals.py` | 97 GPT-4.1 model eval tests via `DefaultAzureCredential` (requires `az login`) |

Frontend test coverage areas:

| Test file | What it covers |
|---|---|
| `VoiceMicButton.test.tsx` | All 6 visual states, keyboard activation (Enter/Escape) |
| `useVoice.test.ts` | WebRTC environment check and `VoiceUIState` enum coverage with pending hook behavior todos |
| `voice-e2e.spec.ts` | Full mock-mode voice session end-to-end flow |

---

## 8. Architecture: How a Voice Request Works

```
1. User clicks 🎤
2. Frontend calls POST /api/realtime/session → receives { token, endpoint, deployment }
3. Frontend opens RTCPeerConnection to Azure OpenAI (WebRTC, using ephemeral token)
4. Frontend opens the Realtime API data channel (`oai-events`) and sends `session.update`
5. User speaks → Azure OpenAI streams audio, detects events, and returns audio/transcript events
6. Transcript appended to chat thread with 🔊 icon
7. The backend WebSocket relay remains available at /api/realtime/ws for ToolCallRequest/ToolCallResponse clients
8. User clicks 🎤 again or presses Escape → WebRTC/data-channel resources are closed
```

---

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| Mic button not shown | Confirm the browser supports `RTCPeerConnection`; the current UI renders the mic button from `isVoiceSupported`. You can also check `GET /api/realtime/health` → `realtime_available` should be `true` in mock mode. |
| Mic permission dialog never appears | The current hook requests microphone access in both mock and live mode. Confirm the page is served over HTTPS or `localhost`, and check browser microphone permissions. |
| WebRTC connection fails | Check browser console for ICE errors. In live mode verify `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_REALTIME_DEPLOYMENT` are set. Ensure frontend uses `{endpoint}/openai/v1/realtime/calls` for WebRTC SDP exchange. |
| Auth fails with `disableLocalAuth` | Your Azure subscription enforces managed identity. Remove `AZURE_OPENAI_API_KEY` from `.env`. Deploy to Azure Container Apps and ensure the MI has `Cognitive Services OpenAI User` role. |
| `.env` overrides managed identity | Ensure `backend/.dockerignore` excludes `.env`. Rebuild: `azd deploy`. |
| Tools not executing | Check uvicorn logs for WebSocket messages. Verify the 3-agent pipeline is healthy (`GET /api/health`). |
| Mock mode not responding | Confirm `MOCK_MODE=true` in `backend/.env`. Restart uvicorn after `.env` changes. |
| WS closes with code 4001 | Ephemeral token expired (TTL ≤ 60 s). Request a new token via `POST /api/realtime/session` before connecting. |
| WS closes with code 4002 | `session_id` not found. Confirm the UUID in query params matches a live session. |
| Text chat broken after voice | Should never happen — voice uses separate connections. File a bug and check `ChatContainer.tsx` state isolation. |

---

## 10. Static validation note

Validated 2026-05-31 (static review, mock_mode path). Fixed discrepancies found during review: health response example now includes `voice_enabled`; backend endpoint/path references now include the `/api` prefix and `WS` method; backend model path updated to `backend/app/models/voice_schemas.py`; frontend hook/ChatContainer paths and type names updated to match `frontend/src`; frontend unit and E2E test commands updated to existing test file paths; architecture and Codespaces notes updated to reflect that the current `useVoice` hook uses WebRTC plus the Realtime API data channel and does not directly open `/api/realtime/ws`; mock-mode and troubleshooting notes updated because the current hook still requests microphone/WebRTC access.

## 11. Constitution Compliance Reminders

> These are non-negotiable per [constitution.md](../../.specify/memory/constitution.md).

- 🔒 **No raw audio stored** — only PII-filtered transcripts (Principle III)
- 🔒 **Ephemeral tokens ≤ 60 s TTL, single-use** (Voice Channel Security)
- 🔒 **No API key exposure** — token is the only credential the frontend ever sees
- ♿ **Keyboard accessible mic button** — Space/Enter to activate, Escape to stop (Principle VI)
- ♿ **ARIA live regions** for all voice state changes (Principle VI)
- 📉 **Graceful degradation** — if voice fails, text chat continues unaffected (Principle VII)
- 🧪 **Tests first** — write failing tests before implementing each phase (Principle V)
