# Feature Specification: AJCU 3-Hour Workshop Documentation Reframe (Reversible)

**Branch**: `014-agent-framework` (docs-only change) | **Date**: 2026-06-01
**Status**: Active for the AJCU @ Fordham 3-hour pre-conference workshop (1:00–4:00 PM)

## Summary

The repository's participant-facing documentation was written for a **7–8 hour
hackathon with 8 sequential labs**. It is being run as a **single 3-hour
pre-conference workshop** (AJCU at Fordham, 1:00–4:00 PM, 5 teams). Participants
have no time to fight configuration, so the docs are reframed around **one
seamless path**: run `azd up` first (Azure + knowledge base baked by the
`postprovision` hook), then spend the rest of the session building and testing
the six AJCU challenge scenarios.

**Critical requirement (this spec):** the reframe MUST be **reversible**. When the
event reverts to the regular 7-hour hackathon, a maintainer must be able to switch
the documentation back to the 7-hour format quickly and losslessly. The
authoritative switch-back procedure lives in [plan.md](plan.md).

## Goals

- **G1** — A participant's first actionable step is `azd up` (azd-first), not a lab.
- **G2** — The three on-ramp lanes (Self-serve `azd` = default, Shared backend,
  Mock/offline) are visible near the top of the README.
- **G3** — No participant-facing doc tells a reader to complete labs before
  provisioning.
- **G4** — The coach facilitation guide shows a 3-hour (1:00–4:00) timeline with
  no 7-hour language.
- **G5** — **Reversibility:** the 7-hour content is preserved (in git history at a
  recorded baseline + a file-by-file change matrix) so the docs can be switched
  back to the 7-hour format with a documented procedure.

## Non-Goals / Preserve (do NOT touch)

- All application code, `backend/`, `frontend/`, `infra/` bicep, `azure.yaml`,
  `scripts/*`.
- The six AJCU challenge cards
  (`labs/05-agent-orchestration/scenarios/ajcu/challenge-*.md`) — **byte-for-byte
  unchanged**, locked to the keynote deck.
- The six-intent taxonomy (`financial_aid`, `registrar`, `campus_ministry`, `it`,
  `student_wellness`, `general`) wherever it appears.
- Crisis-safety / escalation behavior described in docs (feature 007).
- Correct technical content (CORS notes, version matrix, the 8-lab table, the
  manual Codespaces setup) — **relocated, never deleted**.

## In-Scope Files (documentation only)

| # | File | Reframe |
|---|------|---------|
| 1 | `README.md` | azd-first "Start here" section on top; lanes table; demote manual Codespaces/CORS to an appendix; re-title the 8-lab table as optional take-home deep-dives; update metadata/changelog. |
| 2 | `docs/quickstart/HEADSTART.md` | Mark Self-serve `azd` as the default/recommended lane; state postprovision auto-seed up top. |
| 3 | `labs/00-setup/README.md` | Top callout: "If you ran `azd up`, skip this"; manual 11-step CORS checklist is the fallback only. |
| 4 | `labs/06-deploy-with-azd/README.md` | Top callout: "azd up is step one, not the last lab"; soften the hard "prerequisite: Lab 05". |
| 5 | `coach-guide/FACILITATION.md` | Replace the 7-hour (9:00–4:00) timeline with the 3-hour (1:00–4:00) AJCU run-of-show; voice/phone (+1 913) demo marked OPTIONAL/stretch. |

## Acceptance Criteria

- **AC1** — README's first actionable section is the azd-first Start-here path; the
  manual Codespaces/CORS steps are in an appendix.
- **AC2** — The three lanes are visible near the top, Self-serve `azd` marked default.
- **AC3** — No participant-facing doc tells a reader to complete labs before `azd up`.
- **AC4** — `coach-guide/FACILITATION.md` shows a 3-hour (1:00–4:00) timeline, no
  7-hour language.
- **AC5** — The AJCU challenge cards are byte-for-byte unchanged.
- **AC6** — Scenario smoke test still resolves:
  `cd backend && PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/ajcu/smoke_test.py`.
- **AC7** — **Reversibility:** [plan.md](plan.md) contains a complete, exact
  switch-back procedure (git baseline SHA + file-by-file matrix) verified to
  restore the 7-hour docs.

## The 3-Hour AJCU Run-of-Show (source of truth for timings)

| Time | Block | Lead | Minutes |
|------|-------|------|--------:|
| 1:00–1:08 | Open & frame | Sean | 8 |
| 1:08–1:22 | The pattern — three agents | Sean | 14 |
| 1:22–1:32 | Live demo · Card E | Jake | 10 |
| 1:32–1:40 | Form teams · pick a card | All | 8 |
| 1:40–2:40 | Build sprint 1 | Teams + coaches | 60 |
| 2:40–2:50 | Break | — | 10 |
| 2:50–3:05 | Build sprint 2 · harden | Teams + coaches | 15 |
| 3:05–3:55 | Demos · 5 × 10 min | Teams | 50 |
| 3:55–4:00 | Close | Sean | 5 |
