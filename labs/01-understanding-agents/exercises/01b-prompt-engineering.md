# Exercise 01b: Prompt Engineering for Agents

## Learning Objective

By the end of this exercise, you will be able to **write effective system prompts for the LLM-backed stages of All Clear** that produce consistent, accurate, and well-structured responses.

---

## Background: Prompt Structure

Effective prompts for AI agents typically consist of three key components:

### 1. System Message

The system message defines the agent's role, authority boundary, and core behavior.

```text
You are a [role] that [primary function].
Your authority is limited to [allowed actions].
```

### 2. Examples (Few-Shot Learning)

Examples demonstrate the expected input-output format.

```text
Signal: "Power line down across Main St, sparking near a school"
Classification: FIELD_HAZARD

Signal: "When will power be restored on Elm St?"
Classification: CUSTOMER_INQUIRY
```

### 3. Constraints

Constraints define boundaries, limitations, and specific requirements.

```text
Constraints:
- Classify only; never route or open incidents
- Never echo detected PII
- Always return structured JSON
```

---

## Exercise 1: QueryAgent - Signal Classification

**Scenario**: You need to write a system prompt for the All Clear QueryAgent that classifies one inbound signal into a typed `SignalClassification`.

### Requirements

The QueryAgent must:
- Classify signals into the All Clear `SignalCategory` taxonomy
- Return structured JSON matching `SignalClassification`
- Extract entities: `location`, `system`, `severity_indicators`, and `other`
- Flag PII without echoing the values back
- Handle ambiguous signals gracefully with lower confidence
- Never route, deduplicate, assign severity, open incidents, search knowledge, or generate a sitrep

### Your Task

Complete the system prompt below:

```text
You are the QueryAgent for All Clear, a cross-vertical incident-triage assistant.

Your task is to analyze one inbound signal and return a structured SignalClassification.
You classify ONLY.

Available SignalCategory values:
- INFRASTRUCTURE_OUTAGE: power/service outages, blackouts, transformers, substations, grid failures
- FIELD_HAZARD: downed lines, sparking wires, flooding, debris, blocked roads, trees down
- PUBLIC_SAFETY: life-safety threats such as fire, smoke, gas leak, explosion, collapse, injured, trapped
- CUSTOMER_INQUIRY: information or restoration-time questions such as "when will power be restored"
- SERVICE_REQUEST: routine non-urgent service requests
- COMPLIANCE_REPORT: NFIRS, NIBRS, recalls, breach notifications, statutory reporting windows
- STATUS_CHECK: follow-up on an existing incident such as AC-####
- HUMAN_REQUEST: explicit request for a human, representative, manager, or supervisor
- GENERAL_INQUIRY: greetings, thanks, off-topic, or unclear signals

[ADD YOUR EXAMPLES HERE]
[ADD YOUR CONSTRAINTS HERE]

Response format:
{
  "intent": "<specific intent such as report_field_hazard>",
  "intent_category": "<SignalCategory>",
  "target_queue": "field-operations | customer-comms | compliance-desk | engineering | escalations",
  "confidence": <0.0-1.0>,
  "entities": {"location": "<place or null>", "system": "<asset or null>", "severity_indicators": [], "other": []},
  "requires_escalation": <true|false>,
  "escalation_reason": "life_safety | statutory_clock | user_requested_human | policy_keyword_detected | pii_exposure | sentiment_safety | confidence_too_low | null",
  "pii_detected": <true|false>,
  "pii_types": [],
  "sentiment": "NEUTRAL | FRUSTRATED | URGENT | SATISFIED",
  "urgency_indicators": []
}
```

### Solution Template

<details>
<summary>Click to reveal a sample solution</summary>

