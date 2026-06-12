# Lab 05 - Agent Orchestration: Completion Specification

## What "Done" Looks Like

Lab 05 is complete when you have built a working All Clear incident-triage pipeline that processes one inbound **signal** through QueryAgent, RouterExecutor, and ActionAgent stages. You should be able to:

1. Process any inbound signal and receive an appropriate incident-triage response
2. Maintain session context across multiple turns in the same channel/session
3. Classify signals into the All Clear `SignalCategory` taxonomy
4. Route deterministically with dedup, severity/SLA mapping, and escalation using zero LLM calls in RouterExecutor
5. Execute the final action through exactly three ActionAgent tools: `create_incident`, `search_knowledge`, and `generate_sitrep`

A successfully completed Lab 05 means you have a functional bounded-authority orchestration system ready for the later deployment labs.

---

## Checkable Deliverables

### 1. Full Pipeline QueryAgent -> RouterExecutor -> ActionAgent Working

**What it verifies:**
- All three stages are implemented and connected
- Data flows correctly between stages using defined contracts
- QueryAgent classifies only
- RouterExecutor makes zero LLM calls
- ActionAgent returns an `IncidentAction` with citation-grounded sitrep data when opening an incident

**Acceptance Criteria:**
- [ ] QueryAgent parses raw signals into `SignalClassification` objects
- [ ] Classification includes `SignalCategory`, confidence, entities, severity indicators, and PII flags
- [ ] RouterExecutor maps category to queue: `field-operations`, `customer-comms`, `compliance-desk`, `engineering`, or `escalations`
- [ ] RouterExecutor compares duplicate signals to open incidents and chooses `ATTACH_TO_INCIDENT` at cosine similarity >= 0.83, otherwise `OPEN_INCIDENT`
- [ ] RouterExecutor maps severity as `SEV1`-`SEV4` and assigns the matching SLA
- [ ] SEV1, statutory-clock, PII exposure, explicit human request, and low-confidence signals escalate deterministically
- [ ] ActionAgent uses only `create_incident`, `search_knowledge`, and `generate_sitrep`
- [ ] New incidents use `AC-####` ids matching `^AC-\d{4,}$`
- [ ] Attaching a report increments magnitude and does not run knowledge search

**How to Test:**

```bash
cd labs/05-agent-orchestration
python test_lab05.py
```

**Test Cases:**

| Input | Expected Flow | Expected Outcome |
|-------|---------------|------------------|
| "Power line down across Main St, sparking on the road" | QueryAgent -> RouterExecutor -> ActionAgent | `PUBLIC_SAFETY` or `FIELD_HAZARD`, `SEV1`, `OPEN_INCIDENT`, `field-operations`, escalation |
| "Any update on the Elm Street outage?" | QueryAgent -> RouterExecutor -> ActionAgent | `STATUS_CHECK`, no new incident unless no match exists |
| "I want to speak to a human" | QueryAgent -> RouterExecutor -> ActionAgent | `HUMAN_REQUEST`, `escalations`, escalation |
| "Need to file the NFIRS report for last night's fire" | QueryAgent -> RouterExecutor -> ActionAgent | `COMPLIANCE_REPORT`, `SEV1`, `compliance-desk`, escalation |
| "asdfghjkl" | QueryAgent -> RouterExecutor -> ActionAgent | `GENERAL_INQUIRY` or clarification, safe response |

**Verification Script:**

```python
import pytest
from pipeline import AgentPipeline
from query_agent import SignalCategory

@pytest.mark.asyncio
async def test_pipeline_opens_incident():
    pipeline = AgentPipeline()
    action, session_id = await pipeline.process("Power line down across Main St, sparking on the road")
    assert action.incident_id.startswith("AC-")
    assert action.severity.value == "SEV1"
    assert action.escalated
    assert session_id

@pytest.mark.asyncio
async def test_pipeline_human_request_escalates():
    pipeline = AgentPipeline()
    action, _ = await pipeline.process("I want to speak to a human")
    assert action.queue == "escalations"
    assert action.escalated
```

---

### 2. Multi-Turn Session Context Works

**What it verifies:**
- Session IDs are generated and returned
- Previous signals and responses are preserved
- Entity information persists within a session
- Recent context is available to the QueryAgent prompt

**Acceptance Criteria:**
- [ ] First signal creates a session id
- [ ] Reusing the same session id appends turns to the same session
- [ ] `get_history(max_turns=5)` returns recent user/assistant messages
- [ ] `get_context_summary()` mentions recent categories and known entities
- [ ] New session starts with no previous turns

**Test Cases:**

| Scenario | Verification |
|----------|--------------|
| Turn 1: "Power line down across Main St" -> Turn 2: "Any update there?" | Same session has 2 turns |
| Turn 1: incident opened -> Turn 2: same hazard | Dedup may attach as a report when open incident similarity is high |
| 3 turns of conversation | Session records 3 preserved signals |
| New session | Starts fresh with no history |

---

## Verification Steps

### Step 1: Stage Import Verification

```bash
python -c "from query_agent import QueryAgent, SignalCategory; print('QueryAgent OK')"
python -c "from router_agent import RouterExecutor; print('RouterExecutor OK')"
python -c "from action_agent import ActionAgent; print('ActionAgent OK')"
python -c "from pipeline import AgentPipeline; print('Pipeline OK')"
```

