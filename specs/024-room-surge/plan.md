# Implementation Plan: Room Surge recovery

**Branch**: `event/arlington-2026-11-18` | **Feature**: `024-room-surge`
**Revision**: R4, 2026-11-17 11:27 ET | **Spec**: [spec.md](spec.md)
**Event**: **2026-11-17 13:00 Eastern**, seven minutes
**Status**: ⛔ Partial Azure deployment; live acceptance FAILED; private-network correction in progress
**Progress**: `████░░░░░` **4/9 completion gates**
**Sources**: Cowork patch `e1eca20` on `7bed125`; current repository; parent
session verification; user's live-test authorization. No cloud changes in this pass.

**Confirmed target update**: User selected **a separate audience app** in
`MCAPS-2026-segayle`, subscription `9f8986ed-ceb2-414d-8fcb-46d5cfc70618`,
for today. Kitty owns read-only inventory and the local ignored
[deployment plan](..\..\.azure\deployment-plan.md). Initial inventory/deployment
completed; corrective network plan is pending parent validation. Historical
corporate-tenant recovery is deferred until today's demo works. Concrete
**Creation permission is now granted (10:15 ET)** for new separate audience
resources and NEW app-scoped secrets, including coach key. User: “yes create
away. the goal is to get this complete.” This supersedes the earlier unavailable
approval prompt. No repeated elicitation for ordinary isolated creation within
scope; never modify/rotate existing app secrets or touch the private adapter.
**Published-plan gate**: parent reviews, updates agent context, commits/pushes
this R3 checkpoint **before** implementation/deployment. Technical validation,
preflight and deployment handoff remain required. **Docker readiness PASS,
10:20 ET**: parent verified daemon **29.9.3**, **linux**, using `docker version`
and `docker info`. azd 1.37.3 is installed; existing `remoteBuild:false` local
build path can proceed without a remote-build/default change. Image build,
tests and deployment remain separate gates.

## Current Azure evidence — 11:27 ET (supersedes earlier pending entries)

**Published candidate**: `00141cd` includes application code, IaC and minimal
**88-package Linux npm lock**. Isolated full backend **375 PASS**; production-
image Surge tests **26 PASS**; frontend **6 PASS**, Node **22.23.5** build PASS.
Both immutable images were built, pushed and deployed. Parent-owned publication
gate is satisfied for this candidate; later corrective changes need their own
validation/checkpoint.

| Surface | Actual evidence / limit |
|---|---|
| Audience resources | MCAPS 2026, tenant `16b3c013-d300-468d-ac64-7eda0820b6d3`, **`rg-allclear-surge-20261117`**; initial **19-resource preview passed** |
| Models | GPT-5.1 capacity **150**, embedding capacity **50**, provisioning **Succeeded** |
| Backend | Managed identity's OpenAI User role confirmed; **one replica**; immutable image deployed |
| Frontend/control | Public health `mock_mode=false`; coach key configured; keyless control **403**. These do **not** prove report processing |
| Search knowledge | Existing seed script completed **12/12 All Clear articles**, **1536-dimensional vectors**; scoped operator OpenAI User on the new account; no repo secrets |
| **Actual live rehearsal** | **45 attempts: 0 accepted signals, 0 incidents, 2 safety blocks, 43 failures**. Single-report probe also **503**. **FAIL**, not a semantic/throughput result |
| Latency | Reported p95 **2.75s covers only two successful HTTP responses**; **invalid for SC-002 go/no-go** with 43 failures. Never label this a latency pass |
| Cleanup | Live room tally reset confirmed **CLOSED / zero**. Operational records were not purged |
| Confirmed root cause | Activity Log: inherited **`MCAPSGovDeployPolicies`**, policies **`CosmosDB_PublicNetwork_Modify`** and **`CosmosDB_LocalAuth_Modify`** force Cosmos public network and local auth **Disabled**. No private endpoint, and initial ACA environment has no VNet integration |

