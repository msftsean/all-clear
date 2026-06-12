---
description: "Task list for Voice Demo Hardening"
---

# Tasks: Voice Demo Hardening

> ✅ **COMPLETE & MERGED — 2026-06-01.** All T001–T024 done on branch `007-voice-demo-hardening`;
> **merged into `main` via PR #8 (merge commit `281f22d`).**
> Evidence: backend `tests/test_voice/ tests/test_evals.py tests/test_ajcu/` = **285 passed, 2 xfailed**;
> AJCU eval_report **6/6**; AJCU smoke **6/6**; frontend `tsc --noEmit` **0 errors** + vitest **green**;
> ruff clean on changed files (remaining warnings are pre-existing untouched lines).
> Pre-merge it was also re-validated on a throwaway `main + 007` integration tree (same 285/6/6/6 results).
>
> **Post-implementation rubber-duck critique** (agent `impl-critique`) surfaced 6 additional fixes,
> all adopted + tested (see "Phase 7" addendum below). The 7th finding — browser WebRTC→backend
> tool-relay — is the known F13/F14 blocker that genuinely requires live Azure Realtime; documented
> as an open limitation in spec.md, mitigated by US2 graceful degradation (mic hidden in pure mock).

**Input**: Design documents from `specs/007-voice-demo-hardening/`
**Prerequisites**: plan.md ✅ spec.md ✅
**Tests**: REQUIRED — Constitution Principle V (Test-First). Every change lands a failing test first.
**Branch**: `007-voice-demo-hardening` (off `rubberduck/baseline-review-2026-05-31`; main + baseline untouched)

## Format: `[ID] [P?] [Story] Description`
- **[P]**: parallelizable (different files, no dependency)
- All paths are exact.

---

## Phase 1: Foundational (shared safety adapter)

