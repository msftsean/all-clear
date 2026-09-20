# History

## Project Context

All Clear deploys through Azure services and must support a classroom-scale
event.

## Learnings

- 2026-09-20: The event-safe Azure path is shared backend health/OpenAPI
  verification plus the offline QueryAgent eval; personal `azd up` must remain
  an explicitly optional deep dive.
- 2026-09-20: The existing backend CI classification gate is executable from
  `backend/` with the clean CI venv and scored 60/60 locally at the 0.90
  threshold.
- 2026-09-20: APIM event readiness needs explicit RBAC scope, provider
  registration, portal quota/capacity review, deterministic global names,
  10-minute APIM and 45-minute full-stack stop conditions, shared-backend and
  pre-created-gateway fallback, JWT/App Insights prerequisites, and verified
  cleanup.
