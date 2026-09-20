# History

## Project Context

All Clear requires repeatable event delivery and verifier-first exercises.

## Learnings

- Event evidence is strongest in offline/mock mode: `backend/tests` passed 347/347; `labs/01-understanding-agents/test_lab01.py` passed 7/7; `labs/03-spec-driven-development/test_lab03.py` passed 8/8; `labs/04-build-rag-pipeline/verify_index.py` found 15 local records and passed keyword/category checks; `labs/05-agent-orchestration/test_lab05.py` passed 5 with 1 Azure-only skip; the documented surge replay passed with 25 signals, 5 open incidents, and 20 attached reports; Lab 09 extension and completion gates passed. Paths: `backend/tests`, `labs/01-understanding-agents/test_lab01.py`, `labs/03-spec-driven-development/test_lab03.py`, `labs/04-build-rag-pipeline/verify_index.py`, `labs/05-agent-orchestration/scenarios/surge/smoke_test.py`, `labs/09-github-in-the-lab/`.
- Published participant and backend endpoints are reachable now: `participant-runbook/index.html` deployment returned HTTP 200; the published `/api/health`, `/api/docs`, and `/api/openapi.json` endpoints returned HTTP 200, with OpenAPI 3.1 exposing 12 paths including `/api/chat` and `/api/health`.
- Local readiness is not a hosted-deployment proof: `labs/00-setup/verify_environment.py` reported Python, Node, azd, and Docker available, but Azure CLI not logged in, no `.env`, and no local backend; `labs/06-deploy-with-azd/test_lab06.py` scored 8/13 because local health, Azure resources, production health, app status, and logs were not available.
- Timing risk: the participant workbook defines a coherent 390-minute S0-S5 agenda (`participant-runbook/index.html`), while the individual lab headers total substantially more time and include separate prerequisites. Event delivery needs a facilitator-owned mapping of which lab sections are required versus optional before calling the full path time-safe.
- Link/readiness risk: the workbook's root-relative favicon links are valid on the deployed Static Web App but appear missing under a plain local filesystem check; local preview should use an HTTP server rather than opening `index.html` directly.

- A curriculum gate is most useful when it validates claims against repository
  evidence: stage artifacts, local links, workflow filenames, and observable
  completion evidence.
- Participant-facing schedules need arithmetic checks that distinguish working
  time from breaks; the runbook now uses a 390-minute window with 315 minutes
  of work and 75 minutes of breaks.
- Environment-variable completion flags are not exercise evidence. The verifier
  reports them without changing the participant materials owned by other agents.
