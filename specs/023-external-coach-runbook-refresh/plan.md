# Implementation Plan: External Coach Runbook Refresh

**Branch**: `main` | **Date**: 2026-09-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from
`/specs/023-external-coach-runbook-refresh/spec.md`

## Summary

Prepare a precise handoff for refreshing the separate public repo
`Public-sector-hacks-Org/all-clear-coaches-runbook`. The refresh should make
the guide feel current again by adding one new glass-box-audit coaching talking
point, clarifying that some demo deployments may answer a real inbound voice
call while still forbidding outbound/dispatch actions, and updating the repo's
verification report from a stale September 10, 2026 baseline to a fresh rerun.
Because this session lacks direct write access to that repo, the implementation
artifact here is a ready-to-paste prompt plus the usual Spec Kit records.

## Technical Context

**Language/Version**: Markdown in this repository; target repo uses TypeScript
5, React 18, and Vite 5
**Primary Dependencies**: None added here; target repo validation relies on its
existing `npm test` and `npm run screenshots` scripts
**Storage**: N/A in this repo; target repo remains a static site with no
server-side storage
**Testing**: Documentation-only here; target repo validation explicitly relies
on `npm test` (`typecheck`, `test:unit`, `build`, `test:security`,
`test:links`, `test:e2e`) and optionally `npm run screenshots`
**Target Platform**: Separate public static site repo:
`Public-sector-hacks-Org/all-clear-coaches-runbook`
**Project Type**: Spec Kit handoff pack in this repo; static React/Vite site in
the target repo
**Constraints**: Preserve sanitization boundary; no direct changes to the
external repo from this session; do not invent verification evidence; do not
change placeholder runbook status
**Scope**: Four new files under
`specs/023-external-coach-runbook-refresh/`, one history append, and one squad
decision inbox note

## Constitution Check (adapted for external-sanitized content)

*GATE: Must pass before writing the handoff prompt.*

- [x] No proposed copy weakens bounded authority or implies autonomous
      consequential action. The wording keeps outbound contact, public
      notification, and dispatch under human authority.
- [x] No proposed copy leaks secrets, credentials, private endpoints, internal
      hostnames, internal route names, feature codenames, or exact phone
      numbers.
- [x] The glass-box addition stays at the coaching-narrative level and does not
      expose internal scripts, paths, or record counts from upstream material.
- [x] The plan preserves the external repo's own link-allowlist and sharing
      rules by explicitly requiring its `README.md` and
      `docs/EXTERNAL-SHARING-REVIEW.md` to be read first.
- [x] Verification evidence is required to come from real rerun output in the
      external repo, not from hand-written guesses.
- [x] Unknown product status remains unknown: the "other runbooks" placeholders
      stay unchanged unless separately directed.

## Source Review Used For This Plan

Reviewed the current external source snapshot at
`/tmp/coaches-runbook-src/all-clear-coaches-runbook-main/`, including:

- `src/App.tsx`
- `src/content.ts`
- `src/links.ts`
- `README.md`
- `docs/DEPLOYMENT.md`
- `docs/EXTERNAL-SHARING-REVIEW.md`
- `docs/RED-TEAM-EVALUATION.md`
- `docs/EXTERNAL-LINK-REVIEW.md`

Reviewed upstream context in this repo for the stale/missing content to reflect:

- `specs/020-glass-box-audit/spec.md`
- `specs/021-briefing-room-demo-readiness/spec.md`
- `specs/022-event-day-readiness-verification/spec.md`

## Proposed External-Repo Changes

### 1. `src/content.ts`

Add one public-safe stage cue that helps coaches contrast polished unsupported
output with inspectable evidence. Proposed direction:

- add a cue such as **Reveal** or expand **Reflect** to say coaches should
  reward explicit uncertainty and evidence review over unsupported fluency

This keeps the change inside the file that already owns reusable stage-cue copy.

### 2. `src/App.tsx`

Make the content refresh visible where coaches actually read it:

- update the boundary banner and/or the safety / coach-charter area to include
  Bishop's recommended clarification:
  *"Demo deployments may include a real inbound voice channel where the system
  answers a caller, but All Clear does not initiate outbound contact, notify
  the public, or dispatch responders; those actions remain under human
  authority."*
- add one scenario or callout in the existing scenarios / evaluation narrative
  about a system that appears successful until transparent evidence reveals
  missing support, so judges reward recoverable design over polished
  fabrication

Because the current scenario cards are hard-coded in `App.tsx`, at least one
visible scenario/talking-point edit belongs there even if `content.ts` also
gets a cue update.

### 3. `docs/RED-TEAM-EVALUATION.md`

Refresh the stale verification record:

- replace the September 10, 2026 line with the actual rerun date
- rerun `npm test` and update the reported stage results with the real outputs
- run `npm run screenshots` if applicable in that environment and note the
  evidence location consistently with the repo's current documentation style

### 4. Explicit non-goals

- Do **not** add internal route names, feature names, or exact phone numbers
- Do **not** add new external URLs beyond the repo's existing allowlist model
- Do **not** change `other-runbooks` placeholder status unless separately
  instructed
- Do **not** turn the static field guide into a live telephony surface; the
  change is explanatory copy only

## Deliverables In This Repository

```text
specs/023-external-coach-runbook-refresh/
├── spec.md
├── plan.md
├── tasks.md
└── PROMPT.md
```

Plus:

- `.squad/agents/storm/history.md` append with the handoff learning
- `.squad/decisions/inbox/storm-coach-runbook-refresh.md` with a short squad
  decision note

## Verification Matrix

| Surface | Command or check |
|---|---|
| Spec pack exists | Confirm `spec.md`, `plan.md`, `tasks.md`, and `PROMPT.md` are created under `specs/023-external-coach-runbook-refresh/` |
| Prompt accuracy | Cross-check prompt instructions against the inspected external files and repo scripts |
| Sanitization boundary | Confirm prompt forbids credentials, internal hostnames, route names, feature codenames, exact phone numbers, and invented status claims |
| External verification stages | Confirm prompt mirrors the target repo's `npm test` stages and mentions `npm run screenshots` separately |
| Squad memory | Confirm Storm history append and inbox decision note are present |

## Complexity Tracking

*No Constitution Check violations — this section is intentionally empty.*
