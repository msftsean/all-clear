# Decisions Log

**Last Updated:** 2026-05-31T15:10Z

## Active Decisions

### 002 Voice Interaction — Phases 4–8 Completion (Escalation, Hybrid, A11y, Polish) — 2026-05-31

**Author:** Scribe (SQUAD voice squad: backend / frontend / docs sub-agents)
**Status:** Implemented & Verified
**Branch:** feat/ajcu-jesuit-scenario

Closed out the remaining 26 tasks in `specs/002-voice-interaction/tasks.md` (now 75/75).
Phases 4–8, previously deferred, are complete:

- **US2 Escalation (T034–T040):** Voice escalation tests; richer `escalate_to_human`
  tool description (Azure + mock services); voice tool calls now write audit entries
  tagged `input_modality="voice"`; frontend "Connecting you to a support agent…" status.
- **US3 Hybrid (T041–T046):** `POST /session` and the WS relay read/write the shared
  text session store; successful voice tool calls append a PII-filtered `VoiceMessage`
  (`input_modality="voice"`) to `conversation_history`; transcript badges + unified thread.
- **US4 Accessibility (T047–T052):** keyboard/ARIA on `VoiceMicButton`, `aria-live`
  status region, focus return to text input on voice end; a11y tests added.
- **US5/Polish (T069–T075):** 3-layer PII tests + `app/services/pii.py` redaction helper;
  P95 latency assertion in `eval_harness.py`; WS single-session enforcement (close 4002),
  ephemeral-token↔session binding (close 4001), ≤60s TTL cap, instruction sanitization;
  `docs/voice-api.md` + `frontend/README.md` voice section.

**Spec drift adapted:** tasks.md referenced a nonexistent `app/api/chat.py`. Text chat
actually lives at `POST /api/chat` in `backend/app/api/routes.py` over the shared
`get_session_store()`; the shared-session test (T041) was written against the real route.

**Verification:** `tests/test_voice/` 88 passed; `tests/test_voice/ tests/test_evals.py
tests/test_ajcu/` 242 passed / 2 xfailed; ruff clean; frontend `tsc --noEmit` 0 errors,
vitest 18 passed / 11 todo. mock_mode works with no Azure credentials. No changes to
existing text-chat behavior or to CI/deploy/hackathon-site.

### 004 AJCU Scenario — Task Completion Verification + Mobile e2e Fix — 2026-05-31

**Author:** Scribe (verification driven by Switch/Tank/Mouse/Neo)
**Status:** Implemented & Verified
**Branch:** feat/ajcu-jesuit-scenario

Closed out `specs/004-ajcu-jesuit-scenario/tasks.md` (all 30 tasks). Ran the full
verification matrix and marked every task done: AJCU smoke 6/6; `tests/test_evals.py`
+ `tests/test_ajcu/` 155 passed / 2 xfailed; `eval_report.py` 6/6; hackathon-site
typecheck + build clean; site live (HTTP 200).

**One real gap fixed:** the full Playwright run (chromium **+ mobile** projects)
surfaced a failure in `hackathon-site/tests/e2e/coverage.spec.ts` — the `/intents`
coverage check used `getByText(key).first()`, which resolves to the desktop table
cell (`hidden sm:block`, first in DOM) and is `display:none` on the mobile (Pixel 5)
project, so `toBeVisible()` failed. The product is correct (mobile cards render all
six intent keys); the test was not viewport-robust. Fixed by filtering to the visible
occurrence: `getByText(key, { exact: false }).filter({ visible: true }).first()`.
Result: e2e now **43 passed / 5 skipped** on both projects. Prior "17/17" green was
chromium-only and never exercised the mobile project.

**Files Changed:** `hackathon-site/tests/e2e/coverage.spec.ts`,
`specs/004-ajcu-jesuit-scenario/tasks.md`.

**Impact:** Test-only + spec bookkeeping. No product/runtime change; no impact to
text-chat or voice pipelines.

---

### WebSocket Bridge for ACS→Azure OpenAI Audio Relay — 2026-04-09

**Author:** Tank  
**Status:** Implemented & Deployed  
**Commit:** b2d7abc

