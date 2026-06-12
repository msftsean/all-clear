# Exercise 01a: Signal Classification

## Learning Objective

Understand how signal classification works as the foundation of the All Clear incident-triage pipeline. By the end of this exercise, you will be able to:

- Explain the QueryAgent's role in classifying inbound signals
- Build a simple classifier using GitHub Copilot
- Test your classifier against real-world incident-triage signals
- Achieve >90% accuracy on the provided test set

## Background

A **signal** is one inbound communication: a chat message, voice call, phone call, or submitted report. The QueryAgent is the first stage in All Clear. It turns that raw signal into a typed `SignalClassification` with an `intent`, `intent_category`, `target_queue`, entities, PII flags, and confidence.

The QueryAgent has **bounded authority**: it can classify only. It cannot decide severity, deduplicate, open incidents, attach reports, search knowledge, or generate a sitrep. The deterministic `RouterExecutor` handles dedup, severity/SLA mapping, and escalation after classification.

## SignalCategory Taxonomy

Your classifier must categorize signals into one of these All Clear `SignalCategory` values:

| SignalCategory | Description | Example Triggers |
|--------|-------------|------------------|
| `INFRASTRUCTURE_OUTAGE` | Power/service outage or major system failure | "outage", "no power", "blackout", "transformer", "substation" |
| `FIELD_HAZARD` | On-the-ground hazard needing field response | "power line down", "sparking", "flooding", "tree down", "blocked road" |
| `PUBLIC_SAFETY` | Life-safety threat | "gas smell", "fire", "smoke", "explosion", "injured", "trapped" |
| `CUSTOMER_INQUIRY` | Information or restoration-time question | "when will", "ETA", "power restored", "what is the status" |
| `SERVICE_REQUEST` | Routine non-urgent service need | "schedule", "inspection", "service appointment", "meter" |
| `COMPLIANCE_REPORT` | Statutory or regulatory filing | "NFIRS", "NIBRS", "recall", "breach notification", "statutory window" |
| `STATUS_CHECK` | Follow-up on an existing incident | "AC-####", "incident status", "any update", "already reported" |
| `HUMAN_REQUEST` | Explicit request for human handoff | "representative", "supervisor", "real person", "escalate" |
| `GENERAL_INQUIRY` | Greeting, thanks, unclear, or uncategorized signal | Ambiguous signals, small talk, too little information |

## Practice Signals

Before building your classifier, manually classify these 10 signals to build intuition:

### Easy (Clear Category)

1. **"Power line down across Main St, sparking near a school."**
   - Expected: `FIELD_HAZARD`
   - Rationale: Downed/sparking line is an on-the-ground hazard; RouterExecutor will later force severe handling from the indicators.

2. **"Smell of gas near the community center."**
   - Expected: `PUBLIC_SAFETY`
   - Rationale: Gas smell is a life-safety signal.

3. **"Need to file the NFIRS report for last night's fire."**
   - Expected: `COMPLIANCE_REPORT`
   - Rationale: NFIRS is a regulated compliance report format.

### Medium (Requires Context Understanding)

4. **"Water main break flooding the 200 block."**
   - Expected: `FIELD_HAZARD`
   - Rationale: Flooding at a location is a field hazard, even though water service may also be impaired.

5. **"When will power be restored on Elm St?"**
   - Expected: `CUSTOMER_INQUIRY`
   - Rationale: The caller is asking for restoration information, not reporting a new outage.

6. **"Whole neighborhood has no power after the transformer blew."**
   - Expected: `INFRASTRUCTURE_OUTAGE`
   - Rationale: Broad loss of power and transformer failure indicate infrastructure outage.

### Hard (Ambiguous or Multi-Hazard)

7. **"Transformer fire on Oak Ave and people are trapped."**
   - Expected: `PUBLIC_SAFETY`
   - Rationale: Life-safety wins over infrastructure classification.

8. **"I already reported AC-0042. Any update on the crew ETA?"**
   - Expected: `STATUS_CHECK`
   - Rationale: Existing incident id and update request indicate follow-up.

