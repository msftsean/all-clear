AZURE DEMO NOT READY

Live URLs:
- Frontend: https://allclear-q2lt63vq6i5f4-frontend.happysmoke-f829312c.eastus2.azurecontainerapps.io
- Backend health: https://allclear-q2lt63vq6i5f4-backend.happysmoke-f829312c.eastus2.azurecontainerapps.io/api/health
- Foundry: https://ai.azure.com/?cid=learnDocs → **New Foundry off → Keep building with Foundry → View all resources → `allclear-q2lt63vq6i5f4-openai` → Shared resources → Deployments** (official navigation verified; p29 signed-in rendering **unverified**).

| check | result | time | note |
|---|---|---|---|
| Identity | PASS | 2026-11-17 23:36 ET | `azuredays-arl26-allclear-p29@establishedcorp.com`; subscription `0e1d648b-17c8-4724-9405-8e84b4c565c4` (Microsoft Azure Sponsorship). |
| Existing RG | PASS | 23:36 ET | `rg-allclear-p29`, eastus2, Succeeded; initially empty. |
| Azure CLI / azd / Docker | PASS | 23:36 ET | 2.93.0 / 1.37.3 / Docker server 29.9.3. Local builds available. |
| azd identity | PASS | 23:37 ET | Login status confirms p29. No login or account switch performed. |
| Roles | PASS | 23:37 ET | Direct Owner on own RG; inherited group access detailed below. |
| Model quota | UNVERIFIED | 23:37 ET | `az cognitiveservices usage list -l eastus2` returned `[]`, including an unfiltered query. Do not interpret as zero usage or available quota. |
| Deployment attempt 1 | CLI FAILED; ARM later SUCCEEDED | 23:47:40-00:06:26 ET observed | azd exited 1 after **87.6847s**: `npm error Exit handler never called!`. ARM duration **PT17M50.9427648S**, state Succeeded, error null. Success was observed approximately 18m46s after the initial CLI start; do not confuse polling/wall time with ARM duration. |
| Deployment attempt 2 | FAILED before cloud writes | 00:06:59.560-00:07:01.506 ET | **1.9457583s**, exit 1. azd 1.37.3 rejected a map for `docker.buildArgs`; subsequently corrected to list schema. Counted against the cap despite no cloud writes. Attempt 3 later succeeded; all attempts are now consumed. |
| Local azd packaging validation | PASS (cache-warm) | 00:07:26.979-00:07:34.902 ET | Both service images packaged in **7.923088s** after correcting `buildArgs` to a list. No provision/deploy writes; not another deployment attempt or cold-build timing. |
| Deployment attempt 3 | PASS; FINAL | 00:07:57.842-00:09:10.791 ET | Exit 0; **72.9490883s**. azd reports provisioning 4s and deploying 1m2s on the same guarded stack. All three attempts consumed; no more deployment attempts. |
| Knowledge seeding | PASS | 00:09:39.292-00:09:50.660 ET | **11.375s**, exit 0; **4/4** canonical All Clear documents upserted into `knowledge-base` using `text-embedding-3-small`. Keys stayed in Python/child-process memory; no seeder source edits. |
| Model deployments | PASS (ARM metadata) | 00:02 ET | Beast confirmed `gpt-5.1` version `2025-11-13`, GlobalStandard capacity 150 and `text-embedding-3-small` version `1`, Standard capacity 50 are Succeeded. Actual invocation was independently proven later (below); portal rendering remains unverified. |
| Application Insights resource | PASS (ARM metadata) | 00:02 ET | `allclear-q2lt63vq6i5f4-insights` Succeeded; application ID `b5d62388-cc87-44c7-96d0-6abfdfa055e8`. Trace ingestion was independently proven later (below); this row records resource metadata only. |
| Acceptance verifier regression | PASS | 00:07 ET; hardened after live result | Six focused tests passed, including transport/field-redaction and rejection of the observed SEV2/non-escalated result; Ruff passed. Tests are offline. Live acceptance later used exactly three POSTs (below). |
| Backend pytest against live config | SKIPPED (unsupported) | 00:03 ET | `backend/tests/conftest.py` explicitly sets `ENVIRONMENT=test` and `MOCK_MODE=true`; existing pytest is not a live-service runner. Use the explicit live acceptance helper instead. |
| Local image recovery | PASS; not deployment attempts | Before midnight | Frontend Docker build approximately 38 seconds (npm ci 26 seconds) with Microsoft npm proxy. Backend Linux image approximately four minutes; `pip check` and Azure Monitor import passed in the image. |
| Frontend browser / proxy | PASS | 00:09:26-36 ET | Isolated Chromium root HTTP 200 in 4435.6ms; title All Clear; visible live and GPT-5.1 PRIMARY badges; Trust opens. Zero JS/console/HTTP errors, zero writes. Backend preflight `mock_mode=false`, `storage_mode=cosmos`. Badges/health are not served-model proof. |
| Audit route | PASS (simulation labeled) | 00:09:26-36 ET | HTTP 200 in 930.7ms; explicitly displays `LOCAL SIMULATION · NO AZURE CREDENTIALS`. Do not present this audit as a live Azure model/evaluation run. |
| Signal 1: downed/sparking power line | **FAIL — SAFETY BLOCKER** | 00:10:09 ET; 4373.1ms client | `FIELD_HAZARD` → `OPEN_INCIDENT`, `AC-0001`, `field-operations`, **SEV2 / 60m / escalate=false**. Required **SEV1 / 15m / escalation** did not occur. Classifier emitted `downed`, `sparking` but no escalation; routing did not recognize those as life-safety indicators. |
| Signal 2: water bill / call me | PASS | 00:10:13 ET; 2231.6ms client | `HUMAN_REQUEST` → `OPEN_INCIDENT`, `AC-0002`, `escalations`, **SEV3 / 240m / escalated=true**, reason `user_requested_human`. |
| Signal 3: exact duplicate power line | PASS dedup; safety still FAIL | 00:10:15 ET; 1942.8ms client | `ATTACH_TO_INCIDENT` → same `AC-0001`, magnitude **2**, cosine **1.0**. Preserves inherited **SEV2 / 60m / escalate=false**, so dedup works but does not cure unsafe triage. |
| Application write budget | CLOSED | 00:10:17.957 ET | Exactly three acceptance POSTs, all HTTP 200; no retries. Returned results preserve three signals/two incidents, not independent durable-storage proof. No more overnight submissions. |
| Real model / embedding invocation | PASS (dependency telemetry) | 00:10:14 ET request; queried afterward | Successful `chat gpt-5.1` dependency correlated with own OpenAI `POST /openai/v1/responses`, HTTP 200, 1527ms. `text-embedding-3-small` requests also HTTP 200. This is served-request evidence beyond health configuration. |
| Application Insights traces | PASS | After 00:10 ET ingestion | Initial query: 3 traces/24 dependencies; independent later query: **4 traces**, **2** successful `chat gpt-5.1` spans and **3** successful `embeddings text-embedding-3-small` spans, correlated with own OpenAI HTTP requests; own Search and Cosmos operations succeeded. Startup-message-specific query remains 0; do not claim that trace. No request bodies/secrets selected. |
| Foundry p29 portal rendering | UNVERIFIED | Final | ARM model visibility and official classic navigation proven; no authenticated p29 portal rendering was available. Public HTML shell is not proof of selected resource/deployment rows. |
| Electrical-hazard regression fix | **TESTED LOCALLY, NOT DEPLOYED** | 00:16 ET | Deterministic indicator terms add `sparking` and `electrical arcing`. Focused routing/pipeline tests **23 passed in 2.40s**. Does not alter deployed revision, existing unsafe `AC-0001`, safety failure or NOT READY verdict. |
| Integrated local regression | PASS — **NOT DEPLOYED** | 00:20 ET | Final combined run: **92 passed in 11.79s**, three dependency warnings. The earlier **91 passed / 1 failed in 13.21s** exposed a stale sparking-powerline route-test expectation, now strengthened to SEV1/15m/escalation. No live evidence or deployment changed. |
| Bicep build / own-RG preview | PASS | Before attempt 1 | RG-scope preview: **12 displayed resource rows (including two model deployments); database/secret children not individually displayed**. No role assignments, RG creation, subscription deployments, phone or realtime. Preview took 42 seconds. Five existing nullable-resource Bicep warnings. |
| Focused backend tests | PASS | Before attempt 1 | 85 passed in 7.23 seconds: telemetry opt-in, schemas, API, pipeline, zero-LLM routing, voice safety and endpoints. These are mock/unit regressions, not live proof. |
| Frontend build | PASS | Before attempt 1 | TypeScript + Vite; build 7.01 seconds. Existing Browserslist/CSS warnings. |
| Changed Python lint | PARTIAL | Before attempt 1 | New telemetry tests pass Ruff. `main.py` has five pre-existing lint findings (UP035, W293, three E501); no unrelated formatting changes made. |