Phone calls to +19132171946 connected (call answered) but produced dead air — no audio in either direction. ACS media streaming was configured to connect directly to Azure OpenAI Realtime API's WebSocket, but ACS had no managed identity to authenticate with and Azure OpenAI only accepted Entra ID auth. Additionally, CloudEvents callback parsing rejected all events, hiding `MediaStreamingFailed` diagnostics.

**Decision:** Route ACS media streaming through a backend WebSocket bridge (`/ws/acs-media`) instead of connecting ACS directly to Azure OpenAI. The backend authenticates to Azure OpenAI using its existing managed identity.

```
PSTN → ACS → WS [backend /ws/acs-media] → WS [Azure OpenAI Realtime API]
```

**Files Changed:** `backend/app/api/media_ws.py` (new, 296 lines), `backend/app/services/azure/phone.py` (transport_url), `backend/app/api/phone.py` (CloudEvents parsing), `backend/app/main.py` (route registration)

**Impact:** Audio now flows bidirectionally on answered PSTN calls. All 447 tests pass. No infra changes required.

---

### Fix ACS CallbackUri for Container Apps — 2026-04-09

**Author:** Tank  
**Status:** Implemented & deployed  
**Commit:** 365271d

Inbound phone calls failed with "CallbackUri invalid" (400) because Container Apps TLS termination caused `request.base_url` to resolve to `http://` (internal address). ACS requires HTTPS public URLs.

**Decision:** Reconstruct callback URL from `X-Forwarded-Proto` + `Host` request headers (set by Container Apps ingress), with `PHONE_CALLBACK_BASE_URL` config setting as explicit override.

**Files Changed:** `backend/app/api/phone.py`, `backend/app/services/azure/phone.py`, container env

**Impact:** Phone calls now answer correctly. Future services needing public callbacks should follow the same pattern.

---

### Playwright Eval Suite — Deployment Quality Gate — 2026-04-09

**Author:** Mouse  
**Status:** Implemented  
**Files Created:** `frontend/tests/e2e/eval.spec.ts`

Made `playwright.config.ts` environment-portable: `BASE_URL` env var overrides `baseURL`, `webServer` block skipped when targeting live deployment.

**Decision:** Created 24-test eval suite covering homepage, backend health, chat, KB quality, sessions, error handling, voice UI, performance. KB quality assertions are hard failures (demo quality gate, not smoke test). Health endpoint threshold set to 10s (Azure Container Apps cold-start).

**Key Findings:** 2 KB quality failures are real demo risks:
1. Registration queries trigger clarification loop instead of answering
2. Financial aid queries misroute to IT Support instead of Financial Aid

**Impact:** Eval can be run against any environment. Existing tests need refactor to use `BACKEND_URL` env var. WCAG violations in accessibility tests are real and need fixing.

---

### Dedicated Nginx Location Block for SSE Streaming — 2026-04-09

**Author:** Tank  
**Status:** Implemented & Deployed  
**Commits:** db2d48c, dd66ad6  

Live transcript page (`/live`) connected successfully but displayed no transcript text. SSE events from `/api/phone/transcripts/stream` were silently buffered by nginx because the single `/api/` location block was configured with WebSocket semantics (`Connection "upgrade"`, no `proxy_buffering off`).

**Decision:** Added dedicated `location /api/transcripts/stream` block in `frontend/nginx.conf` with SSE-specific proxy settings:
- `proxy_buffering off` + `proxy_cache off` — disables nginx response buffering
- `proxy_set_header Connection ""` — uses HTTP keep-alive instead of WebSocket upgrade
- `proxy_read_timeout 86400` — allows long-lived SSE connections (24h)

The existing `/api/` block remains unchanged for regular REST calls and WebSocket (`/api/realtime/ws/`).

**Rationale:** SSE and WebSocket have fundamentally different proxy requirements:
- WebSocket: needs `Connection "upgrade"` + `Upgrade` header
- SSE: needs `Connection ""` (keep-alive) + `proxy_buffering off`

Nginx longest-prefix matching ensures `/api/transcripts/stream` matches before falling through to general `/api/` block.

**Files Changed:** `frontend/nginx.conf` — added SSE location block before existing `/api/` block