```text
You are the QueryAgent for All Clear. You classify inbound operational signals from field crews, customers, sensors, and partner systems.

Your task is to analyze each signal and return a structured SignalClassification. You classify ONLY: never open incidents, attach reports, search knowledge, assign severity, decide SLA, or choose dedup outcome. The RouterExecutor makes the binding routing decision with zero LLM calls.

Examples:
Signal: "Power line down across Main St, sparking near a school."
Response: {"intent":"report_field_hazard","intent_category":"FIELD_HAZARD","target_queue":"field-operations","confidence":0.94,"entities":{"location":"Main St near a school","system":"power line","severity_indicators":["down","sparking"],"other":[]},"requires_escalation":false,"escalation_reason":null,"pii_detected":false,"pii_types":[],"sentiment":"URGENT","urgency_indicators":[]}

Signal: "Smell of gas near the community center."
Response: {"intent":"report_safety_threat","intent_category":"PUBLIC_SAFETY","target_queue":"field-operations","confidence":0.96,"entities":{"location":"community center","system":"gas","severity_indicators":["smell of gas"],"other":[]},"requires_escalation":true,"escalation_reason":"life_safety","pii_detected":false,"pii_types":[],"sentiment":"URGENT","urgency_indicators":[]}

Signal: "Need to file the NFIRS report for last night's fire."
Response: {"intent":"file_compliance_report","intent_category":"COMPLIANCE_REPORT","target_queue":"compliance-desk","confidence":0.93,"entities":{"location":null,"system":null,"severity_indicators":[],"other":["NFIRS"]},"requires_escalation":true,"escalation_reason":"statutory_clock","pii_detected":false,"pii_types":[],"sentiment":"NEUTRAL","urgency_indicators":[]}

Constraints:
- Always return valid JSON in the exact response format.
- If a signal could fit multiple categories, choose the most specific; life safety wins.
- Set confidence below 0.7 when classification is ambiguous.
- Flag PII by type but never echo PII values.
- Never route, deduplicate, open incidents, attach reports, search knowledge, or generate a sitrep.
```

</details>

---

## Exercise 2: RouterExecutor - No Prompt Required

**Scenario**: You need to explain why the middle stage does not need a system prompt.

### Requirements

The RouterExecutor must:
- Make **zero LLM calls**
- Deduplicate within the same `intent_category`
- Choose `ATTACH_TO_INCIDENT` at or above the 0.83 cosine threshold, otherwise `OPEN_INCIDENT`
- Map severity as `SEV1`-`SEV4` using deterministic rules
- Set SLA minutes from severity
- Apply escalation rules for SEV1, statutory clocks, PII exposure, safety sentiment, explicit human request, and low confidence
- Produce auditable `routing_rules_applied`

### Your Task

Write a short rule card, not a prompt:

```text
RouterExecutor rule card:
1. Dedup: compare signal embedding to open incidents in same intent_category.
2. Outcome: similarity >= 0.83 -> ATTACH_TO_INCIDENT; else OPEN_INCIDENT.
3. Severity: map severity_indicators to SEV1-SEV4 by fixed table.
4. SLA: SEV1=15 minutes, SEV2=60 minutes, SEV3=240 minutes, SEV4=next business day.
5. Escalation: always escalate SEV1 and statutory-clock incidents.
6. Audit: record every rule used in routing_rules_applied.
```

### Checkpoint

- [ ] You did **not** write a RouterExecutor prompt
- [ ] You can explain why deterministic routing is safer than model-based routing
- [ ] You can explain why severity is set by rules, never by model vibes

---

## Exercise 3: ActionAgent - Sitrep with Citations

**Scenario**: You need to write a system prompt for the ActionAgent. The ActionAgent has exactly three tools: `create_incident`, `search_knowledge`, and `generate_sitrep`.

### Requirements

The ActionAgent must:
- Trust the `RoutingDecision`; never re-decide severity, queue, SLA, dedup outcome, or escalation
- Use `create_incident` on the `OPEN_INCIDENT` path
- Use `search_knowledge` for incident runbooks/SOPs on the `OPEN_INCIDENT` path
- Use `generate_sitrep` to produce a citation-grounded situation report
- Skip knowledge search on the `ATTACH_TO_INCIDENT` path and acknowledge the report
- Include citations for every factual claim in the sitrep or response

### Your Task

Write a complete system prompt for the ActionAgent:

```text
[YOUR SYSTEM PROMPT HERE]

Available tools:
- create_incident
- search_knowledge
- generate_sitrep

[YOUR EXAMPLES HERE]
[YOUR CONSTRAINTS HERE]

Citation format: cite source records using the provided Citation objects.
```

### Solution Template

<details>
<summary>Click to reveal a sample solution</summary>

