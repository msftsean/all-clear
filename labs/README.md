# 🛰️ All Clear — Builder Labs (Developer Track)

> **Audience:** developers who will build, extend, and operate All Clear.
> **Companion:** coaches/demo-runners should start with the
> [Coach's Runbook](../coach-runbook/index.html) (capability exercises E1–E5).
> This track is the **hands-on, code-level** version of that material.

All Clear is an **incident-triage** system. Inbound **signals** (chat, voice,
phone, submitted reports) are classified, deduplicated against open
**incidents**, assigned a **severity** and **SLA**, and acted on by a
three-agent pipeline running on the **Microsoft Agent Framework (MAF)**. The
hero scenario is a **surge**: a storm/outage/recall where most signals are
duplicates of a few real incidents.

Before you start, read [`../CONTEXT.md`](../CONTEXT.md) (the domain language)
and [`../shared/constitution.md`](../shared/constitution.md) (the
non-negotiable principles). The labs use those words exactly.

---

## 🧭 The pipeline you are building

```
        signal in                                        response out
            │                                                  ▲
            ▼                                                  │
   ┌─────────────────┐   ┌──────────────────┐   ┌──────────────────────┐
   │   QueryAgent     │──▶│  RouterExecutor   │──▶│     ActionAgent       │
   │  (MAF agent)     │   │ (deterministic,   │   │  (MAF agent, 3 tools) │
   │  classify only   │   │  zero LLM calls)  │   │  create_incident      │
   │                  │   │  dedup → severity  │   │  search_knowledge     │
   │ SignalClassif.   │   │  → SLA → escalate  │   │  generate_sitrep      │
   └─────────────────┘   └──────────────────┘   └──────────────────────┘
```

| Stage | Authority (Constitution Art. II) | Output |
| ----- | -------------------------------- | ------ |
| **QueryAgent** | Classify only — cannot route, create, search, or act | `SignalClassification` |
| **RouterExecutor** | Decide only — **zero LLM calls**, no tools, touches no records | `RoutingDecision` (dedup outcome, SEV1–4, SLA, escalation) |
| **ActionAgent** | Act only through its three tools | `IncidentAction` (incident, sitrep, citations) |

Reference implementation lives in
[`../backend/app/agents/`](../backend/app/agents/) — these labs teach you how it
was built and how to extend it.

---

## 📚 The phases

| Lab | Phase | What you build | Time |
| --- | ----- | -------------- | ---- |
| [00](00-setup/) | **Setup** | Get a working environment (Codespaces or `azd up`); run the full pipeline in **mock mode** offline | 30 min |
| [01](01-understanding-agents/) | **Understanding agents** | Classify a raw signal into a typed `SignalClassification` (intent, entities, severity indicators, PII) | 45 min |
| [02](02-azure-mcp-setup/) | **Azure + MCP setup** | Optional live-path setup for Azure OpenAI, AI Search, and Container Apps; not required for offline first success | 45 min |
| [03](03-spec-driven-development/) | **Spec-driven development** | Use Spec Kit + the All Clear constitution to spec a new capability, then generate code from the spec | 60 min |
| [04](04-build-rag-pipeline/) | **RAG / knowledge** | Optional live-path indexing of incident runbooks & SOPs; the mock KB backs Lab 00/01/05 | 60 min |
| [05](05-agent-orchestration/) | **Orchestration** | Assemble the QueryAgent → RouterExecutor → ActionAgent workflow; run a **surge** and watch dedup attach reports | 90 min |
| [06](06-deploy-with-azd/) | **Deploy** | Optional live-path deployment to Azure Container Apps with Bicep infra | 60 min |
| [07](07-mcp-server/) | **MCP server** | Expose All Clear's tools (`create_incident`, `search_knowledge`, `generate_sitrep`) as an MCP server | 60 min |
| [09](09-github-in-the-lab/) | **GitHub-in-the-lab path** | Fork + run `smoke-test.yml` + complete one bounded Copilot extension behind a red-to-green starter test | 45 min |

**Recommended 180-minute order:** 00 → 01 → 05 are the spine (signal in,
classify, orchestrate) and run in mock mode with no Azure credentials. 02/03/04
deepen the platform. 06/07 are optional live-path topics for teams that already
have Azure access.

---

## 🩺 The vocabulary you must use

These come straight from [`../CONTEXT.md`](../CONTEXT.md). Code and docs use one
canonical term per concept:

- **Signal** — one inbound communication. Never deduplicated away; always preserved.
- **Incident** (`AC-####`) — the real-world event signals describe. Has a severity, queue, SLA clock, magnitude, status.
- **Report** — the attachment of a signal to an incident. Increments **magnitude**.
- **Queue** — destination work stream (`field-operations`, `customer-comms`, `compliance-desk`, `engineering`, `escalations`). *(Replaces 47 Doors "department".)*
- **Severity** — **SEV1** (life safety / total outage / statutory clock; 15-min SLA, always escalates) … **SEV4** (informational; next-business-day). *(Replaces "priority".)*
- **Dedup** — embedding-similarity match of a signal against open incidents in the same `intent_category`. ≥ `DEDUP_THRESHOLD` (default 0.83 cosine) → **ATTACH_TO_INCIDENT**; below → **OPEN_INCIDENT**.
- **Sitrep** — citation-grounded situation report from `generate_sitrep`. No citation, no claim.
- **Surge** — inbound volume spike where most signals duplicate a few incidents. The hero scenario.
- **All clear** — terminal state: every incident resolved, every SLA satisfied. Also the product name.

---

## 🔒 Three rules that outrank everything (Constitution)

1. **Bounded authority.** Each agent does only what its role allows — QueryAgent
   classifies, RouterExecutor decides (no LLM), ActionAgent acts only through its
   three tools. Enforced by code structure, not prompt hope.
2. **Escalation is a safety control.** SEV1 and statutory-clock incidents
   **always** escalate; no model output can downgrade them. Code that weakens
   escalation is a security blocker, not a finding.
3. **Truth over fluency.** Every factual claim in a sitrep or response cites a
   source record. Classification uses typed structured output, never free-text
   parsing. When the system doesn't know, it says so and escalates.

You will prove all three hold in Lab 05.

---

## ▶️ Quick start

```bash
# from repo root
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# run the workshop readiness gates offline (no Azure needed)
npm run readiness
npm run quickstart:mock
```

Then open [Lab 00](00-setup/) and work forward. Each lab has a `README.md`
(walkthrough), a `SPEC.md` (what "done" means), and a verifier
(`test_labNN.py` or a `verify_*.py`) you run to grade your own work.
