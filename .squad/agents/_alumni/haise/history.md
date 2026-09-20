# History

## Project Context

All Clear deploys through Azure services and must support a classroom-scale
event.

## Learnings

- For the 390-minute Day 2 window, the participant workbook schedules APIM as S4
  (60 minutes, 3:30–4:30 ET) and Azure Container Apps deployment as S5 (60
  minutes, 4:30–5:30 ET); see `participant-runbook/index.html` lines 341–349.
- The required event deployment path is the facilitator-provided shared backend
  plus health verification; individual `azd up`, Docker, seeding, Cosmos
  persistence, monitoring, and cleanup are explicitly optional deep-dive steps
  in `labs/06-deploy-with-azd/README.md` lines 10–29.
- Deployment completion evidence is a public backend URL, green `/api/health`,
  and CI eval gating; the detailed deployment proof is in
  `participant-runbook/index.html` lines 419–427 and
  `labs/06-deploy-with-azd/README.md` lines 480–500.
- APIM is feasible as a Consumption gateway when a running backend exists:
  import OpenAPI, pass a signal through, prove `429` rate limiting, `401` JWT
  rejection, token-budget behavior, and Application Insights telemetry; see
  `labs/08-apim-gateway/README.md` lines 1–8, 18–26, 93–216.
- The facilitator fallback is mock mode, which the main lab index says runs
  offline without Azure credentials; `labs/README.md` lines 63–65 and
  `labs/00-setup/README.md` lines 11–15, 52–63. RAG has a pre-populated
  `allclear-kb` index, with `verify_index.py` as its evidence check; see
  `labs/04-build-rag-pipeline/README.md` lines 11–29.

- Event operations should make the shared-backend path the timed baseline:
  full `azd up` is useful for a deep dive but is too dependent on first-time
  provider registration, regional capacity, Docker, and model provisioning.
- APIM Consumption remains the practical 20-participant path in `eastus`;
  unique names, preflight RBAC/provider checks, and a 10-minute stop condition
  are more useful than promising a universal quota.
- The existing `backend/scripts/check_eval.py` is a credential-free CI gate;
  wiring it into the backend workflow provides a concrete eval exercise without
  adding a second workflow.
