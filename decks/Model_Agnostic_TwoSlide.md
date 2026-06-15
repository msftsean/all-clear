# Two-Slide Script - Model-Agnostic Availability

**Output file:** `Model_Agnostic_TwoSlide.pptx`  
**House style:** Antimetal - use `decks\README.md` and `design\DESIGN-antimetal.md`.  
**Audience:** SLED ISVs selling to public safety, human services, courts, and education.  
**Design rule:** Midnight Navy `#1b2540` text only - never pure black. One Chartreuse Pulse CTA per slide max.

---

## Slide 1 - Executive: A model can vanish overnight

- **Layout:** Full-bleed **navy hero gradient** (`#001033 → #0050f8 → #5fbdf7`). Centered headline, short proof row at bottom.
- **Eyebrow (small caps, abcdFont):** MODEL AVAILABILITY IS A PRODUCTION CONTROL
- **Title (ivarTextFont serif, large, white):** A model can vanish overnight - your mission-critical system can't
- **Subtitle (abcdFont, white):** All Clear keeps incident triage governed when a primary chat model is unavailable.
- **Three proof chips (white text, subtle blue border):**
  1. **Continuity:** ordered chat fallback chain
  2. **Governance:** no failover around safety blocks
  3. **Auditability:** active model + fallback chain visible
- **Why It Matters (white card over gradient, Midnight Navy text):** For CJIS-focused public-safety ISVs, a model availability event cannot strand a surge queue or leave an auditor asking why incident triage stopped.
- **Primary CTA (Chartreuse Pulse `#d0f100`, pill):** Design for model availability
- **Speaker line:** "The news lesson is neutral but urgent: model availability is not guaranteed. In All Clear, that no longer means a single unavailable chat deployment strands classification."
- **Citations:** `specs\018-model-agnostic-failover\spec.md`; `backend\app\services\azure\failover_chat_client.py`; `GET /api/health/models`; `CONTEXT.md`.

---

## Slide 2 - Technical: The architecture that makes the claim real

- **Layout:** Light technical surface. Canvas `#f8f9fc`; four white cards with 1px blue shadow-ring border, 20px radius. Midnight Navy text. Use muted red only for the old demo gap.
- **Header:** Model continuity is one layer in a governed system
- **Architecture diagram (left-to-right):**
  1. **Signal arrives** → QueryAgent classification  
     `CONTEXT.md`
  2. **Chat model chain** → `FailoverChatClient(BaseChatClient)` tries primary, then configured fallback on unavailability  
     `backend\app\services\azure\failover_chat_client.py`; `backend\app\core\dependencies.py`
  3. **Deterministic routing** → `RouterExecutor` dedupes, maps Severity, Queue, SLA, and Escalation with zero LLM calls  
     `backend\app\agents\router_agent.py`; `backend\tests\test_router_no_llm.py`
  4. **Action + audit posture** → Incident / Report handling remains bounded by tools and constitution  
     `CONTEXT.md`; `shared\constitution.md`
- **Card 1 - Old demo gap (muted red):** Single chat deployment meant model disappearance could stall the pipeline.  
  **Cite:** `specs\018-model-agnostic-failover\spec.md`
- **Card 2 - Shipped failover (blue/green):** 404 `DeploymentNotFound`, 401/403 access denied, 503 service unavailable, and model-not-found advance to the next configured chat model.  
  **Cite:** `backend\app\services\azure\failover_chat_client.py`
- **Card 3 - Boundaries (blue/green):** 429 rate limits stay on retry/backoff; content-filter and Prompt-Shield blocks remain safety outcomes.  
  **Cite:** `backend\app\agents\retry.py`; `safety\README.md`; `specs\018-model-agnostic-failover\spec.md`
- **Card 4 - Proof (blue/green):** Guardrails, evals, red-team evidence, and compliance posture are documented artifacts.  
  **Cite:** `backend\app\agents\safety.py`; `safety\content-filter\allclear-guardrails.rai.json`; `backend\tests\test_voice\eval_harness.py`; `backend\tests\test_phone\eval_harness.py`; `evals\quality\quality_eval.py`; `evals\red-team\RESULTS.md`; `shared\constitution.md`
- **Per-task model strip (bottom):** Chat `gpt-5.1` / Voice `gpt-realtime` / Embeddings `text-embedding-3-small` - use the right model for the task, plus failover for chat availability.  
  **Cite:** `specs\018-model-agnostic-failover\spec.md`; `backend\app\services\azure\realtime.py`; `backend\app\services\azure\knowledge_service.py`
- **Why It Matters (callout):** For CJIS buyers, resilience is not enough; the fallback path must preserve escalation, audit, PII discipline, and a defensible record of which model served the workload.
- **Primary CTA (Chartreuse Pulse `#d0f100`, pill):** Show `/api/health/models` live
- **Speaker line:** "This is not provider roulette. It is a governed chat failover layer, per-task model selection, deterministic routing, and eval evidence in one architecture."
