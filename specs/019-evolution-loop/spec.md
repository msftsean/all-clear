# Feature Specification: Evolution Loop Initiative

**Feature Branch**: `019-evolution-loop`  
**Created**: 2026-06-20  
**Status**: Draft  
**Input**: AllClear-Evolution-Loop-Runbook.md

## Scope and Non-Negotiables

This spec pack defines six additive product/documentation slices to support the June 23–24 Azure Days for Government narrative and pipeline. The loop must preserve:

- RouterExecutor determinism and zero-LLM behavior.
- Bounded authority across QueryAgent, RouterExecutor, and ActionAgent.
- Escalation and PII controls as release blockers.
- Mock-mode parity for every new live-facing capability.
- Green-gate verification (`pytest` in mock mode, `smoke-test.yml`, frontend tests).

## SPEC-1 — "Make It Yours" Capstone + Lead Capture

**Problem**: The lab ends without a structured call to action or consistent lead capture.  
**In scope**: Final capstone step and short form capturing attendee-provided details (name, agency, surge prompt answers), downloadable export (CSV/JSON).  
**Out of scope**: CRM integration and any non-volunteered attendee data.

### Actionable Requirements

- **S1-FR-001**: The experience MUST include a terminal capstone step that asks for name, agency, and three reflection prompts from the runbook.
- **S1-FR-002**: The system MUST persist each submitted capstone entry to the same project data layer used for mock-mode testing.
- **S1-FR-003**: Users MUST be able to download captured entries in CSV and JSON formats.
- **S1-FR-004**: Capstone capture MUST work in mock mode with no Azure credentials.

### Acceptance Criteria

- **S1-AC-001**: Completing the lab yields a successful capstone submission and export action.
- **S1-AC-002**: A test verifies capture persistence and inclusion of the new record in both exports.
- **S1-AC-003**: Mock-mode execution demonstrates the same behavior without live cloud dependencies.

## SPEC-2 — Azure Footprint & Cost Panel

**Problem**: The Azure consumption/revenue footprint is not visible to attendees.  
**In scope**: ClearBoard panel plus read-only `/api/health/azure-footprint` endpoint showing service inventory and rough estimate object from config table.  
**Out of scope**: Live billing APIs and fabricated pricing.

### Actionable Requirements

- **S2-FR-001**: The endpoint MUST return the full runbook service inventory (OpenAI, Embeddings, AI Search, Container Apps, Cosmos DB, ACS, Key Vault, ACR, Foundry, APIM, Monitor).
- **S2-FR-002**: The endpoint MUST include an estimate object sourced from maintained configuration values.
- **S2-FR-003**: The UI panel MUST clearly label all cost values as estimates.
- **S2-FR-004**: The panel and endpoint MUST render and respond in mock mode.

### Acceptance Criteria

- **S2-AC-001**: Automated tests verify service list completeness and estimate object presence.
- **S2-AC-002**: UI checks confirm estimate labeling and successful rendering in mock mode.
- **S2-AC-003**: No live billing dependency is required for pass.

## SPEC-3 — Responsible-AI Control Map

**Problem**: Existing guardrails are not visibly mapped to Maryland policy references.  
**In scope**: `docs/responsible-ai.md` plus in-app Trust view mapping controls to policy concepts (SB 818, DoIT Responsible Use Policy).  
**Out of scope**: Behavioral changes to the runtime pipeline.

### Actionable Requirements

- **S3-FR-001**: A policy map document MUST enumerate each existing control and associated policy concept.
- **S3-FR-002**: The Trust view MUST list the mapped controls: bounded authority, deterministic router, escalation-as-control, no-PII-echo, audit logging, Foundry red-team/evals, model failover.
- **S3-FR-003**: README MUST link to the Responsible-AI map.
- **S3-FR-004**: Delivery MUST remain documentation/UI-only with no pipeline logic change.

### Acceptance Criteria

- **S3-AC-001**: `docs/responsible-ai.md` exists and is linked from README.
- **S3-AC-002**: Trust view displays all required controls and policy mappings.
- **S3-AC-003**: Change review confirms no runtime code-path modification.

## SPEC-4 — Maryland Scenario Packs (4a–4d)

**Problem**: Generic scenarios reduce audience relevance.  
**In scope**: Four loadable packs (SOC/Sentinel alert-storm, 311/911 city ops, water utility leak surge, traffic/transportation) each with knowledge seeds and signal seeds demonstrating dedup collapse.  
**Out of scope**: Changes to RouterExecutor logic.

### Actionable Requirements

- **S4-FR-001**: The system MUST provide independent load flags for all four packs.
- **S4-FR-002**: Each pack MUST ship with seed knowledge and seed signals aligned to its domain.
- **S4-FR-003**: Each pack MUST visibly demonstrate dedup attachment behavior on ClearBoard.
- **S4-FR-004**: Each pack MUST run in deterministic mock mode.

### Acceptance Criteria

- **S4-AC-001**: Each pack can be loaded independently and verified in mock mode.
- **S4-AC-002**: One automated test per pack confirms duplicate signals attach to existing incidents.
- **S4-AC-003**: Demo output shows pin merge/magnitude behavior for each domain.

## SPEC-5 — GitHub-in-the-Lab Path

**Problem**: The GitHub value narrative is not embedded in participant flow.  
**In scope**: `labs/` track covering fork, Actions smoke test run, and Copilot-led extension exercise behind tests.  
**Out of scope**: New monetization systems or unrelated lab rewrites.

### Actionable Requirements

- **S5-FR-001**: Lab documentation MUST include stepwise GitHub workflow (fork, run CI, implement guided extension, verify green).
- **S5-FR-002**: The exercise MUST offer two completion choices: add one ActionAgent tool or add one scenario pack.
- **S5-FR-003**: A starter failing test MUST be provided for the exercise.
- **S5-FR-004**: Exercise completion MUST be defined as turning the starter test green without weakening existing tests.

### Acceptance Criteria

- **S5-AC-001**: Participants can follow documented steps to execute `smoke-test.yml` on their fork.
- **S5-AC-002**: The starter test fails before the exercise and passes after completion.
- **S5-AC-003**: Existing baseline tests remain intact and green.

## SPEC-6 — "Lab to Production" Leave-Behind

**Problem**: Post-demo next steps are unclear for engaged teams.  
**In scope**: `docs/lab-to-production.md` with architecture, Azure footprint, Responsible-AI map, and direct CTA to engage Sean & Tracy’s team; linked from README and capstone view.  
**Out of scope**: Sales-system automation.

### Actionable Requirements

- **S6-FR-001**: The leave-behind document MUST summarize architecture, footprint, and governance controls in one consumable handoff.
- **S6-FR-002**: The document MUST include a same-day engagement CTA with contact pathway.
- **S6-FR-003**: README and capstone UI MUST link to this document.
- **S6-FR-004**: Content MUST be compatible with mock/demo posture and not depend on live environment data.

### Acceptance Criteria

- **S6-AC-001**: `docs/lab-to-production.md` exists with all required sections.
- **S6-AC-002**: README and capstone include valid links to the document.
- **S6-AC-003**: Reviewer sign-off confirms the document supports day-of follow-up conversations.
