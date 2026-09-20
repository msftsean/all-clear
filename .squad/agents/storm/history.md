# History

## Project Context

All Clear is a bounded-authority incident-triage accelerator requested by
MARYLAND ADMIN 01.

## Learnings

### 2026-09-20 — External coach runbook refresh must stay narrative-level

Reviewed the extracted source for the separate public repo
`Public-sector-hacks-Org/all-clear-coaches-runbook` before drafting a handoff
pack in this repo. Key takeaway: the right refresh is **not** to copy internal
implementation details forward, but to translate recent upstream progress into
two public-safe updates only:
- add a glass-box-vs-black-box coaching cue that rewards inspectable evidence
  and honest limits over polished unsupported output
- clarify that demo deployments may answer a real inbound voice call while
  still forbidding outbound contact, public notification, and dispatch

Also confirmed the repo's own `npm test` chain is the authoritative definition
of "fresh evidence" for `docs/RED-TEAM-EVALUATION.md`, so any update prompt
must require a real rerun rather than a date-only documentation bump.

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
