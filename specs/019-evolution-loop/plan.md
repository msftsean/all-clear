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

## Verification Matrix

| Surface | Command or check |
|---|---|
| Incident schema/safety/voice | `cd backend && PYTHONPATH=. python -m pytest tests/test_schemas.py tests/test_voice/test_safety_net.py tests/test_voice/test_endpoints.py -q` |
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
