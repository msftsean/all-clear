# Room Surge Azure preflight

**Revision:** 2026-11-17 / 07

**Status:** 🟨 MOCK FALLBACK VERIFIED | ⛔ LIVE SHOWCASE NO-GO | 🧪 HYBRID ACCEPTANCE FAILED

**Branch:** `event/arlington-2026-11-18`

**Target:** MCAPS-2026-segayle, `rg-allclear-surge-20261117`, East US 2

**Scope:** New audience resources only. Private red-team and other applications untouched.

## Current checkpoint — R9 verification

The third real-AI canary **failed the unchanged acceptance gates**. All 45
requests completed this time, but semantic grouping and latency still fail.
The audience backend remains on the working mock; there was no cutover.

| Gate | Actual R9 evidence |
|---|---|
| Regression fixes | Shared async Azure credential removes synchronous token acquisition from the async model path; embedding runs before the dedup lock, while routing/persistence remain atomic. Reset-generation guards retain and acknowledge late accepted reports with `room_counted=false`, without changing the new room's counters. Late blocks/errors are also isolated. |
| Release verification | All **390 tests passed in the actual Linux backend image**, with repository-documentation fixtures mounted read-only. Frontend: 14 UI tests and Node 22 production build passed. No threshold, taxonomy, fixture, safety, escalation, role, secret or network changes. |
| Actual candidate | `--hybridr9`, immutable backend digest `sha256:318a475c91f3e21bb7b605052eb586a2a8c01192076a5dc71575961c0d36795a`, Healthy/Provisioned, one replica; real-AI/temporary-memory health and keyless control HTTP 403 verified. |
| Complete original rehearsal | Untouched 45-report fixture, concurrency 40: **43 accepted Signals → 36 Incidents**, two safety blocks, zero errors/room failures, all 45 HTTP responses completed in 19.7s. Complete accounting PASS. |
| Semantic grouping | A/B/C/D produced **10/7/6/10 distinct Incidents**, 33 A-D total: **SC-001 FAIL** against the unchanged four-to-six requirement. E remained three separate Incidents, disjoint from A-D: PASS. |
| End-to-end latency | All 45/45 responses included: median **16.32s**, p95 **17.97s**: **SC-002 FAIL** against eight seconds. No timeout occurred in this run; that does not prove the earlier long-tail cause is eliminated. |
| Cleanup / audience | Candidate reset CLOSED/zero in `finally` after all responses settled. Public room was not reset or replaced; named `--mockfallback` remains 100%. No more paid repetition without a meaningful semantic/performance solution. |
| Hosted frontend | New backward-compatible reset receipt UI is deployed as `--hybridr9`; hosted `index-CXbXlhpf.js` SHA256 `46F1130F6BF45E9F70B4809149F51169B1CDDD100ED8B6263679CF5A63927412` exactly matches the tested package. Public proxied health still truthfully reports mock. |

**Remaining blockers:** free-worded semantic grouping and end-to-end latency
need a real design/calibration solution, not weakened thresholds or card-based
grouping. Durable private Azure still requires investigation/support; the
support packet exists but no ticket was submitted. Hybrid browser acceptance
was not run after failed load/semantic gates. A physical phone/cellular QR scan
remains unconfirmed.

Safe R9 logs contain all 43 pipeline and 45 report-completion rows, with no
429 retry rows. Classification median/p95/max was 7978.2/8198.8/9942.9ms,
embedding 790.4/1887.2/2001.5ms, knowledge 3734.7/4292.4/4593.1ms, and
dedup-lock wait zero. Later candidate state remained CLOSED/zero. All 54
backend runtime Python files byte-match the verified immutable image.

**Tooling caveat:** whole-file lint/type checks are not green at committed HEAD:
Ruff diagnostics, 30 strict mypy errors, two Fast Refresh export warnings, and
Black debt in 12 existing changed files are pre-existing. Ruff was compared
against HEAD diagnostics; mypy was rerun with exact HEAD shadow files and
reported the same 30 errors. No new diagnostic was identified. The two new
test-formatting regressions were fixed; their 14 focused backend cases passed
again, and the three new test files pass Ruff/Black. Runtime source was not
changed by this final formatting cleanup.

## Earlier R8 checkpoint — 14:24 ET

