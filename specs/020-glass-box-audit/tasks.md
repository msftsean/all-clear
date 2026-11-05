# Tasks: Glass-Box AI Audit Workshop Exercise

**Input**: Design documents from `/specs/020-glass-box-audit/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: This feature IS a testing exercise; `scripts/test_evaluator.py`
(User Story 2) is itself the required test suite, run via `unittest`/`pytest`.
No backend/frontend suites are touched, so no additional pipeline tests apply.

## Phase 1: Setup

- [x] T001 Confirm `scripts/` (existing) and create new top-level `exercises/`
      directory for the workshop guide.
- [x] T002 Read and record the four grounding incidents and the cheatsheet's
      4-pillar fix framework from `files/keynote-source-references.md` and
      `files/glass-box-audit-cheatsheet.pdf` (done in research.md).

## Phase 2: Foundational — simulation core (blocks US1 and US2)

- [x] T003 Implement `VendorRecord`, `TraceEvent`, `AuditResult` dataclasses
      in `scripts/audit_simulation.py` per data-model.md.
- [x] T004 Implement deterministic generation of 100 `VendorRecord`s with a
      fixed `BROKEN_RECORD_IDS` set of 5 missing-tax-ID records in
      `scripts/audit_simulation.py`.
- [x] T005 Implement `ReconciliationAgent.run()` producing the full ordered
      `TraceEvent` list (reasoning/scratchpad/api_call/action) with the
      synthetic-data, unauthorized-network, and swarm-coordination flags
      distributed across the 5 broken records, each annotated with its
      grounding-incident `failure_mode_label`, in `scripts/audit_simulation.py`.

**Checkpoint**: `ReconciliationAgent().run()` is importable and returns a
fully deterministic `AuditResult`.

## Phase 3: User Story 1 — Facilitator runs the 120-second live audit (P1) 🎯 MVP

**Goal**: Working `--mode black-box` / `--mode glass-box` CLI over the
foundational simulation.

**Independent Test**: `python scripts/audit_simulation.py --mode black-box`
and `--mode glass-box` both run standalone with no other files present
besides `scripts/audit_simulation.py`.

- [x] T006 [US1] Implement `argparse` CLI with required `--mode
      {black-box,glass-box}` in `scripts/audit_simulation.py`.
- [x] T007 [US1] Implement black-box `main()` path: print only
      `json.dumps(result.black_box_summary)` in `scripts/audit_simulation.py`.
- [x] T008 [US1] Implement glass-box `main()` path: print labeled trace lines,
      the `glass_box_findings` summary, and an explicit contrast against the
      black-box claim in `scripts/audit_simulation.py`.
- [x] T009 [US1] Manually verify determinism: run both modes twice each and
      diff the output (see quickstart.md "Determinism check").

**Checkpoint**: User Story 1 fully functional and independently demoable.

## Phase 4: User Story 2 — Participant writes/inspects a deterministic guardrail (P2)

**Goal**: `scripts/test_evaluator.py` deterministically detects the three
flag types and halts a mocked commit.

**Independent Test**: `python -m unittest scripts/test_evaluator.py -v`
passes with no network access, importing only `scripts/audit_simulation.py`
and the standard library.

- [x] T010 [P] [US2] Implement sibling import-by-file-location
      (`sys.path.insert` on `Path(__file__).resolve().parent`) in
      `scripts/test_evaluator.py`.
- [x] T011 [US2] Implement `GateResult`, `evaluate_trace(trace)`,
      `HaltedWorkflowError`, and `run_guarded_pipeline(trace, commit_fn)` in
      `scripts/test_evaluator.py` (depends on T005 trace shape).
- [x] T012 [US2] Write `test_detects_synthetic_data_generation` asserting the
      exact flagged record-ID set matches `BROKEN_RECORD_IDS`.
- [x] T013 [US2] Write `test_flags_unauthorized_network_attempts` asserting
      the exact flagged record-ID set matches the module's
      `UNAUTHORIZED_NETWORK_RECORD_IDS`.
- [x] T014 [US2] Write `test_flags_emergent_swarm_coordination` asserting the
      exact flagged record-ID set matches `SWARM_COORDINATION_RECORD_IDS`.
- [x] T015 [US2] Write `test_gate_halts_workflow_before_database_commit`
      using `unittest.mock.MagicMock` to prove `commit_fn` is never called
      and `HaltedWorkflowError` is raised on the full (flagged) trace.
- [x] T016 [US2] Write `test_clean_trace_passes_and_commits` (negative
      control) proving a trace with all flags filtered out passes the gate
      and `commit_fn` is called exactly once.
- [x] T017 [US2] Run `python -m unittest scripts/test_evaluator.py -v` and
      confirm all tests pass.

**Checkpoint**: User Stories 1 and 2 both independently functional.

## Phase 5: User Story 3 — Participant reads the workshop guide (P3)

**Goal**: `exercises/01-glass-box-audit.md` documents the live demo,
commands, sourcing, and the "prepare, not scare" All Clear tie-in.

**Independent Test**: Every command in the guide runs successfully; every
file/pattern it references exists in the repository.

- [x] T018 [US3] Write the 120-second run-of-show (timed steps + audience
      voting cues) in `exercises/01-glass-box-audit.md`.
- [x] T019 [US3] Write exact copy-pasteable commands for both CLI modes and
      the evaluator in `exercises/01-glass-box-audit.md` (mirrors
      quickstart.md).
- [x] T020 [US3] Write the four-incident summary table (incident / failure
      mode / Glass-Box fix) sourced from research.md in
      `exercises/01-glass-box-audit.md`.
- [x] T021 [US3] Write the explicit "prepare, not scare" framing section
      naming Microsoft/All Clear's role and citing at least one real existing
      guardrail in this repo (`backend/app/agents/router_agent.py`,
      `backend/app/agents/safety.py`, or `backend/app/services/pii.py`) in
      `exercises/01-glass-box-audit.md`.
- [x] T022 [US3] Write the "extend the guardrail" section explaining how to
      read/extend `scripts/test_evaluator.py` in
      `exercises/01-glass-box-audit.md`.
- [x] T023 [US3] Verify every file path and command referenced in
      `exercises/01-glass-box-audit.md` actually exists/runs.

**Checkpoint**: All three user stories independently functional.

## Phase 6: Polish

- [x] T024 [P] Run the full quickstart.md verification sequence
      (`black-box` + `glass-box` + `unittest`) end to end and confirm exit
      code 0.
- [x] T025 Re-check the Constitution Check gate in plan.md against the final
      files (no backend/frontend/CI files touched).

## Phase 7: Azure Deployment + Evals (User Story 4, optional/additive)

- [ ] T026 [US4] Verify `azd up` deploys the existing `frontend` Container
      App with no Bicep/`azure.yaml` changes, and that
      `https://<AZURE_FRONTEND_URL>/?page=audit` loads the control room with
      no console errors (SC-006). (Live Azure credentials required; not
      attempted here, and no live `azd up` was run.)
