AZURE DEMO NOT READY

Live URLs:
- Frontend: https://allclear-q2lt63vq6i5f4-frontend.happysmoke-f829312c.eastus2.azurecontainerapps.io
- Backend health: https://allclear-q2lt63vq6i5f4-backend.happysmoke-f829312c.eastus2.azurecontainerapps.io/api/health
- Foundry: https://ai.azure.com/?cid=learnDocs → **New Foundry off → Keep building with Foundry → View all resources → `allclear-q2lt63vq6i5f4-openai` → Shared resources → Deployments**. Navigation documented; authenticated p29 rendering **unverified**.

| check | result | time (ET) | note |
|---|---|---|---|
| Current functional status | **LIVE API/SAFETY/DESKTOP ALL PASS**; full request qualified | Final read-only health **02:05:13.231** | **5/9 deployments, 10 authorized signal POSTs; apps running**. Corrected desktop passed; clean audience queue verified at 01:51. Authenticated portal rendering and a measured clean passing participant run remain unproven. |
| Identity / scope | PASS | Initially 23:36; reconfirmed 01:23 | p29; subscription `0e1d648b-17c8-4724-9405-8e84b4c565c4`; only existing `rg-allclear-p29`. No account switch, login, role/policy/provider/app-registration writes. |
| Attempt 1 | CLI FAIL; ARM PASS | 23:47:40.545 start | CLI failed in **87.6847s**, `npm error Exit handler never called!`; ARM continued, actual duration **PT17M50.9427648S**, error null. Observed successful at 00:06:26. |
| Attempt 2 | FAIL before cloud writes | 00:06:59.560–00:07:01.506 | **1.9457583s**; `azure.yaml line 27: cannot unmarshal !!map into []osutil.ExpandableString`. Counted against cap; corrected map to supported list. |
| Attempt 3 | PASS, original stack | 00:07:57.842–00:09:10.791 | **72.9490883s**, cache-warm. Same resources; azd reported provisioning 4s/deploying 1m2s. |
| Attempt 4 | PASS, backend-only | 01:26:33.224–01:27:05.901 | **32.6767145s**, source `207b457`, no infrastructure/model reprovisioning. All seven live-verifier checks subsequently passed; later frontend attempt 5 recorded below. |
| Attempt 5 | **PASS, frontend-only** | 01:47:11.656–01:47:54.209 | **42.5539561s**, committed source `b26e397`; Ready/Healthy/100% latest traffic. **5/9 consumed, four unused**. Serving/public/local asset hashes match; actual desktop acceptance subsequently passed. |
| Knowledge seed | PASS | 00:09:39.292–00:09:50.660 | **11.375s**, 4/4 canonical documents in `knowledge-base`, `text-embedding-3-small`; keys only in process memory. |
| Original acceptance | **Historical safety FAIL**, preserved | 00:10:09–17 | AC-0001 opened **SEV2/60m/not escalated**, not required SEV1; AC-0002 human escalation passed; duplicate attached AC-0001/magnitude2/sim1.0 but retained unsafe severity. Client times 4373.1/2231.6/1942.8ms. Full immutable original results retained. |
| Safety source correction | DEPLOYED; LIVE PASS | 01:27:05.901 deploy; 01:29:54 acceptance | Narrow deterministic `sparking`/`electrical arcing` terms; **92 offline tests passed in 11.79s**; actual unchanged power-line sample now SEV1/escalated. Original AC-0001 severity was not rewritten. |
| Backend recovery acceptance | **All seven checks PASS** | 01:29:44.664–54.441 | Exact same samples: **OPEN AC-0003 SEV1/15m/escalated**, OPEN AC-0004 human SEV3/240m/escalated, ATTACH AC-0003/magnitude2/sim1.0 retaining SEV1/escalation. Client 4009.4/2711.2/2329.9ms; no changed verifier/input or retry. |
| Recovery browser / telemetry | **PASS, fresh recovery evidence** | Browser after recovery; dependencies ≥01:29:40 | Root HTTP 200, 1653.1ms; zero errors/writes. **All three** fresh `chat gpt-5.1` spans correlate to own OpenAI HTTP 200s; three embedding spans/four embedding HTTP 200s (extra knowledge lookup), fresh Search/Cosmos success. New-revision window has four traces. No original counts reused. |
| Real frontend Send rehearsal | **PASS, exactly one extra POST** | 01:36:27.474 | Typed original power line → actual **Send** → same-origin frontend `/api/signals` → live nginx/backend HTTP 200; **2528.0ms** client/2096ms processing. **ATTACH AC-0003, magnitude3, SEV1/15m/escalated, sim1.0**. Desktop displays SEV1/escalated. **Seven total authorized signal POSTs**, no retries; R2 magnitude2 snapshot unchanged. |
| Frontend accuracy recovery iteration | **LOCAL + DEPLOYED + LIVE PASS** | 01:45 validation; 01:49 proof | Five files, six tests/build/zero-warning ESLint pass. Matching live bundle; actual desktop receipt, attachment counter and null-sitrep copy all passed. |
| Corrected desktop signal 1 | **PASS**, real Send | 01:49:30.958 | Original FIELD_HAZARD → **OPEN AC-0005, SEV1/15m/escalated**; 3038.5ms client/2750ms processing. Actual desktop receipt opens; nonnull sitrep ready, approval gate present but not approved. |
| Corrected desktop signal 2 | **PASS**, real Send | 01:49:35.531 | HUMAN_REQUEST → **OPEN AC-0006, SEV3/240m/escalated**, `user_requested_human`; 2482.1ms client/2215ms processing. Desktop receipt/non-null sitrep/approval gate correct; no approval clicked. |
| Corrected desktop signal 3 | **PASS**, real Send | 01:49:38.962 | **ATTACH AC-0005, magnitude2, sim1.0, SEV1/escalated**; 2258.3ms client/2082ms processing. Desktop receipt works at 1440px, **3 signals → 2 incidents, attached counter 1**; **No sitrep returned**, null sitrep, no approval gate. |
| Corrected desktop capture | **ALL PASS** | 01:49:24.570–01:49:42.213 | Three same-origin real POSTs/HTTP 200, no API/state injection/retries/viewport resize/errors. All board/receipt screenshots visually inspected. Lifetime **10 POSTs**, no further signals planned. |
| Final audience queue / health | **PASS, observed** | Retirement 01:51:04.102–07.892; health **01:51:15.229** | **Six resolved / 0 active / counter6 / audit12**, backend healthy/live/Cosmos/GPT-5.1/no failover, frontend HTTP 200. Only AC-0005/6 status changed; all other fields and old AC-0001–4 full documents/ETags preserved. Next expected audience IDs **AC-0007/8**; not yet submitted. |
| Current desktop model proof | **PASS, actual real traffic** | 01:49:32–41 | All **three** `chat gpt-5.1` spans correlate by operation ID with own OpenAI HTTP 200; three embedding spans/three own deployment HTTP 200s. Not receipt-label or health-only proof. |
| Source / active revisions | **PASS, serving content verified** | Backend hash proof 01:36; frontend 01:49 | Backend router live SHA-256 matches committed/local source; frontend live-container/public/local bundle hashes match. Both Ready/Healthy/100% latest traffic. Same 11 resources/models/roles; **5/9 deployments**. |
| Models / p29 ARM permission | PASS, not rendered portal proof | 01:26:07 recheck | Own OpenAI account Succeeded/eastus2; `gpt-5.1` v2025-11-13 GlobalStandard150; `text-embedding-3-small` v1 **Standard50**. Direct guarded ARM account/deployments GETs succeed. |
| Authenticated Foundry portal | **UNVERIFIED** | 01:26–27 bounded browser | Public deployments shell HTTP 200 attempted an Entra auth redirect; guard blocked auth before request. No authorized signed-in browser connection found. No login/token/profile access. ARM reads do not prove rendered p29 model rows. |
| Local preparation / regression | PASS with existing warnings | Before attempt 1; 00:20 rerun | Preview 42s, 12 displayed rows including two model deployments (database/secret children not individually displayed); no new roles. Initial 85 tests/7.23s; frontend build/7.01s. Final **92 tests/11.79s**, six verifier tests. Existing Bicep/CSS/dependency/lint warnings remain. |
| Backend pytest against live config | SKIPPED, unsupported | Verified source | `backend/tests/conftest.py` forces `ENVIRONMENT=test`, `MOCK_MODE=true`; dedicated live verifier used instead. |
| Clean passing participant end-to-end timing | **NOT MEASURED** | One-stack constraint | Cold stages and later successful recovery were observed separately, not a clean-from-empty successful rerun. **35–45 minutes is a planning estimate**, not measured proof. |
| Participant branch / final public checks | **PASS** | 02:05 | Normal non-force branch-only publication verified at report commit `1ccb40e`; main unchanged. Frontend HTTP 200, backend healthy/live/Cosmos, active/last-served GPT-5.1/no failover and exact served UI bundle hash rechecked. **Zero additional POSTs**. |
| Fresh-install source correction | **LOCAL + BOTH ACTUAL LINUX CI PASS** | Published `3827b2d`, 02:14:37.245 | Initial CI397/two failures cleared by manifest/test-only pin matching deployed Search **11.7.0b2**. Fresh install118 packages; **399 backend/18.10s**, eval **60/60,1.000≥0.90**, frontend **22/5.11s**; Ruff/focused4 pass. [Backend CI44257347609](https://github.com/msftsean/all-clear/actions/runs/44257347609) success (pytest+eval); [Offline Smoke44257347515](https://github.com/msftsean/all-clear/actions/runs/44257347515) success, offline gate **1m45s/exit0**. Both source3827b2d; no Azure deployment/POST. |

**Total deploy time / participant estimate.** Initial start → deployed stack:
**21m30.246s**; → seed-ready: **22m10.115s**; → original failed acceptance:
**22m37.413s**. Including approximately 23:36 preflight, about **34 minutes**
elapsed to that failed gate. Backend-only recovery deployment took
**32.6767145s**, separately from fixture preparation/new acceptance.
The later frontend-only correction took **42.5539561s**. Both are warm
same-stack service deployments, not cold participant provisioning.
Backend recovery start → passing three-signal acceptance end
(01:29:54.440876 ET) was **3m21.216s**, including controlled fixture preparation;
acceptance itself was **9.776848s**. These are warm same-stack recovery timings,
not clean participant provisioning.
The 00:10–01:22 authorization wait is **not deployment time**.
No successful clean-from-empty participant run has been timed: creating a
second stack merely to measure it would violate the one-stack rule.
For planning, reserve **35–45 minutes after tools/login/quota are ready**,
based on the observed approximately 22-minute infrastructure/build path plus
preview, seed, acceptance and portal/network contingency; this is a conservative
estimate, **not an achieved completion guarantee**. Excludes tool/dependency
installation, login renewal, capacity waits, unavailable package feeds and
unverified portal access. Never advertise warm backend-only seconds as full
participant timing.

**Status:** 🟩 live API · 🟩 desktop · 🟩 real models/traces · 🟨 portal · 🟨 clean-run timing

**Report revision:** `2026-11-18-r4` · serving frontend `b26e397` / backend `207b457` · reviewed participant snapshot `3827b2d` · latest read-only health 02:05:13 ET.

## Changes and safe merge after the event

Branch `azure/overnight-2026-11-18`; recovery began at `207b457`, current runtime
source `b26e397` (backend unchanged from `207b457`); main untouched.
The complete original report and D01–D39 ledger are retained in that commit.
Stage only task-owned files; existing dirty `.squad` work, other azd environments
and the other two lab reports are unrelated.

**Inventory scope:** task-owned changes from baseline `8ae9276`
(`207b457`, `b26e397`, `3827b2d`, dated docs), **not the whole branch diff against main**.
Remote `origin/main` `16caa52` differs from local main `091953`; before our task
commits, GitHub comparison already showed baseline diverged **31 ahead/3 behind**.
Those pre-existing commits were already server-visible, not newly authored or
reviewed here. After the event, review/cherry-pick the task-owned commits and
revalidate the target; **do not wholesale merge/rebase this diverged branch**.
No main writes or fetch-merges occurred.

**Participant branch published:** at 02:05 ET a normal non-force push created
only `refs/heads/azure/overnight-2026-11-18` in existing `msftsean/all-clear`;
its remote SHA was verified against report commit
`1ccb40ee57ef0e44b2b5936dbf240f8bd96002f4`. This receipt changes documentation
only; reviewed runtime source remains `b26e397`.
No PR/merge/main push or main merge into the tested branch.
Coordinator reviewed the exact fetch/push origin, already-published base and
workflows: Azure SWA push deployments filter main only; this branch's push CI
uses mock mode/no Azure deployment credentials. Local main remained
`091953751907fa05832e49382d5eccbf1a55c511`.
The checkout recipe can fetch the published branch; no main update is required.
The subsequent manifest/test-only participant snapshot
`3827b2df4a237d3278ba6184b62216534257abf2` was normally pushed and its exact
remote ref verified at **02:14:37.245 ET**. Actual Linux Backend CI (pytest/eval)
and Offline Smoke both passed. This newer receipt does not change
the working Azure images or the preserved initial 02:05 publication receipt.

| Files | Why | Merge disposition |
|---|---|---|
| `infra/main.bicep`; `infra/main.parameters.json` | Explicit existing-RG scope, configurable role creation/key auth, workspace-based Insights and Azure-resident runtime secrets. | Review then merge together. Defaults retain managed identity/role creation; p29 alone opts into no-role/key-auth lab mode. Not a production key-auth recommendation. |
| `backend/app/main.py`; `backend/requirements.txt`; `backend/requirements-lock.txt`; `backend/tests/test_telemetry.py` | Opt-in Azure Monitor before app construction; no offline local telemetry buffer; guarded non-PII traces/tests. | Merge after privacy/dependency review. **Validate proxy-index portability**: this environment needed the Microsoft PyPI mirror after TLS metadata failure. |
| `frontend/Dockerfile`; `azure.yaml` | Optional npm registry build arg, public npm fallback, local builds; azd `buildArgs` list schema. | Safe after ordinary public-registry validation. Do not make the Microsoft feed an unconditional public prerequisite. |
| `frontend/src/allclear/{BriefingRoom.tsx,BriefingRoom.test.tsx,Canvas.tsx,Canvas.test.tsx,types.ts}` | Desktop real IncidentCard/receipt access; actual ATTACH counter with both resets; optional `attached_signals`/`sitrep_available` preserve demo/API compatibility and honest null-sitrep labeling. | Commit `b26e397500bc00f465a025363d17c548801a93cb`: red reproduction then **6 tests PASS**, build PASS, five-file ESLint zero warnings. No backend/infra/API/dependency changes or redesign. Matching deployed asset hashes and actual three-send desktop acceptance PASS. |
| `backend/app/agents/router_agent.py` | One-line deterministic life-safety term addition for `sparking` and explicit `electrical arcing`. | Bounded tested fix. No generic `downed` trigger, category-wide elevation, LLM/raw-text classification or PII/audit/dedup change. Recovery deployment status must follow live evidence. |
| `backend/tests/test_router_no_llm.py`; `backend/tests/test_pipeline_e2e.py`; `backend/tests/test_routes.py` | Exact typed failure, case-insensitive terms, ordinary-field-hazard negatives, preserved duplicate/report/audit behavior; strengthened stale sparking-line assertions. | Safe with fix. Red reproduction 4 failed/3 passed; focused 23 passed; integrated 92 passed. No lowered acceptance threshold. |
| `backend/requirements.txt`; `backend/tests/test_voice_tool_path.py` | Commit `3827b2df4a237d3278ba6184b62216534257abf2` aligns manifest Search SDK to **11.7.0b2**, already used since baseline in the unchanged lock/deployed image; strengthens voice SEV1/escalation/duplicate assertions, removes unused import/wrap lint. | Minimal participant reproducibility correction, not a beta upgrade or new production logic. Fresh manifest install/full399 backend/eval60/full22 frontend and both actual Linux CI workflows pass. No Azure redeploy needed or performed. |
| `scripts/verify_live_demo.py`; `scripts/test_verify_live_demo.py` | Explicit-opt-in, exactly-three, no-retry live acceptance; rejects observed unsafe result. | Review as operational tooling. Offline tests must never contact Azure or submit live signals. |
| `specs/019-evolution-loop/{spec,plan,tasks}.md`; this report | Current requirements, recovery authorization, evidence, recipe and cleanup. | Safe dated evidence; do not describe unresolved gates as complete. |

Original pre-fix image identities/digests are preserved in report commit `207b457`.
**Current recovery backend:** revision
`allclear-q2lt63vq6i5f4-backend--azd-1794983208`,
image `allclearq2lt63vq6i5f4acr.azurecr.io/all-clear/backend-p29-demo:azd-deploy-1794983198`,
digest `sha256:17ec76da9a6e4d053e77aa3b7242876d6abbff46803d5896be1f81024d13d79a`.
Ready/healthy at 01:29:05 ET, live/Cosmos/GPT-5.1/no failover; unchanged by
the frontend-only correction.
Minimum replicas backend 1/frontend 1; backend max 1; no teardown scheduled.
Packaging/deployment used clean committed backend
`207b45700e0cbbebe5b23fded728dff47d0998e8`, no untracked backend files;
committed/working router git blob both
`d941609e882e36bbed4a751477287018b4f286a0`. ARM confirms this latest Ready
revision is active and receives 100% ingress traffic. This is source/build/
revision attestation. Subsequently a parent-authorized narrow read-only exec
on that exact serving revision ran only
`sha256sum /app/app/agents/router_agent.py`; live and local file SHA-256 both:
**`b3dfc6338c01b09f73b970e45ec3e0e18a6dfa98a1107a10dde0b3f17b8dc8c7`**.
This **does verify serving router content**, superseding the earlier absence of
an in-container measurement. No content/environment/secret dump or app mutation.

**Current corrected frontend:** revision
`allclear-q2lt63vq6i5f4-frontend--azd-1794984456`,
image `allclearq2lt63vq6i5f4acr.azurecr.io/all-clear/frontend-p29-demo:azd-deploy-1794984448`,
digest `sha256:564ef351a29faa73578ec92788142d0d1f6942f96256c17ebd817cbb55ac0c50`,
Single/latest 100% traffic, active/Healthy/Provisioned.
`index-Co9HNnxP.js` (267497 bytes) has identical serving-container, public GET
and local-dist SHA-256:
`628e7cd782a52c988f62f4ac1f6728f01e4f0ff9f02581767a1eb15e364d1de7`.
Root/asset HTTP 200 confirmed at 01:49:01.627 ET. A transient rollout asset
assertion failed before the uncached GET confirmed the correct live asset;
this was a read-only check, not another deployment.

**Synthetic lifecycle, not retroactive incident correction.** Each explicitly
authorized retirement followed frozen acceptance capture, positive fixture/
evidence/ETag matching and status-only CAS. All summaries, raw attached reports,
severity, magnitudes, 1536-dimension embeddings and original timestamps were
preserved. Durable intent/completion records contain actor p29, reason, IDs,
old/new status, evidence hashes, before/after hashes and ETags.

| Operation | Only fixtures retired | Preserved history / verified resulting totals |
|---|---|---|
| `p29-synthetic-retirement-20261118T062853Z` | AC-0001/2 | Original unsafe SEV2 retained; magnitudes 2/1, reports 1/0; counter2, audit4. |
| `p29-audience-prep-retirement-20261118T063858Z` | AC-0003/4 | AC-0003 **acceptance magnitude2 → one UI rehearsal magnitude3 → resolved**, reports2 retained; counter4, audit8; older full docs/ETags unchanged. |
| `p29-final-desktop-retirement-20261118T065104Z` | AC-0005/6 | 01:51:04.102–07.892: preserve SEV1/escalated/15m/magnitude2/reports1 and SEV3/escalated/240m/magnitude1/reports0. Older AC-0001–4 full docs/ETags and full counter document unchanged. **Six resolved, zero active, counter6, audit12**. |

No deletion, counter reset, severity/embedding rewrite or report loss.
Final health passed **01:51:15.229 ET**. No fixture is active; expected first
audience IDs are **AC-0007/AC-0008**, assuming no intervening traffic.

**Auth/privacy limitation:** no production end-user login is established.
Use synthetic content only; history/transcript/ACS ingress stay fail closed.
Do not treat an app registration or an ARM permission as deployed user sign-in.

## Five-step 9:00 AM demo

**New live safety/dedup acceptance and corrected actual desktop Sends/receipts
all passed.**
Authenticated portal rendering and a measured clean successful participant run
remain unproven; overall report stays NOT READY. Final audience queue is
verified **zero active / six resolved / counter6**, health passed **01:51:15.229 ET**.
Original AC-0001's failed result remains history;
fixture retirement is controlled test preparation, not correction of a real incident.

1. Open the frontend root at desktop width, without demo query parameters.
   Show live mode and `/api/health` with `mock_mode:false`, `storage_mode:cosmos`.
   **Say:** “The live synthetic All Clear demo is working: it escalates hazards
   and attaches duplicates to one incident. These are test reports. No real
   emergency response or crew dispatch is being made.”
2. In **Describe the signal…**, type **“There's a downed power line sparking on
   Oak Street near the school.”**, click **Send**. Required: SEV1/15m/escalation.
   Expect **OPEN**, next ID **AC-0007**, **SEV1/15m/escalated**
   (verified preserved counter 6, not reset).
   This behavior was proven live on AC-0003 and desktop AC-0005.
   If another user has already submitted it,
   explain attachment honestly rather than promise a fresh opening.
   **Say:** “The deterministic router makes this a SEV1 incident, starts a
   fifteen-minute response clock and escalates it to a human.”
3. Type **“My water bill is wrong, can someone call me?”**, click **Send**.
   Expect next ID **AC-0008**, **HUMAN_REQUEST, SEV3/240m/escalations**,
   `user_requested_human` handoff; proven on AC-0004 and desktop AC-0006.
   **Say:** “The callback request goes to a human with a four-hour response
   target. It is not treated as the power-line emergency.”
4. Send the **exact first text again**. Show same incident and increased
   magnitude (**expected AC-0007, magnitude 2**), **SEV1/escalated**.
   Stay on desktop: click **Show decision receipt**. The verified 1440px path
   shows ATTACH/SEV1/15m/similarity/citations; no resize or extra signal needed.
   Show **3 signals → 2 incidents, 1 attached report** and **No sitrep returned**
   on the attach path. First-opening paths may show a ready sitrep/approval gate;
   attachment does not invent a new sitrep/gate. Do not approve public updates.
   **Say:** “Three signals become two incidents. This duplicate remains a
   report on the same SEV1 incident. It does not create another emergency or
   generate a new sitrep, and nothing public is approved automatically.”
5. In Foundry follow the exact classic path at the top; cancel any upgrade offer.
   Inspect existing model rows only, then show actual Insights model/embedding
   dependencies. **Authenticated portal rendering remains unverified.** Never
   select +Deploy model, upgrade the resource or create a project to reach this view.
   **Say:** “Azure permissions and real request telemetry confirm GPT-5.1 and
   the Standard embedding deployment. Signed-in Foundry rendering was not
   independently verified overnight, and the participant time remains an estimate.”

Official navigation sources:
[OpenAI classic deployments](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/how-to/create-resource#deploy-a-model),
[classic-only resources](https://learn.microsoft.com/en-us/azure/foundry/how-to/navigate-from-classic#classic-only-migration-required).
The resource is `kind:OpenAI`, not an upgraded AI Services project.
Avoid simulated boards, Muni Water surge (40 writes), and the locally simulated
audit route as substitutes for live evidence.

## p29 shared Fabric access and source

Read-only role inventory included inherited/group assignments; no shared data was queried.

| Scope | Role | Source |
|---|---|---|
| Own `rg-allclear-p29` | Owner | Direct p29 object `c4894275-c7f1-499d-a0d3-cca1350415eb` |
| `rg-allclear-coach-backend` | Reader | AllClear Participants group `9cc5fccc-d880-4df5-92bc-f08f60372050` |
| `rg-fabric-shared-use2-dev` | Reader; Foundry Project Manager | Fabric Users group `549dbd5c-e254-476e-8ab9-5d30a69a0813` |
| Shared `kv-fabric-shared-use2` | Reader; Key Vault Administrator | Same Fabric Users group |
| Shared `shared-docintel-hack` | Contributor | Same Fabric Users group |
| Shared `acsfabricshareduse2dev01` | Reader; Communication and Email Service Owner | Same Fabric Users group |
| Shared `tin-iothub-fabrichack` | IoT Hub Data Contributor | Same Fabric Users group |

Group names independently confirmed: **SG - Azure Day Fabric Users**, **SG -
Azure Days AllClear Participants**. Assigned roles are not successful data-plane
tests; no subscription assignment appeared. Own-RG assignment IDs
`658bf96f-08be-fdb5-7dc2-f8a5cde27cbd`,
`e3862ed1-ca36-7805-0c1d-1ede77367c8d` were unchanged after original deployment.

## Teardown command — NOT RUN

**Leave running for 9:00 AM.** Ten enabled top-level Bicep resources plus one
Azure-generated smart-detector alert = **11 actual top-level resources**.
All eastus2 except Search eastus and global alert. Review this exact allowlist
after the event. Deletes are documented, not destruction-tested. No RG deletion,
azd teardown, purge, shared-RG operation or new role is included.
The template's `targetScope = 'resourceGroup'`; it does not create a resource
group or invoke a subscription-scope deployment.
Deleting the exact vault soft-deletes its secrets; do not grant data roles to
delete/read them individually. Search indexes follow exact service deletion.

```bash
set -euo pipefail
set +x
test "${AFTER_EVENT_CONFIRMATION:-}" = 'DELETE-ONLY-P29-AFTER-EVENT'
test "$(az account show --query user.name -o tsv)" = 'azuredays-arl26-allclear-p29@establishedcorp.com'
test "$(az account show --query id -o tsv)" = '0e1d648b-17c8-4724-9405-8e84b4c565c4'
SCOPE='/subscriptions/0e1d648b-17c8-4724-9405-8e84b4c565c4/resourceGroups/rg-allclear-p29'
test "$(az group show -n rg-allclear-p29 --query id -o tsv)" = "$SCOPE"
P='allclear-q2lt63vq6i5f4'
delete_exact() {
  local id="$SCOPE/providers/$1" api="$2"
  printf 'Delete exact own-RG resource: %s\n' "$1"
  az resource delete --ids "$id" --api-version "$api" --output none
  az resource wait --ids "$id" --api-version "$api" --deleted --interval 10 --timeout 1200
}
delete_exact "Microsoft.App/containerApps/$P-frontend" '2023-08-01-preview'
delete_exact "Microsoft.App/containerApps/$P-backend" '2023-08-01-preview'
delete_exact "Microsoft.App/managedEnvironments/$P-env" '2023-08-01-preview'
for model in gpt-5.1 text-embedding-3-small; do
  delete_exact "Microsoft.CognitiveServices/accounts/$P-openai/deployments/$model" '2023-10-01-preview'
done
delete_exact "Microsoft.CognitiveServices/accounts/$P-openai" '2023-10-01-preview'
for container in sessions audit_logs incidents; do
  delete_exact "Microsoft.DocumentDB/databaseAccounts/$P-cosmos/sqlDatabases/allclear/containers/$container" '2023-11-15'
done
delete_exact "Microsoft.DocumentDB/databaseAccounts/$P-cosmos/sqlDatabases/allclear" '2023-11-15'
delete_exact "Microsoft.DocumentDB/databaseAccounts/$P-cosmos" '2023-11-15'
delete_exact "Microsoft.Search/searchServices/$P-search" '2023-11-01'
delete_exact 'Microsoft.ContainerRegistry/registries/allclearq2lt63vq6i5f4acr' '2023-07-01'
delete_exact 'Microsoft.KeyVault/vaults/allclearq2lt63vq6i5f4kv' '2023-07-01'
delete_exact "microsoft.alertsmanagement/smartDetectorAlertRules/Failure Anomalies - $P-insights" '2021-04-01'
delete_exact "Microsoft.Insights/components/$P-insights" '2020-02-02'
delete_exact "Microsoft.OperationalInsights/workspaces/$P-logs" '2022-10-01'
# Existing resource group remains. No purge. Any failed delete/wait stops here.
```

Set the manual confirmation variable only after the event. Never broaden the
allowlist, discover deletion targets by wildcard/tag, or force past a failure.

## Current blockers and historical errors

- **Functional safety defect cleared:** the unchanged first signal opened
  AC-0003 in backend recovery and AC-0005 in the final desktop run, both
  SEV1/escalated. Their duplicates attached at magnitude 2 with SEV1/escalation
  preserved. Original failed results remain historical evidence.
- **Functional evidence complete:** new-request-scoped model/embedding telemetry,
  traces, browser, exact three-signal acceptance and narrow durable readback passed.
  No original trace counts were reused as recovery proof.
- **Full-request proof gap:** authenticated p29 Foundry deployment-table rendering
  unavailable. ARM listing permission and official navigation are proven, not UI.
  The isolated browser observed HTTP 200, then blocked
  `GET login.microsoftonline.com/organizations/oauth2/v2.0/authorize`;
  final URL was exactly `chrome-error://chromewebdata/`, with
  `rendered_text: ""`. No Azure authentication error text was returned:
  Azure CLI/azd remained authenticated; this browser had no authorized session.
- **Full-request timing qualification:** no clean-from-empty successful participant
  run was measured. Separate cold-stage and recovered functional evidence do not
  establish that claim; one-stack rule prevents a duplicate timed deployment.
- **Audience preparation passed:** corrected desktop three-send run and audited
  AC-0005/6 retirement verified. Zero active/six resolved/counter6/audit12,
  final live health/frontend HTTP 200 at **01:51:15.229 ET**. No more signal
  POSTs or maintenance planned; next expected IDs AC-0007/8 are not yet executed.
- **Historical, fixed:** attempt 1 npm exit-handler/TLS failure; attempt 2 azd
  buildArgs map schema error. PyPI metadata failed with
  **`received fatal alert: HandshakeFailure`**; Microsoft proxy enabled image build.
- **Limitations, not new capacity errors:** quota CLI/REST returned `[]`; actual
  models succeeded but quota headroom is unknown. Startup-specific trace query
  returned 0; four other traces/real dependencies are proven.
- Backend live-config pytest is unsupported. Public-registry/proxy portability,
  production sign-in and a clean-from-empty successful timing remain unproven.
- **Cleared UI accuracy defects:** the old missing desktop receipt, false
  aggregate zero and unconditional Sitrep ready were reproduced then fixed and
  verified by actual desktop Sends. Current receipt/counter/null-sitrep copy pass;
  old screenshots and mobile workaround are historical, not current defects.
- **Source-only CI follow-up:** initial post-publication failures were the stale
  voice SEV2 assertion and Search vector-query TypeError/fallback under freshly
  resolved SDK 12.1.0. Committed manifest/test-only fix matches proven SDK
  11.7.0b2; fresh local install/full tests/eval and both actual Linux Backend CI
  and Offline Smoke pass. Serving images and application code are unchanged.
- **Storage evidence limit:** an incident's origin summary/citations represent
  its first signal; the `reports` array contains attached duplicate text, not
  every original raw signal. Original AC-0001 magnitude=2/reports length=1;
  AC-0002 magnitude=1/reports length=0. Scripted API acceptance omitted
  `student_id_hash`, so no full raw conversation is persisted for that run.
  Normal UI supplies its own hash; no full conversation readback is claimed.
  Preserve
  observed records without claiming three raw report documents or adding an
  identity to the unchanged verifier merely to conceal this limitation.

## Participant Bash recipe — one stack, guarded scope

Run in Bash from a **clean reviewed clone**, with az/azd/Docker/Python installed,
an existing **clean isolated Python venv activated**, and existing login valid.
Do not overwrite another environment or install into global Python. Backend
dependencies are installed **after selecting the reviewed source below**,
even if another branch's dependencies were installed earlier. This setup is
excluded from the 35–45 minute estimate; it is not cold Azure deployment proof.
Never rerun fresh-environment
steps against the running demo. A different participant must replace **identity,
RG and environment together** with their assigned values. Cohort budget:
six participant embedding deployments plus this demo, not extra test stacks.
Tested tools: Azure CLI **2.93.0**, azd **1.37.3**, Docker server **29.9.3**.
Sources: [domain](../../CONTEXT.md), [azd](../../azure.yaml),
[Bicep](../../infra/main.bicep), [parameters](../../infra/main.parameters.json),
[seeder](../../scripts/seed_search_index.py), [plan](../../specs/019-evolution-loop/plan.md).

### 1. Guard identity; select source; install dependencies; create one environment

```bash
set -euo pipefail
set +x
SUB='0e1d648b-17c8-4724-9405-8e84b4c565c4'
EXPECTED_USER='azuredays-arl26-allclear-p29@establishedcorp.com'
RG='rg-allclear-p29'
ENV_NAME='p29-demo'
BRANCH='azure/overnight-2026-11-18'
SOURCE_COMMIT='3827b2df4a237d3278ba6184b62216534257abf2'
EXPECTED_SCOPE="/subscriptions/$SUB/resourceGroups/$RG"
test "$(az account show --query user.name -o tsv)" = "$EXPECTED_USER"
test "$(az account show --query id -o tsv)" = "$SUB"
test "$(az group show -n "$RG" --query id -o tsv)" = "$EXPECTED_SCOPE"
test "$(az group show -n "$RG" --query location -o tsv)" = eastus2
azd auth login --check-status
docker version --format '{{.Server.Version}}'
test -z "$(git status --porcelain)" || { echo 'STOP: preserve dirty work.'; exit 1; }
case "$(git remote get-url origin)" in
  https://github.com/msftsean/all-clear.git|https://github.com/msftsean/all-clear|git@github.com:msftsean/all-clear.git) ;;
  *) echo 'STOP: expected canonical msftsean/all-clear origin.'; exit 1 ;;
esac
git fetch origin  # branch exists; require the reviewed SOURCE_COMMIT to be published
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git switch "$BRANCH"
  git merge --ff-only "origin/$BRANCH"
else
  git switch --track "origin/$BRANCH"
fi
test "$(git branch --show-current)" = "$BRANCH"
# Allow later report-only commits, but require identical reviewed runtime inputs.
git diff --exit-code "$SOURCE_COMMIT" -- backend frontend infra scripts azure.yaml
python -c "import sys; assert sys.prefix != sys.base_prefix, 'STOP: activate a clean isolated Python venv first.'"
python -m pip install -r backend/requirements.txt
# Uses the default package index (normally public PyPI); if blocked, use your
# approved Microsoft PyPI mirror with --index-url, never disable TLS checks.
workflow_start=$(date -u +%FT%TZ); workflow_seconds=$SECONDS
azd env new "$ENV_NAME" --subscription "$SUB" --location eastus2 --no-prompt
for setting in "AZURE_SUBSCRIPTION_ID=$SUB" "AZURE_LOCATION=eastus2" \
  "AZURE_RESOURCE_GROUP=$RG" "MOCK_MODE=false" "DEPLOY_PHONE=false" \
  "DEPLOY_REALTIME=false" "CREATE_ROLE_ASSIGNMENTS=false" "OPENAI_KEY_AUTH=true" \
  "NPM_CONFIG_REGISTRY=https://registry.npmjs.org/"; do
  azd env set "${setting%%=*}" "${setting#*=}" -e "$ENV_NAME"
done
# Optional only where public npm is blocked and this mirror is reachable:
# azd env set NPM_CONFIG_REGISTRY https://packagefeedproxy.microsoft.io/npm/ -e "$ENV_NAME"
```

Mismatch/expired login is a hard stop; never switch accounts or renew login
autonomously. No provider, subscription, role, policy or app-registration writes.
Settings above are nonsecret. **No `azd env get-values`, secret `.env` exports,
keys in azd, shell tracing, HTTP debugging or secret output.** Runtime keys go
directly from ARM expressions into Container Apps secrets; seed keys stay in memory.
The Linux lock's Microsoft PyPI index must be reachable or reviewed for portability.

### 2. Preview and time the full provisioning/deployment stage

```bash
az bicep build --file infra/main.bicep --stdout >/dev/null
azd provision --preview -e "$ENV_NAME" --no-prompt
# STOP unless entirely EXPECTED_SCOPE, no roles, embeddings Standard,
# Search eastus and other enabled services eastus2.
start=$(date -u +%FT%TZ); start_seconds=$SECONDS
set +e
azd up -e "$ENV_NAME" --no-prompt
rc=$?
set -e
printf 'start=%s end=%s seconds=%s exit=%s\n' \
  "$start" "$(date -u +%FT%TZ)" "$((SECONDS-start_seconds))" "$rc"
test "$rc" -eq 0
```

Keep a second end-to-end timer through seed/acceptance. On failure inspect the
original ARM deployment: it can continue after azd exits. Never overlap attempts
or create another stack. p29's explicit cap is now nine total (three original +
six additional); others need their own authorization. Move Search only on an
actual region/capacity error; eastus succeeded here. Never change embedding SKU.
Backend-only recovery is **not** this fresh-provisioning stage's timing proof.

### 3. Seed knowledge with credentials only in process memory

Explicit overrides avoid the seeder's legacy index/model defaults. Runtime
Search fields are compatible; no seed-code modification was required.

```bash
export EXPECTED_USER SUB RG  # nonsecret scope only
python - <<'PY'
import json, os, subprocess, sys
def az(*args):
    p = subprocess.run(["az", *args, "-o", "json", "--only-show-errors"],
                       check=True, capture_output=True, text=True)
    return json.loads(p.stdout)
account = az("account", "show")
assert account["user"]["name"] == os.environ["EXPECTED_USER"]
assert account["id"] == os.environ["SUB"]
rg = os.environ["RG"]
group = az("group", "show", "-n", rg)
assert group["id"].lower() == (
    f"/subscriptions/{os.environ['SUB']}/resourceGroups/{rg}").lower()
resources = az("resource", "list", "-g", rg)
def one(kind):
    matches = [r["name"] for r in resources if r["type"].lower() == kind.lower()]
    assert len(matches) == 1, "Ambiguous own-RG resources; stop"
    return matches[0]
search = one("Microsoft.Search/searchServices")
model = one("Microsoft.CognitiveServices/accounts")
sk = az("search", "admin-key", "show", "-g", rg, "--service-name", search)
mk = az("cognitiveservices", "account", "keys", "list", "-g", rg, "-n", model)
endpoint = az("cognitiveservices", "account", "show", "-g", rg, "-n", model)
env = dict(os.environ, AZURE_SEARCH_ENDPOINT=f"https://{search}.search.windows.net",
           AZURE_SEARCH_API_KEY=sk["primaryKey"],
           AZURE_OPENAI_ENDPOINT=endpoint["properties"]["endpoint"],
           AZURE_OPENAI_API_KEY=mk["key1"],
           AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small")
raise SystemExit(subprocess.run(
    [sys.executable, "scripts/seed_search_index.py", "--index-name", "knowledge-base"],
    env=env, check=False).returncode)
PY
```

Verify **4/4** upserts. Do not print keys, process environments or connection
strings; do not use shared Search/OpenAI or grant roles for an Entra-only seeder.

### 4. Check read-only health, then exactly three acceptance writes

```bash
: "${FRONTEND:?Set the verified frontend URL}"
: "${BACKEND:?Set the verified backend URL}"
curl --fail --silent --show-error "$FRONTEND" >/dev/null
curl --fail --silent --show-error "$BACKEND/api/health"
python scripts/verify_live_demo.py --backend "$BACKEND" \
  --output participant-live.json --submit-three
printf 'Through seed/API acceptance: start=%s end=%s seconds=%s\n' \
  "$workflow_start" "$(date -u +%FT%TZ)" "$((SECONDS-workflow_seconds))"
```

Run the helper **instead of**, not in addition to, browser submissions. It
refuses reused output and never retries a POST, even on timeout. Investigate an
uncertain write rather than resubmit. Exact sequence: power line, water bill,
exact power-line duplicate. Require SEV1/escalation and same-ID magnitude 2.
Existing incidents can cause attachment; never falsely label that a new opening.
Do not reset/delete data to make a demonstration pass.

### 5. Confirm evidence and leave it running

Read-only browser root/Trust; actual model/embedding dependency telemetry;
Insights traces; model versions/Standard SKU; authenticated p29 Foundry view.
Configuration badges, mock tests and public portal HTML cannot substitute.
If any required gate is missing, retain NOT READY and name the gap. A passing
fresh-from-empty run remains **unproven** unless actually performed within the
one-stack constraint; do not infer it from separately observed stages.
Only after all checks truly pass, record the full usable-path timer:

```bash
printf 'All required checks verified: start=%s end=%s elapsed_seconds=%s\n' \
  "$workflow_start" "$(date -u +%FT%TZ)" "$((SECONDS-workflow_seconds))"
```

## Preserved history, decisions and evidence

Original full D01–D39 record: commit `207b457`, this path. Prep timestamps were
approximate; preview/85 tests/frontend build all preceded attempt 1. Measured
command and request windows above retain their actual durations. Times span
2026-11-17 evening through 2026-11-18 morning, Eastern (UTC-05:00); decision
minute labels are notes, not additional precision claims.

| IDs / time (ET) | Decision and reason |
|---|---|
| D01–D07 / preflight | Confirm exact p29/own existing RG, preserve dirty work/main, local Docker available; hard no-role rule wins; explicit RG scope, phone/realtime off, new p29 environment only. |
| D08–D12 / before attempt 1 | Managed identity defaults preserved; p29 key-auth ARM secrets only; workspace Insights/no offline buffer; Linux lock through Microsoft proxy; secure Docker wincred; preview/85 tests/build passed before deployment. |
| D13–D18 / recovery of initial packaging | Wait original ARM terminal; local images are not deployment attempts; document registry portability; correct spec headings; model badges are not invocation proof; keep no-login/fail-closed limitations; seed explicit correct index/model. |
| D19–D24 / 00:02–00:07 | ARM metadata is not portal UI; pytest forces mock; Foundry classic path; exact ARM duration differs from observation; count schema failure as attempt 2; list-schema packaging passed 7.923088s; third attempt was last then-authorized. |
| D25–D29 / 00:09–00:10 | Attempt 3/seed/browser succeeded; local audit remains simulation; exactly three POSTs exposed genuine safety failure; keep NOT READY and unchanged sample/assertions, report 22m37.413s as failed-path timing. |
| D30–D34 / after 00:10 | Independent model/embedding/trace evidence; fixed exact deferred teardown inventory; leave replicas 1+1; distinguish two visible chat spans from three embeddings; no startup/portal/quota-headroom claims; workers stopped. |
| D35–D39 / 00:14–00:20 | Authorize local-only bounded fix; correct preview count (12 rows versus 11 actual top-level); red→23 green; stale route expectation caught (91 pass/1 fail/13.21s), strengthened then 92 passed/11.79s. No live remediation then; cap 3/3 respected until new user authorization. |
| D40 / 01:22:30 | User: **“Ok you have 6 more attempts. Make it happen.”** Authorizes six additional attempts, total max nine; preserve all original evidence. Parent reconfirms p29/azd at 01:23, same branch/source `207b457`. |
| D41 / 01:25 | Only Kitty deploys backend and may audit/CAS-retire two confirmed synthetic fixtures; Beast owns fresh three writes. No deletion/report loss/severity or embedding rewrite/counter reset. NOT READY pending actual recovery and portal evidence. |
| D42 / 01:26 | New guarded ARM account/deployments GETs prove p29 listing permission, not authenticated browser rendering. Keep the two forms of evidence distinct; no unauthorized login/profile/cookie/token access. |
| D43 / 01:27 | Consolidate stale repeated narrative into current summary plus immutable initial history. Estimate participant time from observed cold stages; exclude authorization wait and never equate backend-only recovery with fresh end-to-end provisioning. |
| D44 / 01:27 | Backend-only attempt 4 succeeded in 32.6767145s, 4/9 consumed. Do not equate deployment exit with new acceptance; Beast waits for audit/CAS fixture retirement completion. |
| D45 / 01:27 | Original fixture identity was positively matched, including creation window, summaries, severity, report counts, embeddings and ETags. Document origin-summary versus raw-duplicate-report storage accurately; no full raw origin/session persistence claim or changed verifier identity field. |
| D46 / 01:28:53–55 | Conditional audited retirement completed for only AC-0001/AC-0002. Only status changed; original unsafe severity, reports, origin summaries, embeddings and counter=2 preserved. Four durable audit documents; not real-incident remediation. |
| D47 / 01:29 | New backend revision/digest Ready and healthy, frontend/models unchanged; Beast authorized exactly three new no-retry POSTs with immutable original verifier/input shape and a new filename. Readiness remains blocked pending actual results and authenticated portal evidence. |
| D48 / 01:29:44–54 | Exactly three new authorized POSTs passed all seven immutable-verifier checks: AC-0003 opens SEV1/15m/escalated; billing AC-0004 escalates; exact duplicate attaches AC-0003/magnitude2/similarity1.0 with SEV1 retained. No changed sample, extra identity field, retries or counter reset. Record functional PASS without claiming authenticated portal UI or a fresh cold deployment. |
| D49 / 01:30:45 | Scoped Cosmos readback proves old fixtures unchanged since audited retirement, stored new AC-0003/AC-0004 business fields and exact attached duplicate, four incidents/counter4 and four maintenance audit documents. Origin summaries/citations and one attached duplicate report are represented; do not claim all three raw signal texts were independently persisted as report documents. |
| D50 / 01:32 | Fresh-only recovery telemetry proves all three model calls, three embedding spans/four HTTP embedding requests including knowledge lookup, own Search/Cosmos success and four new-revision traces. Six signal POSTs at that point. Functional recovery passes; authenticated portal rendering and a clean passing participant timing remain unproven. |
| D51 / 01:33 | Kitty attested clean committed backend packaging, matching committed/working router blob and active Healthy new revision receiving 100% traffic. Same 11 top-level resources, model SKUs and unchanged role assignments. No in-container source-hash fetch or stronger provenance claim. Four of nine deployment attempts used; five remain unused. |
| D52 / Pre-UI freeze | Beast froze bounded recovery: functional checks pass, portal rendering unverified; separate clean participant timing is not proven. Seven new JSON artifacts validated; verifier unchanged from `207b457`. Six signal POSTs then; later one-send rehearsal separately authorized below. |
| D53 / 01:35:33 | Coordinator explicitly authorizes one additional real frontend Send rehearsal of the original power-line text after Beast notifies Kitty. Expected AC-0003 attachment/magnitude3/SEV1/escalation; no retries, batch or counter reinterpretation. Hold report freeze for actual click/network/screenshot proof; six POSTs so far, seven only if submitted. No extra Azure calls just for reporting or deployments for unavailable browser authentication. |
| D54 / 01:36 reported | Parent separately authorized one narrow read-only exec on the exact serving backend revision. Live router SHA-256 equals local `b3dfc6338c01b09f73b970e45ec3e0e18a6dfa98a1107a10dde0b3f17b8dc8c7`; no code/env/secret dump or mutation. This supersedes the earlier lack of in-container source proof without changing attempt count. |
| D55 / 01:36:27 | Real frontend Send rehearsal passed with one original power-line POST through same-origin nginx: AC-0003 attachment/magnitude3/SEV1/escalation/similarity1.0. Total seven signal POSTs; original R2 magnitude2 evidence unchanged. Desktop receipt trigger is absent; verified same-page 430px View button opens receipt without another POST. Document workaround and separate footer escalation label rather than claim an untested desktop click or patch UI unnecessarily. |
| D56 / After UI capture | Coordinator authorizes audit/CAS status-only retirement of positively confirmed synthetic AC-0003/AC-0004 after Beast completion. Preserve all business data except status, counter4, every report/embedding and the magnitude2→3 rehearsal history; expected four resolved/zero active/eight maintenance audit documents. No extra signal/deployment. Morning next expected incident AC-0005, never a counter reset. |
| D57 / UI evidence review | Disclose desktop receipt absence, incorrect browser-local attached aggregate 0 and unconditional Sitrep ready despite null attach sitrep. Correct footer/typed network/receipt evidence supports live functionality; do not hide UX limitations or add unauthorized UI patches. |
| D58 / 01:38:58–01:39:01 | Final audience-prep retirement passed after exact evidence/ETag match: only AC-0003/AC-0004 status changed to resolved. AC-0003 magnitude3/reports2 and all non-status fields preserved; AC-0001/2 full docs/ETags and counter4 unchanged. Four resolved/zero active, eight durable maintenance audit docs. Preserve sequence and expect next audience AC-0005, not a reset. |
| D59 / 01:39:07.947 | Final health live/Cosmos/GPT-5.1/no failover. Leave apps running, teardown NOT RUN, seven total authorized signal POSTs, four of nine deployment attempts consumed. Functional recovery and exact UI path proven with documented UX workarounds; authenticated portal rendering and clean passing participant timing remain unproven. |
| D60 / After UI review | Parent authorizes minimal fixes for three directly coupled desktop accuracy defects: receipt access, attached-report aggregate and a false Sitrep ready claim for null sitrep. Parent owns code/tests/build/commit; Kitty may frontend-only deploy only after explicit validated-commit approval. Backend/clean queue/history unchanged; no preemptive deployment, extra POST or report freeze. Four of nine attempts remain used until another deploy actually starts. |
| D61 / 01:47 reported | Beast reports parent authorization for exactly three actual desktop Sends after Kitty's explicit corrected-frontend Ready signal, original inputs/order and no retries/mocked state. Lifetime POST count stays seven until execution (ten if complete). Capture/freeze first, then release Kitty only for the separately authorized exact AC-0005/AC-0006 synthetic retirement; no preemptive writes or final-ID claims. |
| D62 / 01:45 validation, subsequently committed | Parent's five-file UI correction committed `b26e397500bc00f465a025363d17c548801a93cb`: six focused tests, production build and targeted ESLint zero warnings pass; local bundle index-Co9HNnxP.js. Explicitly authorize Kitty frontend-only attempt 5 after guards, then exactly three original desktop inputs. Only after capture may confirmed AC-0005/6 be audit/CAS-retired; expected final six resolved/zero active/counter6/audit12 and next audience AC-0007/8 are plans until verified. |
| D63 / 01:47:11–54; proof 01:49 | Frontend-only attempt 5 passed in 42.5539561s; five of nine attempts consumed. Clean committed source, Ready/Healthy 100%-traffic revision and matching live-container/public/local asset hashes attest actual deployed UI correction. Backend/queue untouched. Beast may now perform exactly three approved desktop Sends; maintenance waits until frozen capture. |
| D64 / 01:49:24–42 | Corrected desktop acceptance fully captured/frozen: three real Sends, AC-0005 OPEN SEV1/escalated, AC-0006 human escalation, AC-0005 ATTACH/magnitude2. Desktop receipts work for all three at 1440px; attached count1, ready sitreps only when nonnull, null attach shows No sitrep returned/no approval gate. Ten lifetime POSTs, no retries/state injection/extra approvals; no more Beast signals. Release Kitty only for the already authorized positively matched AC-0005/6 audited retirement. |
| D65 / 01:49:32–41 | Fresh final desktop telemetry independently correlates all three GPT-5.1 spans to own OpenAI HTTP 200 and three embedding spans to own deployment HTTP 200. This is actual current-call proof, not a constant receipt/model-health label. |
| D66 / 01:51:04–15 | Final AC-0005/6 status-only CAS retirement passed; all other fields and old AC-0001–4 full docs/ETags preserved, full counter6 unchanged. Six resolved/zero active/audit12; final health/frontend passed 01:51:15.229. Leave apps running, teardown NOT RUN, 10 POSTs/5 of 9 deployments; next audience AC-0007/8 expected, not submitted. |
| D67 / Planned publication | Coordinator plans a guarded normal branch-only push after final docs commit so participants can fetch tested fixes. Exact existing origin/base/workflows reviewed; no main push/merge/PR, no force and no Azure push deployment on this branch. Publication remains pending verified remote ref; recipe handles tracking-new versus existing local branch without reset or merging main. |
| D68 / Merge-safety scope | Inventory means task-owned delta from 8ae9276, not all changes against main. Remote main16caa52/local main091953 differ; baseline was already server-visible and diverged31ahead/3behind before task commits. Publish the night branch for participant access only; after-event review/cherry-pick scoped task commits, never blindly merge/rebase the pre-existing divergent history. |
| D69 / 02:05 delivery receipt | Normal non-force push published only the overnight branch and verified remote SHA equals report commit `1ccb40e`; no main/PR/merge/tag/submodule push. Fresh read-only public checks passed frontend200, backend healthy/live/Cosmos, GPT-5.1 active/last-served/no failover and exact served UI content hash at 02:05:13.231 ET. Zero extra POSTs, no Azure authentication/configuration writes or deployment attempts. Publish this documentation-only receipt on the same branch; no runtime source change. |
| D70 / Initial post-publication CI | 397 passed/two failed: `tests/test_voice_tool_path.py::test_voice_analyze_routes_through_pipeline` retained SEV2 versus correctly fixed SEV1; `tests/test_azure_knowledge_service.py::test_vector_query_uses_supported_k_and_logs_no_signal_text` encountered vector-query TypeError/keyword fallback with SDK12.1.0 from unbounded `>=11.4`. Production knowledge code and baseline/current lock were unchanged; deployed/local SDK remains11.7.0b2. |
| D71 / Source-only correction | Commit3827b2df4a237d3278ba6184b62216534257abf2 changes only requirements Search pin to existing11.7.0b2 and stronger voice SEV1/escalation/duplicate test/format cleanup. New isolated manifest install resolves118packages: full399 backend PASS18.10s, post-format4 PASS7.10s, Ruff format/check PASS; unchanged evaluation60/60 accuracy1.000≥0.90; fullfrontend22 PASS5.11s. No production application-code/image/lock/Azure deployment/POST changes. Recipe pins this participant snapshot, distinct from serving207/b26; actual CI rerun/publication verification pending. |
| D72 / 02:14:37 publication; both actual CI PASS | Normal branch-only push of3827b2d exact remote verified, main/apps unchanged. Actual Linux Backend CI44257347609 completed success (full pytest/eval); Offline Smoke44257347515 success, offline gate1m45s/commandexit0. Both original CI failures resolved for382 without Azure deployment. Only attached gh watch, no manual dispatch/Azure/POSTs; five of nine deployments/ten signal POSTs unchanged. |
| D73 / Participant setup ordering | Require an already activated clean isolated venv, then reinstall reviewed backend/requirements.txt after branch checkout/source382 guard. Prevent a preinstalled main-branch SDK12.1 environment bypassing the pin; do not overwrite another venv or global Python. Start deployment/workflow timer after dependency setup;35–45min estimate excludes installation and still is not clean cold-run proof. |

Nonsecret local evidence lives under session
`bf916367-8877-4639-a05a-4b90d955b6db`, `files/`:
`beast-p29-live.json` (original probe `p29-acceptance-ebb095f68c234aff8307f39660d3fa3c`);
`beast-p29-browser.json`, `beast-p29-preflight.json`,
`beast-p29-azure-metadata.json`, `beast-p29-telemetry.json`,
`beast-p29-dependencies.json`, `beast-p29-model-spans.json`,
`beast-p29-result.json`, `beast-foundry-navigation.json`,
`beast-p29-portal-arm-permissions-r2.json`,
`beast-p29-portal-browser-r2.json`, and original browser screenshots.
Recovery evidence: `beast-p29-live-r2.json` (probe
`p29-acceptance-9ea0b5f080ec4c2c95f9a7d5e36811d9`), browser artifacts under
`beast-r2/`, `beast-p29-dependencies-r2.json`, `beast-p29-traces-r2.json`,
final complete artifact index/summary `beast-p29-result-r2.json`.
Separate UI rehearsal: `beast-p29-ui-rehearsal.json`,
`beast-p29-ui-rehearsal-summary.json`,
`beast-p29-ui-typed.png`, `beast-p29-ui-desktop.png`,
`beast-p29-ui-receipt-mobile.png`.
Final preserved/clean audience queue attestation: `beast-p29-final-demo-state.json`.
Corrected desktop acceptance: `beast-p29-final-desktop.json`,
`beast-p29-final-desktop-{1,2,3}-{board,receipt}.png` and typed screenshot.
Current model proof/final maintenance summary:
`beast-p29-final-desktop-model-spans.json`,
`beast-p29-final-desktop-summary.json` (three JSON files validated; seven PNGs).
New filenames preserve the original evidence.
