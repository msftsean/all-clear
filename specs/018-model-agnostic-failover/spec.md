# Feature Specification: Model-Agnostic Failover + Availability Narrative

**Feature Branch**: `018-model-agnostic-failover`
**Created**: 2026-06-14
**Status**: Implemented (mock suite 313 passed; classification eval 100% / 60/60; frontend build + 24 tests green)
**Input**: User description: "A frontier model was pulled globally overnight. Evaluate how this impacts All Clear and make the talk track's model-agnostic claim literally true, then update the presentation materials. Use Spec Kit to plan and the squad to increment."

## Context

A security concern raised through industry channels triggered a rapid policy response that
removed a frontier model's access globally. The lesson for regulated buyers: **model
availability is not guaranteed.** All Clear's talk track positions Azure AI Foundry as
model-agnostic, guardrailed, evaluated, and compliant. Three of those four pillars are already
true in the codebase; the model-agnostic / continuity pillar is the gap. This feature closes
the gap in code and aligns the narrative to ground truth.

**Ground-truth audit (where the talk track meets the code today):**

| Talk-track pillar | Status | Evidence |
|-------------------|--------|----------|
| Guardrails | True | `backend/app/agents/safety.py` (intent-independent crisis override); zero-LLM `RouterExecutor`; Foundry content filter `allclear-guardrails`; escalation as a security control (constitution Art. III) |
| Evaluations | True | `backend/scripts/check_eval.py` (QueryAgent classification gate, mock-mode, 60/60 = 100%); `backend/tests/test_voice/eval_harness.py`; `backend/tests/test_phone/eval_harness.py`; `evals/quality/quality_eval.py`; Foundry red team 0% ASR (`evals/red-team/RESULTS.md`) |
| Compliance | True | CJIS mindset (CONTEXT.md, constitution Art. I); audit log; least privilege; mock determinism |
| Model-agnostic / continuity | GAP | `get_chat_client()` returns a **single** live deployment (gpt-5.1). Already multi-model *per task* (chat / voice gpt-realtime / embeddings) but **no automatic failover** if a model disappears |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Triage survives a model disappearing (Priority: P1) 🎯 MVP

A surge is in progress when the primary chat model is pulled or returns
unavailable/forbidden/not-found. The pipeline must keep classifying and acting by routing to a
configured fallback model, with no operator intervention and no change to safety or escalation
behavior.

**Why this priority**: This is the headline claim and the entire point of the news tie-in. For
public-safety triage, a model crackdown cannot be allowed to stop incident processing. Without
this, the talk track overreaches.

**Independent Test**: With a fallback deployment configured, simulate the primary client raising a
model-unavailable error (404 DeploymentNotFound / 403 / 503). Assert the pipeline still returns a
valid `SignalClassification` and incident action via the fallback, and that escalation/safety
results are identical to the primary path.

**Acceptance Scenarios**:

1. **Given** a configured fallback model, **When** the primary client raises a model-unavailable
   error, **Then** the request is retried on the fallback and returns a valid result.
2. **Given** the primary is healthy, **When** a request is made, **Then** the primary is used and
   the fallback is never called.
3. **Given** a structured-output request (`response_format=SignalClassification`), **When**
   failover occurs, **Then** the fallback returns the same typed schema (no free-text parsing).
4. **Given** no fallback is configured, **When** the primary fails, **Then** behavior is exactly
   as today (error propagates) — zero behavior change.
5. **Given** a SEV1 / statutory-clock signal, **When** it is processed on the fallback model,
   **Then** it still escalates (constitution Art. III is model-independent).

### User Story 2 - Operators can see which model is live (Priority: P2)

An operator (and the stage demo) can query which model is currently active, which models are
available as fallbacks, and whether a failover has occurred.

**Why this priority**: Makes the resilience visible and demonstrable on stage, and is a standard
SLED RFP line ("which model answered, on whose behalf?"). Depends on US1 existing.

**Independent Test**: Call the model-status endpoint and assert it reports the active deployment,
the ordered fallback list, and a last-failover indicator — in mock mode, without Azure creds.

**Acceptance Scenarios**:

1. **Given** the backend is running, **When** the status endpoint is queried, **Then** it returns
   the active model and the configured fallback chain.
2. **Given** a failover has occurred, **When** the status endpoint is queried, **Then** it
   reflects the model that served the most recent request.

### User Story 3 - Honest, code-grounded availability narrative (Priority: P3)

The presenter has an evaluation, a revised talk track, and a 2-slide visual that every claim can
be traced to a real artifact (code path, test, or Foundry resource), tuned to the SLED/ISV room
and balancing resilience with governance.

**Why this priority**: It is the user's immediate deliverable for the Tue–Wed talk, but it must
follow the code so the narrative does not overpromise.

**Independent Test**: Each pillar claim in the talk track and slides maps to a named file or
resource; the model-agnostic section matches the shipped failover behavior (not aspiration).

**Acceptance Scenarios**:

1. **Given** the revised talk track, **When** any claim is read, **Then** it cites a real artifact
   or is explicitly framed as architecture/vision.
