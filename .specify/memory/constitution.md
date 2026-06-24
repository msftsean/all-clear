<!--
SYNC IMPACT REPORT
==================
Version change: 1.2.0 → 1.3.0
Bump rationale: MINOR — replaced stale legacy domain framing
  with All Clear incident-triage principles from CONTEXT.md and shared/constitution.md.
Modified principles:
  - I. Bounded Agent Authority → All Clear QueryAgent / RouterExecutor / ActionAgent authority boundaries
  - II. Escalation Is a Safety Control → SEV1/statutory/PII/sentiment escalation framing
  - III. Data Discipline → CJIS-mindset PII and audit handling
  - IV. Truth Over Fluency → citation-grounded sitreps and typed structured output
  - V. Test-First Development → verifier-first, mock-mode parity, zero-LLM router tests
  - VI/VII → accessibility and graceful degradation reframed for incident triage
Added sections:
  - None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ Compatible
  - .specify/templates/spec-template.md: ✅ Compatible
  - .specify/templates/tasks-template.md: ✅ Compatible
Follow-up TODOs: None
-->

# All Clear Constitution

## Core Principles

### I. Bounded Agent Authority (NON-NEGOTIABLE)

Each agent component MUST have explicitly defined boundaries enforced architecturally:

- QueryAgent classifies one inbound signal into structured `SignalClassification` data ONLY — no routing decisions, no incident creation, no search, and no record mutation.
- RouterExecutor decides dedup, severity, SLA, and escalation deterministically. It MUST make zero LLM calls, hold no tools, and keep rules configuration-driven and testable.
- ActionAgent acts only through its approved tools: `create_incident`, `search_knowledge`, and `generate_sitrep`. It MUST NOT approve waivers, modify records outside those tools, suppress escalation, or bypass RouterExecutor decisions.
- Dedup attaches signals to incidents as reports; it MUST preserve every signal and MUST NOT delete or hide inbound records.
- Voice, chat, replay, and scenario inputs MUST route through the same bounded pipeline; no modality may create a parallel authority path.
- The absence of unauthorized capabilities MUST be enforced at the code level: methods and tools outside a component's authority simply do not exist.

**Rationale**: Bounded authority keeps the Microsoft Agent Framework pipeline inspectable and safe. All Clear handles incident triage, so model output may classify and summarize, but deterministic code owns routing, escalation, and SLA control.

### II. Escalation Is a Safety Control (NON-NEGOTIABLE)

The system MUST escalate whenever human review is required for safety, legal, operational, or ambiguity reasons:

- SEV1 and statutory-clock incidents always escalate. No model output can downgrade them.
- PII exposure, safety/sentiment triggers, explicit human-contact requests, and low-confidence classifications MUST route to the appropriate human queue.
- Escalation weakening is a release blocker. Code that bypasses, suppresses, or deprioritizes escalation MUST be rejected at review.
- Escalation context MUST be PII-filtered and must include enough cited source records for a human to act.

**Rationale**: Escalation is not a convenience feature; it is a control surface for life safety, regulatory deadlines, and operational accountability.

### III. Data Discipline (CJIS Mindset, Everywhere) (NON-NEGOTIABLE)

All Clear MUST handle incident and reporter data with least privilege and full auditability:

- PII detected in a signal is flagged and never echoed back in responses, logs, synthesized speech, or sitreps.
- Every action that creates or mutates an incident/report record is audit-logged with actor, timestamp, and cause.
- Signal text sent to embeddings is a reviewed data flow: what is vectorized, where vectors live, and retention are documented.
- Agents and services hold only the access their bounded authority requires.
- Raw audio MUST NOT be stored; only PII-filtered transcripts may be persisted when voice is enabled.
- Ephemeral realtime/session tokens MUST expire quickly and MUST NOT be reusable.

**Rationale**: All Clear is CAD-adjacent triage, not a replacement for systems of record. The codebase adopts a CJIS-style discipline: least privilege, no PII echo, and auditable decisions.

### IV. Truth Over Fluency (NON-NEGOTIABLE)

The system MUST prefer grounded, structured, and honest outputs over fluent invention:

- Sitreps and responses cite source records for every factual claim. No citation, no claim.
- Classification uses typed schemas and structured output, never free-text parsing.
- RouterExecutor severity/SLA decisions come from deterministic rules, not model vibes.
- When the system does not know, it says so and escalates instead of inventing.
- `generate_sitrep` MUST produce citation-grounded situation reports suitable for operational review.

**Rationale**: Incident triage requires accountable facts. A polished but unsupported summary is a defect, especially when it could affect public safety, compliance, or customer communications.

### V. Test-First Development

All agent behaviors MUST be validated through verifiers written before implementation:

- Acceptance scenarios from specs MUST become executable tests, evals, fixtures, or checkpoint scripts.
- Boundary violations MUST be tested: QueryAgent cannot route, RouterExecutor makes zero LLM/network calls, and ActionAgent cannot act outside its tools.
- Dedup, severity/SLA mapping, escalation triggers, and citation-grounded sitreps MUST have deterministic tests.
- Mock twins MUST exist for every live service and stay in lockstep; the full pipeline must run offline.
- Existing mock-mode pytest suites, scenario replays, and `smoke-test.yml` MUST remain green. New features add tests rather than deleting or weakening safety assertions.

