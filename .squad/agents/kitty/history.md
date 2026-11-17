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
- 2026-09-20: Tried live `azd up` in subscription `a8a91d76-473f-49e2-ba21-1d394ba9a968`
  (`CopilotLabs DS - 1009`) in `eastus2` using azd env `all-clear-demo` /
  resource group `rg-all-clear-demo`. First run hung on the phone Event Grid
  subscription because checked-in `infra/main.parameters.json` defaults
  (`mockMode=false`, `deployRealtime=true`) overrode the azd env values, so the
  placeholder backend never satisfied the incoming-call validation handshake.
- 2026-09-20: Pre-fix retry failed with `ContainerAppSecretInvalid` because
  backend secret `acs-connection-string` was empty in mock mode. After commit
  `a0afed0`, `azd up --no-prompt` on the same `all-clear-demo` env succeeded
  in `eastus2` and produced live URLs
  `https://allclear-p74h22h3c2hqm-backend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io`
  and
  `https://allclear-p74h22h3c2hqm-frontend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io`;
  `AZURE_AI_PROJECT_ENDPOINT` is still not provisioned by this stack.
- 2026-09-20: Real ACS fallback can work without `az login`: an ACS-scoped
  token from `azd auth token --scope https://communication.azure.com//.default`
  was valid for the phone-numbers REST API. Purchased deployment-specific toll-
  free number `+18333915639` for `allclear-p74h22h3c2hqm-acs` at **$2.00
  USD/month** plus usage charges.
- 2026-09-20: For live phone mode, `DEPLOY_REALTIME=true` is required in
  addition to `MOCK_MODE=false` and `ACS_PHONE_NUMBER`, because
  `AzurePhoneService` bridges calls through the Realtime WebSocket path using
  `AZURE_OPENAI_REALTIME_DEPLOYMENT`.
- 2026-09-20: `azd provision` updates the Container App template/infra but can
  leave the previously deployed service revision or placeholder image serving
  traffic; after changing live/mock phone settings, `azd deploy backend` and
  `azd deploy frontend` were needed to move traffic onto ready All Clear
  revisions. Final health checks: backend `/api/health` healthy with
  `mock_mode=false`, `/api/phone/health` healthy with `phone_available=true`,
  Event Grid `incoming-call` subscription `Succeeded`, but no real inbound PSTN
  test call was placed from this environment.

- 2026-11-17: Room Surge live rehearsal is authorized but blocked pending human restoration of the correct tenant access, confirmation of the audience Container Apps, safe mode/replica/revision checks, and coach-key reference verification. Do not reuse the private redteam adapter, retry the expired TAP auth, or provision blindly; see private session report for the status-only runbook.

- 2026-11-17: User selected MCAPS-2026 audience subscription and authorized a separate app/new app-scoped secrets. Read-only group inventory was blocked by chained Azure credential failure (AADSTS50020/AADSTS130504); do not retry auth or alter defaults. Existing private redteam adapter remains no-touch. Docker CLI present, Linux engine unavailable; local builds blocked under remoteBuild=false. Root deployment plan status remains planning/not ready; private report has corrected tenant ID and evidence.

- 2026-11-17: Docker Desktop Linux engine verified ready (29.9.3); local build path unblocked, keep remoteBuild=false. Added the exact proposed isolated audience RG/resource topology and deployment order to .azure/deployment-plan.md. Cloud inventory remains blocked by known corporate-tenant auth failure; no retry or Azure write. Wait for Forge's focused verifier/key-entry tests before exposure.

- 2026-11-17: Parent verified Docker Linux daemon ready; updated plan to use local build (remoteBuild:false). Final isolated resource topology/regions and proposed RG recorded; actual resource/model quota inventory remains blocked by known MCAPS credential mismatch. Forge verifier and safe key-entry tests are release gates.

- 2026-11-17: Correction: direct Azure CLI selected-subscription metadata identifies MCAPS-2026-segayle, tenant 16b3c013-d300-468d-ac64-7eda0820b6d3. Target inventory found AOAI quota headroom but no suitable reusable endpoint, no Search, and only redteam ACA/ACR; new audience stack is isolated. Plan advanced to Ready for Validation only; RBAC and Communication registration/phone gate remain preflight items.