This is a confirmed infrastructure/policy reachability mismatch, **not an
application-template bug or live semantic-dedup failure**. Do not enable public
Cosmos access, turn local auth back on, request an exemption, or weaken policy.
Initial health and two blocked probes are not an audience-ready URL.

**Bounded correction (Kitty prepares; parent validates before execution)**:
new VNet-integrated ACA environment; Cosmos private endpoint plus private DNS;
managed-identity **SQL Built-in Data Contributor** access; NEW backend/frontend
apps using the current audience-owned models, Cosmos, Search and ACR. Preserve
initial apps and private redteam adapter unchanged. Reuse tested immutable images
unless a separately evidenced code defect requires a tested new candidate.
No new usable audience URL is yet verified.

Validate/preview the isolated network/identity resource delta first, then deploy
new apps, prove private Cosmos DNS/connectivity and managed-identity data access,
and require a successful single-report receipt plus board/persistence/audit
before rerunning the identical 45-request/40-worker fixture. Reset/close after
each controlled test window. If this path misses the decision window, use only a
rehearsed loaded replay or labeled mock fallback; never claim partial health as GO.

**Execution coordination, 10:18 ET**: Forge owns only the known rehearsal
false-pass fixes, protected `--key-env` credential intake, and small masked
board operator-entry UI, with focused tests. No new packages, card grouping,
threshold or mock behavior changes. Parent started Docker Desktop **PID 30064**;
Linux-engine readiness is now verified (29.9.3, linux). Kitty may prepare
isolated deployment configuration but must not expose/deploy the app until the
code-test/build gates pass. Repeated CNE account-mismatch screenshot belongs to
the deferred historical target; do not choose those accounts for MCAPS 2026.

**Verified integration update, 10:23 ET**: Forge implemented the focused verifier
fixes and protected `--key-env NAME` (default `SURGE_COACH_KEY`) plus masked
**Operator controls → Coach key → Set key**. **11 new verifier tests; 26 focused
backend tests pass; 6 Surge UI tests, typecheck and production build pass.**
Parent's full backend rerun: **375 passed in 8.15s**. Parent successfully reran
agent-context update and corrected generated root project paths/commands.
GitHub publication still pending. No new post-fix live rehearsal is claimed.
Explicit-subscription CLI confirms MCAPS 2026 **Enabled**, actual tenant
**`16b3c013-d300-468d-ac64-7eda0820b6d3`**. CNE/MCP context failures do not show
this target is inaccessible; Kitty's correct CLI resource inventory is pending.

## Summary

Preserve the shipped admission/tally wrapper and bounded pipeline. First lock
Spec Kit to observed facts; then restore authorized audience-target access,
harden the rehearsal's false-pass/error handling, verify the release candidate,
preview and deploy through existing infrastructure, run the **authorized**
40-worker live test, diagnose one failure/change at a time, and reset/close,
check real phones, rehearse and freeze. Do not invent a deployment or certify
semantic behavior from mock embeddings.

Setup-plan already ran with `SPECIFY_FEATURE=024-room-surge`; **do not rerun it
or create/switch a branch**. Parent runs update-agent-context and publishes the
checkpoint after reviewing this bounded documentation handoff, before execution.

## Technical Context

**Language/Version**: Python 3.11+; TypeScript 5; React 18

**Primary Dependencies**: FastAPI, Pydantic, Microsoft Agent Framework; Vite 5, Tailwind, Vitest; local `qrcode`

**Storage**: Process-local SurgeRoom and admission window; existing mock store offline, Cosmos incidents/reports/audit live

**Testing**: Focused/full pytest; Surge Vitest; `tsc` + Vite; real HTTP/browser smoke; live fixture rehearsal

**Target Platform**: Existing Azure Container Apps backend + nginx frontend

**Project Type**: Web application (Python backend and TypeScript/React frontend)

**Performance Goals**: A–D 40 reports; 45 total fixture requests; 40 workers; p95 <8s; approximately 1s state poll

**Constraints**: One backend replica/process; no raw board text; no new agent authority/platform; mock viable offline

