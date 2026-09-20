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
- 2026-09-20: Glass-Box Audit Increment 2 infrastructure claim is **structurally
  confirmed**: The existing `frontend` Container App (`infra/main.bicep`
  lines 635–681) is a single SPA host with no route-specific ingress rules or
  per-page resources; `azure.yaml` contains no routing policies or conditional
  build steps. The app already implements client-side query-param routing
  (`App.tsx`: `new URLSearchParams(window.location.search).get("page")`), so
  adding a new `/?page=audit` route requires **zero Bicep and zero azure.yaml
  changes**. Deployment: rebuild SPA bundle → push Docker image → deploy to
  existing app. The infrastructure is already shaped for arbitrary client-side
  SPA additions; Increment 2 is purely React component work.