Total deploy time / participant estimate: **deployment succeeded; no passing
participant run achieved**.
Attempt 1 consumed **87.6847 seconds** before the package failure. Its ARM
provisioning took **17m50.9427648s** and was observed Succeeded at **00:06:26 ET**,
approximately **18m46s** after the initial CLI start. Attempt 2 took **1.9457583s**
and failed azd configuration parsing before cloud writes. A local cache-warm
`azd package --all` then passed in **7.923088s**. Attempt 3 succeeded in
**72.9490883s** at **00:09:10.791 ET**. Initial deployment start to successful
deployment exit was **21m30.246s**, including the failed CLI commands, ongoing
ARM provisioning, investigation and warm-image recovery. Seeding added
**11.375s**; seed-ready was **22m10.115s** after initial deployment start,
including the gap before seeding. Three-signal acceptance finished at
**00:10:17.957 ET**: **22m37.413s** from initial deployment start, but the
**SEV1/escalation gate failed**, so no successful usable-demo duration or proven
participant-completion estimate exists. Reserve at least the observed
approximately 23-minute technical path plus prerequisites, troubleshooting and
portal work; this is a planning floor, **not an achieved successful recipe**.
Including the first recorded preflight at 23:36 ET, this overnight effort took
approximately **34 minutes to the failed acceptance result**. A clean participant
run has not been timed or proven; do not advertise the 73-second warm deployment
as a participant completion estimate.
No further deployment retry or overnight acceptance POST is permitted.
Do not quote that cache-warm success as a
participant's full deployment time. Include prerequisite installation, image
builds (observed frontend approximately 38 seconds and backend approximately
four minutes), ARM completion, deployment, knowledge seeding and acceptance in
the cold-path estimate. No achieved cold-path duration is available yet.

## Changes and merge disposition

Revision: overnight working record, branch `azure/overnight-2026-11-18`; base `8ae9276`.
Existing unrelated Squad and lab/showcase changes are excluded from this task's commits.

