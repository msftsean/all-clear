# Work Routing

How to decide who handles what.

## Routing Table

| Work Type | Route To | Examples |
|-----------|----------|----------|
| Python/FastAPI, MAF agents, Azure services | Shuri | Agent pipeline, MAF workflow, API endpoints, Azure OpenAI/AI Search integration, embedding dedup |
| React/TypeScript, UI components | Stark | ClearBoard, react-leaflet map, surge board, SSE wiring, chat and voice UI |
| Security, auth, access control | Rogers | Tool authority bounds, PII handling, CORS, secrets, managed identity, embedding retention |
| Code review, architecture | T'Challa | Review PRs, design decisions, scope trade-offs |
| Testing, QA, verifiers | Barton | Eval sets, replay fixtures, checkpoint scripts, edge cases, coverage. Verifiers are built BEFORE implementations (Loop Protocol rule 1) |
| Scope & priorities | T'Challa | What to build next, trade-offs, decisions |
| Session logging | FRIDAY | Automatic, never needs routing |

## Issue Routing

| Label | Action | Who |
|-------|--------|-----|
| `squad` | Triage: analyze issue, evaluate @copilot fit, assign `squad:{member}` label | Lead |
| `squad:{name}` | Pick up issue and complete the work | Named member |
| `squad:copilot` | Assign to @copilot for autonomous work (if enabled) | @copilot 🤖 |

## Loop Rule (binding on all members)

The agent implementing a task may not modify that task's tests, eval thresholds, fixtures, or checkpoint scripts. Barton owns those. If a verifier seems wrong, flag it to T'Challa instead of editing it.