- [x] T001 [US1] Write `backend/tests/test_voice/test_safety_net.py::test_apply_safety_override_on_harm` — assert a new `app.agents.safety.apply_safety_override("I want to kill myself")` returns escalation metadata (escalate=True, priority="urgent", department human escalation, crisis_line set); benign text returns None. MUST fail first.
- [x] T002 [US1] Create `backend/app/agents/safety.py` with `apply_safety_override(message: str) -> dict | None` built on `escalation_rules.contains_harm_signal`. Return **app-native** fields ready for `ChatResponse`/audit: `department=Department.ESCALATE_TO_HUMAN`, `status=ActionStatus.ESCALATED`, `escalation_reason=EscalationReason.SENSITIVE_TOPIC`, `priority=Priority.URGENT`, `crisis_line`/`message` text; return None when no harm signal. (Critique #3/#10 — avoid raw AJCU strings.) Make T001 pass.

---

## Phase 2: US1 — Crisis statements always escalate (P1) 🎯 MVP

- [x] T003 [US1] Write `backend/tests/test_ajcu/test_redteam.py::test_chat_runtime_crisis_override` — POST `/api/chat` with a crisis message classified benign; assert response `escalated=True`, no `knowledge_articles`, status reflects escalation. MUST fail first.
- [x] T004 [US1] Write `backend/tests/test_ajcu/test_redteam.py::test_chat_runtime_keyword_stuffing_bypass` — crisis signal wrapped in benign keywords still escalates. MUST fail first.
- [x] T005 [US1] Inject the safety net into `backend/app/api/routes.py` `submit_query`: after `query_agent.analyze`, if `apply_safety_override(message)` is truthy, short-circuit BEFORE clarification/router/KB — return an escalation `ChatResponse` (escalated=True, urgent, crisis-line message, no KB), append a `ConversationTurn`, and write an `AuditLog` with `escalated=True` + `escalation_reason`. Make T003/T004 pass.
- [x] T006 [US1] Write `backend/tests/test_voice/test_endpoints.py::test_voice_crisis_escalates_with_voice_modality` — voice `execute_tool("analyze_and_route_query", {"query": <crisis>})` escalates urgently and audit entry has `input_modality="voice"`. MUST fail first (if not already covered).
- [x] T006b [US1] Write `backend/tests/test_voice/test_endpoints.py::test_voice_kb_tool_crisis_escalates` — `execute_tool("search_knowledge_base", {"query": <crisis>})` MUST escalate and return NO articles (critique #2 — KB tool must not bypass the override). MUST fail first.
- [x] T007 [US1] Ensure voice override parity in `backend/app/services/azure/realtime.py` and `backend/app/services/mock/realtime.py` `execute_tool`: run `apply_safety_override` on **every** free-text tool arg (`query`/`reason`/`message`) for ALL tools incl. `search_knowledge_base`, BEFORE any KB lookup, so escalation is intent-independent in voice too. Make T006/T006b pass.

---

## Phase 3: US2 — Graceful voice degradation, no Azure creds (P1)

- [x] T008 [US2] Write `backend/tests/test_voice/test_endpoints.py::test_session_returns_503_when_voice_disabled` — explicitly force `VOICE_ENABLED=false` + clear settings/service caches (critique #4: do NOT break the existing mock-mode 200 test, which relies on `voice_enabled` defaulting true), POST `/api/realtime/session` returns 503 `{"error": "voice_unavailable"}`. MUST fail first.
- [x] T009 [US2] In `backend/app/api/realtime.py` `create_realtime_session`, return `503 voice_unavailable` when `get_settings().voice_enabled` is false (before contacting any service). Make T008 pass.
- [x] T010 [P] [US2] Write `frontend/src/hooks/useVoice.test.ts::does not connect when health reports unavailable` — `useVoice` must not POST `/session` / open WebRTC when health `realtime_available=false`; expose an `available` flag. MUST fail first.
- [x] T011 [US2] Update `frontend/src/hooks/useVoice.ts` to read `/api/realtime/health`, expose `available`, and never issue the WebRTC connect when unavailable. Make T010 pass.
- [x] T012 [P] [US2] Write `frontend/src/components/ChatContainer.test.tsx::hides mic when voice unavailable` — mic button hidden/disabled with accessible label when `available=false`. MUST fail first.
- [x] T013 [US2] Gate the mic affordance in `frontend/src/components/ChatContainer.tsx` / `VoiceMicButton.tsx` on `available`; render disabled + `aria-label="Voice unavailable"` when false. Make T012 pass.

---

## Phase 4: US3 — Voice session security hardening (P2)

- [x] T014 [P] [US3] Write `backend/tests/test_voice/test_endpoints.py::test_client_instructions_cannot_replace_safety_prompt` — adversarial `instructions` do not remove the fixed safety prompt. MUST fail first.
- [x] T015 [US3] In `backend/app/api/realtime.py` + `backend/app/services/azure/realtime.py` **and `backend/app/services/mock/realtime.py`** (critique #7 — mock parity), stop letting client `instructions` replace `VOICE_SYSTEM_PROMPT`; append only an allowlist of style hints after the fixed prompt. Make T014 pass.
- [x] T016 [P] [US3] Write `backend/tests/test_voice/test_endpoints.py::test_expired_tokens_are_pruned` — repeated `/session` creation prunes expired `_TOKEN_SESSIONS` entries (no unbounded growth). MUST fail first.
- [x] T017 [US3] Add expiry pruning of `_TOKEN_SESSIONS` and an `asyncio.Lock` around the `_ACTIVE_WS_SESSIONS` check/add in `backend/app/api/realtime.py`. Make T016 pass; keep the existing 4002 single-connection test green.

---

## Phase 5: US4 — PII redaction for campus identifiers (P2)

- [x] T018 [P] [US4] Write `backend/tests/test_voice/test_pii_filter.py::test_redacts_student_id_and_dob` — `redact_pii_text` removes a student ID and a DOB; does NOT redact `TKT-`/`ESC-` ticket IDs. MUST fail first.
- [x] T019 [US4] Extend `backend/app/services/pii.py` `redact_pii_text` with bounded student-ID and DOB patterns (guard against ticket-ID false positives). Make T018 pass.

---

## Phase 6: Eval + Red Team + Verification

- [x] T020 Run backend suites: `cd backend && PYTHONPATH=. python -m pytest tests/test_voice/ tests/test_evals.py tests/test_ajcu/ -q` — all green, no regressions.
- [x] T021 Run AJCU eval report + smoke: `python tests/test_ajcu/eval_report.py` (6/6) and the AJCU smoke test.
- [x] T022 Run frontend: `cd frontend && npx tsc --noEmit && npm test -- --run` — 0 type errors, tests green.
- [x] T023 Ruff: `cd backend && ruff check app/ tests/test_voice/ tests/test_ajcu/` — clean.
- [x] T024 Update `.squad/decisions/decisions.md` with a 007 hardening entry; mark this tasks.md complete with an evidence banner; commit on the review branch.

---

## Dependencies
- T002 blocks T005, T007 (adapter first).
- T005 before T003/T004 pass; T007 before T006 pass; T009 before T008 pass (test-first: write test, then impl).
- Phase 6 runs after Phases 1–5.

## Parallel opportunities
- Frontend (T010–T013) parallel with backend security (T014–T017) and PII (T018–T019) — disjoint files.

---

## Phase 7: Post-implementation rubber-duck critique fixes (adopted 2026-06-01)

An implementation critique (sub-agent `impl-critique`) hardened the crisis safety net further:

- [x] C1 [US1] Expand `escalation_rules.contains_harm_signal` runtime coverage (separate
  `_EXTRA_HARM_KEYWORDS`, verbatim §4 dict untouched): "want to die", "end my life",
  "hurt myself", "cut myself", "overdose", "no reason to live", "better off dead", etc.
  Tested in `test_safety_net.py::TestExpandedCrisisPhrasings` (+ no-overtrigger guard). AJCU evals still 6/6.
- [x] C2 [US1] `GET /api/knowledge/search` now applies `apply_safety_override(q)` and returns
  zero articles on a harm signal (unauthenticated KB can't answer a crisis with self-service).
  Tested in `test_redteam.py::test_knowledge_search_crisis_returns_no_articles`.
- [x] C3 [US2] WS relay `/api/realtime/ws` now honors the kill switch — closes **4003** when
  `voice_enabled` is false. Tested in `TestVoiceKillSwitch::test_ws_rejects_when_voice_disabled`.
- [x] C4 [US1] `voice_crisis_result` recursively scans **all** string args (not just
  query/reason/message). Tested in `TestVoiceCrisisRecursiveScan`.
- [x] C5 [US2] `/api/realtime/health` `realtime_available` now requires a real Azure Realtime
  deployment (not merely `voice_enabled`), so pure mock mode does not advertise a mic that can't
  negotiate WebRTC — the frontend stays text-only and honest.
- [x] C6 [US4] PII patterns extended: "student id number is", letter-prefixed/dashed IDs
  ("A-1234567"), "student no.", and month-name DOB ("March 14, 2001"); ticket-ID non-redaction
  preserved. Tested in `test_pii_filter.py::TestPiiStudentIdAndDob`.

---

## Phase 8: Merge + live-runtime verification (2026-06-01)

The hardening was stress-tested against the **running** app (the `grill-me` skill) and then merged.

- [x] V1 Live grill of `POST /api/chat` in `mock_mode` (no Azure creds), pre-merge `main` vs `007`:
  pre-007 `main` **missed 3 of 7** common crisis phrasings — "I want to kill myself" → normal ticket,
  "thinking about suicide" → `pending_clarification`, "going to overdose" → normal ticket. On `007`
  **all 7 escalate** deterministically (`escalation_reason=sensitive_topic`) with **0/5 false positives**
  on idioms ("this homework is killing me", "dying to know"), and **no raw PII echoed** in the
  escalation response. This empirically reproduces baseline finding **F19** in the live runtime.
- [x] V2 Confirmed both `007` and the `/rubberduck` review branch merge **clean** into `main` (0 conflicts).
- [x] V3 Merged `007` → `main` (PR #8, `281f22d`), then re-ran the identical battery against the
  **merged `main`** in `mock_mode`: all 7 crisis phrasings escalate, all benign pass through. Fix confirmed live.

> **Note:** there is no CI job that deploys the backend (only the SWA static sites auto-deploy), so the
> merge does not auto-ship; the demo runs `main` locally in `mock_mode`. The crisis override, routing,
> and PII redaction all fire offline with zero Azure credentials.