**Scale/Scope**: One isolated audience deployment; existing bounded pipeline and three Surge browser routes

**Integration**: Existing chat, semantic embedding, content-safety, knowledge/search, persistence and audit paths; nginx `/api` proxy

**Compatibility**: No new public API or schema needed for recovery; preserve fixture, existing flags and measurement population

**Deployment uncertainty**: Exact audience resources, key status, live mode/models/quota, scale and version are operational verification gates, not assumed findings

## Constitution Check

*Design gate before Phase 0 and rechecked after Phase 1: PASS. This is not a live release GO.*

- [x] Data flow names PII redaction, existing retention/audit, embeddings/external
  services; public evidence excludes raw text and secrets.
- [x] QueryAgent classification-only, zero-LLM RouterExecutor, and ActionAgent's
  three tools are unchanged. Cards never influence routing.
- [x] Crisis, SEV1/statutory, PII, safety/sentiment, human request and
  low-confidence escalation remain mandatory.
- [x] Offline mocks exercise the same authority boundaries; semantic acceptance
  is explicitly separate from bag-of-words behavior.
- [x] Board facts reference incident results; sitrep/receipt factual claims
  retain source-record citations and human review before projection.
- [x] Backend tests, frontend typecheck/build, and live completion evidence are
  listed below; companion sites are unchanged.
- [x] Canonical `CONTEXT.md` vocabulary; no retired domain or broad governance edit.

## Project Structure

```text
specs\024-room-surge\
  spec.md  plan.md  tasks.md  run-of-show.md
  research.md  data-model.md  quickstart.md
  contracts\surge-api.md  checklists\requirements.md
backend\
  app\api\surge.py
  app\services\surge_room.py
  app\core\config.py  app\core\dependencies.py
  app\agents\pipeline.py  app\agents\router_agent.py
  scripts\surge_rehearsal.py
  tests\test_surge_api.py  tests\test_surge_room.py
  tests\test_surge_rehearsal.py  (11 added verifier regression tests)
frontend\
  src\App.tsx  src\allclear\surge\*
  package.json  package-lock.json  Dockerfile  nginx.conf
azure.yaml  infra\main.bicep  infra\main.parameters.json
.github\workflows\smoke-test.yml
```

**Structure decision**: Extend existing web application only. Immediate future
code scope is the rehearsal verifier plus minimal masked non-URL coach entry
in `SurgeBoard.tsx`, with their focused tests; expand only for a
reproducible, isolated release-blocking defect with matching spec/task/evidence.
The parent-generated npm lock alignment must accompany the release; this
planning pass does not edit it.

## Observed verification baseline

These are **already observed**, not commands rerun by this documentation pass.

| Evidence | Result / limit |
|---|---|
| Cowork patch application | Clean `git am`; `e1eca20` on `7bed125`; all required files and `/report`, `/surge`, `/surge/cards` routes present |
| Focused backend | `test_surge_room.py` + `test_surge_api.py`: **15 passed, 1.83s** |
| Full backend, `MOCK_MODE=true` | **364 passed, 8.22s** |
| Surge frontend Vitest | **5 passed**; React `act` warnings around QR tests |
| Frontend production build | **Passed**; existing Browserslist/gradient warnings |
| npm reproducibility | Initial alignment followed by minimal 88-package Linux lock published in `00141cd`; Node 22.23.5 build and immutable image builds passed |
| Actual local Chromium smoke | 390×844 `/report?card=A` → receipt; `/surge` poll updated 1 signal / 1 incident; local QR PNG and six card PNGs generated |
| Smoke caveat | Receipt joined an existing retained incident. No projection/readability/contrast/real-phone certification |
| Cleanup | Local servers stopped after reset: `open=false`, signals=0, incidents=0. Reset did **not** delete incidents/reports/audit |
| Real mock HTTP rehearsal | `python backend\scripts\surge_rehearsal.py --base http://127.0.0.1:8017 --concurrency 40`: **45 requests, 43 signals → 43 incidents**, 2 blocked, 0 failed; A–D 10 distinct each (40), E=3, R=2 blocked; median **0.13s**, p95 **0.22s**; **SC-001 FAIL, SC-002 PASS** |
| Post-fix backend | Forge: **26 focused passed**, including **11 new verifier tests**; parent full mock backend **375 passed in 8.15s** |
| Post-fix frontend | **6 Surge UI tests passed**, typecheck and production build passed; masked non-URL operator-entry path implemented |
| Post-fix actual browser integration | **PASS**, keyed isolated mock backend: missing key →403; masked Coach key /Set key →Open works; 390×844 report A →board polls 1 signal; local QR PNG generated; request observer saw no key in URLs and no `X-Surge-Key` on public calls; reset confirmed `open=false`, signals=0, incidents=0; both helpers stopped. **Not live semantic acceptance** |
| Target access | Explicit CLI subscription Enabled, tenant `16b3c013-d300-468d-ac64-7eda0820b6d3`; initial audience RG/deployment verified; replacement usable URL remains unverified |

