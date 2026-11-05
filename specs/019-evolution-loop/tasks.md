---
description: "Completed task ledger for All Clear consolidation"
---

# Tasks: All Clear Consolidation

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), `CONTEXT.md`
**Status**: Complete on 2026-09-20
**Tests**: Required for behavioral changes.

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

## Final Verification

- [x] T390 Run focused backend schema, safety, and voice endpoint tests.
- [x] T391 Build the primary frontend and all companion sites.
- [x] T392 Confirm `CONTEXT.md`, the Constitution, this spec pack, and active
  templates use the same incident-triage vocabulary.
