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
expectation to SEV1/15m/escalation. It remains
**tested locally, not deployed**; the three-attempt cap and live safety failure
remain. Any future deployment, existing-incident remediation and live
revalidation require separate authorization and must preserve every report.

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
