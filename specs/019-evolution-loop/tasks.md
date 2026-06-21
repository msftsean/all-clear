---
description: "Task list for 019-evolution-loop"
---

# Tasks: Evolution Loop Initiative

**Input**: Design documents from `specs/019-evolution-loop/`  
**Prerequisites**: `spec.md`, `plan.md`  
**Tests**: Required. New work must preserve green baseline gates.

## Phase 0: Governance & Safety Gates

- [x] T001 Confirm RouterExecutor boundary is unchanged and mark `app/agents/router_agent.py` out-of-scope in wave plans.
- [x] T002 Confirm bounded authority and escalation/PII hard-stop criteria are explicit in each spec implementation brief.
- [x] T003 Capture architecture decision summary in `.squad/decisions/inbox/tchalla-evolution-loop.md`.
- [x] T004 Verification: run baseline backend suite (`cd backend && python -m pytest tests/ -q`) and record pass/fail status for comparison.

---

## Wave 1 (Parallel): SPEC-4 + SPEC-3 + SPEC-6

### SPEC-4 Maryland scenario packs (4a/4b/4c/4d)

- [x] T101 [P] Define pack metadata + load flags for SOC/Sentinel, 311/911, water utility, and traffic.
- [x] T102 [P] Create seed knowledge/signal assets for each pack.
- [x] T103 Implement pack loader wiring with deterministic mock-mode behavior.
- [x] T104 [P] Add one dedup attach verification test per pack.
- [x] T105 Verification: prove each pack loads independently and shows pin-merge behavior in ClearBoard.

### SPEC-3 Responsible-AI control map

- [x] T111 Create `docs/responsible-ai.md` with policy-control mapping (SB 818 + DoIT concepts).
- [x] T112 Add/update in-app Trust view content for required controls list.
- [x] T113 Verification: confirm all required controls are present and README link resolves.

### SPEC-6 Lab-to-production leave-behind

- [x] T121 Create `docs/lab-to-production.md` with architecture, footprint, RAI controls, and CTA.
- [x] T122 Add links from README and capstone destination entry point.
- [x] T123 Verification: validate links and confirm document is demo/mock compatible.

### Wave 1 Gate

- [x] T130 Run backend/frontend tests relevant to touched files and ensure `smoke-test.yml` is green before merge.

---

## Wave 2: SPEC-2 + SPEC-1 (Shared UI Surfaces)

### SPEC-2 Azure footprint & cost panel

- [x] T201 Implement read-only `/api/health/azure-footprint` payload contract (service list + estimate object).
- [x] T202 Add ClearBoard footprint/cost panel with “estimate” labeling.
- [x] T203 [P] Add tests for service list completeness and estimate payload shape.
- [x] T204 Verification: mock mode renders panel and endpoint returns expected object.

### SPEC-1 Capstone + lead capture

- [x] T211 Add capstone capture flow fields (name, agency, three reflection prompts).
- [x] T212 Implement persistence + CSV/JSON export path for captured records.
- [x] T213 [P] Add tests for capture persistence and export inclusion.
- [x] T214 Verification: end-of-lab flow produces downloadable lead record in mock mode.

### Wave 2 Gate

- [x] T220 Re-run full backend tests, frontend tests, and `smoke-test.yml`; block merge on any regression.

---

## Wave 3: SPEC-5 GitHub-in-the-lab Path

- [x] T301 Author `labs/` workflow steps for fork → Actions run (`smoke-test.yml`) → Copilot extension exercise.
- [x] T302 Add starter failing test for “add tool or add scenario pack” exercise.
- [x] T303 Define pass criteria and facilitator verification notes.
- [x] T304 Verification: starter test demonstrably fails before implementation and passes after exercise completion.

### Final Gate

- [x] T390 Full regression verification: backend mock suite green, `smoke-test.yml` green, frontend tests green where touched.
- [x] T391 Lead review: confirm RouterExecutor untouched, authority boundaries intact, escalation/PII controls unchanged, mock-mode parity maintained.
