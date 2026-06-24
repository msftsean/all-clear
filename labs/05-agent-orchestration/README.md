# 🔄 Lab 05 - Agent Orchestration

| 📋 Attribute | Value |
|-------------|-------|
| ⏱️ **Duration** | 120 minutes (2 hours) |
| 📊 **Difficulty** | ⭐⭐⭐ Advanced |
| 🎯 **Prerequisites** | Lab 04 completed |

---

## 📈 Progress Tracker

```
Lab Progress: [░░░░░░░░░░] 0% - Not Started

Checkpoints:
□ Step 1: Define Data Contracts (SignalClassification, RoutingDecision, IncidentAction)
□ Step 2: Implement Session Context
□ Step 3: Build the QueryAgent (classify only)
□ Step 4: Build the RouterExecutor (deterministic: dedup → severity → SLA → escalation)
□ Step 5: Build the ActionAgent (create_incident, search_knowledge, generate_sitrep)
□ Step 6: Wire the MAF workflow (QueryStage → RouterExecutor → ActionExecutor)
□ Step 7: Run a SURGE and watch dedup attach reports
```

---

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. 🔗 **Assemble the three-stage pipeline** — chain QueryAgent → RouterExecutor → ActionAgent into one MAF workflow that turns a **signal** into an **incident**
2. 🚦 **Implement deterministic routing** — dedup, severity/SLA mapping, and escalation with **zero LLM calls** (auditable, un-spoofable)
3. 🌊 **Survive a surge** — feed a burst of duplicate signals and watch dedup `ATTACH_TO_INCIDENT` keep one incident per real-world event

---

> 💡 **Extension:** Once your pipeline is working, Exercise 05x shows how the same three-agent architecture handles voice and phone input—no agent changes needed.

## 🔁 Recap: The Three-Stage Pipeline

In Lab 01 you learned the bounded-authority model. Now you implement it. The
reference implementation is real: see
[`backend/app/agents/pipeline.py`](../../backend/app/agents/pipeline.py).

```
   signal: "Power line down across Main St, sparking near a school"
            │
            ▼
   ┌─────────────────┐     ┌──────────────────┐     ┌────────────────────────┐
   │   QueryAgent     │──▶  │  RouterExecutor   │──▶  │      ActionAgent        │
   │  classify ONLY   │     │ ZERO LLM calls    │     │  create_incident        │
   │                  │     │ dedup→sev→SLA→esc │     │  search_knowledge       │
   │ SignalClassif.   │     │ RoutingDecision   │     │  generate_sitrep        │
   └─────────────────┘     └──────────────────┘     └────────────────────────┘
            │                                                    │
            ▼                                                    ▼
   INFRASTRUCTURE_OUTAGE              OPEN_INCIDENT AC-0001, SEV1, field-operations,
   sev indicators: ["sparking",       15-min SLA, escalate=true (life_safety)
   "near a school"]                  → citation-grounded sitrep to the reporter
```

### 🔄 Pipeline Flow

```
signal --> QueryAgent --> RouterExecutor --> ActionAgent --> PipelineResult
```

> The pipeline is modality-agnostic. Text, voice (WebRTC), and phone (ACS) all
> enter through different endpoints but converge at the QueryAgent. Lifecycle
> events publish to the transcript bus so the **ClearBoard** updates live.

### 👥 Stage Responsibilities Recap

| 🤖 Stage | 📥 Input | 📤 Output | 🎯 Responsibility |
|-------|-------|--------|----------------|
| 🔍 **QueryAgent** | Raw signal + channel | `SignalClassification` | Classify intent/category, extract entities, flag PII — **classify only** |
| 🚦 **RouterExecutor** | `SignalClassification` | `RoutingDecision` | Dedup, severity/SLA, escalation — **deterministic, zero LLM** |
| ⚡ **ActionAgent** | `RoutingDecision` | `IncidentAction` | Create/attach incident, search KB, generate cited sitrep — **3 tools only** |

---

## 🏗️ Architecture Overview

In this lab, you assemble the pipeline. The canonical implementation lives in
[`backend/app/agents/`](../../backend/app/agents/) — study it as your reference:

