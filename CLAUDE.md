# 47doors Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-02

## Active Technologies
- TypeScript 5.3, Node.js 18+ + React 18, Vite 5, Tailwind CSS 3.4, @heroicons/react (mirrors `workshop-site/`) (009-coach-prep-site)
- N/A — fully static; content embedded as TS/TSX modules sourced from `coach-guide/*.md` (009-coach-prep-site)
- TypeScript 5, React 18, Node 18+ + Vite 5, Tailwind CSS 3.4, @heroicons/react (013-site-redesign)

- Python 3.11+ (backend), TypeScript 5 (frontend), Node.js 18+ + FastAPI 0.109+, Pydantic v2.5+, React 18, Azure OpenAI, Azure AI Search (001-boot-camp-labs)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11+ (backend), TypeScript 5 (frontend), Node.js 18+: Follow standard conventions

## Recent Changes
- 013-site-redesign: Added TypeScript 5, React 18, Node 18+ + Vite 5, Tailwind CSS 3.4, @heroicons/react
- 007-voice-demo-hardening: Runtime crisis-safety net in live `/api/chat` + voice (intent-independent harm override), voice kill switch (503/4003), token pruning + WS lock, instruction lock, expanded PII redaction. Merged to `main` (PR #8, `281f22d`).
- 009-coach-prep-site: Added TypeScript 5.3, Node.js 18+ + React 18, Vite 5, Tailwind CSS 3.4, @heroicons/react (mirrors `workshop-site/`)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

<!-- MANUAL ADDITIONS START -->
## Voice Feature Build (002-voice-interaction)

### Mission
Implement the voice interaction feature per specs/002-voice-interaction/. Adds real-time voice conversation using Azure OpenAI GPT Realtime API via WebRTC. The existing 3-agent pipeline is exposed as Realtime API function tools.

### Source of Truth
- Spec: specs/002-voice-interaction/spec.md
- Plan: specs/002-voice-interaction/plan.md
- Tasks: specs/002-voice-interaction/tasks.md
- Constitution: .specify/memory/constitution.md

### Execution Rules
1. Follow tasks.md in phase order (Phase 1-8)
2. Write tests BEFORE implementation (Constitution Principle V)
3. After each phase run: cd backend && python -m pytest -x
4. Commit after each phase: feat(voice): Phase N - description
5. Push after each phase commit
6. If tests fail, fix before moving to next phase
7. MVP cutline is Phase 3 — prioritize Phases 1-3
8. Do NOT modify existing text chat functionality
9. For mock mode: ensure voice works without Azure credentials
<!-- MANUAL ADDITIONS END -->

<!-- MANUAL ADDITIONS START -->
## Demo Hardening + Review (007 / 2026-06-01)

### What shipped to `main`
Feature **007-voice-demo-hardening** (PR #8, merge `281f22d`) hardens the live demo path:
- **US1 — Runtime crisis safety net.** `app/agents/safety.py::apply_safety_override` is wired into
  `routes.submit_query` (text) and the voice `execute_tool` chokepoint. Harm detection is
  **intent-independent** and now covers common phrasings ("want to die", "end my life", "hurt myself",
  "overdose", …). `GET /api/knowledge/search` returns zero articles on a harm signal.
- **US2 — Voice kill switch + honest health.** `voice_enabled=false` → `/session` 503, WS close 4003;
  `/api/realtime/health.realtime_available` requires a real Azure Realtime deployment, so pure
  `mock_mode` hides an unusable mic (frontend `useVoice` degrades to text-only).
- **US3 — Session hygiene.** Expired ephemeral tokens pruned; WS guarded by an `asyncio.Lock`;
  instructions anchored to `VOICE_SYSTEM_PROMPT` (client text only appended as escaped hints).
- **US4 — PII redaction.** Context-anchored student-ID + DOB (numeric and month-name) redaction,
  guarded against ticket/escalation-ID false positives.

### Verification convention (proven on the merged `main`)
- Backend: `cd backend && PYTHONPATH=. python -m pytest tests/test_voice/ tests/test_evals.py tests/test_ajcu/ -q` → **285 passed, 2 xfailed**.
- AJCU: `python tests/test_ajcu/eval_report.py` → **6/6**; smoke `PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/ajcu/smoke_test.py` → **6/6**.
- **Live grill** (mock mode, `MOCK_MODE=true uvicorn app.main:app`): pre-007 `main` missed
  "kill myself"/"suicide"/"overdose"; post-merge `main` escalates all crisis phrasings with 0 false
  positives on idioms. See `specs/007-voice-demo-hardening/tasks.md` Phase 8.

### Demo posture
No CI deploys the backend — only the SWA static sites auto-deploy. Run the demo from `main` locally in
**`mock_mode`** (deterministic, zero Azure credentials; safety + routing + PII all fire; voice self-hides).

### `/rubberduck` review dashboard (PR #9, DRAFT — held)
An authenticated, Azure-Portal-styled review page lives at `hackathon-site/src/pages/RubberDuck.tsx`
(route outside the maroon `<Layout>`; SWA built-in auth gates `/rubberduck*` to the `authenticated`
role; GitHub primary, Entra secondary). Kept as a **draft PR** — not merged before the hackathon
because the SWA login is unverified against the live Static Web App.
<!-- MANUAL ADDITIONS END -->