9. **"There is a product recall notification that must be filed within the statutory window."**
   - Expected: `COMPLIANCE_REPORT`
   - Rationale: Recall and statutory window create a compliance report signal.

10. **"This is urgent and I want to talk to a supervisor."**
    - Expected: `HUMAN_REQUEST`
    - Rationale: Explicit human handoff request belongs in the human request category.

## Instructions

### Step 1: Create Your Classifier

Using GitHub Copilot, create a Python function that classifies inbound signals. Start with this skeleton:

```python
# intent_classifier.py

from typing import Literal

SignalCategoryName = Literal[
    "INFRASTRUCTURE_OUTAGE", "FIELD_HAZARD", "PUBLIC_SAFETY",
    "CUSTOMER_INQUIRY", "SERVICE_REQUEST", "COMPLIANCE_REPORT",
    "STATUS_CHECK", "HUMAN_REQUEST", "GENERAL_INQUIRY", "unknown",
]

def classify_intent(signal: str) -> SignalCategoryName:
    """
    Classify one inbound All Clear signal into a SignalCategory value.

    Args:
        signal: One inbound communication from chat, voice, phone, or report

    Returns:
        The classified SignalCategory name, or "unknown" for empty/unusable input
    """
    # Use Copilot to help you implement this!
    # Hint: Start with keyword matching, then add precedence rules for life safety.
    pass
```

### Step 2: Implement Your Logic

Work with Copilot to implement the classifier. Consider these approaches (in order of sophistication):

1. **Keyword Matching**: Simple but effective for clear-cut signals
2. **Weighted Keywords**: Some phrases are stronger indicators than others
3. **Rule-Based Precedence**: Life safety beats outage; compliance clocks beat routine inquiry
4. **Confidence Scoring**: Return `GENERAL_INQUIRY` when confidence is low

Remember: the classifier is modeling QueryAgent behavior. It extracts classification signals only; it does not assign `SEV1`-`SEV4`, open `AC-####` incidents, or attach reports.

### Step 3: Test Against Sample Signals

Create a test file with at least 20 signals and expected categories:

```python
from intent_classifier import classify_intent

TEST_CASES = [
    {"signal": "Power line down across Main St, sparking near a school", "expected_category": "FIELD_HAZARD"},
    {"signal": "When will power be restored on Elm St?", "expected_category": "CUSTOMER_INQUIRY"},
]
```

### Step 4: Iterate and Improve

Review your failures and refine your classifier:

- Are there hazard phrases you missed?
- Are some keywords too broad (for example, "power" in both outage reports and restoration questions)?
- Should life-safety or statutory-clock signals take precedence?
- Are you preserving the difference between a signal, an incident, and a report?

## Success Criteria

Your exercise is complete when:

- [ ] Your `classify_intent()` function handles all 9 `SignalCategory` values
- [ ] You achieve **>90% accuracy** on the signal test set
- [ ] Your code is clean and well-commented
- [ ] You can explain *why* each classification decision was made
- [ ] You can explain why QueryAgent does not decide severity, dedup outcome, SLA, or escalation

## Reflection Questions

After completing the exercise, consider:

1. What types of signals were hardest to classify? Why?
2. How would you handle a signal that seems to belong to multiple categories?
3. What are the limitations of keyword-based signal classification?
4. What fields would a full `SignalClassification` include beyond `intent_category`?
5. Why must severity be mapped by RouterExecutor rules instead of model vibes?

## Next Steps

Once you've completed this exercise, proceed to:

- **Exercise 01b**: Prompt engineering for QueryAgent and ActionAgent
- **Exercise 01c**: Building a complete orchestration flow with bounded authority

---

## Appendix: Sample Test Case Format

```json
[
  {"signal": "Smell of gas near the community center", "expected_category": "PUBLIC_SAFETY"},
  {"signal": "Need to file the NFIRS report for last night's fire", "expected_category": "COMPLIANCE_REPORT"}
]
```

Create at least 20 test cases covering all 9 categories with varying difficulty levels.

