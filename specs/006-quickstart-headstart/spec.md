# Feature Specification: Cold-Start Quickstart (Labs 01 & 04 Head-Start)

**Branch**: `006-quickstart-headstart` | **Date**: 2026-05-31
**Status**: Draft

## Problem Statement

AJCU hackathon participants arrive **cold** — many have never used GitHub
Codespaces, GitHub Copilot, or Azure AI tooling. The facilitated 7-hour run
sheet (`coach-guide/FACILITATION.md`) compresses Lab 01 (90→30 min) and Lab 04
(120→60 min) to start the AJCU scenarios (Lab 05) at 1:00 PM, but the
`labs/manifest.json` effort estimates total **285 min** for Labs 01–04 versus
only **165 min** of scheduled bench time — a **~2-hour gap**. If teams hit that
gap, they never reach the scenarios that prove the value of this work to the
Jesuits.

The two labs that consume that time — Lab 01 (intent classification) and Lab 04
(RAG index build) — are exactly the "plumbing" that already exists in the repo
as working solutions (`backend/app/agents/`, `infra/ai-search/seed-articles/`,
`labs/04-build-rag-pipeline/setup_index.py`). We want to let cold participants
**get to a scenario-ready state in minutes** so their time is spent on the AJCU
scenarios, not setup.

## Goal

Provide a **tiered quickstart** that brings a cold participant from zero to
"scenario-ready" (Labs 01 & 04 effectively done) with minimal plumbing, without
removing the labs for those who want to learn them.

## Scope Guards (what this feature MUST NOT do)

- MUST NOT modify or delete Labs 01–07 content, `start/`, or `solution/` code —
  the labs remain intact as optional deep-dives / pre-work.
- MUST NOT change the live `/api/chat` behavior, the agents, or the scenario
  taxonomy (`intent_classifier.py`, `escalation_rules.py`).
- MUST NOT change existing CI/CD deploy workflows for the hackathon-site or docs.
- MUST NOT commit secrets; any shared-backend endpoint/keys are distributed
  out-of-band, never in the repo.
- MUST NOT require participants to write code to reach scenario-ready state.
- SHOULD reuse existing assets (`setup_index.py`, `verify_index.py`,
  `seed-articles/`, `scripts/smoke-test.sh`, `azure.yaml` hooks) rather than
  duplicate them.

## User Scenarios (prioritized)

### Story 1 (P1 / MVP) — Self-serve `azd` quickstart auto-seeds Labs 01 & 04

**As** a team that wants its own Azure stack,
**I want** `azd up` to provision **and** automatically build/seed the AI Search
index and verify the pipeline,
**so that** when provisioning finishes the environment is already
"Lab-04-complete" and I can go straight to the scenarios.

**Acceptance**
- A documented single command path provisions infra and then runs the seed +
  verify steps via an `azd` `postprovision` (or `postdeploy`) hook.
- The hook is **idempotent** (safe to re-run) and **non-fatal** to provisioning
  (a seed failure prints actionable guidance, does not roll back infra).
- On success it prints a clear "✅ Scenario-ready" banner with next-step links
  to the Lab 05 scenarios.
- Seeds from the canonical six-intent corpus (`infra/ai-search/seed-articles/`).

### Story 2 (P1 / MVP) — One scriptable "make me scenario-ready" entry point

**As** a participant (or coach prepping a shared backend),
**I want** a single script (`scripts/quickstart.sh`) that, given a configured
`.env`, builds the index, verifies it, and runs the smoke test,
**so that** the same logic works for the shared-backend lane and the self-serve
lane (and is what the `azd` hook calls).

**Acceptance**
- `scripts/quickstart.sh` runs: seed index → verify index → backend smoke check,
  with colored PASS/FAIL output consistent with existing `scripts/*.sh`.
- Idempotent; re-running does not duplicate documents (uses stable `article_id`).
- Detects missing env/credentials and prints exactly what to set, exiting non-zero.
- Has a `--mock` / no-Azure path that validates the mock pipeline so a blocked
  participant can still reach a working scenario lane.

### Story 3 (P2) — Tiered Day-0 pre-work guide for cold participants

**As** a cold participant,
**I want** a short "Day 0" guide covering Codespaces + Copilot + `azd auth login`
and which quickstart lane to use (shared backend / self-serve / mock),
**so that** the cold-start happens before the room and I start the day
scenario-ready.

**Acceptance**
- A concise doc (`docs/quickstart/HEADSTART.md`) describing the three lanes,
  when to use each, and the exact commands.
- Cross-linked from the labs entry points (README) without altering lab content.
- Includes a "you are scenario-ready when…" checklist tied to the verify/smoke
  output.

## Functional Requirements

- **FR-001**: Provide `scripts/quickstart.sh` that seeds + verifies the AI Search
  index and runs the backend smoke check, idempotently, with clear pass/fail.
- **FR-002**: Wire the script into `azure.yaml` `postprovision` so `azd up`
  yields a scenario-ready stack; failures are non-fatal with guidance.
- **FR-003**: Seed from `infra/ai-search/seed-articles/` (canonical six-intent
  corpus); index name and endpoints come from environment, not hardcoded.
- **FR-004**: Provide a `--mock` lane that validates the pipeline with no Azure
  credentials (uses existing mock services).
- **FR-005**: Provide `docs/quickstart/HEADSTART.md` describing the three lanes
  and a "scenario-ready" checklist; link from README without altering labs.
- **FR-006**: All new scripts are POSIX/bash, match existing script conventions,
  and never print or commit secrets.

## Success Criteria (measurable)

- **SC-001**: A cold participant reaches "scenario-ready" (index seeded + verify
  + smoke green, OR mock lane green) in **≤ 15 minutes of hands-on time**
  (excluding unattended `azd` provisioning wait).
- **SC-002**: Re-running the quickstart produces no duplicate index documents
  and the same green result (idempotent).
- **SC-003**: The quickstart works in **mock mode with zero Azure credentials**.
- **SC-004**: No existing lab test, backend test, or deploy workflow regresses.
- **SC-005**: The `azd` hook never causes `azd up` to fail due to a seed error
  (provisioning still succeeds; guidance is printed).

## Out of Scope

- Provisioning the actual shared backend (an operational task the coach runs with
  the documented command); this feature provides the *tooling and docs*, not the
  running Azure resources.
- Changes to lab pedagogy, durations in `manifest.json`, or the facilitation
  schedule (may be addressed separately; this feature is the automation lane).
- The opening presentation deck update (handled separately after this is tested).

## Assumptions

- The existing `setup_index.py` / `verify_index.py` logic is correct and can be
  reused or lightly adapted to read from `infra/ai-search/seed-articles/`.
- Backend mock services (`app/services/mock/`) exist and work offline (used by
  `scripts/smoke-test.sh`).
- `azd up` already provisions OpenAI + AI Search (it does, per `infra/main.bicep`).
