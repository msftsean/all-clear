# Feature Name: Statutory-Clock Escalation Detector

## Description

This feature adds a deterministic detector that identifies All Clear signals referencing statutory clocks, life safety, or policy-sensitive conditions and routes them to a human queue. The objective is to prevent unsafe automation decisions by forcing SEV1 when a legal breach-notification deadline, recall reporting deadline, life-safety threat, or total outage is referenced. The feature includes reason codes, confidence metadata, and an auditable decision record so operators can review why escalation happened.

## User Stories

1. As a reporter, I want my signal about a downed power line or gas leak escalated immediately so the incident receives SEV1 handling and a 15-minute SLA.
2. As an All Clear operator, I want escalation reasons attached to each incident so I can understand context before responding.
3. As a compliance reviewer, I want statutory-clock escalations logged so we can demonstrate governance and accountability.
4. As a system administrator, I want stable deterministic escalation behavior so routing quality does not vary across model outputs.

## Functional Requirements

1. The system shall detect statutory-clock terms such as breach notification, recall reporting, legal deadline, and regulatory notice.
2. The system shall detect life-safety and total-outage indicators such as downed power line, gas leak, transformer fire, and outage surge.
3. The system shall return structured output with `escalate`, `severity`, `target_queue`, and `reasons` fields.
4. The system shall preserve original signal text in the escalation payload for human reviewers while preventing PII echo in responses.
5. The system shall include a confidence score and rule hits in the decision metadata.
6. The system shall support configurable term lists without code changes.
7. The system shall provide a fallback decision when confidence is low and ambiguity remains.

## Non-Functional Requirements

- Detection latency should remain under 500 ms in mock mode.
- Output schema must remain compatible with existing orchestration steps.
- Logs must avoid storing secrets and should include trace IDs.
- RouterExecutor behavior must be deterministic and require zero LLM calls.

## Success Criteria

- At least 95 percent of known statutory-clock and life-safety examples are escalated in validation tests.
- No statutory-clock example is silently handled as a standard knowledge reply.
- Validation notes clearly map each requirement to generated implementation behavior.
- Team can demonstrate one end-to-end escalation flow during review.
