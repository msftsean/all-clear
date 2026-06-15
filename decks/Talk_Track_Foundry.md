# Talk Track - Azure AI Foundry + Model Availability

**Tone:** calm architect.  
**Rule for delivery:** every factual claim names an artifact; anything forward-looking is labeled as architecture or vision.

## Opening

"All Clear is a regulated-industry incident-triage agent built on Microsoft Agent Framework. It takes an inbound **Signal**, classifies it, routes it deterministically, creates or attaches an **Incident**, and preserves the **Report** trail for audit."  
**Cite:** `CONTEXT.md`; `backend\app\agents\router_agent.py`; `shared\constitution.md`.

"This matters for the SLED room because your buyers live with CJIS, HIPAA, FERPA, chain-of-custody, auditors, and compliance officers. The demo has to become a governed product."  
**Cite:** `decks\README.md`; `CONTEXT.md`; `shared\constitution.md` Article I.

## Frame the problem

"A security concern raised through industry channels triggered a rapid policy response that removed a frontier model's access globally. The non-political lesson is that model availability is not guaranteed."  
**Cite:** `specs\018-model-agnostic-failover\spec.md`.

"For a consumer demo, that is inconvenient. For an incident-triage system during a surge, it is operational risk."  
**Cite:** `CONTEXT.md` definitions of Signal, Incident, Surge, Severity, Queue, and Escalation.

## The risk

"If the system depends on exactly one chat deployment, the failure mode is obvious: the model disappears, classification stalls, routing stalls, and the queue loses the signal-to-incident bridge."  
**Cite:** `specs\018-model-agnostic-failover\spec.md`.

"In public safety, human services, courts, or education, that is not just downtime. It can become an audit question: what happened, when, who handled it, and why did the triage system stop?"  
**Cite:** `CONTEXT.md`; `shared\constitution.md` Article I.

## Transition

"So the question is not 'which model is best?' The production question is 'what controls survive when a model is unavailable?'"  
**Architecture framing.**

"All Clear answers that across four pillars: model continuity, guardrails, evaluations, and compliance."  
**Cite:** `specs\018-model-agnostic-failover\spec.md`.

## Foundry positioning

"Foundry is the governance plane in this story: model surface, content-filter guardrails, evals, and red-team evidence all belong in the same operating conversation."  
**Cite:** `safety\README.md`; `safety\content-filter\allclear-guardrails.rai.json`; `evals\red-team\RESULTS.md`; `evals\quality\README.md`.

"The architecture vision is not model loyalty. It is a controlled Azure boundary where model choice, safety policy, eval evidence, and operator visibility are explicit."  
**Architecture / vision framing.**

## Model-agnostic layer

"This feature makes the model-agnostic claim literal for the chat path. `FailoverChatClient` implements the Microsoft Agent Framework `BaseChatClient` interface and wraps an ordered list of chat clients: primary first, fallback next."  
**Cite:** `backend\app\services\azure\failover_chat_client.py`; `backend\app\core\dependencies.py`.

"When the primary chat deployment returns a model-unavailability condition - 404 `DeploymentNotFound`, 401 or 403 access denied, 503 service unavailable, or model-not-found - All Clear advances to the next configured model."  
**Cite:** `backend\app\services\azure\failover_chat_client.py`; `specs\018-model-agnostic-failover\spec.md`.

"The layer is intentionally a no-op until a fallback is configured, so existing single-model deployments keep their current behavior."  
**Cite:** `backend\app\services\azure\failover_chat_client.py`; `specs\018-model-agnostic-failover\spec.md`.

"It does not route around 429 rate limits. Those remain the retry/backoff path."  
**Cite:** `backend\app\agents\retry.py`; `specs\018-model-agnostic-failover\spec.md`.

"It does not route around content-filter or Prompt-Shield blocks. A safety block is the system working, not an outage to escape."  
**Cite:** `backend\app\services\azure\failover_chat_client.py`; `safety\README.md`; `specs\018-model-agnostic-failover\spec.md`.

"Operators can also ask the system what is live: `GET /api/health/models` reports the active model, the ordered fallback chain, and the last-served model."  
**Cite:** `GET /api/health/models`; `specs\018-model-agnostic-failover\spec.md`.

