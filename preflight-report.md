# Room Surge Azure preflight

**Revision:** 2026-11-17 / 04

**Status:** 🟨 MOCK FALLBACK VERIFIED | ⛔ LIVE AI NO-GO

**Branch:** `event/arlington-2026-11-18`

**Target:** MCAPS-2026-segayle, `rg-allclear-surge-20261117`, East US 2

**Scope:** New audience resources only. Private red-team and other applications untouched.

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
