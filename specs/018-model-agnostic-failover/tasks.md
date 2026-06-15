---
description: "Task list for 018-model-agnostic-failover"
---

# Tasks: Model-Agnostic Failover + Availability Narrative

**Input**: Design documents from `specs/018-model-agnostic-failover/`
**Prerequisites**: plan.md (required), spec.md (required)

**Tests**: Included and REQUIRED — Loop Protocol Art. V mandates verifiers first, built by Barton,
never edited by the implementer.

**Organization**: Grouped by user story for independent increments. `[P]` = parallelizable
(different files, no dependency). `[Owner]` = squad member per `.squad/routing.md`.

## Format: `[ID] [P?] [Story] [Owner] Description`

## Path Conventions

Web service: backend at `all-clear/backend/`, narrative at `all-clear/decks/`.

---

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 [T'Challa] Run Design Review ceremony (before): confirm `FailoverChatClient` contract,
      unavailability-detector trigger set, and model-status response shape with Shuri, Rogers,
      Barton. Record interface decisions in `.squad/decisions.md`.
- [ ] T002 [P] [Barton] Create test scaffold `backend/tests/test_failover/__init__.py` and shared
      fakes (a `BaseChatClient` stub that raises a chosen error or returns a chosen
      `ChatResponse`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T003 [Shuri] Add fallback config to `backend/app/core/config.py`:
      `azure_openai_fallback_deployment` (default ""), `azure_openai_fallback_endpoint`
      (default ""), `azure_openai_fallback_api_version` (default "preview"). Empty defaults =
      no-op (FR-005, FR-009).
- [ ] T004 [Rogers] Confirm fallback auth path reuses managed-identity/api-key discipline from the
      primary (no plaintext secrets, no new credential surface) — sign-off note in
      `.squad/decisions.md` (constitution Art. I).

**Checkpoint**: Config exists; implementation of stories can begin.

---

## Phase 3: User Story 1 - Triage survives a model disappearing (P1) 🎯 MVP

**Goal**: The pipeline keeps producing valid, typed results via a fallback when the primary model
is unavailable, with identical safety/escalation behavior.

**Independent Test**: Force the primary stub to raise 404 DeploymentNotFound; assert a valid
`SignalClassification` returns via the fallback and escalation parity holds.

### Verifiers for User Story 1 (write FIRST, must FAIL before impl) ⚠️ [Barton owns]

- [ ] T005 [P] [US1] [Barton] `test_failover_advances_on_unavailable`: primary raises
      404/403/503 → fallback serves; assert fallback response returned.
- [ ] T006 [P] [US1] [Barton] `test_no_failover_on_healthy_primary`: primary returns → fallback
      never called.
- [ ] T007 [P] [US1] [Barton] `test_structured_output_passthrough`: failover with
      `response_format=SignalClassification` returns the typed value (FR-004).
- [ ] T008 [P] [US1] [Barton] `test_no_fallback_is_noop`: no fallback configured → primary error
      propagates unchanged (FR-005).
- [ ] T009 [P] [US1] [Barton] `test_429_and_content_filter_not_failover`: a 429 and a
      content-filter/Prompt-Shield error do NOT advance the chain (FR-003, edge cases).
- [ ] T010 [P] [US1] [Barton] `test_escalation_parity`: a SEV1/statutory signal escalates
      identically whether served by primary or fallback (constitution Art. III, SC-003).
- [ ] T011 [P] [US1] [Barton] `test_chain_exhausted_raises_last_error`: all clients unavailable →
      last error propagates, no infinite loop.

### Implementation for User Story 1 [Shuri owns]

- [ ] T012 [US1] [Shuri] Create `backend/app/services/azure/failover_chat_client.py`:
      `FailoverChatClient(BaseChatClient)` wrapping an ordered `list[BaseChatClient]`; override
      `_inner_get_response` to try each in order, advancing on unavailability, recording
      `last_used_index`/`last_used_model`; preserve `options`/`response_format` passthrough
      (FR-001, FR-002, FR-004).
- [ ] T013 [US1] [Shuri] Implement `_is_model_unavailable(exc)` in the same module using the
      cause/context-chain walk pattern from `app/agents/retry.py`; trigger on
      404/DeploymentNotFound/model_not_found, 403/401/access-denied, 503/service-unavailable;
      exclude 429 and content-filter codes (FR-002, FR-003).
- [ ] T014 [US1] [Shuri] Wire `get_chat_client()` in `backend/app/core/dependencies.py` to build
      `[primary, *fallbacks]` and return `FailoverChatClient` only when a fallback deployment is
      configured; otherwise return the bare primary; mock path unchanged (FR-001, FR-005, FR-008).
- [ ] T015 [US1] [Rogers] Security review of the wrapper: confirms no guardrail bypass, no secret
      leakage across endpoints, escalation/PII untouched (constitution Art. I/II/III, FR-006).

**Checkpoint**: `cd backend; ENVIRONMENT=test MOCK_MODE=true python -m pytest tests/test_failover -q`
green; full mock suite still ~274 passed (SC-001, SC-002, SC-003).

---

## Phase 4: User Story 2 - Operators can see which model is live (P2)

**Goal**: A status surface reports active model, fallback chain, and last-served model.

**Independent Test**: Query the status endpoint in mock mode (no creds); assert active + chain.

### Verifiers for User Story 2 (write FIRST) ⚠️ [Barton owns]

- [ ] T016 [P] [US2] [Barton] `test_model_status_reports_chain`: status surface returns active
      model and ordered fallback list in mock mode (FR-007, SC-004).
- [ ] T017 [P] [US2] [Barton] `test_model_status_reflects_last_served`: after a simulated failover,
      status reports the fallback as last-served.

### Implementation for User Story 2 [Shuri owns]

- [ ] T018 [US2] [Shuri] Add a model-status surface (extend `backend/app/api/health.py` or add
      `GET /api/health/models`) returning `{active, fallback_chain, last_served}`, sourced from the
      configured chain and `FailoverChatClient` state; mock-safe synthetic names (FR-007).
- [ ] T019 [P] [US2] [Stark] (Optional polish) ClearBoard badge showing the active model, driven by
      the status surface. Deferrable; not on the MVP cutline.

**Checkpoint**: status endpoint green in mock mode (SC-004).

---

## Phase 5: User Story 3 - Honest, code-grounded availability narrative (P3)

**Goal**: Evaluation + revised talk track + 2-slide visual, every claim traceable, SLED-tuned,
resilience-and-governance balanced.

**Independent Test**: Each pillar claim maps to a named artifact; model-agnostic section matches
shipped failover behavior.

### Implementation for User Story 3 [T'Challa framing + author]

- [ ] T020 [P] [US3] Write `decks/Model_Availability_Impact.md`: non-political news framing; the
      pillar-by-pillar ground-truth audit (backed vs the now-closed gap); emphasize/soften guidance;
      SLED CJIS/HIPAA/FERPA continuity angle; cite exact files (FR-010, SC-005).
- [ ] T021 [P] [US3] Write `decks/Talk_Track_Foundry.md`: the revised talk track — every claim cites
      a real artifact; the model-agnostic section rewritten to describe the shipped
      `FailoverChatClient` + existing per-task multi-model reality; calm-architect tone and mic-drop
      preserved (FR-010, SC-005).
- [ ] T022 [P] [US3] Write `decks/Model_Agnostic_TwoSlide.md`: Slide 1 executive ("a model can
      vanish overnight — mission-critical triage can't"), Slide 2 technical (failover + per-task
      routing + guardrails + evals). Antimetal tokens (navy hero, light surface, muted-red for the
      old gap, one chartreuse CTA); SLED "Why It Matters" lines (FR-010, SC-005).
- [ ] T023 [US3] [T'Challa] Review narrative against shipped code: 0 unsupported claims (SC-005).

**Checkpoint**: all three artifacts written and claim-checked.

---

## Phase 6: Polish & Verification

- [ ] T024 [Barton] Run full mock suite + new failover suite:
      `cd backend; ENVIRONMENT=test MOCK_MODE=true python -m pytest -q`; confirm baseline + new
      tests (SC-001, SC-002, SC-003, SC-004).
- [ ] T025 [P] [Shuri] `cd backend; ruff check .` clean for changed files.
- [ ] T026 [T'Challa] Final review + scope gate; `.squad/decisions.md` entry; merge.
- [ ] T027 [conditional] Retrospective ceremony if any verifier/build/review failed.

---

## Dependencies & Execution Order

- **Setup (P1)** → **Foundational (P2)** blocks all stories.
- **US1 (P1)** is the MVP and must complete before US2 (status reads US1 state).
- **US2 (P2)** after US1.
- **US3 (P3)** narrative depends on US1/US2 being shipped so claims are true; T020 may draft in
  parallel but T021/T022/T023 finalize only after the failover behavior is merged.
- **Polish (P6)** after desired stories.

### Within each story (Loop Protocol)

- Barton's verifiers written and FAILING before Shuri implements.
- Config before client; client before wiring; wiring before status.
- Implementer never edits verifiers.
- Each task ends at its verification command.

### Parallel Opportunities

- All Barton verifier tasks within a story `[P]` run in parallel.
- US3 doc tasks T020/T021/T022 `[P]` (different files) — draft in parallel, finalize after merge.
- T015 (Rogers review) and T016/T017 (US2 verifiers) can proceed once T012–T014 land.

## Notes

- `[P]` = different files, no dependency. `[Owner]` maps to `.squad/routing.md`.
- Verifiers fail before implementation; commit after each task or logical group.
- MVP cutline = end of Phase 3 (US1). US2/US3 are increments that add value without regressions.