**Impact:** Live transcript viewer now functional. Change is additive. Existing `/api/` block untouched, so WebSocket and REST traffic unaffected. If additional SSE endpoints added, they should nest under `/api/transcripts/` (already covered by prefix match) or get own location block.

---

### Intent-Independent Safety Override for AJCU Scenario — 2026-05-31

**Author:** Neo (red team) / Morpheus (review gate)
**Status:** Implemented
**Commits:** 2b61d1f
**Branch:** feat/ajcu-jesuit-scenario

Red teaming the AJCU 6-intent classifier + escalation rules surfaced a CRITICAL bypass (F1): the crisis SAFETY OVERRIDE lived *inside* the `student_wellness` branch of `evaluate_escalation`. An adversary could keyword-stuff a self-harm message (e.g. "my laptop crashed, I want to kill myself") so the classifier picked `it`/`financial_aid`, and the urgent crisis path (988 line, chaplain offer, urgent ticket) was silently skipped.

**Decision:** Make harm detection intent-independent. `evaluate_escalation` now runs `contains_harm_signal(message)` FIRST and, on any hit, coerces the path to `student_wellness` with `safety_override=True` (preserving `original_intent`) before applying intent rules. Per scenario §2.2, safety always wins over intent classification.

**Hardening details:**
- `contains_harm_signal()` strips whitespace (`_despace`) to defeat spacing evasion ("kill my self") — F2.
- Combined phishing+harm vectors keep BOTH `student_wellness` and `security` tickets — F3.
- Leetspeak/homoglyph ("k1ll") still evades the keyword net — documented as strict-xfail (F4) with the recommendation to use an LLM classifier as the primary safety detector in production.

**Files Changed:** `backend/app/agents/escalation_rules.py` (safety-net logic), `backend/tests/test_ajcu/test_redteam.py` (17 probes), `REDTEAM_FINDINGS.md`.

**Impact:** Additive and defensive. No change to text-chat or voice pipelines. Backend suite 155 passed / 2 xfailed; AJCU smoke 6/6; site e2e 17/17.

---

### Docs/Code/Specs Accuracy Reconciliation — 2026-05-31

**Author:** Morpheus (lead) — squad audit (Tank, Switch, Neo, Mouse)
**Status:** Implemented
**Branch:** feat/ajcu-jesuit-scenario

A four-agent accuracy audit was run to ensure all docs, code, and specs match what
was actually built (the `gpt-4o → gpt-4.1` / `gpt-4o-realtime-preview → gpt-realtime`
sweeps plus any other drift).

**Genuine drift found and fixed:**
- `labs/06-deploy-with-azd/infra/main.bicep` — text model default `gpt-4o → gpt-4.1`, model version `2024-05-13 → 2025-04-14`.
- `labs/06-deploy-with-azd/infra/main.parameters.json` — model version `2024-05-13 → 2025-04-14` (model was already `gpt-4.1`).
- `specs/002-voice-interaction/tasks.md` — realtime voice `alloy → marin` (matches `config.py` default).
- `specs/002-voice-interaction/DEMO_RUNBOOK.md` — GPT-4.1 model version `2024-05-13 → 2025-04-14`.
- `labs/00-setup/.env.template`, `labs/02-azure-mcp-setup/start/.env.template`, `labs/02-azure-mcp-setup/start/mcp-config.json.template` — api-version `2024-02-15-preview → 2025-04-01-preview`.

**Deliberately NOT changed (verified correct / preserved on purpose):**
- `docs/index.html` "Before 47 Doors" door legend (IT/FinAid/Housing/…) — this is the narrative *problem* illustration (the many-doors status quo the app solves), NOT the app's intent taxonomy. Accurate as-is.
- `gpt-4o-mini` (cost-comparison tables) and `gpt-4o-audio-preview` (optional audio fallback) — distinct real models, preserved.
- Historical point-in-time test-count claims in `specs/002-voice-interaction/` (e.g. "97 tests", "76 tests pass") — left as dated records.

