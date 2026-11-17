# Phase 0 Research: Room Surge recovery

**Branch**: `event/arlington-2026-11-18` | **Revision**: R3, 2026-11-17 10:15 ET
**Target**: 2026-11-17 **13:00 Eastern** | **Status**: ✅ Design decisions; 🛑 live verification
**Source**: repository inspection, parent-observed results, user live-test
authorization; [plan evidence](plan.md#observed-verification-baseline).

No research agents were spawned. Setup-plan was already completed. This phase
resolves planning choices without pretending inaccessible deployed state is known.

## D1 — Keep the bounded wrapper

**Decision**: Retain `api\surge.py` → `process_signal(channel="report")` →
`SurgeRoom` observation. Do not alter QueryAgent/RouterExecutor/ActionAgent.

**Rationale/evidence**: API passes text/session/channel only; card is normalized
for tally. Tests cover admission, near-duplicate attachment, key fail-closed
behavior, public-state privacy and tally reset. Constitution and spec 019 require
unchanged authority and preserved reports.

**Alternatives rejected**: Card-based dedup, model routing decisions, new
platform, global refactor or reduced escalation would fake the demo or violate
architecture.

## D2 — Separate mock flow from live semantic acceptance

**Decision**: Offline verifies admission/receipts/privacy/near-duplicate
attachment; only live semantic embeddings can certify free-worded collapse.

**Rationale/evidence**: `services\mock\embeddings.py` is normalized bag-of-words.
Real mock HTTP run (not a stand-in): 45 requests, 43 signals →43 incidents,
2 blocked, failed=0; A–D 10 distinct each; E=3; median 0.13s, p95 0.22s.
SC-001 failed, SC-002 passed locally. This matches the **pre-existing FR-005** caveat.
Actual local browser receipt joined a retained incident; smoke verified routes,
polling and local QR, not visual/accessibility/phone certification.

**Alternatives rejected**: Treating stand-in historical success as end-to-end;
claiming mock fragmentation proves broken live semantic dedup; lowering a global
threshold to fix mock token overlap.

## D3 — False-positive rehearsal gates repaired/tested

**Decision**: Add focused script regression tests, then minimal verifier
hardening before live acceptance.

**Original pre-fix finding**: `backend\scripts\surge_rehearsal.py` computed
SC-001 as union size ≤6, allowing **zero coverage** and cross-event merges.
HTTP errors did not determine final exit status; `state.failed` was printed but
not gated. Transport exceptions could terminate without an explicit summary.
**Update 10:23 ET**: Forge repaired these known issues, added 11 verifier
regressions; 26 focused backend tests pass. Original findings describe the
pre-fix script, not current delivered state. No live acceptance run is claimed.

**Chosen acceptance**: All A–D 10/card have accepted incident-bearing receipts;
union 4–6 with pairwise disjoint card sets; three E fixtures stay separate;
all 45 requests accounted for; zero request/network/server failures and
unexpected rate limits. Preserve original fixture/order, 40 workers, latency
population (all HTTP-200 responses, including blocks) and existing percentile
index `max(0, int(n * 0.95) - 1)`. Report errors separately and fail the run;
do not silently improve p95 by dropping failures or changing probes.

R inputs may legitimately pass the live content-safety filter. Verify actual
safe routing/receipt and unchanged authority; do not require two live blocks.
Forty workers scheduling 45 requests is not proof of exactly 40 simultaneous
server start times.

**Alternatives rejected**: Universal poison-block gate; ≤6 alone; excluding
failed requests without failing overall; changing fixture/measurement to pass.

## D4 — Confirmed MCAPS 2026 separate audience target

**Decision**: User selected **MCAPS-2026-segayle**
(`9f8986ed-ceb2-414d-8fcb-46d5cfc70618`) for today's **separate audience app**.
Kitty owns read-only inventory and local ignored
[deployment plan](..\..\.azure\deployment-plan.md), pending inventory. Review
concrete resource permissions before writes; never reuse private redteam.

**Rationale/evidence (observed this session)**:

| Check | Fact | Interpretation |
|---|---|---|
| azd environments | `[]` | Local environment mapping missing; not proof no resources exist |
| Current subscription | `MCAPS-Hybrid-REQ-51667-2023-segayl`, `4b27ac87-dec6-45d5-8634-b9f71bd1dd26`; no AllClear apps | Not a confirmed audience target |
| Selected subscription | `MCAPS-2026-segayle`, `9f8986ed-ceb2-414d-8fcb-46d5cfc70618`; previously only internal `ca-allclear-redteam-20261001` observed | Subscription approved for **separate audience app**; adapter explicitly excluded; fresh inventory pending |
| Correct current CLI context | Explicit subscription `az account show` confirms **Enabled**, actual tenant **`16b3c013-d300-468d-ac64-7eda0820b6d3`** | CNE/MCP wrong-context failure is not MCAPS inaccessibility; Kitty now runs correct CLI inventory; deployed resources unverified |
| Historical event record | [Spec 022 tasks](..\022-event-day-readiness-verification\tasks.md): `a8a91d76-473f-49e2-ba21-1d394ba9a968`, `rg-all-clear-demo`, backend/frontend `allclear-p74h22h3c2hqm-*` | Candidate to verify, not current live proof |
| Historical frontend | `https://allclear-p74h22h3c2hqm-frontend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io` | `/api/health` and `/api/surge/state` DNS failure; cannot infer routes absent |
| Historical backend | `https://allclear-p74h22h3c2hqm-backend.agreeablegrass-0b5ab03b.eastus2.azurecontainerapps.io` | Recorded origin only; not verified healthy |
| Recorded-subscription inventory | `AADSTS130504`, Temporary Access Pass expired; tenant `cbc044cf-defc-4487-8475-4df2b4b237ca` | Human reauthentication prerequisite; no known-failing retry loop |
| Latest device login | Account does not exist in Microsoft CNE tenant and cannot access Azure CLI; external-user membership required | Confirm intended audience target and an invited event/sandbox account or obtain administrator access; do not repeatedly log the same work account into historical tenant |

`infra\main.bicep` declares backend min/max replicas 1/1, external frontend
ingress and `BACKEND_URL`; nginx has SPA fallback and `/api` proxy. These are
repository artifacts, not deployed-state confirmation. Parameter-file mock
default is `${MOCK_MODE=true}`; config also defaults mock on. Template has no
Surge coach-key mapping. None proves the deployed key is absent or mode is mock.
Kitty's private feasibility report confirms application-only deployment is
preferred: blind provisioning can reconcile away a manual coach-key mapping.
No new cloud query, deployment or load was performed by Kitty. Its tenant typo
is not used here; the correct observed tenant is
`cbc044cf-defc-4487-8475-4df2b4b237ca`.

The corporate-tenant TAP/membership path is now **deferred until today's demo
works**, not a prerequisite for the approved MCAPS 2026 target. Resource names,
eligible dependency reuse and exact scoped resource selection remain pending
inventory. **Permission updated 10:15 ET**: user's “yes create away. the goal
is to get this complete” explicitly approves NEW separate audience resources
and NEW app-scoped secrets including coach key. This supersedes the unavailable
approval prompt. No repeated elicitation for ordinary isolated creation;
never alter/rotate existing secrets or reuse private adapter. Parent publishes
the plan first; azure-validate/preflight/deploy handoff precedes deployment.

**Tooling evidence update, 10:20 ET — PASS**: initial Docker named-pipe failure
is resolved. Parent started Desktop **PID 30064**, then verified daemon
**29.9.3**, **linux**, using `docker version` and `docker info`. azd 1.37.3
is installed. Retain `remoteBuild:false` and local image builds; no tooling
installation or remote-build/default change needed. This certifies the engine,
not the still-pending image build or deployment. Code verification has since
passed: **26 focused**, **375 full backend in 8.15s**, **6 UI**, typecheck/build.

**Alternatives rejected**: Blind `azd up`, assuming repository defaults are live,
publishing default keyless mock controls, assuming DNS failure means missing API.

## D5 — Preserve privacy and permission boundaries

**Decision**: Keep key presence checks status-only; use private operator delivery,
implemented masked non-URL entry in `SurgeBoard.tsx`, and protected `--key-env` intake for
the rehearsal script. No secret value,
key-bearing URL or raw payload in evidence.

**Rationale/evidence**: `_require_coach` fails closed when live key is unset;
mock permits no-key only when unconfigured. Board consumes a query key into
sessionStorage and strips URL; this is display hygiene, **not secure delivery**
(URL/log/history exposure is still possible). Current CLI `--key` can expose
secrets in process arguments; add environment support before live use.
Current UI now provides **Operator controls → Coach key → Set key** with a
masked input; Forge reports 6 UI tests and typecheck/build PASS. Legacy query-key
ingress remains compatibility only, never approved live credential delivery.
Deployed positive/negative authorization checks remain G5.
Actual keyed isolated mock browser integration now also **PASS**: missing key
403; password input and Set key →Open; mobile 390×844 report A →board poll
1 signal; local QR PNG. Request observer confirmed no key URL and no
`X-Surge-Key` header on public calls. Reset `open=false`, signals=0, incidents=0;
both helper processes stopped. This proves safe operator-path integration,
**not live semantic/load acceptance or accessibility certification**.
Forge completed the focused verifier fixes, protected `--key-env` intake
(default `SURGE_COACH_KEY`) and small operator-entry UI/tests. No new packages, routing/card grouping,
threshold or mock changes. Kitty waits for code-test/build gates before deploying
or exposing the audience app. Creation permission for NEW app-scoped secrets
remains approved; this does not allow existing-secret rotation.

User's follow-up authorizes live rehearsal after safe target/access/configuration;
the later 10:15 ET approval additionally authorizes NEW audience-app secrets.
It never authorizes existing-secret change/rotation or redteam-app reuse.
Deployed `SURGE_COACH_KEY` remains UNKNOWN until checked; a missing NEW
audience-app key can now be created privately under recorded approval.

**Alternatives rejected**: Publishing coach URLs; outputting secret lists;
pretending another generic rehearsal "go" is still required.

## D6 — Measure serialized-path risk; isolate failures

**Decision**: Preserve pipeline lock; measure live latency and diagnose one
evidence-backed defect/change at a time.

**Rationale/evidence**: Pipeline lock spans `RouterExecutor.decide` (including
embedding) through action completion, preventing simultaneous “no match” races.
Live serialized latency may threaten SC-002, but no live measurement exists.
Category drift, embedding deployment/auth, retained incident vectors, proxy,
quota and transport are distinct failure hypotheses.

**Alternatives rejected**: Claiming an observed lock bottleneck, removing lock,
hardcoding cards, or automatically lowering threshold 0.83→0.80→0.78.

## D7 — Reproducible release and reversible event clock

**Decision**: Include parent-generated aligned lock, retest candidate, preview/
approve the separate-audience resource/release plan, capture previous audience
app revisions when present (otherwise first-release fallback), rehearse
fallback, then close/drain/reset and freeze at 12:30 ET.

**Rationale/evidence**: Patch changed package manifest for `qrcode` /
`@types/qrcode` only; Docker uses `npm ci`. Parent ran
`npm install --ignore-scripts` and produced the needed lock update.
Reset does not delete persistent incident/report/audit data; admitted in-flight
work may finish after close/reset unless drained. Room state is per process.

**Alternatives rejected**: Deploying an unaligned lock, old 12:45 stage time/
past code-freeze dates, store purge to manufacture fresh incidents, untested
backup claims. Existing-app update estimate 5–15 minutes applies only after
prerequisites; reprovisioning estimate remains unknown.

## Operational blocker register (not resolved by writing this document)

| Blocker | Owner / required evidence |
|---|---|
| Exact separate audience resources | Kitty + parent: approved MCAPS 2026 subscription chosen; inventory/RG/apps/FQDN/deployment mapping and concrete resource-write scope pending; no historical-tenant login required today |
| New audience secrets | ✅ Explicit creation approval granted at 10:15 ET; private generation/mapping/runtime verification still pending; no existing-secret change |
| Image build execution | ✅ Docker daemon 29.9.3/linux verified by version + info at 10:20 ET; actual candidate image build remains pending |
| Coach key/private delivery/live configuration | Masked UI and protected script input implemented/tested; operator still verifies live presence/mapping/positive-negative control; NEW app-key creation approved |
| Actual live dependencies, capacity and scale | Operator: live mode, real chat/semantic embedding, stores/search/audit/content-safety access, quota, one backend replica/process and traffic |
| Trustworthy verifier, non-URL control and tested deployed candidate | Implementation owner + parent: focused/full test/build, masked coach entry, private script key intake, aligned lock, checkpoint, deployed revision/image/health evidence |
| Semantic/load/phone/projector readiness | Authorized live run and human checks, then safe cleanup/freeze; no pass inferred from local results |

### Evidence ledger for subsequent execution

For each attempt append: ET timestamp; target IDs (non-secret); commit and app
revision/image/traffic; mode/replica; fixture count/per-card coverage + incident
sets; outcome/error/failed/rate-limit totals; median/p95 with population;
SC/gate result; diagnosis/change and rerun reference; closed/zero cleanup;
operator decision/fallback. No raw texts, device/session IDs, secret values or
credential URLs. **No live deployment or rehearsal entry exists yet.**