The second real-AI canary **also failed acceptance**; public traffic has not been
switched. The actual Azure Search SDK vector-query parameter was corrected, and
knowledge/sitrep completion was moved outside the atomic dedup decision/persist
window. All 384 backend checks passed: 380 runtime/backend tests in the Linux
release image and four repository-documentation checks with their actual
read-only fixtures. This does not establish semantic or latency acceptance.

- New candidate `--hybridr8`, image digest
  `sha256:0c755cd5a5dbb15ac5d7f1e93c2f9b94d10c0a1dc47e4590c64773f96afe7d7b`,
  is Healthy with one replica and actual real-AI/temporary-memory health.
- Untouched 45-report fixture, concurrency 40: **41 accepted HTTP receipts →
  34 Incidents, two safety blocks, two client timeouts** (B and C), wall 60.2s.
  A–D formed 31 distinct Incidents; E remained three separate Incidents.
  Successful-response median 16.46s/p95 18.22s covers only 43/45 requests and
  is **not complete acceptance evidence**. Both success criteria failed.
- Safe diagnostics subsequently showed all 43 non-blocked pipelines completed;
  two classifications took about 82 seconds. No report text or credentials were
  logged. Median classification/embedding/knowledge durations were
  6124.8/1410.8/3785.5ms; median and p95 dedup-lock wait were zero. Forge is
  checking synchronous I/O/event-loop blocking rather than assuming an Azure
  quota explanation.
- Diagnostics show real cosine comparisons: many OPEN decisions had best
  similarity 0.67–0.82; observed ATTACH decisions were at least 0.8308. No
  threshold, category, fixture or card-grouping change has been made. Semantic
  normalization/calibration is not silently claimed solved.
- **Reset race reproduced:** initial `finally` reset returned CLOSED/zero, but
  the two late completions then produced CLOSED/two Signals/two Incidents/zero
  devices. Generation-aware tally handling is being fixed without dropping
  domain reports or audit. A second cleanup of only the quiescent candidate
  completed at 14:24 ET, restoring CLOSED/zero after all requests settled.
  The user's stable room was read-only, not reset.
- Stable public mock remains pinned 100%; verified CLOSED/zero at 14:24 ET.
  The new frontend remains the verified `index-CNv7Cu5d.js` bundle. Hybrid
  browser rehearsal has been authored but not executed because semantic/load
  acceptance failed. Physical cellular QR testing has been requested from the
  user but not confirmed. Durable Azure remains blocked as recorded below.

## Earlier R7 checkpoint — 13:47 ET

**Real Azure AI now processes reports on an isolated canary, but the live
showcase is not ready.** The working public room remains explicitly pinned to
the verified mock revision; it was not switched to the failed canary.

| Track / gate | Actual evidence |
|---|---|
| Approved temporary alternative | `SURGE_DEMO_MEMORY_STORAGE=true` with `MOCK_MODE=false` selects cached in-memory incident/session stores while chat, embeddings and knowledge stay live. The flag defaults false. Reports and audit records disappear on restart; source UI and printable cards disclose this. No fixture, threshold, routing, safety or escalation change. |
| Source/image checks | Forge: 382 backend and 14 Surge UI tests, Node 22.23.5 typecheck/build and targeted ESLint passed. Actual Linux/Python 3.12.16 backend image: 33 focused Surge tests passed; startup without Cosmos returned healthy, `mock_mode=false`, `storage_mode=memory`. |
| App-only release | Required prepare/validate/deploy flow completed. Read-only resource-level network what-if: 0 Create / 0 Delete / 3 Modify / 3 NoChange / 13 Ignore; no infrastructure graph applied. Cosmos public access remains Disabled and local auth disabled. Existing identity, roles, secrets, location and SKUs unchanged. |
| Candidate runtime | Original public backend revision `--hybrid1340`: Healthy, Provisioned, RunningAtMaxScale, one replica; actual revision endpoint reports real AI/memory. Keyless control returned 403. Zero normal traffic. |
| Untouched original rehearsal | Concurrency 40, all 45 requests accounted for: **43 accepted Signals → 34 Incidents, two safety blocks, zero failures**. A/B/C/D formed 10/7/6/8 distinct Incidents: **31 A–D Incidents, disjoint but SC-001 FAIL**. E formed three separate Incidents and did not merge with A–D: PASS. |
| Latency / outcome | All 45 HTTP responses counted; median 15.67s, **p95 16.81s**, wall 17.7s. **SC-002 FAIL**. This is actual end-to-end live evidence, not the earlier model-only smoke. Canary reset CLOSED/zero in `finally`; no cutover. Forge is diagnosing the actual semantic/performance failure without weakening acceptance. |
| Stable audience surface | Backend `--mockfallback` remains 100% pinned, mock, CLOSED and zero at 13:47 ET. New frontend `--hybrid1340` is Healthy and serves `index-CNv7Cu5d.js`; hosted SHA256 `F6DE2F7EC4E13344855ED90380CB0C0FE130A692A61EBC477F8952B4398F1F73` exactly matches the tested packaged bundle. It continues to disclose mock while mock serves traffic. |
| Durable Azure path | Fresh read-only check: private backend provisioning Failed, no revision and no FQDN. Retry activity has Started/Accepted only, correlation `7e874bef-d9eb-411f-a25f-58cdb40b66d1`. Root cause remains unknown. Kitty prepared a support packet; **no support ticket submitted** (entitlement/contact/severity approval still required). |

