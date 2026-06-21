# Lab to Production: All Clear Handoff

This leave-behind is for teams moving from demo momentum to production planning the same day.

## 1) Architecture at a Glance

All Clear runs a bounded three-stage pipeline:

1. **QueryAgent** classifies a signal.
2. **RouterExecutor** deterministically decides dedup/severity/SLA/escalation.
3. **ActionAgent** executes approved tools (incident, knowledge, sitrep).

Key posture: many incoming signals collapse into fewer incidents while preserving attribution and human approval boundaries.

## 2) Azure Footprint Summary

Core footprint used across mock/live storylines:

- Azure OpenAI (chat + embeddings)
- Azure AI Search
- Container Apps
- Cosmos DB
- Azure Communication Services
- Key Vault
- Container Registry
- Azure AI Foundry (red-team/evals)
- API Management (gateway posture)
- Azure Monitor / Log Analytics

All demo narratives remain mock-compatible; no live billing dependency is required for walkthrough fidelity.

## 3) Responsible AI Control Map

Use the policy mapping document for governance conversations:

- [Responsible AI control map](./responsible-ai.md)

Highlighted controls:

- bounded authority
- deterministic router
- escalation as control
- no-PII-echo posture
- audit logging / receipts
- Foundry red-team + evals
- model failover continuity

## 4) Same-Day CTA

If your team wants to move from workshop to pilot, start same day:

1. Pick one domain pack and one operational KPI.
2. Run the mock-mode baseline and keep the green gates.
3. Book a production-readiness working session with **Sean & Tracy’s team** to align architecture, policy controls, and launch plan.

## 5) Conversation Starter for the Working Session

- What must remain deterministic?
- Which escalation paths are mandatory by policy?
- What data classes require strict redaction/no-echo handling?
- Which KPIs prove value in the first 30 days?
