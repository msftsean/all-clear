# Exercise 03b: Generate Implementation Guidance from Your Spec

**Duration:** 20 minutes

## Overview

In this exercise, you will use GitHub Copilot to turn the specification from
Exercise 03a into implementation guidance. You will practice providing precise
context, checking proposed code against the specification, and recording gaps.
This exercise does not promise production-ready generated code.

## Learning Objectives

- Use specifications as context for AI-assisted implementation
- Apply strategic prompting techniques with Copilot
- Validate a proposed implementation against specification criteria
- Iterate on the proposal to improve spec compliance

## Prerequisites

- Completed Exercise 03a (`your-spec.md` exists; use `your-constitution.md` only if created)
- GitHub Copilot extension active in VS Code
- Copilot Chat panel accessible (Ctrl+Alt+I (Windows/Linux) or Cmd+Shift+I (macOS), or click the Copilot Chat icon in the sidebar)

## Instructions

### Part 1: Prepare Your Context (5 minutes)

Before generating code, set up your workspace to maximize Copilot's understanding of your requirements.

#### Step 1: Open Your Specification Files

Open these files in VS Code tabs:
1. `your-spec.md` - Your feature specification
2. `your-constitution.md` - Your feature guardrails, if created

**Why?** Copilot uses open files as context. Having your specs visible helps Copilot generate aligned code.

#### Step 2: Create a Target File

Create a new file for the implementation slice you will review:

```
generated/escalation_detector.py
```

Add a header comment referencing your spec:

```python
"""
All Clear Escalation Detector

Implementation based on:
- Specification: your-spec.md
- Constitution: `.specify/memory/constitution.md` (and `your-constitution.md`, if created)

This module implements deterministic escalation detection
as defined in the feature specification.
"""
```

### Part 2: Generate Initial Code (7 minutes)

Use Copilot Chat to propose a small implementation slice from your specification.

#### Step 1: Open Copilot Chat

Open the Copilot Chat panel (Ctrl+Alt+I (Windows/Linux) or Cmd+Shift+I (macOS), or click the Copilot Chat icon in the sidebar)

#### Step 2: Reference Your Spec

Use the `Agent Mode` command to reference your specification:

```
Agent Mode Based on the specification in your-spec.md, propose a Python class
for the All Clear statutory-clock escalation detector. Include:
1. The core detection method that analyzes signal text for escalation triggers
2. Classification into the EscalationReason values defined in my spec
3. Severity, target queue, and confidence scoring for detections
Follow the constraints in `.specify/memory/constitution.md` and any
`your-constitution.md` for what the agent must NOT do.
```

#### Step 3: Review the Generated Code

Copilot will propose an initial implementation. Before accepting or adapting it,
review:

- [ ] Does it address the core functional requirements?
- [ ] Does it include the escalation reasons from your spec?
- [ ] Does it return the output format you specified?
- [ ] Does it respect the constraints from your constitution?

#### Step 4: Insert and Annotate

Insert or adapt the proposed code in your file. Add comments noting which spec
requirements are addressed:

```python
def detect_escalation(self, signal_text: str) -> EscalationResult:
    """
    Analyze signal text for escalation triggers.

    Implements:
    - FR-001: Process incoming All Clear signals
    - FR-002: Detect statutory-clock and life-safety patterns
    - SC-001: Return result within 500ms (target)
    """
    # Generated code here...
```

### Part 3: Iterate and Refine (5 minutes)

Proposed code rarely matches specifications perfectly on the first try. Use
iterative refinement to improve compliance.

#### Iteration 1: Add Missing Requirements

Review your spec's functional requirements. For any missing ones, prompt Copilot:

```
Agent Mode The current escalation_detector.py is missing FR-003 from my spec
(return structured output with escalate, severity, target_queue, and reasons).
Add a dataclass or Pydantic model that returns those fields using the All Clear
severity values SEV1-SEV4 and queue values from my specification.
```

#### Iteration 2: Enforce Constitution Constraints

Check if the proposed code respects the canonical constitution's prohibited actions:

```
Agent Mode Review escalation_detector.py against the prohibited actions in
.specify/memory/constitution.md. Add safeguards to ensure the detector cannot:
1. Downgrade a statutory-clock or SEV1 signal
2. Echo PII into user-facing responses
Add validation or guards to prevent these actions.
```

#### Iteration 3: Add Error Handling

Ensure the code handles the error conditions from your spec:

```
Agent Mode Add error handling to escalation_detector.py for the error
conditions defined in my specification. Each error should return the
user-facing message I specified and escalate when the system does not know.
```

### Part 4: Validate Against Success Criteria (3 minutes)

Create a validation document to track spec compliance and unresolved gaps.

#### Step 1: Create Validation Notes

Create a file `generated/validation_notes.md`:

```markdown
# Spec Validation Notes

## Success Criteria Compliance

| Criterion | Status | Notes |
|-----------|--------|-------|
| SC-001: [Your criterion] | Pass/Fail/Partial | [Explanation] |
| SC-002: [Your criterion] | Pass/Fail/Partial | [Explanation] |
| SC-003: [Your criterion] | Pass/Fail/Partial | [Explanation] |

## Functional Requirements Coverage

| Requirement | Implemented | Method/Location |
|-------------|-------------|-----------------|
| FR-001 | Yes/No/Partial | [Where in code] |
| FR-002 | Yes/No/Partial | [Where in code] |

## Constitution Compliance

| Prohibited Action | Safeguard Implemented | How |
|-------------------|----------------------|-----|
| [Action] | Yes/No | [Explanation] |

## Gaps Identified

1. [Gap between spec and implementation]
2. [Gap between spec and implementation]

## Improvement Plan

1. [What needs to be fixed/added]
2. [What needs to be fixed/added]
```

#### Step 2: Calculate Compliance Rate

Count your criteria compliance:
- Total success criteria: ___
- Criteria met: ___
- Compliance rate: ___% (report the result; do not treat it as a release gate)

### Part 5: Final Refinement (Optional)

If important requirements remain partial, perform additional iterations:

```
Agent Mode I need to improve spec compliance for escalation_detector.py.
The following requirements are not yet met:
1. [Unmet requirement]
2. [Unmet requirement]
Generate the additional code needed to meet these requirements.
```

## Prompting Tips

### Effective Prompts

**Good:** "Based on FR-002 in my spec, implement detection for the specific All Clear trigger categories I defined: statutory clock, life safety, total outage, PII exposure, and explicit human request"

**Less Effective:** "Add keyword detection"

### Referencing Specific Sections

Use precise references:
- "According to the Success Criteria section of your-spec.md..."
- "The prohibited actions in your-constitution.md state that..."
- "User Story 2's acceptance criteria require..."

### Handling Large Specifications

If your spec is extensive:
1. Generate code for one functional requirement at a time
2. Reference specific sections rather than the whole document
3. Build incrementally, validating each piece

## Common Issues

### Copilot Ignores My Spec

- Ensure spec file is open in an editor tab
- Use `Agent Mode` to explicitly reference files
- Quote specific sections from your spec in the prompt

### Generated Code Doesn't Match My Output Format

- Provide an explicit example in your prompt:
  ```
  Return results in this format:
  {
    "escalate": true,
    "severity": "SEV1",
    "target_queue": "compliance-desk",
    "escalation_reason": "statutory_clock",
    "confidence": 0.95
  }
  ```

### Code Violates Constitution

- Add explicit guards in follow-up prompts
- Request that Copilot add validation checks
- Review the proposed implementation before accepting or adapting it

## Deliverables

By the end of this exercise, you should have:

```
generated/
  |-- escalation_detector.py    # Your reviewed implementation slice
  |-- validation_notes.md       # Documentation of spec compliance
```

## Reflection Questions

After completing this exercise, consider:

1. What percentage of your spec was accurately captured in the first generation?
2. Which types of requirements were easiest/hardest for Copilot to implement?
3. How did having a constitution affect the proposed implementation?
4. What would you do differently in your spec to improve generation quality?

## Completion Criteria

You have successfully completed this exercise when:

- [ ] Reviewed or adapted at least one Python implementation slice from your specification
- [ ] Performed at least 2 iteration/refinement cycles
- [ ] Created validation notes documenting spec compliance
- [ ] Documented which success criteria are met, partial, or unverified
- [ ] Documented any gaps between spec and implementation

## Summary

In this lab, you have learned the spec-driven development workflow:

1. **Write specifications** before code
2. **Use specs as context** for AI-assisted implementation
3. **Validate implementation proposals** against specifications
4. **Iterate** to improve compliance

This methodology produces more predictable, aligned implementation work and
creates documentation that serves as both development guide and acceptance
criteria.

---

**Completion note:** Lab 03 is complete when your spec, implementation slice,
and validation notes agree about scope, authority, and verification.

Return to the [Lab README](../README.md) to review completion criteria and prepare for the next lab.
