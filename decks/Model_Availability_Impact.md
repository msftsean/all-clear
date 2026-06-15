# Model Availability Impact - All Clear

**Purpose:** evaluate how a global model-availability event affects the All Clear narrative and what the presenter should say now that feature `018-model-agnostic-failover` closes the continuity gap.

## 1. The news in one neutral sentence

A security concern raised through industry channels triggered a rapid policy response that removed a frontier model's access globally; the takeaway for regulated buyers is simple: **model availability is not guaranteed**.

## 2. Pillar-by-pillar evaluation

| Talk-track pillar | Presenter claim | Status now | Exact artifact citations |
| --- | --- | --- | --- |
| Model-agnostic continuity | All Clear no longer depends on one chat deployment staying available; `FailoverChatClient` wraps an ordered primary-plus-fallback chat-model chain and advances only on model-unavailability errors. | **Backed - the prior gap is closed by this feature.** No-op unless a fallback is configured. | `backend\app\services\azure\failover_chat_client.py`; `backend\app\core\dependencies.py`; `specs\018-model-agnostic-failover\spec.md` |
| Model-status visibility | Operators and the stage demo can show the active model, ordered fallback chain, and last-served model. | **Backed.** This is the live resilience surface for the talk. | `GET /api/health/models`; `specs\018-model-agnostic-failover\spec.md` |
| Honest failover boundaries | Failover is for model unavailability: HTTP 404 `DeploymentNotFound`, 401/403 access denied, 503 service unavailable, and model-not-found errors. It does **not** route around 429 rate limits or content-filter / Prompt-Shield blocks. | **Backed.** This keeps resilience from becoming safety bypass. | `backend\app\services\azure\failover_chat_client.py`; `backend\app\agents\retry.py`; `specs\018-model-agnostic-failover\spec.md` |
| Per-task model reality | All Clear already uses different models per task: chat on `gpt-5.1` in East US, voice on `gpt-realtime` in Sweden Central, and embeddings on `text-embedding-3-small`. | **Backed.** Say "per-task model selection plus chat failover," not generic provider hopping. | `specs\018-model-agnostic-failover\spec.md`; `backend\app\services\azure\realtime.py`; `backend\app\services\azure\knowledge_service.py` |
| Guardrails | All Clear has layered guardrails: intent-independent crisis override, deterministic zero-LLM routing, Foundry content filter `allclear-guardrails`, and escalation treated as a security control. | **Backed.** This pillar was already true before the failover feature. | `backend\app\agents\safety.py`; `backend\app\agents\router_agent.py`; `backend\tests\test_router_no_llm.py`; `safety\README.md`; `safety\content-filter\allclear-guardrails.rai.json`; `shared\constitution.md` Article III |
| Evaluations | All Clear has executable eval coverage and Foundry red-team results at 0% ASR. | **Backed.** Cite the eval suites and quality harness in the checkout plus the Foundry red-team artifact. | `backend\tests\test_voice\eval_harness.py`; `backend\tests\test_phone\eval_harness.py`; `evals\quality\quality_eval.py`; `backend\scripts\check_eval.py`; `evals\red-team\RESULTS.md`; `evals\quality\README.md` |
| Compliance posture | The codebase uses a CJIS mindset: least privilege, full audit, no PII echo, bounded authority, mock-mode determinism, and escalation-as-security-control. | **Backed.** This is the governance half of the resilience story. | `CONTEXT.md`; `shared\constitution.md` Article I; `README.md`; `backend\app\agents\router_agent.py` |

## 3. What to emphasize vs soften

### Emphasize

- **The old gap is closed:** the model-agnostic claim is now literal for the chat path because a configured fallback deployment can serve when the primary chat model is unavailable.
- **Continuity and governance move together:** All Clear does not fail over around safety decisions; content-filter and Prompt-Shield blocks remain final safety outcomes.
- **Per-task model selection is real today:** chat, voice, and embeddings already use different models because each task has different latency, modality, and quality needs.
- **The status endpoint makes resilience auditable:** `/api/health/models` gives operators a concrete answer to "which model served this request path?"
- **Escalation is model-independent:** SEV1, statutory-clock, crisis, and PII escalation rules are deterministic controls, not model vibes.

### Soften

- Do **not** imply arbitrary provider hopping, dynamic marketplace routing, or automatic migration to any model family.
- Do **not** claim failover covers rate limiting; 429 remains the retry/backoff path in `backend\app\agents\retry.py`.
- Do **not** claim failover bypasses guardrails; safety blocks are correct outcomes.
- Do **not** frame the news politically; keep the neutral lesson to model availability.
- Do **not** say "we are immune to outages." Say "a configured fallback chain prevents a single unavailable chat deployment from stranding triage."

## 4. The SLED continuity angle

For SLED ISVs, the buyer is not only asking whether the agent works; the buyer is asking whether the agent remains defensible when a vendor, regulator, or platform decision changes what models are available. A model crackdown cannot strand a mission-critical CJIS, HIPAA, or FERPA triage system mid-surge. All Clear now tells a balanced story: resilient chat availability through `FailoverChatClient`, transparent model status through `/api/health/models`, deterministic routing and escalation through `RouterExecutor`, and governance controls that refuse to route around safety, audit, or compliance outcomes.