The mock result is consistent with FR-005's existing bag-of-words caveat,
**not proof of a broken live semantic dedup**. Historical stand-in-server success
is not end-to-end acceptance.

## Phase 0 — Research decisions and blocked observations

[research.md](research.md) records completed repository-based decisions:
keep architecture, separate mock flow from live semantics, repair the verifier,
reuse existing infrastructure, and handle keys privately. No unresolved design
choice requires invented evidence. Operational findings remain explicitly blocked:

| Observation | Consequence |
|---|---|
| `azd env list --output json` → `[]` | No selected/recovered azd environment; do not run blind `azd up` |
| Current CLI subscription `MCAPS-Hybrid-REQ-51667-2023-segayl` (`4b27ac87-dec6-45d5-8634-b9f71bd1dd26`) | No AllClear apps found there |
| `MCAPS-2026-segayle` (`9f8986ed-ceb2-414d-8fcb-46d5cfc70618`) | **Enabled**, actual tenant `16b3c013-d300-468d-ac64-7eda0820b6d3`; initial RG `rg-allclear-surge-20261117` deployed; private adapter excluded |
| [Spec 022 task record](..\022-event-day-readiness-verification\tasks.md) | Historical target: subscription `a8a91d76-473f-49e2-ba21-1d394ba9a968`, `rg-all-clear-demo`; apps `allclear-p74h22h3c2hqm-backend` / `allclear-p74h22h3c2hqm-frontend` |
| Recorded frontend origin | `https://allclear-p74h22h3c2hqm-frontend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io`; `/api/health` and `/api/surge/state` both failed DNS, **not** an HTTP route-absence finding |
| Inventory in recorded subscription | Failed `AADSTS130504`: expired Temporary Access Pass; tenant `cbc044cf-defc-4487-8475-4df2b4b237ca`; human reauthentication required |
| Subsequent device-login attempt | Selected account does not exist in tenant Microsoft CNE / cannot access Azure CLI; external-user membership required. Correct target/account or administrator access must be confirmed; repeatedly logging the same account into that tenant will not resolve membership |
| Deployed coach key/live dependencies | `SURGE_COACH_KEY` **UNKNOWN**, not proven blank; model auth, semantic embeddings, quota, replicas and audience deployment not verified |

The early observations above are historical; deployment and failed live
rehearsal have now occurred as recorded in the 11:27 ET ledger.
Kitty independently owns approved-subscription inventory; do not duplicate
known-failing historical-tenant auth retries. The separate audience app in MCAPS
2026 is now the **confirmed target choice**, not a proven deployed app. No
historical tenant sign-in is required for today's path; corporate access work
is deferred. Creation approval is now granted; concrete resource plan, names,
dependency/capacity evidence and technical validation remain gates. Never reuse the private
adapter or its secrets. A five-to-fifteen-minute existing-app update is only an estimate
**after** access/environment/build prerequisites; reprovisioning duration unknown.

## Phase 1 — Model, contracts, quickstart

- [Data model](data-model.md): process-local projection, canonical persistent
  records, tally semantics, transitions and in-flight cleanup caveat.
