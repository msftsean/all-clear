# All Clear Development Guidelines

## Source of Truth

- Constitution: `.specify/memory/constitution.md`
- Domain language: `CONTEXT.md`
- Active consolidation record: `specs/019-evolution-loop/`

## Architecture

All Clear is an incident-triage application. QueryAgent classifies signals,
RouterExecutor deterministically decides dedup/severity/SLA/escalation, and
ActionAgent acts only through `create_incident`, `search_knowledge`, and
`generate_sitrep`. Preserve every signal as a report; dedup never deletes it.

## Technology and Commands

- Backend: Python 3.11+, FastAPI, Pydantic, Microsoft Agent Framework.
- Frontend and companion sites: TypeScript 5, React 18, Vite 5, Tailwind CSS.
- Focused backend verification:
  `cd backend && PYTHONPATH=. python -m pytest tests/test_schemas.py tests/test_voice/test_safety_net.py tests/test_voice/test_endpoints.py -q`
- Primary frontend: `cd frontend && npm run build`
- Companion sites: run `npm run typecheck && npm run build` in `workshop-site/`,
  `coach-site/`, `hackathon-site/`, or `docs-site/` as applicable.

## Non-Negotiables

- Never weaken PII filtering, audit trails, SEV1/statutory escalation, or the
  zero-LLM RouterExecutor.
- Keep mock mode viable without Azure credentials.
- Use `CONTEXT.md` terms; do not reintroduce retired support-domain features,
  branding, datasets, or terminology.
- Update the active specification, plan, tasks, tests, and directly related
  documentation with behavior changes.
