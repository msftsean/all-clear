# Feature Spec: 001-maf-rehost

**Feature:** Rehost the All Clear agent layer on Microsoft Agent Framework (GA line)
**Status:** Draft, ready for `speckit.clarify`
**Owner:** Sean Gayle
**Source system:** 47 Doors (github.com/msftsean/47doors), backend/app/agents/*

---

## Problem Statement

The three-agent pipeline (QueryAgent, RouterAgent, ActionAgent) is implemented as hand-rolled Python classes calling the LLM through `LLMServiceInterface`. The ISV Summit lab teaches Microsoft Agent Framework, so the agent layer must be rehosted on MAF while preserving everything that survived six months of production: the bounded-authority contracts, the mock/live service interface pattern, the prompts and schemas, and the FastAPI host.

## Goals

1. QueryAgent and ActionAgent become MAF `Agent` instances. RouterAgent becomes a deterministic MAF workflow `Executor` (no LLM call, by design).
2. The pipeline is composed as a MAF `Workflow` (Query → Router → Action) and invoked from the existing FastAPI routes through a thin adapter, so `api/routes.py` changes minimally.
3. RouterAgent gains one new capability: embedding-similarity deduplication of inbound signals against open incidents (the Surge Command Center scenario requirement).
4. The entire pipeline runs offline with `USE_MOCK_MODE=true` via a mock chat client and mock embedding function. No Azure dependency for labs 0-3.
5. All existing pytest suites pass or are ported with equivalent coverage.

## Non-Goals

- No changes to the voice/realtime pipeline (`services/azure/realtime.py`, `api/media_ws.py`, phone/ACS). It is reused as-is; only its tool definitions repoint at the new workflow adapter.
- No use of MAF beta connectors (`agent-framework-azure-ai-search`, `agent-framework-azure-cosmos` are beta). The existing `azure-search-documents` knowledge service and Cosmos session/audit services stay untouched.
- No use of `agent-framework-orchestrations` (rc, not GA). Core workflow abstractions only.
- No new agents. Three agents, bounded authority preserved.
- No frontend changes in this feature (surge board is feature 002).

## Functional Requirements

### FR-1: QueryAgent on MAF
- Implemented as `agent_framework.Agent` with the existing system prompt ported to `instructions`, taxonomy swapped to the All Clear signal taxonomy (see CONTEXT.md).
- Returns structured output: a `SignalClassification` Pydantic model (intent, intent_category, target_queue, confidence, entities including location/system/severity_indicators, requires_escalation, escalation_reason, pii_detected, pii_types, sentiment, urgency_indicators).
- Structured output enforced via `ChatOptions(response_format=SignalClassification)`; the typed result is read from `AgentResponse.value`.
- Authority bounds unchanged: classifies only. Cannot create incidents, cannot search knowledge, cannot route.

### FR-2: RouterAgent as deterministic Executor
- Implemented as an `agent_framework.Executor` subclass with an async `@handler` method. No chat client. No LLM call. This is a stated teaching point, preserve it.
- Inputs: `SignalClassification` (+ raw signal text). Output: `RoutingDecision`.
- Logic, in order:
  1. **Dedup:** embed the signal text (injectable async embedding function), cosine-compare against embeddings of open incidents (provided by an `IncidentStoreInterface`). If max similarity ≥ `DEDUP_THRESHOLD` (config, default 0.83), decision is `ATTACH_TO_INCIDENT` with the matched incident_id and increment magnitude. Otherwise `OPEN_INCIDENT`.
  2. **Severity/SLA:** apply the category→queue mapping and severity matrix (ported from the existing CATEGORY_TO_DEPARTMENT and priority rules, renamed for the new domain).
  3. **Escalation:** existing escalation intent set and PII/sentiment rules preserved.
- All thresholds and mappings in config, not code constants buried in the class.

### FR-3: ActionAgent on MAF with bounded tools
- Implemented as `agent_framework.Agent` with three tools (plain async functions passed to `tools=`, MAF wraps them):
  - `create_incident(routing: RoutingDecision) -> IncidentRecord` (delegates to TicketService/IncidentStore)
  - `search_knowledge(query: str) -> list[KnowledgeArticle]` (delegates to existing KnowledgeServiceInterface)
  - `generate_sitrep(incident_id: str) -> SitrepDraft` (citation-grounded, reuses the existing ACTION_AGENT citation prompt pattern)
- Authority bounds unchanged: cannot approve refunds/waivers, cannot modify records outside its tools, cannot bypass escalation.

### FR-4: Workflow composition and adapter
- `WorkflowBuilder().add_chain([...]).build()` composes the pipeline. QueryAgent and ActionAgent participate via `AgentExecutor` (or directly, builder accepts agents); RouterAgent is the custom Executor between them.
- A `AllClearPipeline` adapter class exposes `async process_signal(text, session_id, channel) -> PipelineResult`, matching the call shape the FastAPI routes and the voice tool-execution path already use. Routes change only their import and the result schema names.
- Workflow result obtained via `await workflow.run(message)`; pipeline events (classification done, dedup decision, action taken) published onto the existing transcript/SSE bus for the future surge board.

### FR-5: Mock mode
- `MockChatClient(BaseChatClient)` implementing `_inner_get_response`, returning canned-but-plausible `ChatResponse` objects keyed off simple text matching (same philosophy as the existing `mock/llm_service.py`).
- Mock embedding function: deterministic hash-projection vectors such that scripted duplicate signals in the surge replay file actually exceed the dedup threshold and distinct signals do not. The mock must make the dedup demo work offline.
- `core/dependencies.py` selects mock vs live clients exactly the way it does today.

## Acceptance Criteria

- [ ] `USE_MOCK_MODE=true pytest` green across ported suites
- [ ] Streaming the 25-signal storm replay through `process_signal` in mock mode yields ≤6 open incidents and ≥19 attachments (Exercise 5 checkpoint numbers)
- [ ] Live mode smoke: one signal end to end against a real Azure OpenAI gpt-5.1 deployment produces a typed `SignalClassification`, a `RoutingDecision`, and a created incident
- [ ] RouterAgent source contains zero chat-client imports (lint rule or test asserting it)
- [ ] Voice path: existing realtime tool execution successfully invokes the new adapter
- [ ] `requirements.txt` pins per plan.md Appendix A; `pip install` from a clean venv succeeds

## Clarifications (resolved 2026-06-12 via speckit.clarify)

1. **Dedup scope — RESOLVED: same intent_category only.** RouterExecutor compares an inbound signal's embedding only against open incidents sharing its `intent_category`. Cheaper and fewer false merges. The `IncidentStoreInterface` exposes `get_open_incidents(intent_category)` accordingly.
2. **Incident store — RESOLVED: new `incidents` container.** A dedicated Cosmos `incidents` container (not the tickets container with a discriminator), partitioned by `/intent_category`. Mock mode uses an in-memory `MockIncidentStore`. **Deployment status:** the container and the live `AzureCosmosIncidentStore` are specified and scaffolded in `specs/016-production-deployment` (build tasks D1–D2); the bicep now creates the container.
3. **ATTACH_TO_INCIDENT path — RESOLVED: short ack, no knowledge search.** Attaching a signal increments magnitude, records a report, and returns a short acknowledgment to the reporter. It does NOT run the full ActionAgent knowledge-search path, keeping surge latency flat. Only OPEN_INCIDENT triggers the full ActionAgent run.

### Original open questions (for traceability)

1. Dedup scope: compare against ALL open incidents or only incidents in the same intent_category? (Recommend same-category, cheaper and fewer false merges; confirm.)
2. Incident store: new Cosmos container or reuse the tickets container with a type discriminator? (Recommend new `incidents` container; bicep already creates containers conditionally.)
3. Should `ATTACH_TO_INCIDENT` still trigger an ActionAgent run (e.g., acknowledge the reporter) or short-circuit? (Recommend short ack path, no knowledge search, to keep surge latency flat.)