"And All Clear is already multi-model by task: chat uses `gpt-5.1` in East US, voice uses `gpt-realtime` in Sweden Central, and embeddings use `text-embedding-3-small`."  
**Cite:** `specs\018-model-agnostic-failover\spec.md`; `backend\app\services\azure\realtime.py`; `backend\app\services\azure\knowledge_service.py`.

"So the honest statement is: per-task model selection today, automatic chat failover when configured, and no safety bypass."  
**Cite:** `specs\018-model-agnostic-failover\spec.md`.

## Guardrails

"All Clear's first guardrail is application-level: `safety.py` applies an intent-independent crisis override. If someone expresses self-harm, the crisis path does not depend on whether the classifier guessed the right intent."  
**Cite:** `backend\app\agents\safety.py`; `backend\tests\test_voice\test_safety_net.py`.

"The second guardrail is deterministic routing. `RouterExecutor` is zero-LLM by design: dedup, severity, SLA, queue, and escalation are rules, not model vibes."  
**Cite:** `backend\app\agents\router_agent.py`; `backend\tests\test_router_no_llm.py`; `CONTEXT.md`.

"The third guardrail is platform-level: the `gpt-5.1` deployment carries the Foundry content filter `allclear-guardrails`."  
**Cite:** `safety\README.md`; `safety\content-filter\allclear-guardrails.rai.json`; `evals\register-agent\README.md`.

"The fourth guardrail is constitutional: escalation is a security control. Code that weakens it is a security blocker, not a refactor."  
**Cite:** `shared\constitution.md` Article III; `CONTEXT.md`.

## Evaluations

"All Clear does not ask the audience to trust a prompt. It has executable eval coverage for the agent surfaces."  
**Cite:** `backend\tests\test_voice\eval_harness.py`; `backend\tests\test_phone\eval_harness.py`; `evals\quality\README.md`.

"The quality eval suite runs against the agent surfaces, and the Foundry red-team result shows 0% attack success rate for the recorded run."  
**Cite:** `evals\quality\quality_eval.py`; `backend\scripts\check_eval.py`; `evals\red-team\RESULTS.md`.

"That is the operating model regulated buyers expect: measure behavior, record results, and rerun the suite when the system changes."  
**Architecture framing backed by eval artifacts above.**

## Compliance

"All Clear uses a CJIS mindset everywhere: least privilege, full audit, no PII echo."  
**Cite:** `CONTEXT.md`; `README.md`; `shared\constitution.md` Article I.

"Each agent has bounded authority. QueryAgent classifies. RouterExecutor routes deterministically. ActionAgent can only use its tools."  
**Cite:** `CONTEXT.md`; `backend\app\agents\router_agent.py`; `shared\constitution.md`.

"Mock mode keeps the demo and tests deterministic without Azure credentials."  
**Cite:** `CONTEXT.md`; `specs\018-model-agnostic-failover\spec.md`; `README.md`.

## Real-world use case

"Picture a county outage, campus incident, court notification surge, or public-safety overflow. Hundreds of Signals arrive. Most are duplicates. Some are SEV1. Some carry PII. Some start statutory clocks."  
**Cite:** `CONTEXT.md`.

"All Clear separates signal from noise: preserve every Signal, attach duplicates as Reports, keep Incident magnitude visible, map Severity deterministically, and move work into the right Queue."  
**Cite:** `CONTEXT.md`; `backend\app\agents\router_agent.py`.

"If the primary chat model becomes unavailable during that surge, configured chat failover keeps classification moving while the deterministic routing, escalation, audit, and safety controls remain intact."  
**Cite:** `backend\app\services\azure\failover_chat_client.py`; `backend\app\agents\router_agent.py`; `backend\app\agents\safety.py`; `shared\constitution.md`.

## Close

"For SLED ISVs, the competitive edge is not a clever demo. It is a system your buyer can defend to a compliance officer and an auditor."  
**Cite:** `decks\README.md`; `shared\constitution.md`.

"All Clear's position is balanced: model continuity without safety bypass, guardrails without theater, evals with receipts, and compliance controls that match the domain."  
**Cite:** `specs\018-model-agnostic-failover\spec.md`; `safety\README.md`; `evals\red-team\RESULTS.md`; `CONTEXT.md`.

## Mic-drop

"The future isn't about picking the right model. It's about building systems that work no matter which model is available."  
**Architecture / vision framing, grounded by:** `backend\app\services\azure\failover_chat_client.py`; `GET /api/health/models`; `specs\018-model-agnostic-failover\spec.md`.
