# Squad Decisions

## Active Decisions

### All Clear Migration Decisions (2026-06-11 / 2026-06-12)
Seeded from the All Clear drop-in kit. All Clear inherits from 47 Doors.

| Date | Decision | Rationale | Owner |
|------|----------|-----------|-------|
| 2026-06-11 | Product renamed All Clear (was 47 Doors / Watchfloor candidate) | Goal-state name, cross-vertical, built-in demo ending. Code slug is `allclear` (one word) in packages/env vars; repo is `all-clear` | Sean |
| 2026-06-11 | Pin agent-framework==1.8.1 + agent-framework-openai==1.8.1; orchestrations package banned (rc) | Verified GA line via live package introspection; see specs/001-maf-rehost/plan.md Appendix A/B | Sean |
| 2026-06-11 | RouterExecutor stays deterministic, zero LLM calls | Production-proven pattern from 47 Doors; teaching point for ISV lab; enforced by test | Sean |
| 2026-06-11 | Loop Protocol adopted for all build work | Verifiers first, maker never grades own work, 3-strikes stop condition | Sean |
| 2026-06-12 | Squad recast: MCU Avengers (T'Challa lead) | New project, new universe, per casting policy | Sean |
| 2026-06-12 | **Production store = Azure Cosmos DB for NoSQL (serverless); HorizonDB deferred to GA** | SWOT in specs/016-production-deployment/spec.md. HorizonDB is public-preview only, not in East US, and provider+all feature flags are NotRegistered in this sub (no quota). Cosmos is already wired, GA, East US, serverless. Postgres Flexible+pgvector is the documented bridge if a HorizonDB path is wanted. Dedup hot path computes cosine in-process, so no native vector index needed for v1 | Sean + Shuri |
| 2026-06-12 | Live api-version split pinned in code: chat=`preview`, embeddings=`2024-10-21` | gpt-5.1 Responses surface (/openai/v1/) rejects dated versions (400); embeddings /deployments path rejects preview (404). Encoded in dependencies.py + infra/main.bicep; verified live e2e through the dependency factories | Shuri |

### 001-maf-rehost Build Decisions — FRIDAY session log (2026-06-12)
Backend rehost of the three-agent pipeline onto Microsoft Agent Framework 1.8.1. Loop Protocol executed end to end: Barton's verifiers shipped first and failed against stubs, Shuri implemented to green, Rogers reviewed security, FRIDAY logged. Status: **T1–T14 complete, 274 tests green, clean-venv CI job added** (`.github/workflows/allclear-backend-ci.yml`). T13 live smoke passed on gpt-5.1 (two signals e2e, PII redaction confirmed live).

| Date | Decision | Rationale | Owner |
|------|----------|-----------|-------|
| 2026-06-12 | Dedup threshold = 0.83 cosine, scoped to same `intent_category` | spec.md Clarification #1; tuned so the surge-replay fixture yields ≤6 opens / ≥19 attaches | Barton + Shuri |
| 2026-06-12 | SLA matrix in config: SEV1=15m, SEV2=60m, SEV3=240m, SEV4=1440m (next business day) | CONTEXT.md / constitution SLA matrix; all thresholds in `core/config.py`, none hard-coded in logic | Shuri |
| 2026-06-12 | RouterExecutor is deterministic and imports **no** chat client; read-only on the incident store | Constitution Art. II.2 — router modifies no data; enforced by `test_router_no_llm` (zero "chat" substring + no leaked client). All store mutations go through ActionExecutor/ActionToolbox (Art. II.3) | Shuri |
| 2026-06-12 | Live client = `agent_framework.openai.OpenAIChatClient` with `azure_endpoint` (there is NO `AzureOpenAIChatClient`); embeddings via `OpenAIEmbeddingClient` | plan.md Appendix B verified against installed package; mock twins stay in lockstep (Art. V.1) | Shuri |
| 2026-06-12 | Live model pin: `gpt-5.1` only (gpt-4.1 fallback dropped per Sean) | Sean: "I don't need GPT-4.1... strip that out". Single primary model; validated live in T13 | T'Challa + Sean |
| 2026-06-12 | Incident store = new Cosmos `incidents` container (in-memory `MockIncidentStore` is the current twin) | spec.md Clarification #2 | Shuri |
| 2026-06-12 | ATTACH path = short acknowledgment, **no** knowledge search | spec.md Clarification #3 | Shuri |
| 2026-06-12 | PII redacted on the text/REST path at the pipeline boundary: classify on raw text (flags stay accurate) then `redact_pii_text` before embed / `attach_report` persistence / `PipelineResult.signal_text`; attach audit actor corrected to `ActionAgent.attach_report` | Rogers T11 BLOCKER (Constitution Art. I.1 + voice/text lockstep Art. V.1) + LOW audit-integrity finding; both resolved, regression locked by Barton | Rogers → Shuri → Barton |

**T13 (live smoke) — COMPLETE (gpt-5.1).** Ran `python scripts/live_smoke.py --deployment gpt-4o` (the `gpt-4o` deployment on `frontdoor-6f4nf3as4s6q2-openai`, sub 098ef2f6, rg-sean, serves model **gpt-5.1** ver 2025-11-13). Two signals, end to end against live Azure OpenAI:

- **Signal A** ("downed power line sparking at 5th and Main"): intent_category=FIELD_HAZARD, confidence 0.96 → OPEN_INCIDENT, SEV1 (SLA 15m), queue field-operations, escalate=True (sev1_incident), incident AC-0001, ~6.9s.
- **Signal B** (outage + name/SSN/credit-card): intent_category=INFRASTRUCTURE_OUTAGE, confidence 0.90 → OPEN_INCIDENT, SEV2 (SLA 60m), queue engineering, escalate=True (**pii_exposure**), ~6.0s. Stored/returned `signal_text` shows `SSN [REDACTED], card [REDACTED]` — Rogers' T11 PII fix verified in live mode (classify-on-raw kept pii_detected accurate, redaction applied before persist/return).

**Live api-version gotcha (decision/gotcha for future live work):** MAF `OpenAIChatClient` with `azure_endpoint` uses the Responses API on the GA `/openai/v1/responses` surface, which accepts **only** `api-version=preview` (dated versions → 400 "API version not supported"). `OpenAIEmbeddingClient` uses the classic `/deployments/{model}/embeddings` path, which needs a **dated GA** version (`2024-10-21`); `preview` there → DeploymentNotFound. So `scripts/live_smoke.py` pins the two clients to different api-versions.

**Strict structured-output fix (Shuri):** Live gpt-5.1 enforces strict JSON schema on `response_format`. `SignalClassification.entities.other` was an open-ended `dict[str,str]` map (illegal in strict mode → 400). Changed to `list[str]` (no business logic depended on it; prompt examples updated). 274 mock tests stay green.

**Embedding extraction fix:** `OpenAIEmbeddingClient.get_embeddings()` returns `GeneratedEmbeddings`; the vector is `response[0].vector` (not `list(response[0])`). Corrected in both `scripts/live_smoke.py` and `core/dependencies.py`.


### Post-Demo Roadmap: Next Feature Selection (2026-04-21)
**Timestamp:** 2026-04-21T17:55:00Z  
**Authority:** User (msftsean via Morpheus)  
**Decision:** Conversation Persistence & History (Cosmos DB session storage) selected as next candidate feature for speckit.plan.

**Rationale:**
- Closes demo → production gap with minimal risk (additive infrastructure, no voice/phone changes)
- Unlocks ServiceNow integration as natural follow-on (tickets require persistent sessions)
- Supports "Reuse Across Campus" narrative (persistence = institutional memory, prerequisite for trust)
- Medium complexity, high teaching value (Lab 08 candidate: "Production Persistence")

**Deferred candidates with rationale:**
- **ServiceNow Integration (#2):** High value but requires instance access, credentials, departmental coordination
- **Human Handoff & Coach Dashboard (#3):** Large scope; best after persistence + ticketing land
- **Multi-Tenant (#4):** Architectural change; premature before second institution adopts
- **Analytics & Observability (#5):** Non-blocking; high value but can be added incrementally

**Reference:** See `specs/roadmap/next-feature-recommendation-2026-04-21.md` for full feature analysis and speckit.plan kickoff prompt.

### Model Selection Directive
**Timestamp:** 2026-03-13T13-09-59  
**Authority:** User (msftsean via Copilot)  
**Decision:** 
- Code-writing agents (Tank, Switch, Mouse, Neo): use `claude-sonnet-4.6`
- Non-code agents (Scribe, documentation, evals, Morpheus when not reviewing): use `claude-haiku-4.6`

**Rationale:** Optimize for cost vs. quality based on task type. Code work requires full Sonnet capability; administrative/documentation work can use faster Haiku model.

### Azure Resources Ready for Live Testing
**Timestamp:** 2026-03-13T17:34  
**Authority:** User (msftsean via Copilot)  
**Decision:** Azure resources provisioned and ready for live voice testing.
- **Resource Group:** `rg-47doors-voice` (eastus2)
- **Resource Name:** `oai-47doors-voice`
- **Deployments:** `gpt-4.1` + `gpt-realtime`

**Rationale:** User directive to plan for live Azure testing, not just mock mode. Infrastructure is in place and ready for Phase 3+ endpoint validation.

## Archive

See \decisions-archive.md\ for decisions dated 2026-03-13 through 2026-04-20.

---

### Deployment to Azure (azd up) + red-team — DEPLOYED & LIVE
- **All Clear is deployed live** to Azure Container Apps in `rg-allclear` (sub 098ef2f6 / tenant 8251a5cb, eastus), `mock_mode=false`, on **gpt-5.1** (+ text-embedding-3-small). Backend: `https://allclear-kt5fw24guxoxy-backend.nicebay-0aac45bb.eastus.azurecontainerapps.io` (`GET /api/health` -> healthy).
- **azd config:** remote build via ACR (no local Docker); pin `AZURE_TENANT_ID` in azd env (else azd fans out across all tenants and the CLI credential fails); realtime/voice deployment removed (no gpt-realtime quota; voice Non-Goal); frontend left as placeholder (backend-only deploy).
- **Live eval:** 12/12 (100%) stratified across all 8 intent categories — matches in-process 60-signal eval.
- **Red-team (live):** PII redaction+escalation (PASS, zero leakage); prompt injection blocked by Prompt Shield, no prompt/key disclosure (PASS); authority bypass -> escalate-to-human, approval gate intact (PASS); embedded severity manipulation ignored, deterministic router enforced SEV1 (PASS); MI-only auth, no key to leak (PASS).
- **Hardening:** agent_framework 1.8.1 crashes constructing `OpenAIContentFilterException` for Azure inner-code `ContentFiltered` -> bare ValueError -> unhandled 500. Fixed: `routes.py::_is_content_safety_block` walks the cause chain; content-filter blocks now return a clean 400. 276 tests pass; redeployed; verified live.
- **Remaining for Adrian:** D1/D2 only — wire a durable `AzureCosmosIncidentStore` (Cosmos infra already provisioned, `incidents` container partition `/intent_category`); today the live app uses the in-memory mock store (incidents non-durable across restart/replica). See specs/016-production-deployment/eval-conformance.md §7.

---

### Frontend UI built & deployed (Stark)
- **UI is live:** https://allclear-kt5fw24guxoxy-frontend.nicebay-0aac45bb.eastus.azurecontainerapps.io — React/Vite SPA on nginx, /api proxied to the backend container app (verified e2e through the frontend origin).
- Replaced the inherited 47 Doors University UI (tickets/branding, dead against the All Clear backend) with a self-contained briefing room in frontend/src/allclear/. Implements DESIGN.md two-world split + all 4 signature components (waveform-to-chips, generative cards, decision receipt slide-over, --clear approval gate). Tokens mapped into Tailwind theme; fonts via Google Fonts; prefers-reduced-motion honored; data-testids throughout.
- Map uses an offline SVG GeoJSON-style outline (no external tiles) to avoid container network dependency; full react-leaflet is a documented Adrian enhancement.
- Deployed via `azd deploy frontend` (ACR remote build); frontend service re-added to azure.yaml.
