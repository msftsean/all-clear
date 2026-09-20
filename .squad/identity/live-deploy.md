# Live Azure Deployment (azd up)
Deployed: 2026-09-20T22:56:00Z
Subscription: a8a91d76-473f-49e2-ba21-1d394ba9a968
Resource group: rg-all-clear-demo
AZURE_CONTAINERAPP_URL: https://allclear-p74h22h3c2hqm-backend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io
AZURE_FRONTEND_URL: https://allclear-p74h22h3c2hqm-frontend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io
AZURE_AI_PROJECT_ENDPOINT: none provisioned
Status: live - mock-mode `azd up` now succeeds after commit `a0afed0`; non-mock reprovision + service redeploys produced a healthy backend (`mock_mode=false`), healthy phone endpoint, active ACS number, and live frontend routes, but a real human PSTN call has not yet been placed from this environment.

## Phase 1b follow-up: real ACS/live-calling

Checked: 2026-09-20T22:56Z+
Current ACS resource status: live; `allclear-p74h22h3c2hqm-acs` exists in `rg-all-clear-demo` with host `allclear-p74h22h3c2hqm-acs.unitedstates.communication.azure.com`.
AZ CLI auth status: still blocked for `az account show`, but the allowed REST fallback worked with `azd auth token --scope https://communication.azure.com//.default`.
Purchased phone number: +18333915639
Number type / assignment / capabilities: toll-free / application / calling=inbound, sms=none
Monthly cost estimate: 2.00 USD/month for the number rental, plus ACS usage/per-minute charges once real calls are placed.
Deployment wiring:
- MOCK_MODE=false
- DEPLOY_REALTIME=true
- AZURE_ACS_ENDPOINT=https://allclear-p74h22h3c2hqm-acs.unitedstates.communication.azure.com
- ACS_PHONE_NUMBER=+18333915639
- Event Grid `incoming-call` subscription provisioning state: Succeeded
- Backend `/api/health`: `{"status":"healthy","mock_mode":false,"domain":"all-clear-incident-triage"}`
- Backend `/api/phone/health`: `{"phone_available":true,"mock_mode":false,"phone_enabled":true,"latency_ms":168,"error":null}`
Remaining blocker: no human/external PSTN caller was available through this environment, so a real inbound test call and `/phone` transcript capture are still pending.
Teardown / release reminder: this number is now billable until released. After the demo/test window, release it and do not reuse it across deployments (for example via the ACS phone-number release API/CLI path).
