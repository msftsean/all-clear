# Responsible AI Control Map (Maryland Policy Concepts)

This map ties existing All Clear controls to Maryland policy concepts (SB 818 intent areas and DoIT Responsible Use Policy themes) without changing runtime behavior.

## Scope

- **System:** All Clear incident-triage experience (mock and live postures)
- **Type:** Documentation + UI mapping only
- **Out of scope:** Router/action/query logic changes

## Policy-Control Mapping

| Control in All Clear | Implementation Surface | Policy Concept Mapping (SB 818 + DoIT themes) | Verification Signal |
|---|---|---|---|
| **Bounded authority** | Three-stage pipeline with constrained roles (classify → deterministic route → bounded tools) | Governance, role accountability, least privilege | Agent/tool scopes are explicit in architecture and receipts |
| **Deterministic router** | RouterExecutor rules for severity/SLA/dedup with no LLM routing | Reliability, repeatability, auditable decisioning | Decision receipt shows deterministic route and applied rules |
| **Escalation as a safety control** | Human escalation paths for safety/PII/sentiment and high-severity patterns | Human oversight, harm prevention, accountable intervention | Escalation indicators surfaced in chips/receipt and action outcomes |
| **No-PII-echo posture** | PII detection/redaction posture in user-facing flow and summaries | Data minimization, privacy-by-design, sensitive-data handling | PII state is surfaced while preventing plain-text echo in outputs |
| **Audit logging & decision receipts** | Structured receipt of classification, routing, and actions | Transparency, traceability, operational accountability | Receipt view captures who decided what and why |
| **Foundry red-team and eval practice** | Red-team/eval artifacts and policy validation workflow | Risk management, pre-deployment assurance, continuous evaluation | Foundry/eval references in architecture and delivery checks |
| **Model failover continuity** | Primary/fallback model status with failover badge support | Resilience, service continuity, operational readiness | Model status badge and health endpoints show active/fallback state |

## Maryland Alignment Notes

This document intentionally maps to **policy concepts**, not legal conclusions. Teams should pair this map with agency counsel and governance owners for formal attestations and filing requirements.

## Related Artifacts

- [Lab to Production leave-behind](./lab-to-production.md)
- [Root README](../README.md)
