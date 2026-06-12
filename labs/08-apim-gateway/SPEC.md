# Lab 08 Spec — APIM as the AI Gateway (Day‑2 Stage 4)

## Intent

Front the All Clear agent API with **Azure API Management (Consumption tier)**
acting as the **AI gateway**, adding the four production controls from the
event's Stage‑4 definition: **rate limiting, token budgets, JWT auth, and
observability** — without modifying agent code.

## Why Consumption (decision)

- Serverless, pay‑per‑call, no fixed gateway cost; first 1M calls/month free.
- Provisions in minutes (fits a 60‑min stage) vs ~30–45 min for dedicated tiers.
- **Verified safe for 20 concurrent builders** in the Cloudforce sub / eastus —
  see [`docs/apim-consumption-loadtest.md`](../../docs/apim-consumption-loadtest.md)
  (20/20 created simultaneously, 0 rejections, ~3.5 min).

## Scope (in)

- FR‑1 Provision a Consumption APIM instance per builder.
- FR‑2 Import the All Clear backend via its OpenAPI document.
- FR‑3 Prove a signal triages **through** the gateway.
- FR‑4 `rate-limit-by-key` (per‑caller throttling → 429).
- FR‑5 `azure-openai-token-limit` (per‑caller token budget; `llm-token-limit`
  for non‑AOAI backends).
- FR‑6 `validate-jwt` (401 on missing/invalid bearer).
- FR‑7 APIM diagnostics → Application Insights.
- FR‑8 Clean teardown.

## Scope (out)

- Semantic caching (Consumption has no built‑in/external cache).
- Plain `rate-limit` / `quota` policies (unsupported on Consumption — use the
  `-by-key` variants).
- Dedicated‑tier features (VNet injection, self‑hosted gateway, multi‑region).

## Acceptance criteria

- [ ] `provisioningState = Succeeded` for the builder's Consumption instance.
- [ ] `All Clear API` imported; `POST /allclear/api/signals` returns a triage
      result through the gateway URL.
- [ ] 429 returned past the `rate-limit-by-key` threshold.
- [ ] `x-tokens-remaining` header present; 429 on token‑budget exhaustion.
- [ ] 401 with no bearer; success with a valid token.
- [ ] Requests visible in Application Insights (latency, codes, 429s).

## Mapping

- Day‑2 **Stage 4**, 60 minutes.
- Sits between Stage 3 (MCP — Labs 07/02) and Stage 5 (Deploy — Lab 06).

## Open items for approval

- Confirm whether builders use **their own RG** (clean teardown) or a **shared
  lab RG** (staff delete at end).
- Confirm the JWT issuer/audience to standardize on (Entra tenant + `api://…`).
