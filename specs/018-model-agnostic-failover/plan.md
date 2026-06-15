# Implementation Plan: Model-Agnostic Failover + Availability Narrative

**Branch**: `018-model-agnostic-failover` | **Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/018-model-agnostic-failover/spec.md`

## Summary

Make the talk track's headline "model-agnostic / continuity" claim literally true by adding an
automatic chat-model **failover layer** behind the existing MAF chat-client interface, expose a
model-status surface for the stage demo, then align the evaluation, talk track, and a 2-slide
visual to the shipped behavior. Failover is code + config only — a no-op until a fallback model is
configured, so the current single-model path is unchanged and the mock suite stays green.

## Technical Context

**Language/Version**: Python 3.11+ (backend), Markdown deck scripts (narrative)
**Primary Dependencies**: Microsoft Agent Framework 1.8.1 (`agent_framework`, `agent_framework.openai.OpenAIChatClient`, `BaseChatClient`), FastAPI, Pydantic v2, `azure-identity`
**Storage**: N/A for failover (stateless wrapper); last-served model held in-process
**Testing**: pytest (mock mode, `ENVIRONMENT=test`, `MOCK_MODE=true`) — baseline ~274 passed
**Target Platform**: Azure Container Apps (live); local mock mode (deterministic)
**Project Type**: Web service (backend) + presentation artifacts (decks)
**Performance Goals**: Failover adds no latency on the happy path (primary used directly)
**Constraints**: Mock-twin lockstep (constitution Art. V); no credentials in mock; no change to safety/escalation outcomes (Art. I/II/III)
**Scale/Scope**: One new client wrapper, ~3 config fields, one status endpoint, one test module, three deck artifacts

## Constitution Check

*GATE: must pass before and after design.*

- **Art. I (Data Discipline)** — Failover changes only model selection; PII redaction and audit
  logging are upstream/downstream of the chat client and untouched. Rogers reviews that the
  fallback endpoint uses the same managed-identity/api-key discipline and leaks no secrets. ✅
- **Art. II (Bounded Authority)** — The wrapper is a transport concern; it adds no tools and no
  authority. QueryAgent still only classifies; ActionAgent still has exactly three tools. ✅
- **Art. III (Escalation Is a Safety Control)** — Failover MUST be model-independent for
  escalation. A parity verifier proves SEV1/statutory escalation is identical on primary and
  fallback. Content-filter blocks are explicitly **not** routed around. ✅
- **Art. IV (Truth Over Fluency)** — `response_format` passthrough preserved so classification
  stays typed across failover; narrative claims cite real artifacts. ✅
- **Art. V (Build Discipline / Loop Protocol)** — Barton builds verifiers FIRST; the implementer
  (Shuri) never edits them; every task ends at its verification command; mock twin exercises
  failover offline. ✅

**Result: PASS.** No violations; Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
specs/018-model-agnostic-failover/
├── spec.md      # Feature spec (this feature)
├── plan.md      # This file
└── tasks.md     # Squad-assigned, verifier-first task list
```

### Source Code (repository root)

```text
all-clear/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py                     # +fallback model settings (FR-009)
│   │   │   └── dependencies.py               # get_chat_client() wires failover (FR-001/005)
│   │   ├── services/azure/
│   │   │   └── failover_chat_client.py       # NEW: FailoverChatClient(BaseChatClient) (FR-001..006)
│   │   └── api/
│   │       └── health.py (or routes.py)      # +model-status surface (FR-007)
│   └── tests/
│       └── test_failover/                    # NEW: Barton verifiers (US1/US2 parity, no-op)
└── decks/
    ├── Model_Availability_Impact.md          # NEW: evaluation (US3)
    ├── Talk_Track_Foundry.md                 # NEW: revised, code-grounded talk track (US3)
    └── Model_Agnostic_TwoSlide.md            # NEW: 2-slide visual, Antimetal style (US3)
```

**Structure Decision**: Web-service backend (the failover lives in the existing
`app/services/azure/` provider layer behind `get_chat_client()`), plus markdown deck scripts in
`decks/` matching the existing `ISV_Summit_*` convention. No frontend change is required for the
MVP; an optional ClearBoard "active model" badge (Stark) is deferred to US2 polish.

## Squad Increment Model

Work is incremented by the squad per `.squad/routing.md` and the Loop Protocol:

| Phase | Owner | Ceremony |
|-------|-------|----------|
| Design review (interfaces/contracts for the wrapper + status shape) | T'Challa (facilitator), Shuri, Rogers, Barton | Design Review (before) |
| Verifiers first (US1 failover + parity, US2 status, no-op guard) | **Barton** | — |
| Backend implementation (config, FailoverChatClient, wiring, status) | **Shuri** | — |
| Security review (Art. I/II/III parity, secret hygiene, no routing-around-guardrails) | **Rogers** | — |
| Narrative artifacts (evaluation, talk track, 2-slide) | T'Challa (framing) + author | — |
| Code review + scope gate + merge | **T'Challa** | — |
| Retrospective if any verifier/build fails | T'Challa + involved | Retrospective (after) |
| Session log | FRIDAY | automatic |

Loop rule: Shuri (implementer) may not modify Barton's verifiers; if a verifier looks wrong, flag
to T'Challa.

## Design Notes (contracts agreed at Design Review)

- **FailoverChatClient(BaseChatClient)** wraps an ordered `list[BaseChatClient]`. It overrides
  `_inner_get_response` (and streaming if present), calling each inner client in order; on a
  model-unavailability error it advances, else it re-raises. It records `last_used_index` /
  `last_used_model` for the status surface.
- **Unavailability detector** reuses the cause/context-chain walk pattern from
  `app/agents/retry.py::_is_rate_limit`. Triggers: `404`/`DeploymentNotFound`/`model_not_found`,
  `403`/`401`/access-denied, `503`/service-unavailable. **Excludes** 429 (handled by existing
  retry) and content-filter/Prompt-Shield codes (a correct safety block, not an outage).
- **Wiring**: `get_chat_client()` builds `[primary]` + any configured fallbacks; returns the bare
  primary when no fallback is set (FR-005 no-op). Mock mode returns `MockChatClient` unchanged.
- **Status surface**: extend the health router with active model, ordered fallback chain, and
  last-served model; works in mock mode with synthetic model names.

## Complexity Tracking

No constitution violations — section intentionally empty.
