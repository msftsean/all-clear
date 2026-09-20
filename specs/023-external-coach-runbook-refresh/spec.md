# Feature Specification: External Coach Runbook Refresh

**Feature Branch**: `main`
**Created**: 2026-09-20
**Status**: Draft
**Input**: User description: refresh the separate, sanitized public repo
`Public-sector-hacks-Org/all-clear-coaches-runbook` so its external coach field
guide reflects recent upstream All Clear work without leaking internal-only
details, and capture that work here as a Spec Kit handoff pack plus a ready to
paste implementation prompt.

**Note on scope**: This specification does **not** change the external runbook
repository directly. We do not have direct write access to that repository from
this session. The deliverable in this repository is the documentation and
handoff prompt a coding agent can execute **inside**
`Public-sector-hacks-Org/all-clear-coaches-runbook`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - External coaches see an accurate current picture without internal leakage (Priority: P1)

An external coach or judge opens the public All Clear field guide and gets an
up-to-date explanation of what the workshop demo can now include: bounded
incident triage, transparent review of evidence, and a possible real inbound
voice demo. The guide stays sanitized and abstract — no credentials, private
hostnames, route names, feature codenames, phone numbers, or internal
implementation details leak into public-facing copy.

**Why this priority**: Accuracy without oversharing is the core requirement.
The external guide is intentionally public-safe and must stay that way even
while it becomes more current.

**Independent Test**: Review the proposed prompt and planned edits against the
current external source tree (`src/App.tsx`, `src/content.ts`,
`docs/EXTERNAL-SHARING-REVIEW.md`, `docs/RED-TEAM-EVALUATION.md`) and confirm
they add only abstract/public-safe concepts: a glass-box-vs-black-box coaching
talking point and an inbound-voice clarification that preserves the existing
human-authority boundary.

**Acceptance Scenarios**:

1. **Given** the external guide currently says All Clear does not send outbound
   communications or dispatch responders, **When** the refresh is applied,
   **Then** that safety boundary remains intact **and** coaches are explicitly
   warned that some demo deployments may answer a real inbound caller.
2. **Given** recent upstream work emphasized transparent auditing versus
   polished unsupported output, **When** the refresh is applied, **Then** the
   guide includes a public-safe coaching cue or scenario about rewarding honest
   boundaries and inspectable evidence over theatrical autonomy.
3. **Given** the guide is public and sanitized by design, **When** the refresh
   is applied, **Then** it introduces no private URLs, route names, codenames,
   internal file paths, exact phone numbers, or other internal-only details.

---

### User Story 2 - Verification evidence is current instead of 10-day-stale (Priority: P1)

An organizer reviewing the external repo's verification docs sees fresh,
truthful evidence instead of a stale "Final local verification on September 10,
2026" line. The repo's documented safety, link, content, and browser checks are
re-run and the evidence is updated to match the real outputs.

**Why this priority**: The public guide is making safety and review claims. If
its own verification record is stale, the guide looks abandoned even if the
content is otherwise sound.

**Independent Test**: The handoff prompt instructs the external-repo agent to
run that repo's real validation flow (`npm test`, plus `npm run screenshots` if
applicable) and update `docs/RED-TEAM-EVALUATION.md` with the actual date and
results of that rerun.

**Acceptance Scenarios**:

1. **Given** `docs/RED-TEAM-EVALUATION.md` currently cites September 10, 2026,
   **When** the refresh is executed in the external repo, **Then** it is
   replaced with the actual re-verification date and outcome from the current
   run.
2. **Given** the external repo's `npm test` pipeline runs typecheck, unit,
   build, security/content, link, and e2e checks, **When** the refresh is
   executed, **Then** the evidence update mirrors those exact stages rather than
   a hand-written summary detached from the real command.
3. **Given** screenshots are part of the external repo's evidence workflow,
   **When** the environment supports it, **Then** the refresh also regenerates
   screenshots without changing the public-safety boundary.

### Edge Cases

- The external guide must not imply "no live communication exists at all" once
  a real inbound voice demo exists; the wording needs clarification, not a
  safety-boundary rollback.