| Task-owned file | Why changed | Merge after the event |
|---|---|---|
| `infra/main.bicep` | Explicit resource-group scope; optional role assignments and OpenAI key authentication; workspace-based Application Insights and Container Apps secret wiring. | Review, then merge: defaults retain managed identity and role creation; this lab explicitly disables new roles. Key-auth opt-in is a constrained lab exception, not the production recommendation. |
| `infra/main.parameters.json` | Wire opt-in settings through azd, preserving `createRoleAssignments=true` and `openAiKeyAuth=false`. | Safe with the Bicep changes; never copy p29 environment overrides into default production settings. |
| `backend/app/main.py` | Opt-in Azure Monitor initialization before app construction; no local offline telemetry buffer; non-PII live/model startup trace. | Merge with dependency and tests after telemetry/privacy review. No classification/routing authority changes. |
| `backend/requirements.txt` | Add the Azure Monitor OpenTelemetry distribution. | Merge with tested lock. |
| `backend/requirements-lock.txt` | Reproducible Linux dependency resolution after local wheel-metadata TLS failure. | **Review portability first**: the Microsoft proxy index may not be reachable outside this environment; validate from a participant network before general adoption. |
| `backend/tests/test_telemetry.py` | Verify telemetry opt-in/out behavior without live service calls. | Safe with startup change; focused regressions passed. |
| `backend/app/agents/router_agent.py` | Local-only one-line life-safety term addition for `sparking` and explicit `electrical arcing`, addressing observed FIELD_HAZARD under-triage. | Bounded source merge candidate after integrated tests; **NOT DEPLOYED**. No generic `downed` trigger/category-wide elevation, LLM or raw-text classification, PII/audit/dedup changes. |
| `backend/tests/test_router_no_llm.py`; `backend/tests/test_pipeline_e2e.py`; `backend/tests/test_routes.py` | Reproduce exact typed live failure; cover case-insensitive electrical indicators, ordinary downed-tree non-escalation and preserved SEV1 duplicate/report/audit behavior. Strengthen pipeline and route sparking-line expectations to SEV1/15m/escalation rather than weaken them. | Safe with the local router fix. Red first: 4 failed/3 passed/16 deselected in 2.96s; focused suites: **23 passed in 2.40s**; final integrated telemetry/schema/API/pipeline/router/voice suites: **92 passed in 11.79s**. Existing lint findings remain; zero new diagnostics in Forge's original three-file comparison. These are offline tests, not live remediation. |
| `scripts/verify_live_demo.py`; `scripts/test_verify_live_demo.py` | Guarded, no-retry live acceptance helper; three signal writes require explicit opt-in. | Review as operational tooling; do not make test runs contact Azure or submit extra signals by default. |
| `frontend/Dockerfile` | Parameterize npm registry; keep public npm as fallback; omit audit/fund chatter during image install. | Safe after validating normal public-registry builds still work. |
| `azure.yaml` | Pass the optional npm registry build argument to the local frontend image build using azd's required list schema. | Safe with Dockerfile after parse/deploy validation; do not make a Microsoft-only feed an unconditional public prerequisite. |
| `specs/019-evolution-loop/{spec,plan,tasks}.md` | Record restricted deployment, safety defaults and measured verification; keep entries under appropriate headings. | Safe documentation update; leave live acceptance incomplete until evidence exists. |
| This report | Participant recipe, timings, evidence limits, access source, demo and deferred teardown. | Merge as dated operational evidence, not a timeless production-readiness guarantee. |

No main checkout, push or branch switch is needed during this run. The coordinator
alone may commit task-owned paths on `azure/overnight-2026-11-18`; review that diff
after the event before merging. Existing dirty `.squad` files, the other two lab
reports and other azd environments are unrelated and must not be staged.

**Authentication limitation:** this is a bounded demonstration deployment, not
an authenticated production service. An existing app registration is not proof
that end-user sign-in is configured. Do not enter personal information or invite
public traffic. History/transcript/ACS ingress routes remain fail closed until
server-verified ownership exists; do not bypass those controls to make a demo work.

**Deployed revision identity (nonsecret):** registry
`allclearq2lt63vq6i5f4acr.azurecr.io`, tag `azd-deploy-1794978486`.
Backend revision `allclear-q2lt63vq6i5f4-backend--azd-1794978515`,
image `all-clear/backend-p29-demo`,
digest `sha256:b28a4b339138a47141df3f64b73d85ccbf08dac3fbbca626f8655d8795729f9d`
(created 00:08:36.015 ET).
Frontend revision `allclear-q2lt63vq6i5f4-frontend--azd-1794978533`,
image `all-clear/frontend-p29-demo`,
digest `sha256:4252de6f6bd42badea70b2b3b4ac3ef33f68e14f63b879b2de064bbf4d8286ce`
(created 00:08:31.191 ET). Both revisions Ready; both apps retain minimum
one replica. Image identity proves what was deployed, not safety correctness.

**Local source differs from these deployed images.** Forge subsequently added
the narrowly scoped electrical-hazard regression fix and tests, **TESTED
LOCALLY, NOT DEPLOYED**. No fourth deployment, hotpatch or extra signal was
performed. The stored `AC-0001` remains the observed SEV2/non-escalated incident;
the source fix does not migrate it. Future authorized remediation/revalidation
must account for that existing incident without deleting or hiding its reports.

## Five-step 9:00 AM demo

**Do not present this as a ready or safety-correct demo.** Root page, live/model
badges and Trust interaction are browser-proven, but the prescribed power-line
signal failed mandatory SEV1/escalation acceptance. A 9:00 AM operator can show
the evidence and limitation transparently, or defer the demo; do not silently
substitute a different prompt to disguise the failed gate. Authenticated portal
views remain unverified. Use a desktop-width
window. Do not choose `?demo=loaded`, `?demo=hero`, simulate surge, or the
40-signal water scenario as evidence of live classification. Overnight verifier
submits exactly three signals; the morning operator's rehearsal is a separate
write and may attach to incidents already created overnight.

1. **Open the frontend root URL**, with no demo query parameters. The audience
   sees the incident-triage briefing room. Confirm the live service indicator
   and open backend `/api/health` in a second tab to show `mock_mode: false`.
2. Show the recorded result for **“There's a downed power line sparking on
   Oak Street near the school.”** Required: **SEV1 / 15m / human escalation**.
   Actual overnight result: **AC-0001 / SEV2 / 60m / not escalated**.
   Explain that this is a blocking safety defect, not success. Do not enter
   another overnight signal or promise a corrected live result. Only after a
   separately authorized fix/redeployment/revalidation may an operator type it
   in **“Describe the signal…”** and click **Send** as a passing demonstration.
3. Type **“My water bill is wrong, can someone call me?”** and click **Send**.
   This is a morning-operator action, not an instruction for extra overnight
   writes. The recorded result is **HUMAN_REQUEST**, **AC-0002**, **SEV3 / 240m**,
   queue **escalations**, reason **user_requested_human** and escalated true.
4. Show the recorded exact power-line duplicate: **ATTACH_TO_INCIDENT**,
   **AC-0001**, magnitude **2**, similarity **1.0** rather than a second incident.
   If a separately authorized morning run is performed, enter that exact text
   again and compare the incident ID; do not claim its still-SEV2 state passes.
   Click **Show decision receipt**
   to explain QueryAgent classification versus zero-LLM RouterExecutor rules.
   Every signal remains a report. Do not approve a public update.
