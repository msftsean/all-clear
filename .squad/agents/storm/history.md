# History

## Project Context

All Clear is a bounded-authority incident-triage accelerator requested by
MARYLAND ADMIN 01.

## Learnings

### 2026-09-20 — Increment 2 section added to exercise guide

Added "## Increment 2 — Azure deployment + evals (optional)" to
`exercises/01-glass-box-audit.md`, covering:
- `azd up` deployment (reuses existing frontend Container App, no new infra)
- Hosted control room at `https://<AZURE_FRONTEND_URL>/?page=audit` (SC-006)
- Foundry eval suite with `--skip-upload` (local-only) and full modes
- Five test scenarios (clean, fabrication_only, network_only, swarm_only, all_violations)
- Clear messaging that everything in Increment 1 works offline; this section is additive

Adapted from `specs/020-glass-box-audit/quickstart.md` Increment 2 section.
Matched existing guide's heading structure, bash code-block style, and voice
("reassuring, hands-on, practical"). Section makes optionality explicit so
facilitators understand zero Azure = still complete demo.
