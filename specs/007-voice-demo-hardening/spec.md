# Feature Specification: Voice Demo Hardening

**Feature Branch**: `007-voice-demo-hardening`
**Created**: 2026-05-31
**Status**: Draft
**Input**: Rubber-duck review of the hackathon baseline (`backup/main-2026-05-31-hackathon-baseline`). Findings recorded in session `findings` table, owner `rubberduck`.

## Context

The 002-voice-interaction feature shipped "all green" (75/75 tasks) but a rubber-duck
review of the hackathon baseline surfaced demo-day risks across security, safety, and
graceful degradation. One reproducible 500 (hybrid voice→text) was already fixed on the
review branch. This feature hardens the remaining findings so the live Fordham demo is
safe and resilient, and so the app runs end-to-end on a fresh clone with **no Azure
credentials** (`mock_mode`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crisis statements always escalate safely (Priority: P1)

A student in distress types or speaks a crisis statement (self-harm, threats, Title IX,
mental-health emergency). Regardless of how the intent classifier labels the message, the
system MUST route to human escalation with urgent priority and MUST NOT surface
irrelevant self-service/KB content.

**Why this priority**: Student safety is the highest-stakes behavior in a live demo and
the most damaging to get wrong publicly. The hardened intent-independent override already
exists in `escalation_rules.py` but is not invoked by the live `/api/chat` or voice
runtime — only by the scenario/eval layer.

**Independent Test**: Send crisis phrasings (including keyword-stuffed attempts to bypass)
to `/api/chat` and to a voice tool call; assert `escalated=true`, urgent priority, and no
KB/self-service payload. Red-teamable.

**Acceptance Scenarios**:

1. **Given** a crisis message classified as a benign intent, **When** it is processed by `/api/chat`, **Then** the response is a human escalation with urgent priority (safety override).
2. **Given** a crisis message in a voice tool call, **When** `execute_tool` runs, **Then** the result escalates and the audit entry records the escalation with `input_modality="voice"`.
3. **Given** a message that stuffs benign keywords around a harm signal, **When** processed, **Then** the harm signal still forces escalation.

### User Story 2 - Voice degrades gracefully with no Azure credentials (Priority: P1)

A hackathon participant clones the repo with no Azure config and runs in `mock_mode`. The
app MUST NOT present a broken voice experience: either voice is clearly unavailable, or it
works against a mock path. No blank screens, no unhandled 404s, no console crashes.

**Why this priority**: Every participant runs mock mode first. A voice button that 404s on
connect undermines the demo and the workshop.

**Independent Test**: With `voice_enabled=false`/`mock_mode=true`, call
`POST /api/realtime/session` and assert `503 voice_unavailable`; assert the frontend
hides/disables the mic affordance when `/api/realtime/health` reports unavailable.

**Acceptance Scenarios**:

1. **Given** `voice_enabled` is false, **When** a client calls `POST /api/realtime/session`, **Then** it receives `503` with `{"error": "voice_unavailable"}`.
2. **Given** `/api/realtime/health` reports voice unavailable, **When** the chat UI renders, **Then** the mic button is hidden or disabled with an accessible "voice unavailable" label.

### User Story 3 - Voice session security cannot be subverted (Priority: P2)

An attacker (or a curious participant) cannot weaken the agent's safety prompt via the
session `instructions` field, cannot open concurrent WebSocket connections for one session
through a check/add race, and cannot rely on stale tokens accumulating in server memory.

**Why this priority**: These are correctness/security hardening items. Lower demo
probability than P1 but important for a public, networked deployment.

**Independent Test**: Unit/integration tests for: client `instructions` cannot replace the
fixed safety prompt; two near-simultaneous WS connects for one session yield exactly one
acceptance; expired tokens are pruned from server state.

**Acceptance Scenarios**:

1. **Given** a session request with adversarial `instructions`, **When** the realtime session is created, **Then** the fixed safety prompt is preserved and only allowlisted style hints (if any) are appended.
2. **Given** two concurrent WS connects for the same `session_id`, **When** both race, **Then** exactly one is accepted and the other closes with 4002.
3. **Given** tokens whose TTL has elapsed, **When** new sessions are created, **Then** expired entries are removed from in-memory state.

### User Story 4 - Voice PII redaction covers campus identifiers (Priority: P2)

Voice transcripts and ticket descriptions must not retain student IDs or dates of birth in
addition to the already-covered SSN/card/email/phone.

**Why this priority**: FERPA-adjacent privacy; campus IDs and DOBs are the most likely PII
a student speaks to a college support agent.

**Independent Test**: Feed transcripts containing a student ID and a DOB through
`redact_pii_text`; assert both are redacted before storage.

**Acceptance Scenarios**:

1. **Given** a voice utterance containing a student ID, **When** it is stored, **Then** the ID is redacted.
2. **Given** a voice utterance containing a date of birth, **When** it is stored, **Then** the DOB is redacted.

### Edge Cases

- Voice tool call with a crisis signal **and** a policy keyword → still escalates urgently (override wins).
- `instructions` field absent → fixed safety prompt used unchanged.
- WS connect with valid token but for a different `session_id` → rejected 4001 (already covered; keep regression).
- Expired token reused after pruning → rejected 4001.
- Mock mode with `voice_enabled` forced true via env → session creation still must not 500.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST apply an intent-independent crisis/harm safety override in the live `/api/chat` runtime and in the voice `execute_tool` runtime, forcing human escalation with urgent priority before any self-service/KB content is returned.
- **FR-002**: The crisis override MUST NOT be bypassable by keyword-stuffing or by an adversarial intent classification.
- **FR-003**: `POST /api/realtime/session` MUST return `503 voice_unavailable` when `settings.voice_enabled` is false.
- **FR-004**: The chat UI MUST hide or disable the voice mic affordance (with an accessible label) when `/api/realtime/health` reports voice unavailable, and MUST NOT issue a WebRTC connect that 404s in mock mode.
- **FR-005**: Client-supplied `instructions` MUST NOT replace the fixed voice safety system prompt; only an allowlisted, bounded set of style hints may be appended after it.
- **FR-006**: WebSocket single-session enforcement MUST be free of a check/add race (guard with an async lock or atomic structure).
- **FR-007**: In-memory ephemeral-token state MUST prune expired entries (no unbounded growth); behavior MUST be documented as single-worker for the demo or backed by shared state.
- **FR-008**: `redact_pii_text` MUST redact student IDs and dates of birth in addition to SSN, credit card, email, and phone.
- **FR-009**: All changes MUST preserve existing passing tests and MUST keep `mock_mode` working with no Azure credentials.
- **FR-010**: Existing text-chat behavior and the deployed hackathon-site MUST NOT regress.

### Key Entities

- **Session** (`conversation_history`): shared text+voice store; voice appends `VoiceMessage`.
- **AuditLog** (`input_modality`, `escalated`, `escalation_reason`): records safety overrides.
- **Settings** (`voice_enabled`, `mock_mode`): drive graceful degradation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of a curated crisis red-team set escalates to human with urgent priority via the live `/api/chat` and voice runtimes (0 leaks of KB/self-service content).
- **SC-002**: With no Azure credentials, the app starts and a participant can complete a text conversation and observe a clearly-degraded (non-crashing) voice affordance in under 5 minutes from clone.
- **SC-003**: `POST /api/realtime/session` returns 503 (not 500) when voice is disabled, verified by test.
- **SC-004**: Backend voice + evals + AJCU suites pass (no regressions) and the AJCU red-team suite remains green with the new crisis-override cases added.
- **SC-005**: No unbounded growth of in-memory token state across repeated session creation (verified by test).

## Known Limitations *(documented; out of scope for 007)*

- **Browser voice tool relay (F13/F14).** The intent-independent crisis/PII override is enforced at
  the backend voice tool chokepoint (`execute_tool` in both mock and Azure realtime services) and is
  validated by unit + WebSocket-relay tests. However, the browser WebRTC path negotiates media
  directly with the Realtime endpoint and does not yet relay Realtime function-call events to the
  backend `/api/realtime/ws` relay. Proving the override end-to-end through a real browser voice call
  requires a live Azure OpenAI Realtime deployment (unavailable in this environment). `execute_tool`
  is the correct chokepoint; wiring the data-channel tool relay and validating against a real
  deployment is deferred to a future cycle. **Mitigation:** US2 graceful degradation hides the mic
  in pure mock mode (`/health.realtime_available=false`), so the demo stays text-only and honest.