```
backend/app/agents/
  📄 schemas.py        # Data contracts: SignalClassification, RoutingDecision, IncidentAction
  📄 query_agent.py    # QueryAgent (MAF agent) — classify only
  📄 router_agent.py   # RouterExecutor (MAF executor) — deterministic, zero LLM
  📄 action_agent.py   # ActionExecutor + ActionToolbox (3 tools)
  📄 envelopes.py      # ClassifiedSignal / RoutedSignal hand-off envelopes
  📄 pipeline.py       # build_workflow(): QueryStage → RouterExecutor → ActionExecutor
  📄 escalation_rules.py  # Escalation logic (safety control)
  📄 safety.py         # PII / harm safety net
```

---

## 📝 Step-by-Step Instructions

### 🔹 Step 1: Define Data Contracts

Before implementing stages, establish the typed contracts that flow between
them. These mirror [`backend/app/agents/schemas.py`](../../backend/app/agents/schemas.py)
(Constitution Art. IV: structured output, never free-text parsing). Open
`start/models.py`:

#### 1a: 📋 QueryAgent output — `SignalClassification`

```python
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class SignalCategory(str, Enum):
    INFRASTRUCTURE_OUTAGE = "INFRASTRUCTURE_OUTAGE"
    FIELD_HAZARD = "FIELD_HAZARD"
    PUBLIC_SAFETY = "PUBLIC_SAFETY"
    CUSTOMER_INQUIRY = "CUSTOMER_INQUIRY"
    SERVICE_REQUEST = "SERVICE_REQUEST"
    COMPLIANCE_REPORT = "COMPLIANCE_REPORT"
    STATUS_CHECK = "STATUS_CHECK"
    HUMAN_REQUEST = "HUMAN_REQUEST"
    GENERAL_INQUIRY = "GENERAL_INQUIRY"

class SignalEntities(BaseModel):
    location: Optional[str] = None
    system: Optional[str] = None
    severity_indicators: list[str] = Field(default_factory=list)

class SignalClassification(BaseModel):
    """QueryAgent output. Authority: classify only."""
    intent: str
    intent_category: SignalCategory
    confidence: float = Field(..., ge=0.0, le=1.0)
    entities: SignalEntities = Field(default_factory=SignalEntities)
    pii_detected: bool = False
    pii_types: list[str] = Field(default_factory=list)
    urgency_indicators: list[str] = Field(default_factory=list)
```

#### 1b: 🚦 RouterExecutor output — `RoutingDecision`

```python
class Severity(str, Enum):
    SEV1 = "SEV1"  # life safety / total outage / statutory clock — 15-min SLA, always escalates
    SEV2 = "SEV2"  # major, public-facing, spreading — 1-hour SLA
    SEV3 = "SEV3"  # contained, single-party — 4-hour SLA
    SEV4 = "SEV4"  # informational — next business day

class RoutingDecision(BaseModel):
    """RouterExecutor output. Deterministic — zero LLM calls."""
    outcome: str                 # "OPEN_INCIDENT" | "ATTACH_TO_INCIDENT"
    target_queue: str            # field-operations | customer-comms | compliance-desk | engineering | escalations
    severity: Severity
    sla_minutes: int
    escalate: bool = False
    escalation_reason: Optional[str] = None
    matched_incident_id: Optional[str] = None   # set on ATTACH_TO_INCIDENT
    dedup_similarity: Optional[float] = None
    routing_rules_applied: list[str] = Field(default_factory=list)
```

#### 1c: ⚡ ActionAgent output — `IncidentAction`

```python
class IncidentAction(BaseModel):
    """ActionAgent / attach-path output."""
    status: str                  # opened | attached | escalated | error
    incident_id: Optional[str]   # AC-####
    queue: str
    severity: Severity
    citations: list[dict] = Field(default_factory=list)  # every claim cites a source record
    estimated_response_time: str
    escalated: bool = False
    user_message: str            # acknowledgment shown to the reporter (never echoes PII)
```

**Task:** Complete the data models in `start/models.py` to match
[`schemas.py`](../../backend/app/agents/schemas.py). 📝

### 🔹 Step 2: Implement Session Context

Session context maintains state across conversation turns. Open `start/pipeline.py` (the session helper classes live at the top of this scaffold):

#### 2a: 💾 Session Store

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class ConversationTurn:
    """A single turn in the conversation."""
    turn_id: str
    timestamp: datetime
    user_message: str
    agent_response: str
    intent: str
    entities: dict