- [Contract](contracts/surge-api.md): exact request/response fields, authorization,
  admission/status codes, frontend routes, and measurement contract.
- [Quickstart](quickstart.md): Windows local checks and gated deployment/rehearsal
  operator sequence; no key values or key-bearing URLs.
- Parent successfully updated agent context and published `00141cd`. **Post-design Constitution Check:
  PASS**, with live release gates still blocked.

## Phase 2 — Recovery execution sequence

Each phase ends with updated task status, sanitized evidence, and a parent-owned
checkpoint (commit/revision ID when appropriate). Never mark blocked work done.
No application changes are authorized **within this documentation assignment**.

1. **Read-only preflight (Kitty + operator)**: inventory the confirmed MCAPS
   2026 subscription; identify separate audience RG/apps and deployment mapping
   in `.azure\deployment-plan.md`. Historical tenant auth is not today's gate.
   Review/validate concrete new resources within the granted creation scope;
   create only NEW audience-app secrets as approved, never alter existing secrets.
   Check ingress/proxy,
   revision/image/traffic, one backend replica/process, `mock_mode=false`,
   operational chat/semantic embeddings/stores/search/audit and quota. Check
   coach-key **presence/mapping only**, never list its value. Stop on unknowns.
   A missing NEW audience-app key may now be created under recorded approval.
2. **Minimal verifier repair (Forge)**: in
   `backend\scripts\surge_rehearsal.py` plus focused tests, require all A–D
   10/card accepted incident-bearing responses; 4–6 union, pairwise-disjoint
   event sets; three distinct E incidents separate from A–D; all 45 outcomes
   accounted for; zero HTTP/transport/timeout/malformed-response errors,
   `failed=0`, unexpected rate limits=0. Make network failures explicit/nonzero,
   not an unhandled traceback or false pass. Keep exact fixture, 40 workers,
   existing HTTP-200 latency population (including blocks) and percentile
   formula. Grade R on actual safe routing, not mandatory refusal. Add private
   `--key-env <environment-variable-name>` intake so live use need not put a
   key value in process arguments;
   never log headers, bodies, device/session IDs or key URLs. Preserve flags.
   In `frontend\src\allclear\surge\SurgeBoard.tsx` provide the now-implemented
   operator-only `type="password"` entry, using memory/session
   only and existing `X-Surge-Key` control calls. Add focused `Surge.test.tsx`
   coverage for valid/invalid control, no credential in URL/join/cards/logs, and
   unchanged public board/attendee flow. This is now implemented/tested,
   including keyed mock browser integration; legacy query-key compatibility remains but
   must never be used for live credential delivery. It grants no permission
   to rotate an existing secret.
3. **Targeted → regression → reproducible build**: prove verifier fails on zero
   coverage, missing card, cross-event merge, errors/network failure, server
   failures and slow p95; passes valid and safely routed/nonblocked R cases.
   Run focused/full backend and Surge tests/build on the same candidate; verify
   aligned lock with `npm ci --ignore-scripts`. Fix only failures coupled to
   this recovery. Parent checkpoints tested source and evidence.
4. **Separate audience release using existing infrastructure design**: follow
   Kitty's approved concrete resource plan. If audience apps already exist,
   capture prior healthy revisions/images/traffic and prefer application-only
   updates. If new audience resources are needed, validate Bicep/what-if and
   confirm preview stays within granted scope before scoped provisioning;
   no blind `azd up`. Do not execute until azure-validate/preflight/deploy handoff.
   Create/select a target-specific deployment mapping, never overwrite another
   environment. No existing-secret changes; NEW audience coach-key creation
   is explicitly approved. Docker daemon 29.9.3/linux is verified ready for
   local build; remote ACR build is not needed to solve the resolved engine blocker.
   For existing-app image updates:
   infra lacks `SURGE_COACH_KEY` mapping and blind provisioning can erase a
   manually configured mapping. Preserve it and verify actual
   traffic/revision/image, public health, SPA deep links, `/api/surge/state`,
   live models, and fail-closed unauthenticated control. Repository Bicep already
   expresses backend scale 1/1; verify reality rather than changing it blindly.
