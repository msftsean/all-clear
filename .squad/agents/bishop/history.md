# History

## Project Context

All Clear is a bounded-authority incident-triage accelerator requested by
MARYLAND ADMIN 01.

## Learnings

### 2026-09-20 — Event Readiness Review (facilitated, gate: PASS)

Reviewed the squad's preserved event-readiness work (originally started under
the retired Apollo-cast roster, carried forward without rework) plus new
verifier findings:

- **Event path (Storm/Forge):** `docs/event-readiness/DELIVERY_PLAN.md` locks
  a 390-minute S0-S5 spine with executable completion evidence per stage and
  an explicit optional/cut list. Confirmed against `labs/README.md` and each
  lab's own stated duration/prerequisites.
- **Azure preflight (Kitty):** `docs/event-readiness/AZURE_PREFLIGHT.md`
  covers RBAC, provider registration, quota/capacity, naming, JWT/App
  Insights readiness, shared-backend fallback, and a 20-participant dress
  rehearsal + cleanup checklist. Reviewed independently of the original
  (Haise) author per reviewer-lockout convention.
- **Readiness verifier (Beast):** `scripts/curriculum-readiness.mjs` +
  `npm run curriculum:verify` is the automated gate; its own tests
  (`tests/curriculum/curriculum-readiness.test.mjs`) pass 3/3.
- **Missing exercises (Forge):** Lab 09 bounded `participant_extension/`
  closes the environment-variable-only completion gap; the MCP red-team probe
  (Lab 07) and model-continuity exercise (Lab 05) are deterministic, offline,
  and correctly scoped as optional/take-home.

**Gate outcome:** Reran the verifier after fixing 3 findings (a false-positive
in the env-var completion-gate check, a broken `01c-agent-orchestration.md`
link, and a stale `shared/constitution.md` reference in the surge scenario
README) — now exits 0. Backend `tests/test_failover` (22 passed),
`tests/test_schemas.py`, and `verify_model_continuity.py` all pass. Lab 09
starter + completion tests pass with and without the shortcut env var (the
gate now requires the real extension). **Verdict: GO** — the accelerator is
event-ready for the required S0-S5 spine; Labs 02/06/07/08, voice/phone, and
Exercise 05y remain explicitly optional per the delivery plan.

### 2026-09-20 — T031 Glass-Box Audit Correction Verification

Coordinator corrected exercises/01-glass-box-audit.md (lines 331–335) to accurately state that `AZURE_AI_PROJECT_ENDPOINT` missing causes `glass_box_eval.py` to exit with code 2, not warn/fallback. Verified accuracy against `evals/glass-box-audit/glass_box_eval.py` lines 215–217: script returns 2 on missing env var. Marked T031 done and annotated with verification evidence.
