---
description: "Pending handoff task list for refreshing the external All Clear coach runbook repository"
---

# Tasks: External Coach Runbook Refresh

**Input**: [spec.md](./spec.md), [plan.md](./plan.md)
**Prerequisites**: External repo access and a working checkout of
`Public-sector-hacks-Org/all-clear-coaches-runbook`

**Status**: All tasks below are **pending**. No change has been made yet in the
external repository; this file is the forward-looking execution ledger for that
repo's coding agent.

## Phase 1: Re-establish the external-sharing boundary

1. [ ] **T001** Read `README.md` and `docs/EXTERNAL-SHARING-REVIEW.md` in the
   external repo before editing; preserve the repo's sanitized/public-safe
   boundary, HTTPS allowlist model, and "synthetic workshop use only" framing.
2. [ ] **T002** Reconfirm that no planned copy adds credentials, private
   hostnames, internal route names, feature codenames, exact phone numbers, or
   invented status claims for unreleased materials.

## Phase 2: Refresh runbook content

3. [ ] **T003** Edit `src/content.ts` to add one new stage cue (or expand an
   existing cue) about glass-box versus black-box coaching: reward inspectable
   evidence, explicit uncertainty, and recoverable design over polished but
   unsupported success.
4. [ ] **T004** Edit `src/App.tsx` to add one public-safe scenario or talking
   point in the scenarios/evaluation flow about an apparent success that should
   be challenged until the team can show evidence.
5. [ ] **T005** Edit `src/App.tsx` to add Bishop's inbound-voice clarification
   sentence in the coach-charter and/or safety boundary area while preserving
   the existing "no outbound communications or dispatch responders" claim:
   "Demo deployments may include a real inbound voice channel where the system
   answers a caller, but All Clear does not initiate outbound contact, notify
   the public, or dispatch responders; those actions remain under human
   authority."

## Phase 3: Refresh verification evidence

6. [ ] **T006** Run the external repo's full validation flow with `npm test`
   so the refreshed documentation is backed by real current evidence.
7. [ ] **T007** Update `docs/RED-TEAM-EVALUATION.md` with the actual
   re-verification date and the real outputs/results from the new `npm test`
   run; do not guess counts or reuse the September 10, 2026 wording.
8. [ ] **T008** Run `npm run screenshots` if the environment supports the
   repo's normal screenshot capture flow, and record any refreshed evidence in
   the place that repo already uses for screenshot notes.

## Phase 4: Preserve intentional unknowns and placeholders

9. [ ] **T009** Review the `other-runbooks` placeholder section and leave it
   unchanged unless explicit product direction authorizes changing the status of
   "Workforce Navigator" or "Constituent Connect".

## Phase 5: Final validation and handoff

10. [ ] **T010** Re-run or confirm the full validation set is green:
    `npm run typecheck`, `npm run test:unit`, `npm run build`,
    `npm run test:security`, `npm run test:links`, and `npm run test:e2e`
    (typically via `npm test`).
11. [ ] **T011** Make any necessary minimal test or copy assertions pass
    without weakening the repo's security/content/link checks.
12. [ ] **T012** Prepare a concise change summary that calls out the new
    glass-box coaching cue, the inbound-voice clarification, the refreshed
    verification date/evidence, and the deliberate decision to leave other
    runbook placeholders unchanged.

## Dependencies & Execution Order

- T001-T002 gate every later task.
- T003-T005 can be implemented together once the boundary review is complete.
- T006 must happen before T007 because the documentation update must be based on
  real output.
- T008 may follow T006 or T010 depending on the repo's preferred evidence flow.
- T009 is a bounded review task and should not turn into speculative edits.
- T010-T012 close the work only after the content and documentation refresh are
  complete.
