# Implementation Plan: AJCU Jesuit Scenario & Hackathon Reference Site

**Branch**: `feat/ajcu-jesuit-scenario` | **Date**: 2026-05-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-ajcu-jesuit-scenario/spec.md`

## Summary

Deliver the AJCU Jesuit reskin of 47 Doors plus a mobile-first static reference
site for the Fordham pre-conference workshop. The agent pipeline (already
reskinned in commit `47a43f6`) classifies student messages into six Jesuit
intents and applies *cura personalis* escalation rules. This plan completes,
commits, deploys, end-to-end tests (Playwright), red-teams, and evaluates the
work. Implementation is carried out by the existing **Matrix SQUAD**.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5 (frontend & site),
Node.js 18+
**Primary Dependencies**: Backend — FastAPI 0.109+, Pydantic v2.5+. Site — Vite 5,
React 18, React Router v6, Tailwind CSS 3. Test — pytest, Vitest, Playwright.
**Storage**: Azure AI Search (KB seed corpus); no DB for the static site
**Testing**: pytest (backend evals + AJCU smoke test), Playwright (site e2e),
Vitest (frontend unit)
**Target Platform**: Linux server (backend), Azure Static Web Apps (site)
**Project Type**: Web application (backend + frontend) plus an auxiliary static
site (`hackathon-site/`)
**Performance Goals**: Static site first-paint < 2s on mobile; classifier eval
runs in < 5s
**Constraints**: Site is pure static (no backend/API/DB); must not modify existing
text-chat or voice functionality
**Scale/Scope**: 6 intents, 6 challenge cards, 6 static routes, ~30 KB seed
articles, workshop cohort scale (tens of concurrent attendees)

## Constitution Check

*GATE: Must pass before implementation. Re-check after design.*

- **I. Bounded Agent Authority** — ✅ Unchanged. QueryAgent classifies only;
  RouterAgent routes only; ActionAgent tickets/retrieves only. The reskin swaps
  the taxonomy and rules, not the boundaries.
- **II. Human Escalation for Policy Decisions** — ✅ Strengthened. *Cura
  personalis* escalation rules add Jesuit-context human-touch keywords
  (discernment, appeal, distress). Campus ministry offers a human rather than
  auto-acting.
- **III. Privacy-First Data Handling** — ✅ Static site stores no PII. Distress
  narratives in tickets follow existing handling. No new PII path.
- **V. Test-First Development** — ✅ Eval pack, Playwright e2e, and red-team suite
  are authored as executable checks; the AJCU smoke test already gates the agent.
- **VI. Accessibility as Requirement** — ⚠️ Site must meet basic a11y (semantic
  landmarks, alt text, keyboard nav). Tracked as a polish task.
- **VII. Graceful Degradation** — ✅ SWA navigation fallback handles deep links;
  classifier degrades to keyword scoring without Azure credentials (mock mode).

No violations requiring Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/004-ajcu-jesuit-scenario/
├── spec.md       # Feature spec (done)
├── plan.md       # This file
└── tasks.md      # Dependency-ordered tasks
```

### Source Code (repository root)

```text
backend/
├── app/agents/
│   ├── intent_classifier.py     # 6 Jesuit intents + negation handling (done)
│   ├── escalation_rules.py      # ESCALATION_RULES + evaluator (done)
│   └── system_prompt.md         # Verbatim classifier prompt (done)
└── tests/
    ├── test_evals.py            # Existing eval suite
    └── test_ajcu/               # NEW: AJCU eval pack + red-team suite

infra/ai-search/seed-articles/   # KB seed corpus, 6 departments (done)

labs/05-agent-orchestration/scenarios/ajcu/
├── challenge-*.md               # Cards A–F (done)
└── smoke_test.py                # 6/6 end-to-end smoke test (done)

frontend/                        # Existing app; dashboard reskinned (done)
└── tests/e2e/                   # Existing Playwright suites (unchanged)

hackathon-site/                  # NEW static reference site (to commit)
├── src/{pages,components,data}/ # Cards A–F, pattern, intents, rules, run-of-show
├── tests/e2e/                   # NEW: Playwright site suite
├── playwright.config.ts         # NEW
└── .github/workflows/deploy-hackathon-swa.yml  # SWA deploy + smoke (to commit)

coach-guide/ajcu-framing.md      # Facilitator framing (done)
```

**Structure Decision**: Web application (backend + frontend) already exists. The
hackathon reference site is an independent static SPA under `hackathon-site/`,
deployed separately to Azure SWA, so it cannot affect the production app.

## Implementation Phases (SQUAD ownership)

- **Phase 1 — Setup**: gitignore + commit the static site, deploy workflow.
  *Switch (FE), Morpheus (review).*
- **Phase 2 — Foundational verification**: confirm the committed agent reskin is
  green (smoke test, backend evals). *Tank (BE), Mouse (QA).*
- **Phase 3 — US1 site e2e** (P1): Playwright config + route/deep-link tests
  against the production build. *Mouse (QA), Switch (FE).*
- **Phase 4 — US2/US3 eval pack** (P1): AJCU eval pack measuring classification +
  escalation correctness across the six challenges and safety cases. *Tank (BE).*
- **Phase 5 — US4 red team** (P2): adversarial/jailbreak suite against classifier
  + escalation; fix criticals or document known limitations. *Neo (Security).*
- **Phase 6 — Deploy**: build `dist/`; deploy to Azure SWA if a token is present,
  else document the gated step. *Switch (FE).*
- **Phase 7 — Polish & report**: a11y pass, docs, squad history + decisions log.
  *Morpheus (review), Scribe (log).*

## Complexity Tracking

No constitution violations; table intentionally empty.
