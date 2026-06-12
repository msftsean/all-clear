# 🛡️ Lab 08 — APIM as the AI Gateway (Stage 4)

| 📋 Attribute         | Value            |
| -------------------- | ---------------- |
| ⏱️ **Duration**      | 60 minutes (Day‑2 Stage 4) |
| 📊 **Difficulty**    | ⭐⭐⭐ Advanced  |
| 🎯 **Prerequisites** | A running All Clear backend (Lab 06 deploy, or the shared lab API) |
| 💳 **APIM SKU**      | **Consumption** (serverless, pay‑per‑call, no fixed gateway cost) |

---

> 🛡️ **Stage 4 of the Day‑2 build lab.** You already have an agent (Stage 1),
> retrieval (Stage 2), and a discoverable MCP server (Stage 3). Now you put a
> **production AI gateway** in front of it: rate limits, token budgets, JWT
> auth, and full observability — without changing a line of agent code.

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. 🚪 **Provision an APIM Consumption instance** and understand why Consumption is the right SKU for a class of 20 builders.
2. 🔌 **Import the All Clear backend** into APIM and call your agent *through* the gateway.
3. 🚦 **Throttle traffic** with `rate-limit-by-key` so one caller can't starve the rest.
4. 🪙 **Cap LLM spend** with the `azure-openai-token-limit` policy (token budgets per caller).
5. 🔐 **Require a JWT** with `validate-jwt` so only authorized callers reach the agent.
6. 📊 **See everything** by wiring APIM diagnostics to Application Insights.

---

## 💳 Why the Consumption SKU (read this first)

We deliberately use the **Consumption** tier for this lab:

| Reason | Detail |
| --- | --- |
| **No fixed cost** | The gateway is shared/serverless — you pay per call, and the first 1M calls/month are free. 20 empty lab gateways cost ~$0 standing. |
| **Fast to provision** | Consumption instances come up in a couple of minutes, not the ~30–45 min a dedicated tier takes — critical inside a 60‑min stage. |
| **Auto‑scales** | No scale units to size; the platform scales with load. |
| **No per‑region instance quota wall** | Verified empirically for this event — see [`docs/apim-consumption-loadtest.md`](../../docs/apim-consumption-loadtest.md) for the 20‑simultaneous‑create test in the Cloudforce subscription. |

> ⚠️ **Consumption tier caveats you'll hit in this lab.** Use the **`-by-key`**
> policy variants (`rate-limit-by-key`, `quota-by-key`) — the plain `rate-limit`
> and `quota` policies are **not supported** on Consumption. Semantic caching is
> **out of scope** here because Consumption has no built‑in or external cache.

---

## 📈 Progress Tracker

```
Lab Progress: [░░░░░░░░░░] 0% - Not Started

Checkpoints:
□ Step 1: Provision the APIM Consumption instance
□ Step 2: Import the All Clear backend API
□ Step 3: Call the agent through the gateway
□ Step 4: Add rate-limit-by-key (traffic throttling)
□ Step 5: Add azure-openai-token-limit (token budget)
□ Step 6: Add validate-jwt (authentication)
□ Step 7: Wire observability to Application Insights
□ Step 8: Clean up
```

---

## 🚪 Step 1 — Provision the APIM Consumption instance

Each builder creates **their own** Consumption gateway. Names are globally
unique, so suffix yours (initials + a number).

```bash
# Pick a globally-unique name, e.g. acl-apim-<yourinitials>
APIM_NAME="acl-apim-<yourinitials>"
RG="rg-allclear-<yourinitials>"     # your own resource group
LOC="eastus"

az apim create \
  --name "$APIM_NAME" \
  --resource-group "$RG" \
  --location "$LOC" \
  --sku-name Consumption \
  --sku-capacity 0 \
  --publisher-name "All Clear Lab" \
  --publisher-email "you@example.com" \
  --no-wait

# Poll until Succeeded (usually 1–3 minutes on Consumption)
az apim show -n "$APIM_NAME" -g "$RG" --query provisioningState -o tsv
```

✅ **Checkpoint:** `provisioningState` returns `Succeeded`.

---

## 🔌 Step 2 — Import the All Clear backend API

Import your backend's OpenAPI document (this app serves it at `/api/openapi.json`).

```bash
BACKEND_URL="https://<your-backend>.azurecontainerapps.io"

az apim api import \
  --resource-group "$RG" \
  --service-name "$APIM_NAME" \
  --path allclear \
  --api-id allclear \
  --display-name "All Clear API" \
  --specification-format OpenApi \
  --specification-url "$BACKEND_URL/api/openapi.json" \
  --service-url "$BACKEND_URL"
```

