# Feature Spec: 016-production-deployment

**Feature:** Deploy the All Clear backend (and frontend shell) to Azure Container Apps with a durable incident store
**Status:** Ready to build — handoff to Adrian
**Owner:** Sean Gayle
**Depends on:** 001-maf-rehost (backend T1–T14 complete, 274 tests green, live-smoked on gpt-5.1)
**Date:** 2026-06-12

---

## Problem Statement

All Clear's backend pipeline (QueryAgent → RouterExecutor → ActionExecutor on Microsoft Agent Framework) is fully implemented and validated against live Azure OpenAI gpt-5.1, but **nothing is deployed**. The live smoke test ran the pipeline locally against the model endpoint; there is no running host, and the incident store is still the in-memory `MockIncidentStore` — so incidents do not survive a process restart. This feature stands up the production footprint: hosting on Azure Container Apps, a durable incident store, managed-identity auth, and an azd one-command deploy that matches the 001 spec.

The inherited `infra/main.bicep` + `azure.yaml` come from the 47 Doors "University Front Door" accelerator and **drift from the All Clear spec** (wrong model, no `incidents` container, no embedding deployment, stale branding). This feature reconciles them.

## Goals

1. `azd up` provisions and deploys the full stack into Azure Container Apps from a clean subscription.
2. The incident store is durable (survives restarts) and implements `IncidentStoreInterface` with no behavioral drift from `MockIncidentStore` (Constitution Art. V.1 lockstep).
3. Live model is **gpt-5.1 only** (gpt-4.1 dropped per owner). Embeddings via `text-embedding-3-small`.
4. Auth is managed-identity-first for Azure OpenAI; no API keys in app config in production.
5. The api-version split discovered in T13 is encoded so live calls work in-container.

## Non-Goals

- Frontend feature build (the React surge board per `frontend/DESIGN.md`) — separate feature; this deploys a placeholder/static frontend container only.
- Voice/ACS production hardening — covered by 007-voice-demo-hardening.
- Multi-region / DR topology. Single region (East US) to match the existing Azure OpenAI resource.
- Azure HorizonDB adoption — see the Database Decision below; explicitly deferred to a future feature.

---

## Database Decision: Cosmos DB now, HorizonDB later

The incident store needs to: persist `IncidentRecord` docs, store one embedding vector per incident, return open incidents (and their vectors) filtered by `intent_category`, increment magnitude on attach, and allocate `AC-####` ids. **Note:** the dedup hot path is `get_open_incident_vectors(intent_category)` — the RouterExecutor pulls vectors and computes cosine **in-process**. So a native vector index is an optimization, **not a requirement** for v1; any store that persists a float array and filters by category suffices.

**Decision: Azure Cosmos DB for NoSQL (serverless).** Rationale: it is already provisioned and code-integrated (sessions + audit_logs), serverless bills ~nothing at demo scale, it is GA with an SLA, and the incident shape is a natural JSON document partitioned by `intent_category` (which is exactly the dedup query key). Lowest delta to ship.

### SWOT