- The glass-box coaching addition must stay narrative-level and public-safe; it
  must not expose internal scripts, paths, record counts, or scenario internals
  from the upstream teaching exercise.
- The "Workforce Navigator" and "Constituent Connect" placeholders remain an
  open product-status question; this refresh must not invent URLs, timelines, or
  readiness claims for them.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: This Spec Kit record MUST document that the target of the refresh
  is the separate repository `Public-sector-hacks-Org/all-clear-coaches-runbook`
  and that the deliverable here is a handoff package, not a direct code change
  to that repository.
- **FR-002**: The handoff package MUST include `spec.md`, `plan.md`,
  `tasks.md`, and a single self-contained `PROMPT.md` under
  `specs/023-external-coach-runbook-refresh/`.
- **FR-003**: The planned external-repo edits MUST include a public-safe
  glass-box/black-box coaching addition in the runbook content, using generic
  narrative wording only.
- **FR-004**: The planned external-repo edits MUST include Bishop's
  safety-boundary clarification, preserving the existing outbound/dispatch
  restriction while explicitly allowing a real inbound voice-answering demo.
- **FR-005**: The planned external-repo work MUST refresh
  `docs/RED-TEAM-EVALUATION.md` with an actual new verification date and real
  rerun evidence, not guessed counts.
- **FR-006**: The planned external-repo work MUST leave the "other runbooks"
  placeholders unchanged unless a separate instruction authorizes changing them.
- **FR-007**: The handoff prompt MUST instruct the external-repo agent to read
  that repo's own sanitization guidance first (`README.md` and
  `docs/EXTERNAL-SHARING-REVIEW.md`) and to preserve its HTTPS allowlist /
  public-safe boundaries.
- **FR-008**: The handoff prompt MUST end with a definition-of-done checklist
  that mirrors the external repo's real validation flow: typecheck, unit tests,
  build, content/secret scan, link check, and e2e.

### Incident-Triage / Safety Constraints *(complete for every feature)*

- **Sanitization boundary**: Public-facing copy must remain abstract and
  external-safe. No credentials, private endpoints, internal hostnames beyond
  the repo's existing allowlist pattern, internal route names, feature
  codenames, or exact phone numbers may be introduced.
- **Authority boundary**: The proposed wording must continue to state that
  outbound contact, public notification, and dispatch remain under human
  authority.
- **Grounding boundary**: The new coaching material may describe transparent
  audit behavior at a narrative level, but it must not claim specific internal
  exercise mechanics as public facts unless those facts already belong in the
  external repo.
- **Verification boundary**: Documentation must be updated from real command
  output, not manually invented evidence.

## Key Entities

- **External coach field guide**: The separate public React/Vite static site in
  `Public-sector-hacks-Org/all-clear-coaches-runbook`.
- **Sanitization boundary**: The external-sharing rules that prohibit secrets,
  internal-only identifiers, and over-specific operational details.
- **Glass-box audit talking point**: A public-safe coaching cue that rewards
  inspectable evidence and honest uncertainty over unsupported fluency.
- **Verification record**: The dated evidence block in
  `docs/RED-TEAM-EVALUATION.md` backed by the repo's actual test pipeline.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `specs/023-external-coach-runbook-refresh/` exists with exactly
  `spec.md`, `plan.md`, `tasks.md`, and `PROMPT.md`.
- **SC-002**: The specification and plan explicitly state that the actual code
  changes belong in the separate external repo, not this repository.
- **SC-003**: `PROMPT.md` gives an external-repo coding agent exact, bounded
  edit instructions for `src/App.tsx`, `src/content.ts`, and
  `docs/RED-TEAM-EVALUATION.md`.
- **SC-004**: `PROMPT.md` includes the inbound-voice clarification sentence and
  a public-safe glass-box coaching addition without leaking internal-only
  details.
- **SC-005**: `PROMPT.md` ends with a definition-of-done checklist matching the
  external repo's validation stages and reminding the agent to preserve the
  sanitization boundary.