Public board: <https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/surge>.
Refresh existing tabs to load the new mode-aware bundle. Physical-phone cellular
QR testing remains unverified. The sections below preserve earlier chronological
preflight and fallback evidence; they do not supersede this checkpoint.

## Summary

Azure authentication, effective write permissions, Bicep compilation, ARM validation,
and Provider-level what-if passed. Preview shows **19 creates, zero modifications,
zero deletions**, all inside the approved audience resource group. No ACS/phone or
Realtime resources are included. Model quota fits the requested capacities; actual
capacity and live application behavior remain deployment/acceptance gates.

The azd preview initialized the approved empty resource group despite its generic
"no changes" banner. A subsequent resource inventory was empty. No application
resources, real coach secret, or live rehearsal existed at preflight completion.

## Tools and validation

| Check | Result |
|---|---|
| Isolated azd preview using Azure CLI authentication | PASS |
| Skill Bicep validation helper: CLI/auth/compile/ARM validate/what-if | PASS |
| Explicit `az deployment group what-if --validation-level Provider` | PASS |
| Subscription effective permissions and scoped runtime-role review | PASS |
| Assigned policy review and ARM policy validation | PASS |
| Frontend Node 22.23.5 typecheck/production build | PASS |
| Production nginx image and all three Surge SPA routes | PASS |
| Backend Linux image, dependency consistency and SDK imports | PASS |
| Full backend suite with regenerated declared-dependency lock | 375 passed |
| Focused Surge tests inside the production backend image | 26 passed |

Use the isolated audience environment, `deployPhone=false`, `deployRealtime=false`,
`mockMode=false`, and exactly one backend replica. Supply the new secure
`surgeCoachKey` parameter through protected input, never a URL, source file,
transcript, or command-line literal.

## Issues and remediation

Five existing Bicep conditional-resource warnings remain. The selected live Cosmos
and disabled Realtime branches passed ARM Provider validation.

Docker package-download TLS handshakes fail on this host. TLS verification was not
disabled: the frontend uses verified Node22 host-built assets with the identical
nginx runtime; the backend installs its complete resolved lock from host-downloaded
Linux wheels. Both final images were tested.

The previous backend lock contained unrelated Agent Framework integrations and
versions outside the declared manifest bounds. It was regenerated to 88 Linux
Python3.12 packages, retaining compatible pins, and independently tested.

## What-if resource families

New backend/frontend Container Apps, Container Apps environment, AOAI account and
chat/embedding deployments, scoped AOAI role, ACR, Cosmos account/database/three
containers, Key Vault and new-account key copies, Log Analytics, and AI Search.
No existing resource is modified or deleted.

## Next gate

Finish the recorded validation workflow, provision/deploy only the new audience
stack, verify real models/storage/coach controls and one replica, then execute the
authorized 40-concurrent rehearsal. Require complete report accounting, no failed
requests or cross-event merges, A-D collapsing to at most six Incidents, and p95
under eight seconds. Reset only the tally to CLOSED/zero; preserve domain data.

## Initial live result and private-path recovery

The initial stack deployed successfully with live mode, one replica and working
protected coach controls. Its real rehearsal failed: 45 attempts, zero accepted
Signals/Incidents, two safety blocks, 43 failures. The 2.75-second p95 represented
only two successful HTTP responses and is not acceptance evidence. The board was
reset CLOSED/zero.

Activity logs confirmed inherited MCAPS governance modified Cosmos to disable
public networking and account-key authentication. The initial ACA environment
had no private path. Do not undo those policies or add public-access exceptions.