5. **Authorized live rehearsal**: user's follow-up supplies permission to run
   once all preflight/release gates pass. Obtain coach key privately; open on
   an operator-only device. Run repaired verifier against the **public frontend**
   to exercise proxy and backend. Log commit/revisions, time, replica, fixture
   coverage/card incident sets, outcomes, errors, counts, median/p95 and gate
   result, without raw report text or credentials.
6. **If FAIL, isolate and rerun**: separate transport/proxy/auth/429/503, model
   classification category drift, embedding deployment/vector quality,
   same-category similarity and persistent-incident reuse. Inspect sanitized
   records. The dedup lock spans embedding and action awaits: **measure live
   serialized-path latency**; it is a risk, not an observed bottleneck. Select
   one evidence-backed bounded fix, add a failing test, update task/spec,
   repeat tests/preview/deploy as needed, and rerun the identical fixture.
   No card routing, automatic global threshold reduction or safety bypass.
   If time/gates fail, select the verified fallback, not an unsafe shortcut.
7. **Clean, real-phone test, rehearsal, freeze**: close intake, wait for
   in-flight requests to settle, reset tally, close/confirm repeated
   `open=false`, zero counters/tiles, stable replica. Preserve every operational
   record; no store purge to fake fresh incidents. Test five cellular phones,
   QR/card origin, accessibility and projector readability; run the seven-minute
   show and fallback. Close/drain/reset again. Parent freezes tested checkpoint;
   no change after freeze without repeating affected release gates.

## Verification Matrix

Run in PowerShell from repository root unless stated otherwise. Baseline passes
above remain checked; reruns below certify **future** code changes.

| Scope | Command / evidence |
|---|---|
| Verifier focused | `$env:MOCK_MODE='true'; $env:PYTHONPATH=(Join-Path $PWD 'backend'); python -m pytest backend\tests\test_surge_rehearsal.py backend\tests\test_surge_room.py backend\tests\test_surge_api.py -q` — **26 passed** |
| Backend regression | `$env:MOCK_MODE='true'; $env:PYTHONPATH=(Join-Path $PWD 'backend'); python -m pytest backend\tests -q` |
| Safety if pipeline touched | Above full suite plus inspect zero-LLM/tool/PII/SEV1/statutory regressions; never bypass them |
| Frontend reproducibility | `Set-Location frontend; npm ci --ignore-scripts` |
| Frontend test/type/build | `Set-Location frontend; npx vitest run src\allclear\surge; npm run typecheck; npm run build` — each exit code must succeed |
| Deployment preview | Separate audience resource plan/environment/image/config diff reviewed; creation + NEW app-secret permission granted; Bicep validation/what-if and azure-validate/preflight/deploy handoff required before execution |
| Live acceptance | Repaired `backend\scripts\surge_rehearsal.py`, confirmed frontend origin, `--concurrency 40`; private environment key, no `--key` secret in recorded commands |
| UX/rehearsal | 390×844 phone + actual phones; 1920×1080 board/projector; card print/scan; keyboard/focus/labels/contrast/dictation; fallback and cleanup record |

## Completion gates

