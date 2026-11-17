# Phase 1 Quickstart: Verify, release, rehearse

**Branch**: `event/arlington-2026-11-18` | **Revision**: R3, 2026-11-17 10:15 ET
**Target**: **TODAY 2026-11-17 13:00 Eastern**
**Status**: 🟨 Local baseline ready; 🛑 separate audience deployment not verified
**Source**: [plan](plan.md), [tasks](tasks.md), observed parent verification

This is the **future operator sequence**, not evidence that these steps ran.
The current assignment changes docs only. Stay on the event branch; do not rerun
setup-plan or create another feature. Live Azure testing is authorized once
the exact safe target is confirmed; no secret changes or private redteam reuse.

**Confirmed target update**: User selected a **separate audience app** in
`MCAPS-2026-segayle`, subscription `9f8986ed-ceb2-414d-8fcb-46d5cfc70618`.
Kitty's inventory and local ignored
[deployment plan](..\..\.azure\deployment-plan.md) supply exact resource names,
permissions and FQDN. Historical corporate-tenant auth is deferred until today's
demo works. At 10:15 ET user explicitly approved NEW separate audience resources
and NEW app-scoped secrets including coach key. No further elicitation for
ordinary isolated creation; no existing secrets may change/rotate. Parent
publishes this plan to GitHub FIRST, then implementation and technical deployment
handoff proceed.

## 1. Local offline checks (PowerShell)

From repository root, no Azure credentials required:

```powershell
$env:MOCK_MODE = 'true'
$env:PYTHONPATH = Join-Path $PWD 'backend'
python -m pytest backend\tests\test_surge_room.py backend\tests\test_surge_api.py -q
python -m pytest backend\tests -q
```

Initial baseline remains **15 focused /364 full passed**, Surge UI **5 passed**.
Latest post-fix evidence: **26 focused**, **375 full backend in 8.15s**,
**6 Surge UI tests**, typecheck and production build **PASS**. Include existing
`backend\tests\test_surge_rehearsal.py` in focused invocation.

In `frontend`, with parent-generated aligned lock:

```powershell
npm ci --ignore-scripts
npx vitest run src\allclear\surge
npm run typecheck
npm run build
```

Run sequentially and stop on **any** nonzero exit; a later command's success
must not hide an earlier failure. Lock update is necessary because Docker uses
`npm ci`; Bishop does not regenerate or edit it.

## 2. Optional local flow rehearsal

Use two operator-owned terminals. Backend, from root:

```powershell
$env:MOCK_MODE = 'true'
$env:PYTHONPATH = Join-Path $PWD 'backend'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend, from `frontend`:

```powershell
npm run dev -- --host 127.0.0.1
```

Use the printed frontend origin and existing development API proxy; verify it
reaches the selected backend before reporting. Open `/surge` locally, expand
Operator controls and Set key with a non-secret offline placeholder (mock
server key unconfigured), then reset/open and `/report?card=A`. Submit
**near-identical**, not broad paraphrase,
wording from two devices; observe receipt and board. `/surge/cards` generates
six local QR cards. No external QR service is needed.

```powershell
python backend\scripts\surge_rehearsal.py --base http://127.0.0.1:8000 --concurrency 40
```

The equivalent command using base `http://127.0.0.1:8017` was already observed
against the **real mock HTTP server**:
45 requests /43 signals /43 incidents /2 blocked /0 failed; median 0.13s,
p95 0.22s; SC-001 FAIL, SC-002 PASS. Broad paraphrase fragmentation is expected
with mock bag-of-words; it is not live semantic acceptance.

Close/drain/reset; confirm closed and zero counters/tiles. Stop only the local
servers you started, by terminal interrupt or specific PID; do not kill shared
processes by name. Operational records are not deleted by reset.

## 3. Resolve cloud blockers read-only (Kitty/operator)

Inventory the **approved MCAPS 2026 subscription** for today's separate audience
app and dependencies; never reuse the private redteam adapter or its secrets.
Parent's explicit-subscription `az account show` confirms **Enabled** and actual
tenant **`16b3c013-d300-468d-ac64-7eda0820b6d3`**. CNE/MCP wrong-context errors
do not establish MCAPS inaccessibility; Kitty now inventories with correct CLI
subscription context. Resource/FQDN readiness remains unverified.
Do not retry historical-tenant sign-in: expired TAP in
`cbc044cf-defc-4487-8475-4df2b4b237ca` and later Microsoft CNE account-membership
failure are historical blockers for tomorrow's deferred corporate path,
**not prerequisites for today's selected subscription**.

