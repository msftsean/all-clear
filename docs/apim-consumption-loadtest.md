# APIM Consumption — 20× simultaneous create test (Cloudforce sub)

**Question asked:** Can 20 participants *simultaneously* create their own Azure
API Management **Consumption**-tier instances in the Cloudforce subscription
without hitting a quota / per‑subscription‑per‑region wall?

**Answer: Yes.** Verified empirically — 20/20 succeeded with zero rejections.

## Test setup

| Parameter | Value |
| --- | --- |
| Subscription | Cloudforce Sponsorship (`098ef2f6-cea4-4839-8093-ef90622e1b8c`) |
| Region | `eastus` |
| Resource group | `rg-apim-loadtest-eus` (single RG, deleted after) |
| SKU | **Consumption** (`--sku-name Consumption --sku-capacity 0`) |
| Count | 20 instances, fired back‑to‑back with `az apim create --no-wait` |
| Date | 2026-06-12 |

## Result

| Metric | Value |
| --- | --- |
| Control‑plane submissions **rejected** | **0 / 20** |
| Provisioning **Succeeded** | **20 / 20** |
| Provisioning **Failed** | 0 |
| **Timeout** (>25 min) | 0 |
| Wall‑clock to all‑Succeeded | **~3.5 minutes** |

No quota, throttle (429), or `OperationNotAllowed` errors were returned at
submit time or during provisioning. All 20 reached `provisioningState =
Succeeded`. Raw per‑instance data: `all-clear/apim-loadtest-result.json`.

## Why this matters / context

- The Azure APIM **service‑limits doc does not publish a hard
  per‑subscription‑per‑region cap on the number of Consumption instances** — the
  documented Consumption limits are management‑plane (3,000 API operations,
  1,500 tags, 100 loggers/products, etc.), not instance count. This test
  confirms the practical ceiling is comfortably above 20 in this subscription
  and region.
- **Consumption is the correct SKU for the lab:** serverless, pay‑per‑call
  (first 1M calls/month free), provisions in minutes, and — as shown here —
  scales to a full class creating gateways at once.

## Reproduce

The test script is `C:\Users\segayle\apim_loadtest.ps1` (fires N creates with
`--no-wait`, polls each to a terminal state, writes a JSON summary). Re‑point
`$sub`, `$count`, and `$loc` to retest in another subscription/region.

## Cleanup

All 20 instances were created in a single throwaway RG
(`rg-apim-loadtest-eus`), deleted via `az group delete --yes` immediately after
the test. Consumption instances have no fixed standing cost, so the test
incurred effectively $0.

## Recommendation for the event

- ✅ Safe to have all ~20 Day‑2 participants create their own Consumption APIM
  gateway concurrently in the Cloudforce sub / `eastus` (Stage 4 / Lab 08).
- Give each builder a **unique global name** (collision, not quota, is the only
  realistic failure mode — names are globally unique).
- Prefer **one RG per participant** for clean teardown, or a shared lab RG that
  staff delete at the end.
