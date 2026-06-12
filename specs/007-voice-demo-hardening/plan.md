# Implementation Plan: Voice Demo Hardening

**Branch**: `007-voice-demo-hardening` | **Date**: 2026-05-31 | **Spec**: ./spec.md
**Input**: Feature specification from `specs/007-voice-demo-hardening/spec.md`

> **Status (2026-06-01): ✅ COMPLETE & MERGED into `main`** (PR #8, merge commit `281f22d`).
> Verified live in `mock_mode` against the merged `main` — see `tasks.md` Phase 8. The "No changes to
> `main`" constraint below was the *development-time* rule (work stayed on a branch off the baseline);
> the branch was merged only after a full rubber-duck critique, the test/eval/red-team suite, and a
> live crisis-battery grill all passed.

## Summary

Harden the live demo path of the voice feature against the rubber-duck findings: make the
intent-independent crisis-escalation override fire in the **runtime** (`/api/chat` + voice
`execute_tool`), degrade voice gracefully with no Azure creds, lock the safety prompt
against client `instructions`, remove the WS check/add race + prune expired tokens, and
expand PII redaction to student IDs/DOBs. All work is test-first and must keep `mock_mode`
running with zero Azure credentials. No changes to `main`, the baseline backup, or the
deployed hackathon-site.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5 / React 18 (frontend)
**Primary Dependencies**: FastAPI, Pydantic v2, Vitest, Pytest
**Storage**: In-memory session store (mock) via `get_session_store()`; in-memory token/WS dicts in `realtime.py`
**Testing**: `pytest` (backend), `vitest` + `tsc --noEmit` (frontend); AJCU red-team suite `tests/test_ajcu/test_redteam.py`
**Target Platform**: Linux server + browser SPA
**Project Type**: Web application (backend + frontend)
**Performance Goals**: No regression to existing voice P95 < 5000 ms tool round-trip
**Constraints**: MUST run with no Azure credentials (`mock_mode=true`); single-worker demo assumption documented
**Scale/Scope**: Hackathon demo; ~7 source files touched, test-first

## Constitution Check

*GATE: must pass before and after design.*

- **I. Bounded Agent Authority (NON-NEGOTIABLE)**: ✅ Reinforced — the override caps agent autonomy by forcing human escalation on harm signals; no new autonomous authority added.
- **II. Human Escalation for Policy Decisions (NON-NEGOTIABLE)**: ✅ This is the core of US1 — moves the hardened escalation rule into the live runtime so policy/crisis topics reach a human.
- **III. Privacy-First Data Handling (NON-NEGOTIABLE)**: ✅ US4 expands PII redaction; no new PII retention; mock mode keeps secrets out.
- **V. Test-First**: ✅ Every requirement is delivered test-first (failing test before implementation).
- **Result**: PASS — no violations; Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
specs/007-voice-demo-hardening/
├── spec.md        # done
├── plan.md        # this file
└── tasks.md       # next (/speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── api/
│   │   ├── realtime.py        # FR-003 503 kill switch, FR-005 instructions, FR-006 WS lock, FR-007 prune
│   │   └── routes.py          # FR-001 crisis override in /api/chat
│   ├── agents/
│   │   ├── escalation_rules.py    # source of contains_harm_signal/evaluate_escalation (reused)
│   │   └── safety.py              # NEW: thin runtime adapter (apply_safety_override) shared by text+voice
│   ├── services/
│   │   ├── pii.py             # FR-008 student ID + DOB patterns
│   │   ├── azure/realtime.py  # FR-001 voice override in execute_tool, FR-005 prompt build
│   │   └── mock/realtime.py   # FR-001 voice override (mock parity)
│   └── core/config.py         # voice_enabled (read only)
└── tests/test_voice/ + tests/test_ajcu/   # test-first + red team

frontend/
└── src/
    ├── hooks/useVoice.ts          # FR-004 honor health availability; no 404 connect in mock
    └── components/VoiceMicButton.tsx / ChatContainer.tsx   # FR-004 hide/disable + a11y label
```

**Structure Decision**: Web app (existing backend + frontend). A new small
`backend/app/agents/safety.py` adapter wraps the existing `escalation_rules` functions so
both the text route and the voice services share one runtime safety net (DRY, single source
of truth), rather than duplicating override logic in two call sites.

## Phase 0: Research / Decisions

- **D1 — Where to enforce the override**: Apply as a *post-classification, pre-action*
  gate. In `/api/chat`, after `QueryAgent.analyze` and before `RouterAgent`/`ActionAgent`
  return KB content. In voice, inside `execute_tool` for `analyze_and_route_query` /
  `escalate_to_human` before composing the result. Rationale: intent-independent — runs
  regardless of classifier output (FR-002).
- **D2 — Graceful voice degradation**: Backend `/session` returns 503 when
  `voice_enabled` is false (FR-003). Frontend gates the mic button on `/api/realtime/health`
  `realtime_available` and never POSTs SDP when unavailable (FR-004). This resolves the mock
  404 without building a fake WebRTC peer (which cannot produce real audio anyway).
- **D3 — Instructions**: Drop client free-text override of the system prompt. Keep an
  allowlist of style hints (e.g., `concise`, `formal`) appended after the fixed safety
  prompt; ignore anything else (FR-005). Preserves the existing sanitization test intent.
- **D4 — WS race + token prune**: Wrap the active-session check/add in an `asyncio.Lock`
  and prune expired `_TOKEN_SESSIONS` entries on each `/session` create (FR-006, FR-007).
  Document single-worker for the demo.
- **D5 — PII**: Add bounded regexes for campus student IDs (e.g., 6–10 digit or
  letter+digits patterns) and common DOB formats to `redact_pii_text` (FR-008), avoiding
  over-redaction of ticket IDs (which use a `TKT-`/`ESC-` prefix).

## Phase 1: Design

- No new persistent entities. Reuse `Session`, `AuditLog`, `VoiceMessage`, `Settings`.
- New module `safety.py` exposes `apply_safety_override(text) -> SafetyDecision | None`
  built on `contains_harm_signal`; returns escalation metadata (department, urgent, reason).
- Contracts unchanged (no new endpoints); `/session` adds a 503 response shape already
  used for `voice_unavailable`.

## Complexity Tracking

No constitution violations. Table intentionally omitted.