Historical reference only (not today's target):

- Subscription `a8a91d76-473f-49e2-ba21-1d394ba9a968`, `rg-all-clear-demo`.
- Apps `allclear-p74h22h3c2hqm-backend` / `allclear-p74h22h3c2hqm-frontend`.
- Recorded frontend:
  `https://allclear-p74h22h3c2hqm-frontend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io`.
  Both public health/state probes failed DNS; route availability remains unknown.
- Current local `azd env list --output json` was `[]`.
- MCAPS 2026 previously showed only internal `ca-allclear-redteam-20261001`;
  it remains **excluded**. Kitty's fresh inventory is pending.

Record only status-safe checks: key present/mapped (no secret output), private
coach availability, `mock_mode=false`, working chat/semantic embedding,
content-safety/knowledge/stores/audit dependencies, quota, one serving backend
replica/process, correct revision traffic, external frontend and `/api` proxy.
Key state is **UNKNOWN**, not proven blank. If the NEW audience app needs a key,
create it privately under the recorded approval; never touch existing secrets
or deploy exposed keyless mock controls.

## 4. Repair verifier and checkpoint candidate

Forge completed T019a–e's focused fixes/tests; no new packages, card grouping,
threshold or mock changes. Verifier requires complete A–D coverage, 4–6 separated
incidents, E separation, zero request/server errors, explicit network failures,
actual safe R outcomes and private environment credential intake. Preserve the
45 fixtures, 40 workers and HTTP-200 latency denominator/percentile.
Protected script intake is `--key-env <environment-variable-name>`; pass only
the variable name, never the key value, as an argument.
T019e's masked Operator controls /Coach key /Set key is implemented and tested.
Legacy query-key ingestion remains but is not approved credential delivery.
Actual keyed mock browser PASS additionally verifies missing-key 403, masked
entry/authorized Open, mobile report→board polling/QR, no key URL and no coach
header on public calls; closed/zero reset and helper shutdown confirmed.
Live semantic/load, real phones and accessibility/projection remain separate.

Run section 1 plus the new verifier tests; parent records tested commit and
lock alignment. No global threshold lowering/card buckets; if a live defect
later appears, isolate one evidenced cause with its own test.

## 5. Preview, approve, deploy separate audience target

Only after G2/G3/G4: follow Kitty's approved concrete resource plan. Reuse an
eligible existing audience app via application-only update if found; otherwise
validate Bicep/what-if and complete azure-validate/preflight/deploy handoff before
scoped audience resource creation under granted approval. Establish target-
specific deployment mapping, not blind `azd up`.
Capture previous healthy revisions/images/traffic where available; for first
release explicitly record no prior revision and use the tested fallback.
Infra lacks Surge key mapping, so preserve any manual mapping during image-only
updates. NEW audience app-scoped secrets, including coach key, are explicitly
approved; generate/deliver privately, never change/rotate existing secrets.

**Build-engine readiness PASS, 10:20 ET**: parent verified Docker daemon
**29.9.3**, **linux**, with `docker version` and `docker info`, after starting
Desktop **PID 30064**. azd 1.37.3 installed; proceed with existing
`remoteBuild:false` local build path. No duplicate Docker start, new packages or
remote-build/default change is needed. Actual image build remains to be verified.
Forge code tests/build now pass; Kitty still waits for published candidate and
technical deployment gates before deployment/exposure.

Deploy tested images only after build/resource/secret gates. Verify actual backend and
frontend revision/image/traffic, `/api/health`, `/api/surge/state`,
`/report`, `/surge`, `/surge/cards`, live model/dependency connectivity,
one backend replica/process, unauthorized control=403 and private coach control.
Record rollback to captured healthy revisions for both apps, or close/disable
first-release traffic and use verified fallback; no image/version match or health
failure → STOP. Do not delete operational records.

## 6. Authorized live rehearsal

Authorization is already supplied by the user's follow-up; readiness gates,
not another generic “go,” are blocking. Obtain coach key via approved private
channel; do not print it or use a key-bearing URL/process argument.

Using implemented/tested protected `--key-env` intake, provision the approved
`SURGE_COACH_KEY` in the operator process without literal values in command
history, then:

```powershell
# $AudienceFrontend is the exact verified public audience origin, not a guessed host.
python backend\scripts\surge_rehearsal.py --base $AudienceFrontend --concurrency 40 --key-env SURGE_COACH_KEY
```

The script's focused verification now passes. This live invocation remains
blocked by deployment/readiness gates, not pending key-input implementation.

Record sanitized candidate/revisions/time/replica, 45 outcomes, A–D incident
sets/10-per-card coverage, E separation, R actual outcomes, errors/failed/rate
limits and median/p95. All gates in [spec success criteria](spec.md#success-criteria-and-release-evidence)
must pass. Do not write raw bodies, device IDs or credentials to artifacts.
On failure use T022's isolate/test/one-change/redeploy/rerun loop with unchanged
fixture; measure live dedup-lock latency rather than claiming a bottleneck.

## 7. Clean, phone-check, rehearse, freeze

Close → wait for in-flight completion → reset tally → close → repeatedly verify
`open=false`, all counters zero, tiles empty, stable replica. Never delete
incidents/reports/audit or claim reset cleans persistent history.

Test five cellular phones, scan actual printouts at the verified origin,
check keyboard/focus/contrast/dictation and room projection, then run
[seven-minute show/fallback](run-of-show.md). Close/drain/reset again afterward.
By 12:30 ET parent records exact deployed/tested revision, GO or verified
fallback, rollback and checkpoint; 12:45 final closed-board/QR/fallback check.
Stage time is **13:00 ET** regardless of unresolved cloud access.