5. In a separate tab open **https://ai.azure.com/?cid=learnDocs** as p29.
   Switch **New Foundry off → Keep building with Foundry → View all resources**,
   select the own-RG OpenAI resource, dismiss an upgrade offer with **Cancel**,
   then open **Shared resources → Deployments** and inspect the existing
   `gpt-5.1` and `text-embedding-3-small` rows.
   Compare the backend model evidence and Application Insights traces.
   These labels are verified against official documentation, **not an
   authenticated p29 browser**. Do not select **+ Deploy model**, upgrade the
   OpenAI resource or create a project. This account is `kind: OpenAI`, not an
   upgraded AI Services project; do not promise the newer Models + endpoints UI.

Portal navigation sources, checked by Beast at 00:05 ET:
[Create an Azure OpenAI model deployment](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/create-resource#deploy-a-model)
and [classic-only resources](https://learn.microsoft.com/en-us/azure/foundry/how-to/navigate-from-classic#classic-only-migration-required).
These support the route, not the claim that p29 has rendered those pages.

## p29 access and its source

The read-only role query included inherited assignments and group memberships.
No access to other RGs was exercised except the explicitly requested role inventory.

| Scope | Role | Assignment source |
|---|---|---|
| `rg-allclear-p29` | Owner | Direct user `c4894275-c7f1-499d-a0d3-cca1350415eb` |
| `rg-allclear-coach-backend` | Reader | Group `SG - Azure Days AllClear Participants` (`9cc5fccc-d880-4df5-92bc-f08f60372050`) |
| `rg-fabric-shared-use2-dev` | Reader; Foundry Project Manager | Group `SG - Azure Day Fabric Users` (`549dbd5c-e254-476e-8ab9-5d30a69a0813`) |
| Shared RG / `kv-fabric-shared-use2` | Reader; Key Vault Administrator | Same Fabric Users group |
| Shared RG / `shared-docintel-hack` | Contributor | Same Fabric Users group |
| Shared RG / `acsfabricshareduse2dev01` | Reader; Communication and Email Service Owner | Same Fabric Users group |
| Shared RG / `tin-iothub-fabrichack` | IoT Hub Data Contributor | Same Fabric Users group |

These are assigned RBAC roles, not successful data-plane tests. Key Vault Administrator can administer vault data (including secrets); Contributor on Document Intelligence permits resource management, subject to deny assignments/policies. No secrets or other shared-resource data were read. Both group display names were confirmed with read-only directory queries. No subscription-scope assignment appeared.

Final own-RG assignment inventory was unchanged: pre-existing Owner assignment
IDs `658bf96f-08be-fdb5-7dc2-f8a5cde27cbd` and
`e3862ed1-ca36-7805-0c1d-1ede77367c8d`. No role, policy, provider-registration,
application-registration, account-switch or login writes occurred.

## Teardown (NOT RUN)

**NOT RUN. Leave everything running for 9:00 AM.** Enabled Bicep resources
contain 10 top-level resources; Azure generated one smart-detector alert.
Kitty verified **11 actual top-level resources**,
all in `rg-allclear-p29`: two apps, environment, OpenAI, Cosmos,
Search, registry, vault, Insights, workspace and its global smart-detector alert.
All are eastus2 except Search eastus and the global alert. Backend minimum
replicas 1; frontend minimum replicas 1. No scheduled teardown.

The following is a deliberately gated **after-event-only Bash command**.
It deletes a fixed allowlist, never resources discovered by wildcard/tag/query.
Children are removed before parents where separately addressable management
resources exist; apps precede their environment/registry and monitoring alert
precedes Insights/workspace. Deleting the exact vault soft-deletes its secrets
with it: p29 lacks own-vault data roles, so do not grant roles or read/delete
secret values individually. Search index deletion similarly follows its exact
service's deletion. No purge, role change, resource-group deletion, azd
teardown, or cross-RG operation is included. These delete commands are documented,
**not executed or destruction-tested**.

```bash
set -euo pipefail
set +x
test "${AFTER_EVENT_CONFIRMATION:-}" = 'DELETE-ONLY-P29-AFTER-EVENT'
test "$(az account show --query user.name -o tsv)" = \
  'azuredays-arl26-allclear-p29@establishedcorp.com'
test "$(az account show --query id -o tsv)" = \
  '0e1d648b-17c8-4724-9405-8e84b4c565c4'
SCOPE='/subscriptions/0e1d648b-17c8-4724-9405-8e84b4c565c4/resourceGroups/rg-allclear-p29'
test "$(az group show -n rg-allclear-p29 --query id -o tsv)" = "$SCOPE"
P='allclear-q2lt63vq6i5f4'
delete_exact() {
  local relative="$1" api="$2" id="$SCOPE/providers/$1"
  printf 'Delete exact own-RG resource: %s\n' "$relative"
  az resource delete --ids "$id" --api-version "$api" --output none
  az resource wait --ids "$id" --api-version "$api" --deleted \
    --interval 10 --timeout 1200
}
delete_exact "Microsoft.App/containerApps/$P-frontend" '2023-08-01-preview'
delete_exact "Microsoft.App/containerApps/$P-backend" '2023-08-01-preview'
delete_exact "Microsoft.App/managedEnvironments/$P-env" '2023-08-01-preview'
delete_exact "Microsoft.CognitiveServices/accounts/$P-openai/deployments/gpt-5.1" '2023-10-01-preview'
delete_exact "Microsoft.CognitiveServices/accounts/$P-openai/deployments/text-embedding-3-small" '2023-10-01-preview'
delete_exact "Microsoft.CognitiveServices/accounts/$P-openai" '2023-10-01-preview'
for container in sessions audit_logs incidents; do
  delete_exact "Microsoft.DocumentDB/databaseAccounts/$P-cosmos/sqlDatabases/allclear/containers/$container" '2023-11-15'
done
delete_exact "Microsoft.DocumentDB/databaseAccounts/$P-cosmos/sqlDatabases/allclear" '2023-11-15'
delete_exact "Microsoft.DocumentDB/databaseAccounts/$P-cosmos" '2023-11-15'
delete_exact 'Microsoft.Search/searchServices/allclear-q2lt63vq6i5f4-search' '2023-11-01'
delete_exact 'Microsoft.ContainerRegistry/registries/allclearq2lt63vq6i5f4acr' '2023-07-01'
delete_exact 'Microsoft.KeyVault/vaults/allclearq2lt63vq6i5f4kv' '2023-07-01'
delete_exact "microsoft.alertsmanagement/smartDetectorAlertRules/Failure Anomalies - $P-insights" '2021-04-01'
delete_exact "Microsoft.Insights/components/$P-insights" '2020-02-02'
delete_exact "Microsoft.OperationalInsights/workspaces/$P-logs" '2022-10-01'
# The existing rg-allclear-p29 remains. Never purge soft-deleted resources.
```

Set `AFTER_EVENT_CONFIRMATION` manually to the exact gate text **only after the
event**. Review the allowlist against this report first. Any failed delete/wait
stops the sequence; inspect that exact own-RG resource instead of broadening
scope or retrying with force.

## Blockers and exact errors

- Attempt 1: **`npm error Exit handler never called!`**; direct
  `registry.npmjs.org` TLS failed. Local image recovery with a Microsoft package
  feed succeeded, but does not prove a successful azd deployment.
- Dependency resolver: **`received fatal alert: HandshakeFailure`** when
  retrieving PyPI wheel metadata. The Linux lock uses the verified Microsoft
  package proxy; external-network portability remains unproven.
- Attempt 2 exact error: **`azure.yaml line 27: cannot unmarshal !!map into []osutil.ExpandableString`**.
  `docker.buildArgs` must be a list for azd 1.37.3. Corrected and validated by
  local packaging before the **third and final attempt**, which succeeded.
  No second stack or additional deployment attempt is authorized.
- **Unresolved safety gate:** first required signal returned
  **`FIELD_HAZARD → OPEN_INCIDENT AC-0001; severity=SEV2; sla_minutes=60; escalate=false; action.escalated=false`**,
  not SEV1/escalation. Classifier severity indicators were `["downed","sparking"]`;
  it returned `requires_escalation=false`. Beast's source trace found the
  deterministic router's life-safety recognition does not include these
  indicators, so the field-hazard path maps to SEV2. The duplicate inherits that
  unsafe result. Do not downgrade the expected assertion or alter the sample.
- **Local fix is not live remediation:** `sparking` and `electrical arcing`
  now trigger the existing deterministic life-safety route in source. Exact
  reproduction tests failed before the change and all 23 focused routing/pipeline
  tests pass after it; the final combined seven-file suite passed **92 tests in
  11.79s** after strengthening the directly coupled route test. The branch-only
  fix has **not** been built into/deployed
  over the recorded revisions or live-validated; all deployment attempts and
  application acceptance writes remain consumed. Existing unsafe incident data
  is unchanged. Readiness remains **NOT READY**.
- Deployment URLs, browser/health proof, all three responses, embedding dedup,
  actual model invocation and Application Insights traces are proven.
  **Authenticated p29 Foundry portal visibility remains unverified.**
  Configured model names or `/health/models` alone are not proof
  that a request used that model.
- Empty CLI/REST quota responses (`[]`) are an evidence gap, not a capacity
  error or a reason to provision a second stack.
- Existing backend pytest cannot test live config: `backend/tests/conftest.py`
  forces `ENVIRONMENT=test` and `MOCK_MODE=true`. Live-config pytest is
  **skipped as unsupported**, not passed. The 85 regressions are mock/unit tests;
  the dedicated verifier supplies the bounded live acceptance lane.

## Participant Bash recipe

Run from the repository root in **Bash** (WSL/Git Bash/Linux), not PowerShell.
These commands are a source-reviewed recipe, not a claim that a fresh
participant has completed it. Only Kitty may execute Azure writes during this
overnight run. p29 already has an environment and stack: **do not create a
second environment or rerun this recipe against the running demo**.

Canonical sources: [`CONTEXT.md`](../../CONTEXT.md),
[`azure.yaml`](../../azure.yaml),
[`infra/main.bicep`](../../infra/main.bicep),
[deployment parameters](../../infra/main.parameters.json),
[knowledge seeder](../../scripts/seed_search_index.py),
[active plan](../../specs/019-evolution-loop/plan.md).

### 1. Guard the identity and existing resource group

Prerequisites: the tested branch, Azure CLI, azd, Docker server, Node/npm,
Python 3.11+ and backend dependencies. Schedule participant embeddings in
cohorts of **six plus this demo**; seven simultaneous deployments is the stated
limit. Do not discover capacity by creating extra stacks.

```bash
set -euo pipefail
set +x                        # no shell tracing of secret operations
SUB='0e1d648b-17c8-4724-9405-8e84b4c565c4'
EXPECTED_USER='azuredays-arl26-allclear-p29@establishedcorp.com'
RG='rg-allclear-p29'
ENV_NAME='p29-demo'
BRANCH='azure/overnight-2026-11-18'
EXPECTED_SCOPE="/subscriptions/$SUB/resourceGroups/$RG"
test "$(az account show --query user.name -o tsv)" = "$EXPECTED_USER"
test "$(az account show --query id -o tsv)" = "$SUB"
test "$(az group show --name "$RG" --query id -o tsv)" = "$EXPECTED_SCOPE"
test "$(az group show --name "$RG" --query location -o tsv)" = 'eastus2'
azd auth login --check-status   # check only; stop if expired, never log in/switch
az version --query '"azure-cli"' -o tsv
azd version
docker version --format '{{.Server.Version}}'
git status --short
```

For another participant, a coach must replace **all three** p29 identity,
own-RG and environment values with that participant's assigned values before
execution; never borrow the demo or shared RG. A mismatch/expired login is a
hard stop. Do not run `az account set`, login, provider registration, role,
policy, app-registration or subscription-scope writes.

### 2. Select the reviewed branch and create one environment

Only switch a clean participant clone; preserve any existing dirty worktree.
No command below touches main or creates a resource group. On a fresh clone
where the branch is not local, fetch that branch and create its tracking branch
first; do not reset existing work.

```bash
test -z "$(git status --porcelain)" || {
  echo 'STOP: preserve existing work; use a clean participant clone.'; exit 1;
}
git switch "$BRANCH"
test "$(git branch --show-current)" = "$BRANCH"
azd env new "$ENV_NAME" --subscription "$SUB" --location eastus2 --no-prompt
azd env set AZURE_SUBSCRIPTION_ID "$SUB" -e "$ENV_NAME"
azd env set AZURE_LOCATION eastus2 -e "$ENV_NAME"
azd env set AZURE_RESOURCE_GROUP "$RG" -e "$ENV_NAME"
azd env set MOCK_MODE false -e "$ENV_NAME"
azd env set DEPLOY_PHONE false -e "$ENV_NAME"
azd env set DEPLOY_REALTIME false -e "$ENV_NAME"
azd env set CREATE_ROLE_ASSIGNMENTS false -e "$ENV_NAME"
azd env set OPENAI_KEY_AUTH true -e "$ENV_NAME"
# Only on a network that cannot reach public npm; verify reachability first:
azd env set NPM_CONFIG_REGISTRY https://packagefeedproxy.microsoft.io/npm/ -e "$ENV_NAME"
```

Those azd settings contain **no secrets**. Do not use `azd env get-values`,
export a `.env`, store keys in azd, print ARM `listKeys` output, enable `set -x`,
or log environment/Container Apps secret values. Runtime secrets are evaluated
in Azure by ARM into Container Apps secrets; seeding may hold credentials only
in process memory.

### 3. Preview, then time one stack

```bash
az bicep build --file infra/main.bicep --stdout >/dev/null
preview_start=$SECONDS
azd provision --preview -e "$ENV_NAME" --no-prompt
printf 'Preview: %s seconds\n' "$((SECONDS-preview_start))"
# STOP unless the preview is entirely inside EXPECTED_SCOPE, creates no roles,
# and keeps embeddings on Standard. Search eastus; other enabled services eastus2.
deploy_start=$(date -u +%FT%TZ)
deploy_seconds=$SECONDS
set +e
azd up -e "$ENV_NAME" --no-prompt
deploy_rc=$?
set -e
printf 'Deployment start=%s end=%s seconds=%s exit=%s\n' \
  "$deploy_start" "$(date -u +%FT%TZ)" \
  "$((SECONDS-deploy_seconds))" "$deploy_rc"
test "$deploy_rc" -eq 0
```

Keep the timer running through the seed and acceptance steps for the **usable
participant path**, and separately report azd elapsed time. On failure inspect
the exact error and original ARM deployment status; ARM can continue after azd
exits. Retry only the same environment after terminal state, at most **three
total attempts**. A warm retry excludes initial build/provisioning work and is
not a cold participant estimate. Move Search eastus→eastus2 only if a real
Search capacity/region error requires it; Search eastus already succeeded here.
Never change embeddings from Standard, increase quota, or create a second stack.

### 4. Seed the own-RG knowledge index without secret files

Use the existing `scripts/seed_search_index.py` with **explicit** index/model
overrides: its legacy defaults are not this deployment's configuration.
Runtime knowledge retrieval uses the supported `id`, `title`, `content`,
`snippet`, `department`, `category`, `tags` and `content_vector` fields.
Do not run `backend/scripts/seed_knowledge_base.py` unchanged: its Entra-only
embedding authentication needs a data role that this lab does not create.

The following wrapper queries **only the guarded own RG**, captures credentials
directly into Python memory and supplies them only to the seeder child process.
It does not print, persist or place keys in shell history/azd. Keep shell tracing,
HTTP tracing and terminal session recording off; do not dump process environments.
The branch's backend dependencies must already be installed in this Python.

```bash
export EXPECTED_USER SUB RG  # identity/scope only; never export secret values
seed_seconds=$SECONDS
python - <<'PY'
import json
import os
import subprocess
import sys

def az_json(*args):
    result = subprocess.run(
        ["az", *args, "--output", "json", "--only-show-errors"],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)

account = az_json("account", "show")
assert account["user"]["name"] == os.environ["EXPECTED_USER"], "Identity mismatch"
assert account["id"] == os.environ["SUB"], "Subscription mismatch"
rg = os.environ["RG"]
group = az_json("group", "show", "--name", rg)
assert group["id"].lower() == (
    f"/subscriptions/{os.environ['SUB']}/resourceGroups/{rg}"
).lower(), "Scope mismatch"
assert group["location"] == "eastus2", "Region mismatch"
resources = az_json("resource", "list", "--resource-group", rg)

def one(resource_type):
    matches = [
        r for r in resources
        if r["type"].lower() == resource_type.lower()
    ]
    assert len(matches) == 1, f"Expected one {resource_type}; stop for review"
    return matches[0]["name"]

search = one("Microsoft.Search/searchServices")
openai = one("Microsoft.CognitiveServices/accounts")
search_keys = az_json("search", "admin-key", "show", "-g", rg,
                      "--service-name", search)
model_keys = az_json("cognitiveservices", "account", "keys", "list",
                     "-g", rg, "-n", openai)
model = az_json("cognitiveservices", "account", "show",
                "-g", rg, "-n", openai)
env = dict(os.environ)
env.update({
    "AZURE_SEARCH_ENDPOINT": f"https://{search}.search.windows.net",
    "AZURE_SEARCH_API_KEY": search_keys["primaryKey"],
    "AZURE_OPENAI_ENDPOINT": model["properties"]["endpoint"],
    "AZURE_OPENAI_API_KEY": model_keys["key1"],
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT": "text-embedding-3-small",
})
result = subprocess.run([
    sys.executable, "scripts/seed_search_index.py",
    "--index-name", "knowledge-base",
], env=env, check=False)
raise SystemExit(result.returncode)
PY
printf 'Knowledge seed: %s seconds\n' "$((SECONDS-seed_seconds))"
```

Only article IDs/titles, counts and timing should appear. Verify all documents
upserted; a partial seed is not acceptance. Do not use shared Search/OpenAI
resources, create another embedding deployment or grant a role to bypass errors.

### 5. Accept and record before claiming readiness

Set `FRONTEND` and `BACKEND` from the exact verified URLs in this report (nonsecret).

```bash
: "${FRONTEND:?Set the verified frontend URL}"
: "${BACKEND:?Set the verified backend URL}"
curl --fail --silent --show-error "$FRONTEND" >/dev/null
curl --fail --silent --show-error "$BACKEND/api/health"
curl --fail --silent --show-error "$BACKEND/api/health/models"
```

Inspect `mock_mode: false`. In a clean browser use the five-step script above;
submit the three specified signals **once each** and record intent, outcome,
incident ID, severity, SLA, escalation, magnitude and duplicate similarity.
Capture actual served-model evidence, embedding success, App Insights traces
and p29 Foundry portal visibility. A model-health configuration value, HTTP 200
HTML, unit-test pass, screenshot of a simulated board or a resource deployment's
Succeeded state cannot substitute for those checks. Keep readiness **NOT READY**
and report exact gaps if any fail. Leave the stack running for the event.

The optional scripted equivalent is
`python scripts/verify_live_demo.py --backend "$BACKEND" --output participant-live.json --submit-three`.
Run it **instead of**, never in addition to, the browser's three submissions.
It refuses an existing output file and never retries a POST, even on timeout;
an uncertain write requires investigation, not resubmission. Its JSON evidence
contains synthetic acceptance results, not credentials. The separate browser
check must remain read-only when the helper owns the three writes.

## Decision and execution ledger

All times are Eastern (UTC-05:00). Never record secrets, tokens, passwords, or connection strings.
Preparation/preflight ledger times through D12 are approximate minute-level
notes, not captured command start/end timestamps. Their verification order is
**before attempt 1 (23:47:40.5447848 ET)**. Precisely measured deployment,
packaging, seed and acceptance windows/durations are identified separately.

Local nonsecret verifier artifacts are in session
`bf916367-8877-4639-a05a-4b90d955b6db`, `files/`:
`beast-p29-live.json` (three exact results and timestamps),
`beast-p29-browser.json`, `beast-p29-preflight.json`,
`beast-p29-azure-metadata.json`,
`beast-p29-telemetry.json`, `beast-p29-dependencies.json`,
`beast-p29-model-spans.json`, `beast-p29-result.json`,
`beast-foundry-navigation.json`, plus
`beast-p29-briefing-room.png` and `beast-p29-glass-box-audit.png`.
They are local evidence references, not published URLs or credentials.

| ID | Time | Decision / evidence / reason |
|---|---|---|
| D01 | 23:36 | Confirm p29 before Azure work. Account and subscription matched; own RG exists and is empty. |
| D02 | 23:37 | Preserve the dirty worktree; create only the requested overnight branch. Do not modify main or existing unrelated artifacts. |
| D03 | 23:37 | Retain local Docker builds because the Docker server responds; remote ACR build is unnecessary. |
| D04 | 23:38 | Interpret the HARD RULE "No role assignments" as prohibiting all new role assignments, even inside own RG. The later instruction to keep RG-scoped assignments cannot override it. Investigate existing API-key support and Azure-resident secret references rather than create RBAC grants. |
| D05 | 23:38 | The current Bicep already has implicit resource-group scope and creates no RG or app registration. Make scope explicit; never use subscription deployment commands. |
| D06 | 23:38 | Disable optional phone/realtime for this chat-and-dedup demo. Keep live service mode; mock authentication, if needed, is separate from mock classification. All enabled resources except Search must be eastus2. |
| D07 | 23:38 | Do not reuse the existing azd environment or its unrelated deployment plan. Create `p29-demo` bound to own RG only. |
| D08 | 23:42 | Add `createRoleAssignments` (default true) and `openAiKeyAuth` (default false). Only `p29-demo` opts into no-role/key-auth mode. The OpenAI key is evaluated by ARM directly into a Container Apps secret, never an output or local file. Existing Cosmos/Search secrets stay Azure-resident. |
| D09 | 23:43 | Add workspace-based Application Insights and opt-in Azure Monitor SDK startup; disable local offline export storage and live metrics. Emit one non-PII startup trace naming live/mock mode and model. No prompt/body collection is enabled. |
| D10 | 23:45 | Direct PyPI wheel-metadata downloads failed with `received fatal alert: HandshakeFailure` using uv and Docker. Direct wheel downloads work. Resolve the Linux lock through the host's configured Microsoft package-feed proxy; emit that nonsecret index in the lock so Docker can reproduce installation. The temporary pip-tools Windows lock was replaced with the correct uv Linux lock (no pywin32). Review package-index portability before merge. |
| D11 | 23:47 | Docker uses `wincred`, not plaintext credential storage. No credential values were inspected. Retain the existing ACR admin-secret pull approach rather than create AcrPull roles. |
| D12 | Before attempt 1 | Proceed only after own-RG preview, 85 regressions and frontend build passed. Exact prep command timestamps were not retained; do not infer completion after the deployment start from rounded ledger notes. Existing unrelated `.azure/deployment-plan.md` is not overwritten or treated as p29 proof; this report and the active spec pack contain the p29 plan/evidence. No provider registration or subscription-scope commands are authorized. |
| D13 | 23:49-23:58 | Treat the failed azd command and still-running ARM deployment separately. Do not cancel, overlap provisioners or consume a retry until the original deployment becomes terminal. Local image validation is not another Azure deployment attempt. |
| D14 | 23:58 | Document npm proxy as an optional network workaround, not a universal registry requirement; keep the Dockerfile public-registry fallback. Distinguish warm retry timing from cold participant readiness. |
| D15 | 00:01 | Keep the restricted deployment subsection outside Key Entities and the Verification Matrix; restore consolidation verification tasks under their original heading. Mark T503 complete only from the recorded preview/test/build evidence. |
| D16 | 00:01 | Keep the morning script source-checked but unproven until Beast supplies browser/portal and exactly-three-signal evidence. `/api/health/models` alone can echo configuration and is insufficient served-model proof. No public update is approved during acceptance. |
| D17 | 00:01 | Preserve no-end-user-auth and fail-closed privacy limitations explicitly. Restrict demonstration content to synthetic examples; do not present resource access or an existing app registration as deployed sign-in. |
| D18 | 00:02 | Use the existing API-key-capable Search seeder with explicit `knowledge-base` and `text-embedding-3-small` overrides. Kitty verified runtime field compatibility; do not modify product code merely to add an unused queue field or use an Entra-only seed path without data roles. |
| D19 | 00:02 | Record independent own-RG ARM model/App Insights metadata separately from portal and data-plane evidence. Beast cannot use an authenticated browser profile or log in; rendered Foundry portal visibility remains an explicit gap even though p29 ARM reads succeeded. |
| D20 | 00:03 | Skip existing backend pytest against live config: its conftest forces test/mock settings. Use the focused-tested, explicit-opt-in live verifier for exactly three no-retry writes; do not rerun it through a browser submission or after an uncertain POST. |
| D21 | 00:05 | Correct the source-checked portal recipe to Foundry classic, because the deployed account is `kind: OpenAI`. Follow official Shared resources → Deployments navigation; never upgrade/create resources to obtain the newer portal UI. Signed-in p29 visibility remains unverified. |
| D22 | 00:06 | Original ARM deployment was observed Succeeded at 00:06:26 ET. Authorize attempt 2 only after this terminal state, on the same stack; no model/region changes or overlapping deployment. Exact ARM service duration is PT17M50.9427648S; approximately 18m46s is CLI-start-to-observation wall time. |
| D23 | 00:07 | Count the 1.9457583s azd schema-parse failure as attempt 2 despite no cloud writes. Correct `docker.buildArgs` map to supported list schema and validate locally before the final attempt. Stop after attempt 3 fails; do not relabel parse failures to evade the cap. |
| D24 | 00:07 | Official azd schema confirms `buildArgs` list syntax. Both images passed local-only `azd package --all` in 7.923088s (cache-warm); Kitty starts the final third `azd up` on the same guarded environment. Packaging does not reset or extend the deployment-attempt budget. |
| D25 | 00:09 | Final attempt 3 succeeded in 72.9490883s at 00:09:10.791 ET; deployment writes are now closed. Kitty seeds knowledge with process-memory keys; Beast may inspect read-only UI/health now but must wait for seed-ready before exactly three signal writes. Readiness remains NOT READY until all requested evidence, including portal rendering, is proven. |
| D26 | 00:09 | Beast's isolated browser proves the live root page, badges and Trust interaction with no writes/errors. The separate audit route explicitly declares local simulation; retain that label and never use its output as live Azure/Foundry evidence. Configured health/model badges remain distinct from actual served-model proof. |
| D27 | 00:09 | Knowledge seeding succeeded: 4/4 canonical documents in 11.375s, keys only in process memory. Seed-ready authorizes Beast's exactly-three no-retry acceptance writes; no further application writes are assigned to another agent. |
| D28 | 00:10 | Exactly three live POSTs completed. Power-line input failed required SEV1/escalation (actual SEV2/60m/not escalated); billing escalation and duplicate attachment passed. Keep NOT READY, disclose the safety failure prominently, preserve the original expectation/sample, and do not manufacture a passing demo using a different prompt. All deployment attempts and acceptance writes are consumed. |
| D29 | 00:10 | Record initial-start-to-acceptance elapsed 22m37.413s as a failed-path observation, not a successful participant estimate. Keep deployed infrastructure running for the event while the coordinator reports the blocker; do not perform unauthorized remediation/redeployments or additional POSTs. |
| D30 | After 00:10 | Kitty confirmed App Insights ingestion: 3 traces/24 dependencies with actual `chat gpt-5.1` → successful own OpenAI HTTP request correlation, plus successful embeddings/Search/Cosmos operations. Count that as real served-model/telemetry proof, but do not claim the absent startup-specific trace. |
| D31 | After 00:10 | Build the deferred teardown from Kitty's exact 11-resource inventory and explicit child dependencies. Keep a manual after-event gate, no discovery-based deletion, no purge and no KV data-role workaround. All teardown remains NOT RUN and deployment remains up. |
| D32 | After 00:10 | Kitty closed Azure work with attempts 3/3, unchanged role inventory, exact ready revisions/image digests and minimum replicas 1+1. Preserve these nonsecret identifiers for audit, leave the stack running for 9:00 AM, and report overall NOT READY despite healthy infrastructure. |
| D33 | After 00:10 | Beast independently persisted telemetry: 4 traces, two successful `chat gpt-5.1` spans and three successful `text-embedding-3-small` spans with matching own-resource HTTP operations. Record observed counts without claiming every ingestion item has arrived, startup-trace visibility, quota headroom or authenticated portal rendering. |
| D34 | 00:13 | Beast closed bounded acceptance and visually inspected the root screenshot. Final sanitized summary and correlated model-span artifacts validate as JSON; six verifier tests explicitly reject the observed SEV2/non-escalated result. Both Azure workers have stopped calls/writes, deployment remains up, safety and portal gaps remain unresolved. |
| D35 | 00:14 | Coordinator authorized Forge only a local deterministic-router regression fix and focused tests for the observed downed/sparking field hazard. No fourth deployment, hotpatch or extra POST is permitted. If tests pass, label the source change TESTED LOCALLY, NOT DEPLOYED; preserve all deployed evidence and NOT READY verdict. |
| D36 | 00:15 | Correct preview counting without changing actual inventory: preview displayed 12 rows, including two model deployments, not 12 top-level resources. Bicep enables 10 top-level resources; Azure's generated smart-detector alert makes 11 actual top-level resources. Database/secret children were not individually displayed in that preview. |
| D37 | 00:16 | Forge completed local-only deterministic life-safety terms `sparking`/`electrical arcing` plus exact-input and negative/duplicate/report/audit regressions. Red reproduction: 4 failed/3 passed; green focused routing/pipeline: 23 passed in 2.40s. No new lint findings; no Azure/network submissions. Label TESTED LOCALLY, NOT DEPLOYED, retain recorded image identity and unsafe AC-0001, and require separate authorization for any future deployment/revalidation. |
| D38 | 00:19 | Coordinator's integrated local run found one directly coupled stale route-test expectation: 91 passed/1 failed in 13.21s. Forge is strengthening that sparking-powerline route test from SEV2 to required SEV1/15m/escalation and rerunning the combined suite. Record this intermediate failure honestly; no cloud writes, live evidence changes or assertion weakening. |
| D39 | 00:20 | Forge strengthened `test_routes.py`'s directly coupled sparking-powerline expectation to SEV1/15m, `escalate=true`, `sev1_incident`, action status escalated. Final combined telemetry/schema/routes/pipeline/router/voice-safety/voice-endpoints suite: 92 passed, three dependency warnings, 11.79s. Local safety change is four files total (one production tuple line plus three test files), TESTED LOCALLY, NOT DEPLOYED. Preserve NOT READY, existing unsafe incident, consumed budgets and all measured deployment/acceptance timings. |
