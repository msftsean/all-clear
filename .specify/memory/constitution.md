<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 (implicit, unversioned) -> 2.0.0
Bump rationale: MAJOR — replaces the retired support domain and workflow
assumptions with the All Clear incident-triage architecture and its active
verification gates.
Modified principles:
  - Data Discipline -> Data Discipline and Privacy
  - Bounded Authority -> Bounded Incident Authority
  - Escalation Is a Safety Control -> Escalation and Severity Are Safety Controls
  - Truth Over Fluency -> Grounded Operational Output
  - Build Discipline -> Verifier-First Delivery
Added sections:
  - Delivery and Documentation Constraints
Removed sections:
  - References to retired product domains, deleted specifications, squad records,
    and unavailable smoke workflows.
Templates requiring updates:
  - .specify/templates/plan-template.md: updated
  - .specify/templates/spec-template.md: updated
  - .specify/templates/tasks-template.md: updated
Follow-up TODOs: None
-->

# All Clear Constitution

## Core Principles

### I. Data Discipline and Privacy (NON-NEGOTIABLE)

- The system MUST flag PII in inbound signals and MUST NOT echo it in responses,
  logs, synthesized voice, sitreps, or public updates.
- The system MUST persist only PII-filtered transcripts; it MUST NOT retain raw audio.
- Every incident or report mutation MUST be audit-logged with actor, timestamp, and
  cause.
- Embedding, retention, and external-service data flows MUST be documented and
  reviewed whenever they change.

**Rationale**: All Clear is incident triage. It handles operationally sensitive
information and adopts a least-privilege, audit-first posture.

### II. Bounded Incident Authority (NON-NEGOTIABLE)

- QueryAgent MUST classify only. It MUST NOT route, search, create, attach, or mutate.
- RouterExecutor MUST deterministically deduplicate, map severity/SLA, and decide
  escalation. It MUST make zero LLM calls, hold no action tools, and mutate no records.
- ActionAgent MUST act only through `create_incident`, `search_knowledge`, and
  `generate_sitrep`. It MUST NOT override RouterExecutor decisions or suppress
  escalation.
- Every signal MUST remain attributable. Dedup MUST attach a report to an incident;
  it MUST NOT delete or hide a signal.
- Chat, voice, phone, replay, and mock inputs MUST use the same bounded pipeline.

**Rationale**: Architectural boundaries make triage decisions inspectable,
testable, and safe under operational pressure.

### III. Escalation and Severity Are Safety Controls (NON-NEGOTIABLE)

- SEV1 and statutory-clock incidents MUST escalate; model output MUST NOT downgrade
  either condition.
- Life-safety, PII, safety/sentiment, explicit-human-request, and low-confidence
  triggers MUST route to an appropriate human queue.
- Changes that weaken, bypass, or deprioritize escalation MUST block release.
- Public communications MUST require human approval before publication.

**Rationale**: Escalation protects people, regulatory obligations, and operational
accountability; it is not a convenience feature.

### IV. Grounded Operational Output (NON-NEGOTIABLE)

- Classification MUST use typed structured output rather than free-text parsing.
- RouterExecutor severity/SLA outcomes MUST come from deterministic rules, not model
  inference.
- Sitreps and factual responses MUST cite source records. No citation, no claim.
- When guidance or evidence is unavailable, the system MUST state that limitation and
  escalate when needed.

**Rationale**: Fluent but unsupported incident information is a safety and trust
defect.

### V. Verifier-First Delivery (NON-NEGOTIABLE)

- New or changed behavior MUST have executable verification before or with its
  implementation; safety, routing, dedup, and PII controls MUST never be weakened to
  make a test pass.
- The mock pipeline MUST remain runnable without Azure credentials and exercise the
  same authority boundaries as live services.
- Changed backend behavior MUST run focused pytest coverage; changed frontend or
  companion-site behavior MUST typecheck and build.
- A feature is complete only when its spec, plan, tasks, tests, and directly related
  documentation agree with the delivered behavior.

**Rationale**: Incident systems need reproducible proof, not demonstration-only
confidence.

## Delivery and Documentation Constraints

- Domain language MUST follow `CONTEXT.md`: signal, incident, report, magnitude,
  queue, severity, SLA, sitrep, surge, and ClearBoard.
- Feature specs MUST define affected authority boundaries, escalation/PII behavior,
  mock-mode behavior, and measurable verification.
- Plans MUST identify the exact verification commands and any compatibility or
  migration impact.
- Tasks MUST name concrete files, preserve the bounded pipeline, and include
  validation work for every changed behavioral surface.
- The repository MUST NOT reintroduce retired support-domain features, branding,
  datasets, or terminology.

## Governance

This Constitution supersedes prior project guidance. Amendments require a documented
rationale, an impact review across active specifications and templates, and semantic
versioning:

- **MAJOR**: removes or fundamentally changes a principle or governed domain.
- **MINOR**: adds a principle or materially expands a requirement.
- **PATCH**: clarifies wording without changing an obligation.

Every implementation plan and pull request MUST record Constitution compliance.
Conflicts are resolved in this order: life safety and statutory escalation, privacy
and security, grounded operational truth, then user experience and delivery speed.

**Version**: 2.0.0 | **Ratified**: 2026-01-20 | **Last Amended**: 2026-09-20
