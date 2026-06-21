# Implementation Plan: Evolution Loop Initiative

**Branch**: `019-evolution-loop` | **Date**: 2026-06-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/019-evolution-loop/spec.md`

## Summary

Generate a spec-driven delivery loop for six additive initiatives that improve demo conversion, Azure/GitHub narrative clarity, and public-sector relevance. Execute in three waves to maximize safe parallelism while preserving architecture guardrails and deterministic test gates.

## Explicit Protections (Hard Stops)

1. **RouterExecutor untouchable**: `app/agents/router_agent.py` remains deterministic and zero-LLM; no randomness or “smart routing” additions.
2. **Bounded authority**: QueryAgent stays classify-only; ActionAgent remains limited to approved tools; no unauthorized capability expansion.
3. **Escalation/PII controls**: safety/PII/sentiment escalation cannot be weakened; no PII echo in logs, acknowledgements, or sitreps.
4. **Mock-mode parity**: every live-facing addition has a deterministic mock path.
5. **Green tests gate**: no merge without mock `pytest` green, `smoke-test.yml` green, and frontend tests green where touched.

## Wave Sequencing

| Wave | Included Specs | Why This Order | Dependency Rule |
|------|----------------|----------------|-----------------|
| **Wave 1** | SPEC-4a/4b/4c/4d, SPEC-3, SPEC-6 | Additive with low collision risk; no shared critical UI surfaces except links/docs | Can run in parallel worktrees |
| **Wave 2** | SPEC-2, SPEC-1 | Both touch ClearBoard/capstone UX and should converge after low-risk additive work | Starts after Wave 1 merge window or isolated worktree coordination |
| **Wave 3** | SPEC-5 | Depends on scenario pack assets and exercises from prior waves | Starts only after SPEC-4 availability is confirmed |

## Phase Plan

### Phase 0 — Governance & Baseline Gate

- Confirm constitution alignment against runbook non-negotiables.
- Freeze RouterExecutor scope (documented as out-of-bounds).
- Record architecture decisions in squad decision inbox.

### Phase 1 — Wave 1 Execution (Parallel Additive)

- Deliver scenario packs (SPEC-4), Responsible-AI map (SPEC-3), and lab-to-production leave-behind (SPEC-6).
- Validate each stream independently in mock mode.
- Merge only after green checks.

### Phase 2 — Wave 2 Execution (UI Surface Coordination)

- Deliver Azure footprint panel (SPEC-2) and capstone lead capture (SPEC-1).
- Use explicit integration checkpoints for shared ClearBoard/capstone files.
- Verify no regression in escalation, PII handling, or dedup behavior.

### Phase 3 — Wave 3 Execution (GitHub Lab Path)

- Deliver `labs/` GitHub-in-the-lab exercise (SPEC-5) with starter failing test and pass criteria.
- Verify exercise does not weaken existing suites or bypass guardrails.

### Phase 4 — Final Verification & Merge Readiness

- Run required quality gates across touched areas.
- Confirm all six spec acceptance criteria are covered by tests or deterministic manual checks.
- Final lead review for scope discipline and guardrail compliance.

## Verification Matrix

- **Backend baseline/regression**: `cd backend && python -m pytest tests/ -q`
- **PR smoke gate**: `smoke-test.yml` must pass
- **Frontend where touched**: `cd frontend && npm test && npm run test:e2e`
- **Spec-specific checks**:
  - SPEC-1 export + persistence test
  - SPEC-2 footprint endpoint payload test
  - SPEC-4 one dedup attach test per pack
  - SPEC-5 starter test fail→pass exercise path
  - SPEC-3/SPEC-6 documentation link integrity checks
