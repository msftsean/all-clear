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

## Restricted participant deployment (2026-11-18)

- [x] T501 Add explicit RG scope and opt-in no-role/key-auth parameters without
  changing the default managed-identity path.
- [x] T502 Add Azure Monitor export and workspace-based Application Insights,
  keeping credentials out of outputs and local telemetry storage.
- [x] T503 Verify Bicep preview, telemetry tests, existing safety/pipeline
  regressions, and frontend production build.
- [ ] T504 Deploy one p29 stack (original three attempts; six more explicitly
  authorized at 01:22:30 ET, maximum nine total), prove the requested
  live signals, model/telemetry behavior and authenticated p29 Foundry portal
  rendering, and commit the timed morning report. Functional recovery passed;
  authenticated portal rendering is still unverified, and a clean passing
  participant end-to-end timing has not been measured under the one-stack rule.
- [x] T505 Reproduce the live downed/sparking FIELD_HAZARD safety failure and
  add bounded deterministic `sparking`/`electrical arcing` matching, ordinary
  field-hazard negatives, and duplicate/report/audit regressions. Focused
  router/pipeline suites: 23 passed; strengthen the directly coupled API route
  expectation and pass the combined 92-test regression suite.
  **Tested locally, not deployed at the original 00:20 stop**; recovery
  deployment/acceptance is tracked separately in T506.
- [x] T506 Use the 01:22:30 ET recovery authorization for backend-only
  deployment of the safety fix and new three-signal acceptance; retire only
  confirmed original synthetic fixtures to resolved with an audit trail.
  Preserve every report, original severity/embeddings and monotonic IDs.
  Record new revision and measured recovery timing without obscuring original
  safety failure. Attempt 4 passed in 32.6767145s; all seven new live-verifier
  checks and scoped old/new fixture readback passed. Authenticated Foundry portal
  rendering remains a separate incomplete gate under T504.
- [x] T507 After the single authorized frontend Send rehearsal, conditionally
  retire only confirmed synthetic AC-0003/AC-0004 to resolved with durable audit.
  Verify all four fixtures preserved/resolved, zero active incidents, counter 4
  unchanged and eight maintenance audit documents; leave the live stack running.
  Final verification/health passed at 01:39:07.947 ET; AC-0003's rehearsal
  magnitude 3 and two attached reports are preserved, not active. At this
  checkpoint seven signal POSTs/four deployments had been used; later desktop
  verification/final lifecycle is recorded in T508/T509.
- [x] T508 Correct the three desktop live-result accuracy defects with focused
  tests/build: actual receipt access, attached-report total and no false
  sitrep-ready claim for null action sitrep. Deploy only the validated committed
  frontend after explicit approval, preserving backend, clean queue and history.
  Five files committed as `b26e397500bc00f465a025363d17c548801a93cb`;
  six tests/build/targeted zero-warning ESLint pass. Attempt 5 frontend-only
  deployment passed in 42.5539561s with matching serving/public/local asset
  hashes; actual three-send desktop acceptance passed receipt/counter/null-sitrep
  checks. Its separately authorized final lifecycle is tracked in T509.
- [x] T509 After the corrected frontend is explicitly Ready, capture the
  separately authorized three real desktop Sends with unchanged original inputs,
  accurate receipt/attachment/sitrep rendering and no retries/mocked state.
  Then conditionally retire only the confirmed new synthetic fixtures and verify
  preserved records, zero active incidents and updated counter/audit totals.
  Real desktop receipts/count1/null-sitrep copy and fresh model/embedding spans
  passed. Final six resolved/zero active/counter6/audit12 and health/frontend HTTP
  200 verified 01:51:15.229 ET; 10 signal POSTs/five of nine deployments used.
  Next audience AC-0007/8 expected, not executed; backend/infra unchanged.

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
