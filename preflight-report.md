# Room Surge Azure preflight

**Revision:** 2026-11-17 / 01  
**Status:** PASS - infrastructure preview and production images; live acceptance pending  
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