**Architectural honesty note (the one real structural finding):**
The AJCU 6-intent classifier (`backend/app/agents/intent_classifier.py`) and the
intent-independent escalation safety net (`backend/app/agents/escalation_rules.py`)
are a **scenario layer** used by the AJCU smoke test, eval pack, and red-team suite
(`backend/tests/test_ajcu/`, `labs/05-agent-orchestration/scenarios/ajcu/`). They are
**not wired into the live `/api/chat` 3-agent pipeline**, which intentionally retains
the generic product taxonomy (`IntentCategory` in `enums.py`, driven by `QueryAgent` /
`RouterAgent`). This is **by design** — the standing constraint is "do not modify
existing text-chat / voice functionality." Migrating the live pipeline to the 6 Jesuit
intents is a separate, larger change deferred to a future spec-kit cycle (it would touch
schemas, mock data, and the full test suite) and was not undertaken overnight.

**Impact:** Documentation/label-accuracy only. No change to live text-chat or voice runtime behavior.

---

## 2026-06-01 — 007 Voice Demo Hardening (rubber-duck-driven; review branch only)

**Branch:** `007-voice-demo-hardening` (off `rubberduck/baseline-review-2026-05-31`, off `c8088ef`).
`main` + `backup/main-2026-05-31-hackathon-baseline` + tag `baseline-2026-05-31-hackathon` kept pristine.

**Why:** An experimental rubber-duck review of the hackathon baseline surfaced a real 500 and a set
of demo-risk safety gaps. This branch fixes them through a spec-kit workflow (spec/plan/tasks +
plan critique + implementation critique) WITHOUT touching live text-chat or voice contracts.

**What changed (all tested, intent-INDEPENDENT crisis safety is the throughline):**
- NEW `backend/app/agents/safety.py` — single runtime safety net for text + voice.
  `apply_safety_override` (app-native enums) + `voice_crisis_result` (recursive arg scan, articles:[]).
- `routes.py::submit_query` — crisis short-circuit AFTER analyze, BEFORE clarification/router/KB.
- `routes.py::search_knowledge` — crisis query returns 0 articles (unauthenticated KB can't answer a crisis).
- `services/{mock,azure}/realtime.py::execute_tool` — crisis override at top, covers ALL tools incl. KB.
- `escalation_rules.py` — expanded runtime harm-phrase coverage via `_EXTRA_HARM_KEYWORDS`
  (verbatim §4 dict untouched); catches "want to die / end my life / hurt myself / overdose / …".
- `api/realtime.py` — (1) 503 voice kill switch on `/session` AND 4003 on `/ws` when `voice_enabled` false;
  (2) instruction LOCK — client text can never replace `VOICE_SYSTEM_PROMPT`, only appended as hints;
  (3) `_prune_expired_tokens()` + `asyncio.Lock` around `_ACTIVE_WS_SESSIONS` check/add;
  (4) `/health.realtime_available` now requires a real Azure Realtime deployment (honest mic gating).
- `services/pii.py` — context-anchored student-ID + DOB redaction (no ticket-ID false positives).
- Frontend (graceful degradation) — `useVoice` probes `/health`, exposes `available`; mic hidden/disabled
  with `aria-label="Voice unavailable"` when voice can't actually negotiate WebRTC.

**Evidence:** backend `tests/test_voice/ tests/test_evals.py tests/test_ajcu/` = 285 passed, 2 xfailed;
AJCU eval_report 6/6; AJCU smoke 6/6; frontend tsc 0 errors + vitest green; ruff clean on changed files.
(`tests/test_gpt4o_evals.py` 97 errors are PRE-EXISTING live-Azure auth failures — no creds here.)

**Known open limitation (documented, NOT fixed — needs live Azure):** browser WebRTC does not yet relay
Realtime function-calls to the backend `execute_tool` chokepoint, so the voice crisis/PII override is
proven only at the backend tool layer (unit/WS tests), not end-to-end through a real browser voice call.
`execute_tool` is the correct chokepoint; wiring the data-channel tool relay + validating against a real
Realtime deployment is deferred to a future cycle. Mitigation: US2 hides the mic in pure mock mode.

**Status:** review branch only — NOT merged to main. A separate `main` rubber-duck pass + merge-decision
report follow so the maintainer can choose whether to adopt 007.
