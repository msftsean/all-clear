---
description: "Completed task ledger for All Clear consolidation"
---

# Tasks: All Clear Consolidation

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), `CONTEXT.md`
**Status**: Complete on 2026-09-20
**Tests**: Required for behavioral changes.
**Last Updated**: 2026-11-17 — Phase 3 participant documentation completed. Backend and frontend verification passed. Mockmode enabled in public docs. Quickstart and bootcamp guides updated.

## Phase 1: Retire University-Support Runtime

- [x] T001 Remove the retired support classifier, dynamic branding, fixtures, and
  related APIs from `backend/` and `frontend/`.
- [x] T002 Preserve and rename neutral session, audit, voice, and safety data models
  for the All Clear incident domain.
- [x] T003 Update voice tool definitions and endpoint tests to use incident IDs,
  queues, severity, and escalation controls.
- [x] T004 Verify focused backend schema, safety, and voice endpoint tests.

## Phase 2: Align Active All Clear Delivery

- [x] T101 Remove retired brand defaults and legacy UI components from the primary
  frontend.
- [x] T102 Replace retired support knowledge seeds with neutral operational
  incident-response guidance.
- [x] T103 Update scripts, package metadata, deployment guidance, and runtime copy
  to use All Clear terminology.
- [x] T104 Verify the primary frontend production build.

## Phase 3: Rewrite Companion Materials

- [x] T201 Rewrite `workshop-site/` as an incident-triage workshop companion.
- [x] T202 Rewrite `coach-guide/` and `coach-site/` as All Clear facilitator
  materials.
- [x] T203 Rewrite `hackathon-site/` as an All Clear scenario/reference site.
- [x] T204 Rewrite `docs-site/` as an All Clear operations companion.
- [x] T205 Typecheck and build every companion site.

## Phase 4: Prune and Synchronize Specification Records

- [x] T301 Delete obsolete support-domain scenarios, specifications, runbooks,
  validation records, and workflow references.
- [x] T302 Amend `.specify/memory/constitution.md` for the incident-only system.
- [x] T303 Replace this spec, plan, and task ledger with the completed
  consolidation record.
- [x] T304 Update Spec Kit templates with current authority, escalation, PII,
  mock-mode, and verification expectations.
- [x] T305 Verify the tracked-content legacy-brand scan returns no matches.

## Phase 5: Participant-Facing Documentation (Nov 17)

- [x] T501 Update README.md with mock-mode quickstart (no Azure credentials, `MOCK_MODE=true`,
  exact backend/frontend commands, Node 18, Copilot CLI binary, GHE.com sign-in).
- [x] T502 Update `.specify/memory/constitution.md` to match current code and
  incident-triage boundaries (no changes needed — already aligned).
- [x] T503 Update `specs/019-evolution-loop/spec.md` and `plan.md` to reflect
  verified behavior and test counts (347 backend + 4 frontend, Nov 17).
- [x] T504 Update `docs/bootcamp/PARTICIPANT_GUIDE.md` with mock-mode setup,
  Copilot CLI install path, GHE.com sign-in, copy/paste tips, test coverage,
  96% resilience score clarification, and routing zero-LLM fact.
- [x] T505 Update `docs/bootcamp/QUICK_REFERENCE.md` to reflect mock-mode
  commands, Copilot CLI, test counts, Azure optional-stretch guidance, RG naming
  convention `rg-allclear-pNN`, and East US 2 embeddings Standard.
- [x] T506 Verify all links in participant docs point to canonical files and
  no coach-only content is exposed.

## Final Verification

- [x] T390 Run focused backend schema, safety, and voice endpoint tests.
- [x] T391 Build the primary frontend and all companion sites.
- [x] T392 Confirm `CONTEXT.md`, the Constitution, this spec pack, and active
  templates use the same incident-triage vocabulary.

## Post-Consolidation Privacy Hardening (2026-11-12)

- [x] T401 Fail closed on session-history retrieval until a verified
  server-side owner contract exists; remove caller-hash history fetches from the
  frontend.
- [x] T402 Scope internal transcript subscriptions by call, redact published
  transcript data, and reject public SSE/ACS media access until ownership and
  ingress identity can be verified.
- [x] T403 Keep realtime safety instructions server-controlled and generate
  server-owned session IDs instead of trusting caller-selected IDs.
- [x] T404 Fix Lab 07 MCP pipeline invocation and make both offline probe modes
  fail on tool error responses.
- [x] T405 Run focused backend privacy/realtime tests, frontend build, and both
  offline Lab 07 MCP probes.
- [x] T406 Preserve trusted pre-redaction PII metadata in both Lab 07 variants
  and the Lab 05 solution pipeline using a typed keyword-only flag and a frozen
  classification replacement; keep caller-selected sessions disabled.
- [x] T407 Add offline MCP regressions for PII redaction and benign-request
  escalation despite model denial, plus literal-marker and fallback cases;
  run focused Lab 05/07 tests and both offline runtime probes.
