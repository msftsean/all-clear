# Feature Specification: All Clear Consolidation

**Feature Branch**: `main`
**Created**: 2026-09-20
**Status**: Complete
**Input**: Consolidate the repository on the All Clear incident-triage product and
remove retired support-domain behavior and materials.

## User Scenarios & Testing

### User Story 1 - Operate one incident-triage product (Priority: P1)

A responder submits a signal through text, voice, or phone and receives the same
All Clear incident-triage behavior regardless of channel.

**Why this priority**: The bounded incident pipeline is the product; legacy
support-domain behavior cannot coexist with it.

**Independent Test**: Run the mock pipeline with a field hazard and verify it opens
an `AC-####` incident with an All Clear queue and severity.

**Acceptance Scenarios**:

1. **Given** a field-hazard signal, **When** it reaches the pipeline, **Then** the
   system classifies, routes, and opens or attaches an incident without a
   retired support-domain API.
2. **Given** a crisis signal through text or voice, **When** it is processed,
   **Then** the system returns the deterministic safety escalation without
   self-service knowledge content.

### User Story 2 - Learn and demonstrate All Clear consistently (Priority: P2)

A participant, coach, or stakeholder uses any companion site and receives the
same All Clear explanation of signals, incidents, surge deduplication, severity,
SLA, safety, voice/phone intake, and ClearBoard.

**Why this priority**: The public educational surfaces must not teach a retired
product model.

**Independent Test**: Build each companion site and scan tracked content for retired
branding and support-domain terminology.

**Acceptance Scenarios**:

1. **Given** a visitor opens the workshop, coach, hackathon, or operations site,
   **When** they follow its main flow, **Then** it presents only All Clear
   incident-triage concepts and does not expose retired-domain language.
2. **Given** a contributor searches tracked content, **When** they scan for
   retired product identifiers, **Then** no active reference remains.

### User Story 3 - Plan future work against current governance (Priority: P3)

A contributor starts a new feature with Spec Kit and receives templates and
governance that reflect the current system instead of deleted workflows.

**Why this priority**: Stale planning artifacts create future regressions.

**Independent Test**: Review the Constitution and templates for current domain
language, required safety gates, and active verification expectations.

**Acceptance Scenarios**:

1. **Given** a new feature plan, **When** its Constitution Check is completed,
   **Then** it covers bounded authority, escalation, PII, mock mode, and verifiers.
2. **Given** a generated task list, **When** behavior changes, **Then** it includes
   focused validation and direct documentation updates.

## Requirements

### Functional Requirements

- **FR-001**: The runtime MUST use the signal-to-incident pipeline and MUST NOT expose
  retired support-domain or mutable-branding APIs.
- **FR-002**: Voice and phone tool definitions MUST use incident terminology and the
  same safety override as text intake.
- **FR-003**: Companion sites and seed knowledge MUST use All Clear domain language.
- **FR-004**: Retired support-domain classifiers, data, scenarios, assets,
  runbooks, and planning records MUST be removed.
- **FR-005**: The Spec Kit Constitution, active spec, plan, tasks, and templates MUST
  define the current All Clear architecture and validation gates.
- **FR-006**: Conversation history MUST fail closed until the backend can bind
  records to a verified server-side owner; caller-supplied session IDs and hashes
  MUST NOT authorize retrieval.
- **FR-007**: Phone transcript delivery MUST be call-scoped and PII-redacted before
  publication or logging, and MUST fail closed until call ownership and ACS ingress
  are verifiable.
- **FR-008**: Realtime sessions MUST use server-generated session IDs and the
  server-owned safety prompt; the Lab 07 offline verifier MUST fail on tool errors.
- **FR-009**: Both Lab 07 MCP variants MUST detect PII from original input at
  the boundary, send only redacted text to models, logs, and storage, and pass the
  trusted PII flag separately into Lab 05 deterministic routing. QueryAgent
  output MUST NOT clear that flag; PII alone MUST trigger escalation for otherwise
  benign requests without changing severity/SLA.

### Restricted participant deployment (2026-11-18)

- Live chat and embedding dedup MUST be deployable to an existing participant
  resource group without creating role assignments, changing subscription
  configuration, or registering an application.
- Managed identity remains the default. Explicit key authentication MUST keep
  model credentials in Azure Container Apps secrets, never deployment outputs,
  local environment files, telemetry, or documentation.
- Application Insights export is opt-in through its connection-string environment
  variable, with local offline export storage disabled. Mock mode remains offline.
- The prescribed downed/sparking power-line acceptance signal MUST open a SEV1
  incident with mandatory escalation; its exact duplicate MUST attach to that
  incident without suppressing severity or escalation. A successful deployment
  and working dedup do not satisfy readiness if this safety gate fails.
- Deterministic life-safety matching MUST recognize `sparking` and explicit
  `electrical arcing` severity indicators case-insensitively. Generic `downed`,
  fallen-tree or empty indicators MUST NOT elevate every field hazard to SEV1.
  A locally tested source correction MUST NOT be described as deployed or as
  retroactively correcting an existing incident.

### Key Entities

- **Signal**: An attributable inbound report received from any supported channel.
- **Incident**: The operational event represented by one or more signals.
- **Report**: The association created when a signal attaches to an incident.
- **Queue**: An All Clear destination work stream.
- **Sitrep**: A citation-grounded operational summary.

## Success Criteria

- **SC-001**: The mock pipeline opens an `AC-####` incident for a representative
  field-hazard signal.
- **SC-002**: Focused schema, safety, and voice endpoint tests pass.
- **SC-003**: The primary frontend and all companion sites typecheck and build.
- **SC-004**: A tracked-content scan returns zero retired-brand matches.
- **SC-005**: Focused privacy/realtime tests and both offline Lab 07 MCP probe
  variants pass; unauthenticated history, transcript, and ACS-ingress access is
  rejected without contacting live services.
- **SC-006**: Offline Lab 07 regression tests prove PII-triggered escalation
  despite model `pii_detected=false`, redaction across model/log/storage/output
  surfaces, and no PII false-positive from a literal redaction marker.
