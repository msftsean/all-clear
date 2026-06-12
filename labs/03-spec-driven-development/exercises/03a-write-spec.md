# Exercise 03a: Write a Spec for an All Clear Escalation Capability

**Duration:** 25 minutes

## Overview

In this exercise, you will write a complete specification for an **All Clear escalation capability**. This capability monitors inbound signals to identify situations that require mandatory human handoff, such as statutory clocks, life safety, total outages, PII exposure, or explicit requests for a human.

## Learning Objectives

- Practice writing clear, implementable specifications
- Define user stories from multiple stakeholder perspectives
- Create measurable success criteria
- Document constraints and boundaries

## Background: The Escalation Capability

All Clear receives high-volume signals during incidents and surges. Some signals require immediate human attention regardless of model output:

- A downed power line, gas leak, or transformer fire
- A statutory clock such as breach notification or recall reporting
- A total outage or spreading public-facing impairment
- PII exposure that must not be echoed back
- An explicit request for human handoff

The escalation capability will analyze incoming signals, identify mandatory escalation triggers, assign reason codes, force SEV1 where required, and route the incident to the appropriate human queue.

## Instructions

### Part 1: Create Your Specification (15 minutes)

1. Create a new file called `your-spec.md` in the lab directory
2. Use the template from `templates/spec-template.md` as your starting point
3. Complete each section for an All Clear capability such as a statutory-clock detector or escalation-reason classifier

#### Required Sections

**Feature Name:**
Name your feature clearly (e.g., "Statutory-Clock Escalation Detector" or similar)

**User Stories (minimum 3):**

Write user stories from these perspectives:

1. **Reporter Perspective:** A person whose urgent signal must receive immediate triage
2. **Operator Perspective:** A human queue member who needs clear escalation context
3. **System/Admin Perspective:** An administrator who needs auditability and stable routing behavior

**Functional Requirements (minimum 5):**

Consider these categories:
- Input processing (what signal data does the capability receive?)
- Detection logic (how does it identify escalation signals?)
- Classification (which `EscalationReason` values are emitted?)
- Routing (which queue receives the incident?)
- Notification (how are humans alerted?)

**Success Criteria:**

Define measurable criteria such as:
- Detection accuracy (precision/recall targets)
- Response time requirements
- False positive/negative thresholds
- Coverage requirements

**Constraints:**

Address these constraint categories:
- Technical (language, framework, dependencies)
- Compliance (PII handling, audit records, accessibility)
- Operational (what the capability cannot do)

### Part 2: Create Your Constitution (10 minutes)

1. Create a new file called `your-constitution.md` in the lab directory
2. Use the template from `templates/constitution-template.md` as your starting point
3. Complete the following sections for the All Clear incident-triage context

#### Required Sections

**Core Principles (minimum 3):**

Use principles from the All Clear constitution:
- Data discipline with a CJIS mindset
- Bounded authority
- Escalation is a safety control
- Truth over fluency

**Agent Boundaries:**

Define what the agent:
- IS authorized to do
- Is NOT authorized to do
- Must escalate to humans

**Prohibited Actions:**

List actions the agent must NEVER perform:
- Related to PII or signal preservation
- Related to unauthorized incident mutation
- Related to suppressing escalation or fabricating citations

**Compliance Requirements:**

Address:
- CJIS-mindset data discipline
- Audit logging and traceability
- Accessibility and clear communication

## Example Content

Here's an example user story to guide your writing:

> **Story: Statutory Clock Referenced**
>
> As a **compliance operator**,
> I want **signals that mention breach-notification deadlines to force SEV1 and escalate**
> So that **a legally mandated clock is never delayed by automation**
>
> **Acceptance Criteria:**
> - [ ] Signals containing statutory-clock terms are flagged within 30 seconds
> - [ ] Flagged signals produce `EscalationReason.STATUTORY_CLOCK`
> - [ ] RouterExecutor assigns SEV1 with a 15-minute SLA
> - [ ] The incident is routed to `compliance-desk` and escalated to humans

Here's an example prohibited action:

| Prohibited Action | Severity | Rationale |
|-------------------|----------|-----------|
| Downgrading a statutory-clock signal below SEV1 | Critical | Statutory clocks always escalate; model output cannot downgrade them |
| Echoing PII from a signal into a response | Critical | All Clear uses CJIS-mindset data discipline and must not expose sensitive data |

## Validation Checklist

Before moving to Exercise 03b, verify your spec:

- [ ] Feature name is clear and descriptive
- [ ] At least 3 user stories with acceptance criteria
- [ ] At least 5 functional requirements with severity/queue terminology
- [ ] Success criteria are measurable (include numbers/percentages)
- [ ] Constraints address privacy, audit, and accessibility
- [ ] At least 2 concrete examples with inputs/outputs

Verify your constitution:

- [ ] At least 3 core principles in precedence order
- [ ] Agent boundaries clearly define permitted vs. prohibited actions
- [ ] Prohibited actions include rationale
- [ ] Escalation protocol is defined
- [ ] Data discipline and audit requirements are addressed

## Tips for Writing Effective Specs

1. **Be Specific:** Instead of "fast response time," write "response time < 500ms for 95th percentile"

2. **Include Edge Cases:** What happens when:
   - A signal contains multiple escalation reasons?
   - The confidence score is borderline?
   - The target queue is unavailable?

3. **Define "Not" as much as "Is":** Explicitly state what the feature will NOT do

4. **Use Consistent Terminology:** Define terms like "signal," "incident," "severity," "queue," and "escalation" and use them consistently

5. **Consider Failure Modes:** What happens when detection fails? What's the fallback?

### Extension: Voice-Aware Specification

When writing specs for agents that may be accessed via voice, consider adding these constraints:
- **Response length** — spoken responses should be 2–3 sentences max
- **Phonetic clarity** — IDs and codes should be spelled out ("A-C dash 0-0-4-2")
- **PII handling** — never echo back sensitive data the caller provides
- **Silence handling** — what happens when the caller stops talking? (VAD timeout)

Try adding a "Voice Modality" section to your escalation capability spec that addresses these constraints.

## Deliverables

When complete, you should have:

1. `your-spec.md` - Complete feature specification
2. `your-constitution.md` - Complete agent constitution

## Next Steps

Once your spec and constitution are complete, proceed to [Exercise 03b: Generate from Spec](03b-generate-from-spec.md) to use Copilot to generate code from your specifications.