**Azure Cosmos DB for NoSQL (serverless) — CHOSEN**
- Strengths: already in the stack/bicep; serverless → near-zero idle cost; GA + SLA; partition by `intent_category` makes same-category dedup queries cheap; native vector search available if we later want server-side ANN; in East US.
- Weaknesses: no relational joins/transactions across docs (we don't need them); magnitude increments need optimistic concurrency (etag) rather than a SQL `UPDATE ... SET m=m+1`.
- Opportunities: vector indexing can be switched on later without a data model change.
- Threats: RU spikes under an extreme surge — mitigated by serverless autoscale and the small open-incident cardinality per category.

**Azure Database for PostgreSQL Flexible Server + pgvector — bridge option**
- Strengths: ACID magnitude increments + a real audit table; pgvector (hnsw/ivfflat) for server-side dedup; Entra passwordless auth; **Postgres-compatible, so it is the clean migration path toward HorizonDB**.
- Weaknesses: a brand-new service to provision, wire, and authenticate (not currently in the stack); more ops than serverless Cosmos; min-cost burstable instance still bills 24×7 unlike serverless.
- Opportunities: if the team wants relational semantics or a Postgres skillset, this is the low-regret choice and pre-positions for HorizonDB.
- Threats: schedule risk for an ASAP handoff (more new surface than extending Cosmos).

**Azure HorizonDB — DEFERRED (not viable for this build)**
- Strengths: next-gen managed Postgres; disaggregated compute/storage; native DiskANN vector search + in-DB AI model management — the best long-term fit for an agentic, vector-heavy workload.
- Weaknesses: **public preview only (since Jun 2026), no GA, no SLA, no published pricing.**
- Opportunities: because it is Postgres-compatible, building on Postgres/pgvector now makes a later HorizonDB move low-friction.
- Threats: **availability** — see quota finding below. Not appropriate to put a deliverable handoff on a preview service.

### HorizonDB quota / availability finding (tenant `8251a5cb-...`, sub `098ef2f6-...` Cloudforce Sponsorship)

Checked live with `az` on 2026-06-12:
- Provider `Microsoft.HorizonDB` exists but is **`NotRegistered`**.
- Every preview feature flag is **`NotRegistered`**, including `Microsoft.HorizonDB/publicpreview`, `/eastus`, `/centralus`, `/westus2`, `/westus3`, `/swedencentral`, `/australiaeast`.
- The `clusters` resource type is offered only in **Australia East, Central US, Sweden Central, West US 2, West US 3** — **East US is not a live preview region** (our Azure OpenAI lives in East US).

**Conclusion: there is effectively no HorizonDB quota in this tenant today.** Using it would require registering the provider + opting into the public-preview allowlist **and** placing the database in a non-East-US region (cross-region latency to the model, or relocating the whole stack). For an ASAP handoff this is unjustified risk. Revisit HorizonDB at GA via a dedicated migration feature; the `IncidentStoreInterface` abstraction keeps that swap cheap.

---

## Functional Requirements

### FR-1: Durable incident store (`AzureCosmosIncidentStore`)
- New `app/services/azure/incident_store.py` implementing `IncidentStoreInterface` against a Cosmos `incidents` container.
- Document shape = `IncidentRecord` fields (incident_id, queue, severity, status, summary, intent_category, magnitude, sla_minutes, created_at, updated_at, escalated) **plus** an `embedding: list[float]` field and an `id`/partition key.
- **Partition key: `/intent_category`** (matches the dedup query scope from 001 Clarification #1).
- `attach_report` increments `magnitude` using etag optimistic concurrency.
- `next_incident_id()` allocates monotonic `AC-####` ids (a small counter document or `MAX(seq)+1` query under the partition); must be race-safe.
- Behavior must match `MockIncidentStore` exactly so the existing interface tests pass against both.

### FR-2: Dependency wiring
- `core/dependencies.py:get_incident_store()` branches on `settings.use_mock_services`: mock → `MockIncidentStore`, live → `AzureCosmosIncidentStore` (today it returns the mock unconditionally — **bug**).

### FR-3: api-version handling (from T13)
- Chat (`OpenAIChatClient`, Responses API on `/openai/v1/`) must use `api-version=preview`; dated versions return 400.
- Embeddings (`OpenAIEmbeddingClient`, `/deployments/...`) must use a **dated GA** version (e.g. `2024-10-21`); `preview` returns DeploymentNotFound (404).
- Therefore the two clients are pinned independently in `dependencies.py` (mirroring `scripts/live_smoke.py`).

### FR-4: Infrastructure (`infra/main.bicep`)
- Azure OpenAI account with two deployments: **gpt-5.1** (chat) and **text-embedding-3-small** (embeddings). Drop the gpt-4.1 default.
- Cosmos: add an **`incidents`** container (partition `/intent_category`) alongside `sessions` and `audit_logs`.
- Backend Container App env: `AZURE_OPENAI_API_VERSION=preview`, `AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small`, `AZURE_OPENAI_DEPLOYMENT=<gpt-5.1 deployment name>`, plus the Cosmos endpoint/db.
- Managed identity: grant the backend MI **Cognitive Services OpenAI User** (already present) and **Cosmos DB Built-in Data Contributor** (data-plane RBAC) so the app reads/writes incidents without a key.
- Rename the azd project/template/tags from `university-front-door-agent` to `all-clear`.

### FR-5: azd deploy
- `azd up` (provision + deploy) succeeds from a clean env; `azd deploy` redeploys app code.
- Health endpoint `GET /health` returns 200 from the backend Container App FQDN.

---

## Acceptance Criteria

- [ ] `AzureCosmosIncidentStore` passes `tests/test_incident_store_interface.py` (same suite as the mock).
- [ ] `get_incident_store()` returns the Cosmos store when `MOCK_MODE=false`, mock otherwise.
- [ ] `USE_MOCK_MODE=true pytest` stays green (274+).
- [ ] `azd up` provisions OpenAI(gpt-5.1 + embeddings), Cosmos(+incidents container), Container Apps, ACR, Key Vault, Log Analytics with no manual steps.
- [ ] Backend Container App `GET /health` → 200; `POST /signals` with a downed-power-line signal returns a SEV1 `OPEN_INCIDENT` and the incident **survives a container restart** (durability proof).
- [ ] A duplicate signal in the same `intent_category` returns `ATTACH_TO_INCIDENT` (dedup works against the durable store, not just in-process memory).
- [ ] No API keys for Azure OpenAI in container env (managed identity only); `disableLocalAuth: true` retained.
- [ ] Live calls succeed in-container (proves the api-version split is correct in prod, not just in `live_smoke.py`).

## Open questions for Adrian

1. Cosmos data-plane auth: managed identity (preferred, needs the data-contributor role assignment) vs. the existing key-in-Key-Vault pattern. Spec assumes MI; confirm.
2. `next_incident_id()` strategy under concurrency: counter doc vs. `MAX+1`. Spec leans counter doc for race-safety.
3. Frontend: deploy the static placeholder now, or wait for the real surge board? Spec deploys placeholder.