@dataclass
class Session:
    """Maintains conversation state across turns."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    turns: list[ConversationTurn] = field(default_factory=list)
    context: dict = field(default_factory=dict)  # Arbitrary context storage

    def add_turn(
        self,
        user_message: str,
        agent_response: str,
        intent: str,
        entities: dict
    ) -> ConversationTurn:
        """📝 Record a conversation turn."""
        turn = ConversationTurn(
            turn_id=str(uuid.uuid4()),
            timestamp=datetime.now(tz=None),
            user_message=user_message,
            agent_response=agent_response,
            intent=intent,
            entities=entities
        )
        self.turns.append(turn)
        return turn

    def get_history(self, max_turns: int = 5) -> list[dict]:
        """📚 Get recent conversation history for context."""
        recent = self.turns[-max_turns:] if len(self.turns) > max_turns else self.turns
        history = []
        for t in recent:
            history.append({"role": "user", "content": t.user_message})
            history.append({"role": "assistant", "content": t.agent_response})
        return history

    def get_context_summary(self) -> str:
        """📋 Generate a summary of conversation context."""
        if not self.turns:
            return "No previous conversation."

        recent_intents = [t.intent for t in self.turns[-3:]]
        all_entities = {}
        for t in self.turns:
            all_entities.update(t.entities)

        return f"""Previous topics: {', '.join(set(recent_intents))}
Known entities: {all_entities}
Turn count: {len(self.turns)}"""
```

#### 2b: 🗄️ Session Manager

```python
class SessionManager:
    """Manages multiple concurrent sessions."""

    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> Session:
        """🔍 Get existing session or create new one."""
        if session_id and session_id in self._sessions:
            return self._sessions[session_id]

        session = Session(session_id=session_id) if session_id else Session()
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        """🔍 Get session by ID."""
        return self._sessions.get(session_id)

    def delete(self, session_id: str) -> bool:
        """🗑️ Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
```

**Task:** Complete the session management in `start/pipeline.py`. 📝

### 🔹 Step 3: Implement QueryAgent

The QueryAgent transforms raw user input into structured data. Open `start/query_agent.py`:

```python
from openai import AsyncAzureOpenAI
from models import SignalClassification, SignalCategory, SignalEntities
from session import Session
import json