```text
You are the ActionAgent for All Clear. You execute the already-decided RoutingDecision through exactly three tools: create_incident, search_knowledge, and generate_sitrep.

Your role is to:
1. Trust the RoutingDecision exactly as provided.
2. On OPEN_INCIDENT, call create_incident with the target queue, severity, SLA, and classification context.
3. Search incident runbooks/SOPs with search_knowledge after the incident is created.
4. Generate a citation-grounded sitrep with generate_sitrep.
5. On ATTACH_TO_INCIDENT, do not search knowledge; acknowledge that the signal was attached as a report and include the incident id if provided.

Examples:
RoutingDecision: OPEN_INCIDENT, queue=field-operations, severity=SEV1, signal="Smell of gas near the community center"
Action: create_incident, search_knowledge for gas leak response SOP, generate_sitrep with citations, then respond with the incident id and escalation status.

RoutingDecision: ATTACH_TO_INCIDENT, matched_incident_id=AC-0042, magnitude=38, signal="Power still out on Elm St"
Action: skip knowledge search and acknowledge that the report was added to AC-0042.

Constraints:
- Never change severity, queue, SLA, escalation, or dedup outcome.
- Never suppress or weaken escalation.
- Use only the three available tools.
- Every factual claim in a sitrep must cite a source record.
- Never echo PII from the signal.
- If a tool fails, return a safe fallback that preserves the RoutingDecision and requests human review.
```

</details>

---

## Exercise 4: Voice System Prompt (Extension)

Voice interactions use the **same three-stage pipeline** but need modality-specific constraints because spoken responses must be:
- **Concise** (2-3 sentences max)
- **Phonetically clear** (spell out incident IDs character-by-character: "A-C dash zero zero four two")
- **PII-safe** (never echo back SSN, phone numbers, DOB, or other sensitive personal data)

### Your Task

Write a voice-specific response prompt for the ActionAgent that trusts the same QueryAgent -> RouterExecutor -> ActionAgent pipeline, keeps spoken responses short, spells `AC-####` IDs clearly, filters PII, and handles the "I didn't catch that" case without guessing.

---

## Best Practices

### 1. Be Specific

**Instead of:**
```text
You are a helpful assistant.
```

**Write:**
```text
You are the QueryAgent for All Clear. You classify one inbound signal into SignalClassification and cannot route, open incidents, attach reports, search knowledge, or generate a sitrep.
```

### 2. Use Examples

```text
Example input: "Water main break flooding the 200 block"
Example output: {"intent_category":"FIELD_HAZARD","target_queue":"field-operations"}
```

### 3. Set Clear Boundaries

```text
Constraints:
- QueryAgent classifies only
- RouterExecutor needs no prompt and makes zero LLM calls
- ActionAgent must not re-decide severity or suppress escalation
- Never echo detected PII
```

### 4. Define Output Format

Specify the exact structure you expect, preferably the `SignalClassification` schema.

### 5. Handle Edge Cases

If the signal is unclear, set low confidence, use `GENERAL_INQUIRY` when no category is supported, and do not invent location, system, or severity indicators.

---

## Common Mistakes to Avoid

1. **Vague Instructions**: say exactly which stage you are prompting and what it may do.
2. **Missing Examples**: include downed lines, gas smell, restoration-time questions, NFIRS reports, and `AC-####` status checks.
3. **Contradicting Bounded Authority**: never ask QueryAgent to open an incident or ActionAgent to re-decide severity.
4. **Assuming Context**: RouterExecutor performs dedup; the model should not guess duplicates from memory.
5. **Overly Complex Prompts**: move deterministic rules into code and keep prompts focused.

---

## Testing Prompts with GitHub Copilot

Create a test file to document prompt behavior:

```python
SYSTEM_PROMPT = """Your QueryAgent system prompt here..."""
TEST_CASES = [
    {"input": "Smell of gas near the community center", "expected_category": "PUBLIC_SAFETY"},
    {"input": "Hello", "expected_category": "GENERAL_INQUIRY"},
]
```

Use Copilot to generate additional test cases for outage surge, product recall, and low-confidence signals.

---

## Checkpoint

Before moving on, verify you can:

- [ ] Explain the three components of an effective prompt
- [ ] Write a QueryAgent prompt with role definition, examples, constraints, and structured output
- [ ] Explain why RouterExecutor needs no prompt
- [ ] Write an ActionAgent prompt that uses exactly three tools
- [ ] Define clear output formats using JSON schemas
- [ ] Identify and fix common prompt engineering mistakes
- [ ] Test prompts iteratively using Copilot
- [ ] (Extension) Voice response prompt written with modality-specific constraints

---

## Next Steps

Continue to [Exercise 01c: Agent Orchestration](./01c-agent-orchestration.md) to learn how to coordinate the bounded-authority pipeline.
