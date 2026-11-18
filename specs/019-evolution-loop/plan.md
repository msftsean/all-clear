# Implementation Plan: All Clear Consolidation

**Branch**: `main` | **Date**: 2026-09-20 | **Spec**: [spec.md](./spec.md)

## Summary

Consolidate the runtime, companion sites, documentation, and Spec Kit on All
Clear incident triage. Remove the retired support-domain stack rather than
translating it, preserve the bounded signal-to-incident pipeline, and verify
every supported delivery surface.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript 5, Node.js 18+
**Primary Dependencies**: FastAPI, Pydantic, Microsoft Agent Framework, React,
Vite, Tailwind CSS
**Storage**: Mock incident/session stores; Azure-backed services in live mode
**Testing**: pytest, TypeScript compiler, Vite builds, Playwright where present
**Target Platform**: Linux-hosted API and static web applications
**Project Type**: Web application plus static companion sites
**Constraints**: Mock mode needs no Azure credentials; RouterExecutor is
deterministic and zero-LLM; no PII echo; public content requires human approval
**Scope**: `backend/`, `frontend/`, four companion sites, labs/docs/infra seeds,
and active Spec Kit records

## Constitution Check

| Gate | Result |
|---|---|
| PII handling and audit records remain incident-only | Pass |
| QueryAgent, RouterExecutor, and ActionAgent boundaries remain intact | Pass |
| SEV1/statutory/safety escalation cannot be weakened | Pass |
| Mock and live paths retain the same bounded pipeline | Pass |
| Retired support-domain behavior and terms are removed | Pass |

## Delivery Phases

### Phase 1 - Remove retired runtime behavior

Delete the retired support classifier, models, services, dynamic branding, APIs,
fixtures, tests, and assets. Preserve neutral session, audit, voice, and safety
primitives under All Clear names.

### Phase 2 - Align active channels

Update primary frontend defaults, mock realtime tools, voice/phone schema copy,
knowledge seeds, scripts, and deployment descriptions to signals, incidents,
queues, severity, SLAs, and ClearBoard.

### Phase 3 - Rewrite public and learning surfaces

Rewrite the workshop, coach, hackathon, and operations companion sites. Remove
retired support scenarios and historical material, then replace them with surge,
dedup, incident response, safety, and voice/phone examples.

### Phase 4 - Prune and synchronize Spec Kit

Delete obsolete feature records and legacy delivery guidance. Amend the
Constitution and replace the active spec, plan, and task ledger with this
consolidation record. Update templates so future work performs the current
Constitution Check.

### Restricted participant deployment (2026-11-18)

Keep the existing resource-group Bicep entry point, explicitly declare its scope,
and parameterize role-assignment creation and OpenAI key authentication while
preserving their managed-identity defaults. The p29 environment disables role
assignments and optional phone/realtime, enables live services, and passes the
OpenAI key only through ARM secret expressions. Add workspace-based Application
Insights and opt-in Azure Monitor SDK export with no local offline buffer.
Validate the Bicep build and own-RG preview, focused telemetry/safety/pipeline
tests, frontend production build, and the three live signals. Record actual
timings and portal-verification limitations in
`docs/lab/azure-overnight-2026-11-18.md`.