At 11:34 ET, both new corrective templates passed the skill's full Bicep helper
and scoped Provider previews: `infra/surge-network.bicep` adds private networking,
Cosmos SQL private endpoint/DNS and a VNet-integrated ACA environment;
`infra/surge-apps.bicep` adds new apps with user-assigned identities and
database-scoped Cosmos data access. Existing apps and governance settings remain
unchanged. Bootstrap mode creates identities/roles before image pull; verify
ACR Pull propagation before deploying apps.

The same tested immutable images are retained. The new Search index is seeded
with all 12 All Clear articles and 1536-dimensional embeddings. Live acceptance
must be repeated after the private path works; fallback decision is 12:10 ET.

The private environment's first asynchronous creation failed on the missing
subscription feature `Microsoft.Network/AllowBringYourOwnPublicIpAddress`, which
ARM preview did not detect. It is now Registered on MCAPS and Microsoft.Network
registration was refreshed; the unchanged network template then Succeeded.
Identity bootstrap and live ACR Pull/Cosmos role checks passed. Do not equate
registered prerequisites or healthy public routes with passing live acceptance.

## ⛔ Final private application failure

At 12:17:52 ET, `allclear-surge-live-backend` failed to provision a revision:
`ContainerAppOperationError`, with no additional provider explanation. No revision
or FQDN exists; the private frontend was never created. Correlation:
`f851acdb-4556-456c-bbd4-71f5c7bd0a1e`. The network/private endpoint/DNS and role
bootstrap succeeded; the remaining revision failure is not explained by that
success and was not a user cancellation. Stop speculative infrastructure changes
after the fallback cutoff. Do not relax governance or claim live semantic success.

## ✅ Deployed, explicitly labelled mock fallback

Only the original audience backend's `MOCK_MODE` flag changed to true; its existing
coach key, image and safety controls were preserved. Runtime mode disclosures now
appear on `/report`, `/surge` and `/surge/cards`. Mock A-D cards offer explicit
sample wording; live own-word instructions remain unchanged. Actual report text
still traverses the normal pipeline: no card-based grouping or changed thresholds.

| Final check | Verified result |
|---|---|
| Focused frontend tests / TypeScript / Node22 production build | 11 passed / PASS / PASS |
| New modules, cards and tests: strict targeted ESLint | PASS |
| Existing board/report strict lint baseline | Four fast-refresh warnings and one unused-disable error reproduced from HEAD; not introduced or suppressed |
| New frontend revision | `allclear-sbuqtpuppifra-frontend--mocklabel1236`, Healthy/Running, 100% traffic |
| Deployed immutable frontend digest | `sha256:9a7eb0ed665c595e59c7fb7f13e89554b196a9a9eddc463bc9bc91e48a60cb56` |
| Repeated-wording mock load, concurrency40 | 40 accepted Signals → 4 disjoint Incidents, 40 devices, A-D10 each, zero failures |
| Mock p95 across all40 attempts / wall | 0.213s / 0.380s |
| Actual public mobile-browser flow | Two isolated390×844 contexts, sample input/receipt, board polling2 Signals →1 Incident |
| QR / processing disclosure / key handling | Board PNG + six card PNGs; all three pages labelled mock; masked control key, no public API or URL key |
| Browser errors / mobile horizontal overflow | Zero / none |
| Final protected reset | CLOSED, zero Signals/Incidents; domain reports/audit not deleted |
| Physical cellular QR scan | NOT VERIFIED |
| Original live semantic acceptance | FAILED; mock results do not replace it |

The fresh validation workflow completed before the frontend-only image update.
No infrastructure template was applied. A read-only existing-network Provider
preview showed zero resource Create/Delete, three Modify, three NoChange and
thirteen Ignore. The helper's text-marker counts included nested property
removals and must not be reported as resource deletions. The existing frontend
registry secret/proxy/environment/ingress were preserved; no role or secret changed.

**Board:** https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/surge

**Mock A-D cards:** https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/surge/cards?only=ABCD

**Replay, not audience reporting:** https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io/?demo=loaded

Retrieve the existing coach secret from the original audience backend's Azure
Portal Secrets view; enter it under Operator controls → Coach key → Set key.
Open the board, then scan on a physical phone, choose A-D, use the sample and send.
Reset after testing. Mock grouping demonstrates repeated wording, not live AI;
mock domain data is in memory and disappears on app restart.