**Rationale**: Agent systems fail in subtle ways. Verifier-first work protects All Clear's bounded authority, escalation controls, and demo reliability.

### VI. Accessibility as Requirement

The user interface MUST meet accessibility standards as functional requirements, not afterthoughts:

- WCAG AA compliance MUST be achieved; high-contrast views should target stronger contrast where practical.
- All interactive elements MUST be keyboard navigable and screen-reader compatible.
- ClearBoard incident pins, magnitude indicators, SLA breach states, and all-clear states MUST have non-color-only affordances.
- Voice controls, when enabled, MUST be keyboard accessible and accompanied by visible state and text fallback.
- Text input MUST remain available for every function; voice must never be the only path.

**Rationale**: Incident triage tools must remain usable under stress, across devices, and by participants with different access needs.

### VII. Graceful Degradation

The system MUST continue providing useful, honest behavior when dependencies fail:

- If Azure OpenAI is unavailable, the system MUST fall back to deterministic/mock behavior where available or escalate with a clear message.
- If Azure AI Search is unavailable, incident creation and escalation MUST continue; responses must not fabricate missing knowledge.
- If incident storage is unavailable, the system MUST log for retry where safe, inform the user, and avoid claiming an incident was created.
- If voice/realtime transport fails, the text path MUST remain available and preserve PII-filtered context.
- Degradation states MUST be logged for operational visibility.

**Rationale**: All Clear's promise is resilient triage, not perfect dependency uptime. Partial, honest functionality is better than silent failure or invented certainty.

## Security & Compliance Constraints

### Data Access Boundaries

- System MUST NOT access systems of record beyond the minimum incident-triage context required by bounded tools.
- System MUST NOT store financial account data, secrets, credentials, or unnecessary personal data.
- System MUST retain signals, reports, incidents, vectors, and logs according to documented retention policy.

### Integration Security

- All external API calls MUST use authenticated, encrypted connections.
- API credentials MUST NOT be stored in code or logs.
- Rate limiting MUST be implemented on public endpoints.
- Azure service mocks MUST not require live credentials.

### Voice Channel Security

- Ephemeral tokens for realtime sessions MUST have short TTL and MUST NOT be reusable.
- Tool-call relays MUST validate session ownership before executing ActionAgent tools.
- Audio data MUST NOT transit through the backend when direct browser-to-Azure transport is configured.
- Tool-call results relayed to clients MUST be PII-filtered.
- Voice audit entries MUST include `input_modality="voice"` and degradation events.
- The system MUST NOT expose Azure OpenAI API keys to the frontend.

### Audit Requirements

- All routing decisions MUST be logged with timestamp, signal/report identifiers, incident identifier when present, queue, severity, SLA, and escalation status.
- Audit logs MUST be append-only.
- Sitreps MUST retain citations to source records used for each factual claim.

## Development Workflow

### Code Review Requirements

- All changes MUST be reviewed before merge.
- Reviewer MUST verify Constitution compliance for boundary enforcement, escalation triggers, data discipline, and citation grounding.
- Security-sensitive changes MUST receive security-focused review.
- Voice or realtime changes MUST include PII, degradation, and tool-boundary review.

### Quality Gates

- All relevant tests MUST pass before merge.
- Code coverage and safety/eval coverage MUST not decrease for changed behavior.
- Accessibility tests/checks MUST pass for UI changes.
- Performance-sensitive paths, especially dedup surge handling, MUST meet documented thresholds.
- RouterExecutor MUST remain deterministic and zero-LLM by test.

### Documentation Standards

- API contracts MUST be documented in OpenAPI format where applicable.
- Agent boundaries and escalation rules MUST be documented and version-controlled.
- Material architecture decisions MUST be logged in `.squad/decisions.md` or the squad decision inbox before promotion.
- Domain terminology MUST follow `CONTEXT.md`; if code/docs and `CONTEXT.md` disagree, update the stale artifact.

## Governance

This Constitution establishes non-negotiable principles for All Clear. All development decisions MUST comply with these principles.

### Amendment Process

1. Propose amendment with rationale and impact analysis.
2. Review against existing principles for conflicts.
3. Update version number per semantic versioning:
   - MAJOR: Principle removal or fundamental redefinition.
   - MINOR: New principle or material expansion of existing guidance.
   - PATCH: Clarifications, wording improvements, non-semantic changes.
4. Update dependent templates if affected.
5. Document migration plan for existing code if breaking change.

### Compliance Verification

- All pull requests MUST include Constitution compliance notes/checklist.
- Regular reviews of system behavior MUST assess boundary, escalation, data, and citation adherence.
- Incident post-mortems MUST assess Constitution adherence.

### Conflict Resolution

- Constitution principles take precedence over convenience or speed.
- When principles conflict, prioritize: life safety and statutory escalation > data discipline/security > truth/citations > user experience.
- Document conflicts and resolutions in the decision log.

**Version**: 1.3.0 | **Ratified**: 2026-01-20 | **Last Amended**: 2026-06-24