The live Oak Street signal exposed FIELD_HAZARD under-triage: downed/sparking
indicators produced SEV2 without escalation. Add only `sparking` and explicit
`electrical arcing` to the existing deterministic life-safety terms, not generic
`downed` or a category-wide elevation. Reproduce the exact typed classification,
test ordinary field hazards remain unchanged, and prove a fresh first/duplicate
pair retains SEV1, escalation, reports and audit records offline. The focused
router/pipeline suites passed 23 tests after a red reproduction. This fix is
also covered by the final integrated telemetry/schema/API/pipeline/router/voice
suite: 92 passed after strengthening the existing sparking-powerline route-test
expectation to SEV1/15m/escalation. It was
**tested locally, not deployed** at the original three-attempt stop.
At 01:22:30 ET the user authorized six additional attempts (4–9); deploy the
committed fix backend-only on the same stack and revalidate the unchanged three
signals. Positively confirmed original synthetic fixtures may be retired to
resolved with an audit trail, never deleted, rewritten or counter-reset.
Record recovery revision/timing/results separately; retain original failed
evidence and keep readiness blocked until all required proof is obtained.
Backend-only attempt 4 succeeded in 32.6767145 seconds. The unchanged new
three-signal live run passed all seven verifier checks: AC-0003 opened
SEV1/15m/escalated and the duplicate attached at magnitude 2; AC-0004 handled
the explicit human request. Scoped storage readback confirmed preserved
original fixtures and monotonic counter 4. Authenticated p29 Foundry portal
rendering remains unverified, independently of functional recovery.
One separately authorized frontend Send rehearsal then attached to AC-0003 at
magnitude 3, retaining SEV1/escalation. At that checkpoint, its desktop receipt
trigger was absent; the same-page 430px View control opened the actual receipt.
The browser-local attachment count and unconditional Sitrep ready label were not
authoritative evidence. After capture, audited status-only retirement of the
two new synthetic fixtures left four preserved/resolved incidents, zero active,
counter 4 and eight maintenance audit documents. Health passed at the
01:39:07.947 ET checkpoint; subsequent desktop acceptance used AC-0005/6 below.
No clean passing participant end-to-end rerun was timed; the 35–45 minute
estimate is planning, not achieved timing proof.
The real frontend rehearsal also exposed three directly coupled desktop
accuracy defects: receipt access, attached aggregate zero despite attachment,
and Sitrep ready despite null action sitrep. Parent authorized minimal local
correction, focused tests/build and committed-source frontend-only deployment
by Kitty after explicit approval. Backend and preserved fixture queue had to stay
unchanged; no preemptive deployment was authorized.
Five frontend files were committed as
`b26e397500bc00f465a025363d17c548801a93cb`, with six focused tests, build and
targeted zero-warning ESLint passing. Actual attached outcomes/reset handling,
optional compatibility fields and null-sitrep copy correct the live rendering
without backend/API/dependency changes. Kitty was explicitly authorized attempt 5,
frontend-only, after preflight. Attempt 5 passed in 42.5539561 seconds;
serving-container/public/local asset hashes match. Actual desktop acceptance
passed all three original inputs through real Send controls at 1440px:
AC-0005 opened SEV1/escalated, AC-0006 handled the human request and the duplicate
attached to AC-0005 at magnitude 2. Desktop receipts, attached counter 1 and
null-sitrep/no-approval-gate rendering passed without mocks/retries/resize.
After frozen capture, the authorized AC-0005/6 status-only CAS retirement passed,
preserving all other fields, older documents/ETags and full counter document.
Final six resolved/zero active/counter6/audit12 and health/frontend HTTP 200 were
verified at 01:51:15.229 ET. Next audience IDs are expected AC-0007/8 without
reset, not yet submitted. Final desktop calls also have fresh real-model/
embedding HTTP correlation proof. Ten total signal POSTs, five of nine
deployment attempts used; apps remain running for 9:00 AM.

## Verification Matrix

| Surface | Command or check |
|---|---|
| Incident schema/safety/voice | `cd backend && PYTHONPATH=. python -m pytest tests/test_schemas.py tests/test_voice/test_safety_net.py tests/test_voice/test_endpoints.py -q` |
| History/transcript/realtime privacy | `cd backend && PYTHONPATH=. python -m pytest tests/test_conversation_persistence.py tests/test_transcripts/test_transcript_bus.py tests/test_transcripts/test_sse_http.py tests/test_media_ws_security.py tests/test_voice/test_endpoints.py tests/test_voice/test_azure_realtime.py tests/test_voice/test_pii_filter.py tests/test_voice/test_safety_net.py -q` |
| Lab 07 offline MCP probe | `python labs/07-mcp-server/exercises/mcp_red_team_probe.py --server start` and `--server solution` |
| Lab 07 trusted PII and offline orchestration | `python -m pytest labs\07-mcp-server\test_lab07.py labs\05-agent-orchestration\test_lab05.py -q -k "not live_azure"` |
| Primary web app | `cd frontend && npm run build` |
| Workshop companion | `cd workshop-site && npm run typecheck && npm run build` |
| Coach companion | `cd coach-site && npm run typecheck && npm run build` |
| Hackathon companion | `cd hackathon-site && npm run typecheck && npm run build` |
| Operations companion | `cd docs-site && npm run typecheck && npm run build` |
| Retired brand scan | The repository retired-brand scan returns no paths |

## Project Structure

```text
backend/app/             # Incident pipeline, APIs, services, and safety controls
frontend/src/allclear/   # Primary ClearBoard experience
workshop-site/           # Incident-triage workshop companion
coach-guide/             # Facilitator source material
coach-site/              # Facilitator companion
hackathon-site/          # Scenario/reference companion
docs-site/               # Operations companion
specs/019-evolution-loop/# Consolidation record
```

**Structure Decision**: Keep the existing multi-surface structure because each
site serves a distinct audience; all surfaces share the canonical All Clear
domain language from `CONTEXT.md`.

## Security Hardening Follow-up (2026-11-12)

No verified end-user principal or ACS ingress identity is currently configured.
Session-history and phone transcript routes therefore fail closed; the transcript
bus supports per-call subscriptions and redacts event data, but the public stream
will remain unavailable until the backend can authorize a call owner. Realtime
uses server-generated session IDs and ignores client prompt overrides. Do not
re-enable these routes based on caller-supplied hashes or IDs.

Lab 07 derives trusted PII detection from redaction of original input before
logging or invoking Lab 05. Its normal and fallback paths preserve escalation.
Lab 05 accepts an optional keyword-only `pii_detected: bool = False`, merging
it with QueryAgent detection via `dataclasses.replace` before RouterExecutor.
Existing positional signal/session calls remain compatible; MCP still ignores
caller-selected session IDs. No routing rules, auth mechanism, or live-service
dependencies are added. Regression tests use a local model stand-in reporting
no PII; both runtime probes also exercise the real credential-free pipeline.