class QueryAgent:
    """
    🔍 Transforms raw user input into structured, actionable data.

    Responsibilities:
    - 📝 Parse natural language queries
    - 🏷️ Extract entities (names, dates, IDs, etc.)
    - 🎯 Classify intent
    - 📚 Enrich with conversation context
    """

    def __init__(self, openai_client: AsyncAzureOpenAI, model_deployment: str):
        self.client = openai_client
        self.model = model_deployment

    async def process(
        self,
        user_message: str,
        session: Session
    ) -> SignalClassification:
        """
        Process user message into structured query.

        Args:
            user_message: Raw user input
            session: Current conversation session

        Returns:
            SignalClassification with intent, entities, and metadata
        """
        system_prompt = """You are the QueryAgent for All Clear incident triage.
Your ONLY job is to classify one inbound signal. You do not route, create, or
search. Classify the signal and return structured JSON.

1. 🎯 Classify intent_category into one of:
   - INFRASTRUCTURE_OUTAGE: downed lines, power/water/network outages
   - FIELD_HAZARD: on-the-ground hazard (debris, flooding, spill)
   - PUBLIC_SAFETY: life-safety threat (fire, gas leak, people in danger)
   - CUSTOMER_INQUIRY: status/info request ("when will power return?")
   - SERVICE_REQUEST: routine, non-urgent service
   - COMPLIANCE_REPORT: statutory/recall/NFIRS-NIBRS reporting
   - STATUS_CHECK: follow-up on an existing incident
   - HUMAN_REQUEST: explicit request for a human
   - GENERAL_INQUIRY: uncategorized

2. 🏷️ Extract entities:
   - location: place referenced (street, block, building)
   - system: asset referenced (grid, line, app, main)
   - severity_indicators: phrases signalling danger ("fire", "no power", "injured", "sparking")

3. 🚩 Detect PII (names, phone numbers, addresses tied to a person). Flag it;
   NEVER echo it back.

Respond with JSON only:
{
    "intent": "<short intent label>",
    "intent_category": "<one of the categories above>",
    "confidence": <0.0-1.0>,
    "entities": {"location": "...", "system": "...", "severity_indicators": [...]},
    "pii_detected": <bool>,
    "pii_types": [...],
    "urgency_indicators": [...]
}"""

        # 📚 Include recent signals from this session/channel for context
        context_summary = session.get_context_summary()

        user_prompt = f"""Session context:
{context_summary}

Current signal: {user_message}

Classify this signal and respond with JSON."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return SignalClassification(
            intent=result["intent"],
            intent_category=SignalCategory(result["intent_category"]),
            confidence=result["confidence"],
            entities=SignalEntities(**result.get("entities", {})),
            pii_detected=result.get("pii_detected", False),
            pii_types=result.get("pii_types", []),
            urgency_indicators=result.get("urgency_indicators", []),
        )
```

**Task:** Complete the QueryAgent in `start/query_agent.py`. It **classifies only** — it must never create or route. 📝

### 🔹 Step 4: Implement the RouterExecutor

> 🚨 **This is the most important stage.** The RouterExecutor makes **zero LLM
> calls** — by design and by test (Constitution Art. II & III). Severity, SLA,
> and escalation are safety-critical and must be deterministic and auditable, so
> a caller (or an attacker) can never *talk* the system into a lower severity.
> It takes no `AsyncAzureOpenAI` client. It is pure code.

The RouterExecutor runs three deterministic phases: **dedup → severity/SLA →
escalation**. Open `start/router_agent.py`:

```python
from models import SignalClassification, RoutingDecision, Severity

# Severity → response SLA (minutes). CONTEXT.md severity/SLA matrix.
SLA_MINUTES = {Severity.SEV1: 15, Severity.SEV2: 60, Severity.SEV3: 240, Severity.SEV4: 1440}

# intent_category → destination queue.
QUEUE_FOR = {
    "INFRASTRUCTURE_OUTAGE": "engineering",
    "FIELD_HAZARD": "field-operations",
    "PUBLIC_SAFETY": "field-operations",
    "CUSTOMER_INQUIRY": "customer-comms",
    "SERVICE_REQUEST": "customer-comms",
    "COMPLIANCE_REPORT": "compliance-desk",
    "STATUS_CHECK": "customer-comms",
    "HUMAN_REQUEST": "escalations",
    "GENERAL_INQUIRY": "customer-comms",
}

DEDUP_THRESHOLD = 0.83  # cosine; from config

class RouterExecutor:
    """Deterministic routing. NO LLM. NO tools. Touches no records."""

    def __init__(self, incident_store, embedder):
        self.incidents = incident_store   # read-only lookup of open incidents
        self.embed = embedder             # embedding function for dedup

    def route(self, sig: SignalClassification, signal_text: str) -> RoutingDecision:
        rules = []

        # Phase 1 — DEDUP: compare against open incidents in the SAME category.
        match_id, similarity = self._best_match(signal_text, sig.intent_category)
        if similarity is not None and similarity >= DEDUP_THRESHOLD:
            rules.append(f"dedup>={DEDUP_THRESHOLD}")
            sev = self._severity(sig)
            return RoutingDecision(
                outcome="ATTACH_TO_INCIDENT",
                target_queue=QUEUE_FOR[sig.intent_category.value],
                severity=sev, sla_minutes=SLA_MINUTES[sev],
                matched_incident_id=match_id, dedup_similarity=similarity,
                routing_rules_applied=rules,
            )

        # Phase 2 — SEVERITY / SLA (rules, not vibes).
        sev = self._severity(sig)
        rules.append(f"severity={sev.value}")

        # Phase 3 — ESCALATION (safety control). SEV1 and statutory clocks
        # ALWAYS escalate; no model output can downgrade them.
        escalate, reason = False, None
        if sev == Severity.SEV1:
            escalate, reason = True, "sev1_incident"
        elif "statutory" in " ".join(sig.urgency_indicators).lower():
            escalate, reason = True, "statutory_clock"
        elif sig.confidence < 0.70:
            escalate, reason = True, "confidence_too_low"
        elif sig.pii_detected:
            rules.append("pii_flagged")
        if escalate:
            rules.append(f"escalate:{reason}")

        return RoutingDecision(
            outcome="OPEN_INCIDENT",
            target_queue=QUEUE_FOR[sig.intent_category.value],
            severity=sev, sla_minutes=SLA_MINUTES[sev],
            escalate=escalate, escalation_reason=reason,
            routing_rules_applied=rules,
        )

    def _severity(self, sig: SignalClassification) -> Severity:
        """Map severity indicators to SEV1..SEV4 deterministically."""
        text = " ".join(sig.severity_indicators_all()).lower()
        if any(k in text for k in ("fire", "gas", "injured", "trapped", "no power", "statutory")):
            return Severity.SEV1
        if sig.intent_category.value in ("INFRASTRUCTURE_OUTAGE", "FIELD_HAZARD"):
            return Severity.SEV2
        if sig.intent_category.value in ("CUSTOMER_INQUIRY", "SERVICE_REQUEST", "STATUS_CHECK"):
            return Severity.SEV4
        return Severity.SEV3
```

**Task:** Complete the RouterExecutor in `start/router_agent.py`. Verify with a
test that it imports **no** OpenAI client and makes zero network calls. 📝

> Compare your implementation against the real
> [`router_agent.py`](../../backend/app/agents/router_agent.py) — note how it is
> a MAF `Executor`, not an `Agent`, precisely because it never calls a model.

### 🔹 Step 5: Implement the ActionAgent

The ActionAgent acts on the `RoutingDecision` through **exactly three tools** and
nothing else (Constitution Art. II). Open `start/action_agent.py`:

- 🆕 **create_incident** — on `OPEN_INCIDENT`, mint a new incident `AC-####` in the target queue at the decided severity
- 📚 **search_knowledge** — RAG over incident runbooks/SOPs (Lab 04); returns `KnowledgeArticle`s used to ground the response
- 📝 **generate_sitrep** — produce a **citation-grounded** situation report; every factual claim cites a source record (Art. IV)

Path rules:
- **`OPEN_INCIDENT`** → `create_incident` → `search_knowledge` → `generate_sitrep` → return `IncidentAction(status="opened")` with citations.
- **`ATTACH_TO_INCIDENT`** → **no** knowledge search (keeps surge latency flat) → increment the matched incident's magnitude → return a short acknowledgment `IncidentAction(status="attached")`.
- **`escalate=True`** → hand off to the `escalations` queue; never suppress it.

**Task:** Complete the ActionAgent + its toolbox in `start/action_agent.py`.
Reference [`action_agent.py`](../../backend/app/agents/action_agent.py). 📝

### 🔹 Step 6: Wire Up the MAF Workflow

Connect the three stages into one Microsoft Agent Framework workflow. Open
`start/pipeline.py`:

```python
class AgentPipeline:
    """Coordinates QueryAgent, RouterExecutor, and ActionAgent."""

    async def process(self, signal_text: str, session_id: str | None = None) -> tuple[IncidentAction, str]:
        session = self.session_manager.get_or_create(session_id)

        # 🔍 Stage 1: QueryAgent — classify the signal (LLM)
        classification = await self.query_agent.classify(signal_text, session.get_context_summary())

        # 🚦 Stage 2: RouterExecutor — decide deterministically (NO LLM)
        decision = await self.router_executor.route(classification, signal_text)

        # ⚡ Stage 3: ActionAgent — act through its three tools
        action = await self.action_agent.execute(decision, session.get_history())

        session.add_turn(signal_text, action.user_message, classification.category.value, classification.entities)
        return action, session.session_id
```

In the real codebase this is assembled with a MAF `WorkflowBuilder`
(`QueryStage → RouterExecutor → ActionExecutor`); the adapter above and the
workflow share the same three stages so they produce identical incidents and
audit entries (Constitution Art. V). See
[`pipeline.py`](../../backend/app/agents/pipeline.py).

**Task:** Complete the pipeline in `start/pipeline.py`. 📝

### 🔹 Step 7: Run a Surge

The hero scenario: a burst of signals where most are **duplicates** of a few
real incidents. A correct pipeline opens *one* incident per real-world event and
**attaches** the rest, incrementing magnitude.

```python
# test_surge.py
async def test_surge():
    """🌊 40 callers, one downed line — expect 1 incident, 40 reports."""
    pipeline = AgentPipeline(...)

    surge = [
        "Power line down across Main St, sparking near the school",   # OPEN_INCIDENT (SEV1)
        "There's a downed power line on Main Street, wires on the road",  # ATTACH
        "Main St has a line down, looks dangerous",                   # ATTACH
        "When will the power be back on Elm St?",                     # CUSTOMER_INQUIRY (SEV4)
        "Smell of gas near the community center",                     # OPEN_INCIDENT (SEV1, new event)
    ]

    session_id = None
    for signal in surge:
        action, session_id = await pipeline.process(signal, session_id)
        print(f"signal : {signal}")
        print(f"outcome: {action.status}  {action.incident_id}  {action.severity}\n")
```

```bash
python test_surge.py
```

✅ Expect the three "Main St line down" signals to share **one** incident id
(the 2nd and 3rd `ATTACH_TO_INCIDENT`), the gas-leak signal to `OPEN_INCIDENT` a
new SEV1, and the Elm St question to be a SEV4 customer inquiry.

---

## ✅ Deliverables

By the end of this lab, you should have:

| 📋 Deliverable | ✅ Success Criteria |
|-------------|------------------|
| 🔍 QueryAgent | Classifies signals into a typed `SignalClassification` (classify only) |
| 🚦 RouterExecutor | Deterministic dedup + severity/SLA + escalation, **zero LLM calls** |
| ⚡ ActionAgent | Acts through exactly three tools (create_incident, search_knowledge, generate_sitrep) |
| 🔄 Pipeline | QueryAgent → RouterExecutor → ActionAgent working end-to-end → `PipelineResult` |
| 🌊 Surge handling | Duplicate signals `ATTACH_TO_INCIDENT`; one incident per real-world event |
| 🧪 Test Results | Surge test passes; SEV1 always escalates |

- **(Optional) Exercise 05x:** [Voice & Phone Extensions](exercises/05x-voice-phone-extensions.md) — See your pipeline respond to spoken queries and phone calls

---

## 🔧 Troubleshooting Tips

### ⚠️ Common Issues

**Issue:** Signal classification is inconsistent
- ✅ **Solution:** Lower temperature in QueryAgent (use 0.1 or lower)
- ✅ **Solution:** Add explicit signal examples per `SignalCategory` in the system prompt
- ✅ **Solution:** Use structured output format (JSON mode)

**Issue:** RouterExecutor produces the wrong severity or queue
- ✅ **Solution:** Verify QueryAgent extracted the right `severity_indicators` and `intent_category`
- ✅ **Solution:** Check the deterministic severity/queue maps — never let the model decide severity
- ✅ **Solution:** Confirm SEV1 / statutory-clock signals always set `escalate=True`

**Issue:** Surge opens duplicate incidents instead of attaching
- ✅ **Solution:** Verify dedup compares within the same `intent_category`
- ✅ **Solution:** Check `DEDUP_THRESHOLD` (default 0.83) and your embedding function
- ✅ **Solution:** Ensure matched signals return `ATTACH_TO_INCIDENT` with a `matched_incident_id`

### 📋 Debugging Checklist

1. [ ] 📄 Data contracts (SignalClassification, RoutingDecision, IncidentAction) match `schemas.py`
2. [ ] 🎯 QueryAgent returns valid `SignalCategory` values and never creates/routes
3. [ ] 🚫 RouterExecutor imports **no** OpenAI client (zero LLM calls)
4. [ ] 🆙 SEV1 and statutory-clock incidents always escalate
5. [ ] 🔁 Dedup attaches duplicates; magnitude increments; no signal is deleted
6. [ ] 📝 Sitreps cite a source record for every factual claim
7. [ ] 🚩 Detected PII is never echoed in responses or logs

---

## 📚 Additional Resources

- 📖 [Azure OpenAI Structured Outputs](https://learn.microsoft.com/azure/ai-services/openai/how-to/structured-outputs)
- 🔧 [Pydantic Model Validation](https://docs.pydantic.dev/latest/)
- 🔄 [Python Async/Await Patterns](https://docs.python.org/3/library/asyncio.html)
- 🏗️ [Agent Orchestration Patterns](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-openai-e2e-chat)

---

## ➡️ Next Steps

Once your pipeline handles multi-turn conversations correctly, proceed to:

**[Lab 06 - Deploy with azd](../06-deploy-with-azd/README.md)** 🚀

In the next lab, you will containerize your agent system and deploy it to Azure using the Azure Developer CLI.

---

## 📊 Version Matrix

| Component | Required Version | Tested Version |
|-----------|-----------------|----------------|
| 🐍 Python | 3.11+ | 3.12.10 |
| 🤖 Azure OpenAI | GPT-5.1 | 2025-01-01-preview |
| 🔧 Pydantic | 2.5+ | 2.10+ |
| 🔄 asyncio | 3.11+ | Built-in |

---

<div align="center">

[← Lab 04](../04-build-rag-pipeline/README.md) | **Lab 05** | [Lab 06 →](../06-deploy-with-azd/README.md)

📅 Last Updated: 2026-02-26 | 📝 Version: 1.1.0

</div>