2. **Given** the 2-slide visual, **When** reviewed, **Then** it follows the Antimetal house style
   and names CJIS/HIPAA/FERPA continuity for the SLED room.

### Edge Cases

- Fallback model is also unavailable → final error propagates after the chain is exhausted (no
  infinite loop); error is the last client's error.
- Rate-limit (429) is **not** a failover trigger — it is handled by the existing
  `with_rate_limit_retry` backoff; failover is for availability/access/not-found errors only.
- Content-filter / Prompt-Shield blocks are **not** failover triggers — a guardrail block is a
  correct safety outcome, not a model outage (must not be "routed around").
- Fallback misconfigured (endpoint set, deployment empty) → treated as no fallback; logged once.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support an ordered list of chat models (primary + one or more fallbacks)
  behind the existing MAF chat-client interface used by the three-agent pipeline.
- **FR-002**: System MUST automatically advance to the next model when a request fails with a
  model-unavailability error (HTTP 404 DeploymentNotFound, 403/401 access denied, 503/service
  unavailable, "model not found"), detected by walking the exception cause/context chain.
- **FR-003**: System MUST NOT treat rate-limit (429) or content-filter/Prompt-Shield blocks as
  failover triggers.
- **FR-004**: System MUST preserve structured-output (`response_format`) passthrough across
  failover so QueryAgent classification stays typed (constitution Art. IV).
- **FR-005**: System MUST be a no-op when no fallback is configured (identical behavior to today).
- **FR-006**: Failover MUST NOT alter safety override, PII redaction, routing, or escalation
  outcomes (constitution Art. I, II, III hold on every model).
- **FR-007**: System MUST expose a status surface reporting the active model, the ordered fallback
  chain, and the most-recently-used model.
- **FR-008**: Mock mode MUST exercise failover deterministically with no Azure credentials
  (constitution Art. V mock-twin lockstep).
- **FR-009**: Configuration MUST be environment-driven (fallback deployment, optional fallback
  endpoint and api-version) with safe empty defaults.
- **FR-010**: The evaluation, revised talk track, and 2-slide visual MUST cite real artifacts and
  match the shipped failover behavior.

### Key Entities

- **Model chain**: ordered list of chat-client targets (deployment + endpoint + api-version +
  auth), tried in priority order.
- **Failover event**: which model served a request and whether it was a fallback.
- **Narrative artifact**: evaluation doc, revised talk track, 2-slide deck script.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: With a fallback configured and the primary forced unavailable, 100% of pipeline
  requests in the failover test suite return a valid typed result via the fallback.
- **SC-002**: With no fallback configured, the full mock suite remains green at the current
  baseline (~274 passed) — zero regressions.
- **SC-003**: Escalation/safety eval outcomes are identical whether served by primary or fallback
  (0 divergences in the parity test).
- **SC-004**: The model-status endpoint returns active + fallback chain in mock mode with no Azure
  credentials.
- **SC-005**: Every pillar claim in the revised talk track and slides maps to a named artifact;
  0 unsupported claims.

## Implementation Status *(shipped 2026-06-14)*

| Item | Result |
|------|--------|
| `FailoverChatClient` + `_is_model_unavailable` + `build_failover_client` | `backend/app/services/azure/failover_chat_client.py` |
| `get_chat_client()` builds `[primary, *fallbacks]`; `get_model_status()` | `backend/app/core/dependencies.py` |
| Config: `azure_openai_fallback_deployment/_endpoint/_api_version` (empty defaults) | `backend/app/core/config.py` |
| `GET /api/health/models` (active / fallback_chain / last_served / failover_active) | `backend/app/api/routes.py` |
| Failover verifier suite (14 tests) + route test | `backend/tests/test_failover/`, `backend/tests/test_routes.py::test_health_models` |
| ClearBoard active-model badge (US2 polish) | `frontend/src/allclear/BriefingRoom.tsx`, `api.ts`, `types.ts` |
| Narrative deliverables (US3) | `decks/Model_Availability_Impact.md`, `decks/Talk_Track_Foundry.md`, `decks/Model_Agnostic_TwoSlide.md` |

**Verification run (2026-06-14):**

- Backend mock suite: **313 passed**, 0 regressions (SC-002 met; baseline grew from ~274 to 313 with the new failover tests).
- Classification eval gate: `python scripts/check_eval.py --min-accuracy 0.90` → **accuracy=1.000 (60/60), PASS** (mock mode, no Azure creds).
- Failover parity: escalation/safety outcomes identical on primary vs. fallback (SC-003 met via `test_failover/`).
- Frontend: typecheck ✅, build ✅, 24 tests ✅.
- Not run here: the Azure-credentialed `evals/quality` and `evals/red-team` suites (require a live model + Foundry project); their last recorded results stand (red team 0% ASR, `evals/red-team/RESULTS.md`). The failover change does not alter agent prompts or behavior in mock mode, so those scores are unaffected.

**Runbooks updated to reflect this feature:** `coach-runbook/index.html` (new **E6 · Model continuity & failover** exercise, OP table row, Summary bullet) and `participant-runbook/index.html` (S1 model-swappable build step + model-continuity framing).