### Step 2: Teaching Verifier

```bash
python test_lab05.py
```

Expected output includes:
- QueryAgent classifies incident-triage signals
- RouterExecutor returns `RoutingDecision` with severity/SLA/escalation
- Full pipeline opens `AC-####` incidents and produces citations

### Step 3: Compile Check

```bash
python -m py_compile start\*.py solution\*.py test_lab05.py
```

---

## Assessment Rubric

### Total Points: 25 (Agent Orchestration)

| Criteria | Points | Description |
|----------|--------|-------------|
| **QueryAgent Implementation** | 5 | Correctly classifies signals and extracts entities |
| **RouterExecutor Implementation** | 5 | Deterministic dedup, severity/SLA, and escalation with zero LLM calls |
| **ActionAgent Implementation** | 5 | Exactly three tools and citation-grounded sitreps |
| **Pipeline Orchestration** | 5 | QueryAgent -> RouterExecutor -> ActionAgent flow works end-to-end |
| **Session Management** | 5 | Multi-turn signal context maintained correctly |

### Detailed Scoring Guide

#### QueryAgent Implementation (5 points)
- **5 points:** Extracts category, entities, confidence, PII flags; handles edge cases; uses session context
- **4 points:** Works for common cases but misses some entities or edge cases
- **3 points:** Basic category classification works but entity extraction incomplete
- **2 points:** Returns structured output but classification unreliable
- **0-1 points:** Not functional or returns invalid data

#### RouterExecutor Implementation (5 points)
- **5 points:** Dedup, queue, severity, SLA, and escalation rules all deterministic and correct
- **4 points:** Deterministic routing works but one rule is incomplete
- **3 points:** Basic routing works but dedup or escalation is incomplete
- **2 points:** Only maps categories to queues
- **0-1 points:** Calls an LLM or routing mostly fails

#### ActionAgent Implementation (5 points)
- **5 points:** Uses only `create_incident`, `search_knowledge`, `generate_sitrep`; every sitrep claim cites a source
- **4 points:** Three tools work but citation detail is thin
- **3 points:** Opens incidents but attach path or sitrep is incomplete
- **2 points:** Partial action execution
- **0-1 points:** ActionAgent not functional

#### Pipeline Orchestration (5 points)
- **5 points:** Full flow works, handles errors, and records session turns
- **4 points:** Pipeline works but error handling incomplete
- **3 points:** Happy path works but edge cases fail
- **2 points:** Partial flow works but stages are loosely connected
- **0-1 points:** Pipeline not connected

#### Session Management (5 points)
- **5 points:** History tracked, context summarized, entities persist, cleanup possible
- **4 points:** Sessions work but context is not fully utilized
- **3 points:** Basic session tracking only
- **2 points:** Sessions created but state not maintained properly
- **0-1 points:** No session management or broken

---

## Common Failure Modes and Resolutions

### Classification Is Inconsistent

**Symptom:** Same signal classified differently on repeated runs.

**Resolution:** Use structured output, low temperature, and clear examples. QueryAgent may use an LLM, but it must return a typed classification and never route.

### RouterExecutor Uses a Model

**Symptom:** The routing stage has an OpenAI client or prompt.

**Resolution:** Remove the model call. RouterExecutor is deterministic code. It uses category, severity indicators, PII flags, confidence, and dedup similarity to produce `RoutingDecision`.

### Severity Can Be Downgraded by Wording

**Symptom:** A signal like "gas smell near the community center" becomes low severity because the reporter says it is "probably fine."

**Resolution:** Severity comes from deterministic rules. Life-safety, total outage, and statutory clocks force `SEV1` and escalation.

### Sitrep Has Uncited Claims

**Symptom:** `generate_sitrep` summarizes facts that do not appear in incident or knowledge records.

**Resolution:** Apply "no citation, no claim." Every factual statement must cite an incident, signal, report, or knowledge record.

### Duplicate Reports Open Too Many Incidents

**Symptom:** A surge creates one incident per duplicate signal.

**Resolution:** Dedup within the same category before opening a new incident. Similarity >= 0.83 means `ATTACH_TO_INCIDENT`, and magnitude increments.

---

## Success Checklist

Before proceeding to Lab 06, ensure all items are checked:

- [ ] QueryAgent returns `SignalClassification`
- [ ] SignalCategory values match All Clear taxonomy
- [ ] RouterExecutor makes zero LLM calls
- [ ] RouterExecutor implements dedup threshold 0.83
- [ ] RouterExecutor maps `SEV1`-`SEV4` and SLA minutes
- [ ] RouterExecutor escalates SEV1 and statutory-clock incidents
- [ ] ActionAgent exposes exactly three tools
- [ ] New incidents use `AC-####`
- [ ] Reports attach to existing incidents and increment magnitude
- [ ] Sitreps are citation-grounded
- [ ] Pipeline connects all stages in order
- [ ] Session ID generated and returned
- [ ] Signal history maintained across turns
- [ ] All pipeline tests pass

**Estimated Time:** 2-3 hours

**Points Possible:** 25 (Agent Orchestration)

**Prerequisites:**
- Lab 04 completed (RAG pipeline with All Clear knowledge records)
- Understanding of bounded authority from Lab 01
- Azure OpenAI configured for optional live QueryAgent prompt testing

**Next Step:** Proceed to Lab 06 - Deploy with azd