| Gate | State | Completion evidence / stop condition |
|---|---|---|
| G0 Spec Kit alignment | ✅ | Parent context update succeeded; code/IaC/lock checkpoint `00141cd` published; R4 records actual failure/corrective gates |
| G1 Local baseline | ✅ | Observed 15 + 364 backend, 5 UI, build, browser flow and closed/zero cleanup; **not** live semantic proof |
| G2 Audience target/config plan | 🟨 | Initial target/inventory/19-resource preview complete; corrective VNet/private-endpoint/DNS/MI plan requires parent validation before execution |
| G3 Trustworthy verifier + private control | ✅ | 11 new verifier tests /26 focused passes; protected `--key-env`; 6 UI passes, typecheck/build; actual keyed mock browser verifies masked entry, 403 without key, authorized Open, public-request credential separation and cleanup |
| G4 Tested release checkpoint | ✅ | `00141cd`: isolated backend 375, production-image Surge 26, UI 6, Node 22.23.5 build, Linux lock and immutable image build/push pass |
| G5 Deployed candidate | 🟨 | Initial images deployed/models Succeeded/MI role/one replica/live-mode health/keyless 403 verified, but report 503: no working Cosmos network/data path. Replacement deployment and successful report/persistence/audit required |
| G6 Live semantic/load | ⛔ | FAILED: 45 attempts, 0 accepted, 0 incidents, 2 blocked, 43 failed; 2.75s p95 on two responses invalid. Identical full successful rerun required |
| G7 Cleanup + human rehearsal | 🟨 | Failed-run reset CLOSED/zero confirmed; replacement cleanup, real phones/accessibility/projection and seven-minute/fallback run remain |
| G8 Freeze / final GO | ⬜ | Parent records exact tested/deployed checkpoint, fallback artifact and presenter/operator GO; any unknown safety/privacy gate = NO-GO |

### Today-only decision checkpoints (ET; targets, not promises)

| By | Checkpoint / fallback decision |
|---|---|
| 10:20 | Target + isolated creation/NEW-secret approval confirmed; publish plan, converge inventory/technical preflight and fallback preparation |
| 10:50 | G3/G4 verifier + tested candidate; avoid feature expansion |
| 11:27 actual | Initial deployment partial; live run FAILED; policy root cause confirmed; private-network correction preparing, not executed |
| 11:45 target | Corrective preview/validation and private network/MI canary decision; if delayed, prepare tested loaded replay/mock in parallel |
| 12:10 | Hard live-vs-verified-fallback decision based on working canary plus full live acceptance; no policy bypass or unproven URL |
| 12:30 | G7/G8 freeze: real phones, projection, rehearsal, cleanup and rollback/fallback proven |
| 12:45 | Closed-board/fallback/QR final check; no unverified late changes |
| **13:00** | Showcase; these checkpoints do not move the stage time |

## Risks, rollback and scope discipline

- **Policy-enforced Cosmos isolation**: public/local-auth Disabled; initial
  ACA lacks private connectivity. New VNet-integrated apps/private endpoint/DNS/
  MI SQL role need parent validation and proof. Initial resources/key/models
  exist; their health did not establish report acceptance. Never bypass policy
  or touch initial apps/private redteam to make the new path work.
- **Semantic/latency uncertainty**: use live evidence and fixed fixture; mock
  fragmentation and fast mock p95 cannot predict live success. Do not weaken
  dedup correctness or lock protection to improve counts/timing.
- **Retained incidents / resets**: room counts differ from durable magnitude;
  repeat fixtures may join earlier incidents. Record baseline and reuse; never
  claim reset created a clean incident store or demand all receipts say opened.
- **Credential handling**: URL stripping/sessionStorage is display hygiene,
  not secure delivery. Never project/share key-bearing links, shell history,
  process arguments or screenshots. Create only NEW audience secrets under
  recorded approval; never modify/rotate existing ones.
- **Rollback**: operator routes traffic to captured previously healthy revisions
  for **both** apps and rechecks version/health/control. Tally may disappear on
  revision restart; reports/incidents/audit must remain. If rollback lacks Surge,
  use verified replay, not an old UI as a claimed live surge.
  For a first audience release with no prior healthy revision, explicitly record
  “no prior revision”; close intake/disable audience traffic and use verified
  fallback rather than inventing a rollback. Do not delete operational records.
- **Fallback**: rehearse `/?demo=loaded` on a known working local/deployed build;
  optionally a captured sanitized replay. Any voice/multilingual backup needs
  its own proof. Label mock/replay/seeded reports honestly.

## Complexity Tracking

No Constitution exceptions. No new platform, agent, persistence layer, global
threshold change, or card-driven dedup. Unresolved operational release gates
remain blocked rather than being justified as architectural exceptions.