✅ **Checkpoint:** The `All Clear API` shows up under **APIs** with your
operations (e.g. `POST /api/signals`, `GET /api/health`).

---

## 📨 Step 3 — Call the agent through the gateway

```bash
GATEWAY_URL=$(az apim show -n "$APIM_NAME" -g "$RG" --query gatewayUrl -o tsv)

curl -s "$GATEWAY_URL/allclear/api/health"
# Then route a real signal through the gateway:
curl -s -X POST "$GATEWAY_URL/allclear/api/signals" \
  -H "Content-Type: application/json" \
  -d '{"text":"Downed power line sparking on Oak Street near the school."}'
```

✅ **Checkpoint:** You get the same triage result as calling the backend
directly — but now it flows through APIM.

---

## 🚦 Step 4 — Throttle traffic (`rate-limit-by-key`)

Apply an inbound policy on the `allclear` API. In the portal **APIs → All Clear
API → All operations → Inbound processing → Policy code editor**, or via REST,
add:

```xml
<inbound>
  <base />
  <rate-limit-by-key calls="20" renewal-period="60"
       counter-key="@(context.Request.IpAddress)" />
</inbound>
```

✅ **Checkpoint:** The 21st call within 60 s from the same IP returns
**429 Too Many Requests**.

---

## 🪙 Step 5 — Cap LLM spend (`azure-openai-token-limit`)

If All Clear's traffic to Azure OpenAI is fronted by this API, add a token
budget so a single caller can't burn the shared model quota:

```xml
<inbound>
  <base />
  <azure-openai-token-limit
       counter-key="@(context.Request.IpAddress)"
       tokens-per-minute="1000"
       estimate-prompt-tokens="true"
       remaining-tokens-header-name="x-tokens-remaining" />
</inbound>
```

> 💡 For non‑Azure‑OpenAI LLM backends use the equivalent `llm-token-limit`
> policy. Both emit remaining‑token headers you can watch in Step 7.

✅ **Checkpoint:** Responses carry an `x-tokens-remaining` header; exceeding the
budget returns **429** with a `Retry-After`.

---

## 🔐 Step 6 — Require a JWT (`validate-jwt`)

Lock the gateway to authorized callers (e.g. Entra ID tokens):

```xml
<inbound>
  <base />
  <validate-jwt header-name="Authorization" failed-validation-httpcode="401"
       failed-validation-error-message="Unauthorized">
    <openid-config url="https://login.microsoftonline.com/<tenant-id>/v2.0/.well-known/openid-configuration" />
    <audiences>
      <audience>api://allclear</audience>
    </audiences>
  </validate-jwt>
</inbound>
```

✅ **Checkpoint:** A request with **no** bearer token returns **401**; a request
with a valid token succeeds.

---

## 📊 Step 7 — Wire observability to Application Insights

```bash
AI_KEY=$(az monitor app-insights component show \
  -g "$RG" --app <your-appinsights> --query instrumentationKey -o tsv)

# Create the APIM logger bound to App Insights, then attach API diagnostics
az apim logger create -g "$RG" --service-name "$APIM_NAME" \
  --logger-id appinsights --logger-type applicationInsights \
  --credentials instrumentationKey=$AI_KEY
```

Then enable **Diagnostics** on the `allclear` API (portal: **APIs → All Clear
API → Settings → Diagnostics logs → Application Insights**) and set sampling to
100% for the lab.

✅ **Checkpoint:** Calls show up in App Insights **Application Map** /
**Requests**, with latency, response codes, and the rate‑limit 429s.

---

## 🧹 Step 8 — Clean up

```bash
az apim delete -n "$APIM_NAME" -g "$RG" --yes --no-wait
```

---

## ✅ Stage 4 Deliverables

- [ ] An APIM **Consumption** gateway in front of your All Clear backend.
- [ ] A signal successfully triaged **through** the gateway.
- [ ] `rate-limit-by-key` returning 429 past the threshold.
- [ ] `azure-openai-token-limit` emitting remaining‑token headers / 429 on budget.
- [ ] `validate-jwt` rejecting unauthenticated calls with 401.
- [ ] APIM telemetry flowing into Application Insights.

---

## 🔭 What's next

**Stage 5 (Lab 06):** deploy on Azure Container Apps with the eval suite gating
CI — the gateway you built here fronts that deployment.