- [x] T027 [US4] [P] Create `evals/glass-box-audit/` directory mirroring
      `evals/quality/` layout: `requirements.txt`, `README.md`.
- [x] T028 [US4] Create `evals/glass-box-audit/scenarios.json` with the 5
      `EvalScenario` rows (`clean`, `fabrication_only`, `network_only`,
      `swarm_only`, `all_violations`) per data-model.md.
- [x] T029 [US4] Write `evals/glass-box-audit/glass_box_eval.py`: builds each
      scenario's trace via helpers, imports `evaluate_trace` from
      `scripts/test_evaluator.py` (no reimplementation), asserts each
      scenario's actual verdict matches `expected_passed`/`expected_flags`,
      and uploads results to the Foundry project's Evaluations tab; supports
      `--skip-upload` for a credential-free local dry run.
- [x] T030 [US4] Export `scenarios.json` to
      `.foundry/datasets/glass-box-audit-guardrail-seed-v1.jsonl` and add a
      new `glass-box-audit-guardrail` entry to `.foundry/agent-metadata.yaml`
      `evaluationSuites`, parallel to `quality-smoke`/`safety-redteam`.
- [x] T031 [US4] Add the "Increment 2: Azure deployment + evals" section to
      `exercises/01-glass-box-audit.md` documenting the `azd up` + eval-run
      steps for facilitators who want them. (Verified: the documentation now
      correctly states that a missing `AZURE_AI_PROJECT_ENDPOINT` causes
      `glass_box_eval.py` to exit with code 2; confirmed against lines 215–217
      of the script.)
- [x] T032 [US4] Run `python glass_box_eval.py --skip-upload` locally and
      confirm its 5 verdicts match `python -m unittest
      scripts/test_evaluator.py -v`'s assertions exactly (SC-007 local
      proof, before attempting a live Foundry upload).

**Checkpoint**: User Story 4 independently functional; Increment 1's local
CLI/browser demo is provably unaffected (SC-008) since none of T026–T032
modify `scripts/audit_simulation.py`, `scripts/test_evaluator.py`, or
`frontend/src/allclear/GlassBoxAudit.tsx`.

## Dependencies & Execution Order

- Phase 1 (Setup) → Phase 2 (Foundational, blocks everything) → Phase 3 (US1,
  MVP) → Phase 4 (US2, depends on Phase 2's trace shape) → Phase 5 (US3,
  documents US1+US2, so written last) → Phase 6 (Polish) → Phase 7 (US4,
  fully additive, may run anytime after Phase 4 since it only imports from
  `scripts/test_evaluator.py`).
- T011–T017 (US2) depend on T003–T005 (Foundational) but not on T006–T009
  (US1's CLI layer), so US1 and US2 could be implemented in either order once
  Phase 2 is done; US3 documents both so it is sequenced last for accuracy.
- T026–T032 (US4) depend only on Phase 4 (`scripts/test_evaluator.py`
  existing) and are otherwise independent of Phase 3/US1's CLI and Phase
  5/US3's docs; they do not block or get blocked by Phase 6.

## Notes

- Phases 1–6 operate on exactly 3 files: `scripts/audit_simulation.py`,
  `scripts/test_evaluator.py`, `exercises/01-glass-box-audit.md` — plus the
  browser demo (`frontend/src/allclear/GlassBoxAudit.tsx`,
  `frontend/src/App.tsx`, `frontend/src/index.css`) added in a later
  same-session increment, still with no `backend/` or CI changes.
- Phase 7 (T026–T032) adds `evals/glass-box-audit/` (new directory) and one
  additive entry in `.foundry/agent-metadata.yaml`; still no changes to
  `backend/`, `infra/main.bicep`, `azure.yaml`, or `.github/workflows/`.
- Task checkboxes above are marked complete as each is implemented in this
  same work session; see quickstart.md for the final verification transcript.
  Phase 7 tasks are left unchecked pending implementation.
