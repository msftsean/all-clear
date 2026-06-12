# 🤖 Lab 01 - Understanding AI Agents

| 📋 Attribute | Value |
|-------------|-------|
| ⏱️ **Duration** | 90 minutes |
| 📊 **Difficulty** | ⭐⭐ Intermediate |
| 🎯 **Prerequisites** | Lab 00 completed |

---

## 📈 Progress Tracker

```
Lab Progress: [░░░░░░░░░░] 0% - Not Started

Checkpoints:
□ Understand Multi-Agent Architecture & Bounded Authority
□ Learn QueryAgent Pattern (classify only)
□ Learn RouterExecutor Pattern (deterministic, zero LLM)
□ Learn ActionAgent Pattern (three tools)
□ Complete Exercise 1a: Signal Classification
□ Complete Exercise 1b: Prompt Engineering
□ Achieve >90% Classification Accuracy
□ Complete Self-Assessment
```

---

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. 🏗️ **Understand multi-agent vs single agent architectures** - Compare the trade-offs between monolithic AI systems and distributed agent patterns
2. 🔄 **Learn the QueryAgent → RouterExecutor → ActionAgent pattern** - Master All Clear's three-stage pipeline and its *bounded authority* model
3. 🎯 **Practice signal classification** - Build and test a classifier that turns a raw incident **signal** into a typed `SignalClassification`

---

## 🤔 Why Multi-Agent Over Monolithic?

When building AI-powered applications, a natural first instinct is to create a single, powerful agent that handles everything. While this works for simple use cases, it quickly becomes problematic as complexity grows.

### ❌ The Monolithic Problem

A single-agent architecture suffers from:

| 🚫 Issue | 📝 Description |
|---------|-------------|
| **Prompt Bloat** | System prompts grow unwieldy as you add more capabilities |
| **Context Confusion** | The model struggles to stay focused when handling disparate tasks |
| **Testing Difficulty** | Hard to isolate and test specific behaviors |
| **Maintenance Burden** | Changes to one capability risk breaking others |
| **Cost Inefficiency** | Every request pays for the full prompt, even for simple tasks |

### ✅ The Multi-Agent Solution

Breaking your system into specialized agents provides:

- 🎯 **Separation of Concerns** - Each agent has a clear, bounded responsibility
- 📝 **Focused Prompts** - Shorter, more precise instructions lead to better outputs
- 🧪 **Independent Testing** - Test each agent in isolation
- 📈 **Selective Scaling** - Route simple queries to cheaper/faster models
- 🔍 **Easier Debugging** - Trace issues to specific agents in the pipeline

---

## 🔄 The Three-Stage Pipeline

All Clear uses a three-stage pipeline on the Microsoft Agent Framework. Each
stage has **bounded authority** (Constitution Art. II) — it can do only what its
role permits, enforced by code structure, not prompt hope:

```
        signal in                                          response out
            │                                                    ▲
            ▼                                                    │
   ┌─────────────────┐    ┌──────────────────┐    ┌────────────────────────┐
   │   QueryAgent     │──▶ │  RouterExecutor   │──▶ │      ActionAgent        │
   │  (MAF agent)     │    │ (deterministic,   │    │   (MAF agent, 3 tools)  │
   │  classify ONLY   │    │  ZERO LLM calls)  │    │   create_incident       │
   │                  │    │  dedup → severity  │    │   search_knowledge      │
   │ SignalClassif.   │    │  → SLA → escalate  │    │   generate_sitrep       │
   └─────────────────┘    └──────────────────┘    └────────────────────────┘
```

> 💡 The reference implementation is real and shipped:
> [`backend/app/agents/query_agent.py`](../../backend/app/agents/query_agent.py),
> [`router_agent.py`](../../backend/app/agents/router_agent.py),
> [`action_agent.py`](../../backend/app/agents/action_agent.py), wired in
> [`pipeline.py`](../../backend/app/agents/pipeline.py).

### 👥 Stage Responsibilities

#### 🔍 QueryAgent - The Classifier

**Purpose:** Turn one raw **signal** into a structured, typed `SignalClassification`.

**Responsibilities:**
- 📝 Parse the natural-language signal
- 🏷️ Extract entities (`location`, `system`, `severity_indicators`)
- 🚩 Detect PII and flag it (never echo it back — Constitution Art. I)
- 🎯 Identify `intent` and `intent_category` (a `SignalCategory`)
- 📊 Emit a confidence score

**Authority:** *classify only.* It cannot route, create, search, or act.

| 📥 Input | 📤 Output |
|----------|----------|
| Raw signal text + channel | `SignalClassification` (intent, category, entities, PII flags, confidence) |

#### 🚦 RouterExecutor - The Decider

**Purpose:** Decide what happens to the classified signal — **deterministically**.

**Responsibilities:**
- 🔁 **Dedup:** embedding-similarity match against open incidents in the same `intent_category`. ≥ `DEDUP_THRESHOLD` (default 0.83 cosine) → `ATTACH_TO_INCIDENT`; below → `OPEN_INCIDENT`
- 🚦 Map severity indicators to **SEV1–SEV4** and the matching **SLA** (15 min → next business day)
- 🆙 Apply **escalation rules** (safety control): SEV1 and statutory-clock incidents *always* escalate
- 📋 Record which `routing_rules_applied`

**Authority:** *decide only.* It makes **zero LLM calls**, holds no tools, and
touches no records. Severity is set by rules, never by model vibes — so a caller
(or attacker) cannot talk the system into a lower severity.

| 📥 Input | 📤 Output |
|----------|----------|
| `SignalClassification` | `RoutingDecision` (outcome, target_queue, severity, sla_minutes, escalate) |

#### ⚡ ActionAgent - The Doer

**Purpose:** Act on the decision through exactly three tools, and respond.

**The three tools (and nothing else):**
- 🆕 **create_incident** — opens a new incident (`AC-####`) on the `OPEN_INCIDENT` path
- 📚 **search_knowledge** — RAG over incident runbooks/SOPs (Lab 04), returns `KnowledgeArticle`s
- 📝 **generate_sitrep** — a **citation-grounded** situation report; every claim cites a source record

**Authority:** *only what its tools permit.* It cannot approve waivers, modify
records outside its tools, or suppress escalation. On the `ATTACH_TO_INCIDENT`
path it skips knowledge search (keeps surge latency flat) and just acknowledges.

| 📥 Input | 📤 Output |
|----------|----------|
| `RoutingDecision` | `IncidentAction` (incident, sitrep, citations, user_message) |

---

## 🛡️ Bounded Authority — the decision matrix

Clear boundaries between stages are not a style choice; they are a security
control. Here is who is allowed to do what:

| 📋 Concern | 🔍 QueryAgent | 🚦 RouterExecutor | ⚡ ActionAgent |
|---------|------------|-------------|-------------|
| Parse/understand the signal | ✅ Yes | ❌ No | ❌ No |
| Classify intent & severity *indicators* | ✅ Yes | ❌ No | ❌ No |
| Decide severity / SLA / dedup outcome | ❌ No | ✅ Yes | ❌ No |
| Apply escalation rules | ❌ No | ✅ Yes | ❌ No |
| Make LLM calls | ✅ Yes | 🚫 **Never** | ✅ Yes |
| Create/mutate incident records | ❌ No | ❌ No | ✅ Yes (via tools) |
| Generate the final response/sitrep | ❌ No | ❌ No | ✅ Yes |

### 🚫 Anti-Patterns to Avoid

1. ❌ **RouterExecutor calling the model** — routing must stay deterministic and auditable; zero LLM calls is enforced by test
2. ❌ **ActionAgent re-deciding severity or skipping escalation** — trust the RoutingDecision; weakening escalation is a security blocker
3. ❌ **QueryAgent creating incidents or searching** — it only classifies
4. ❌ **Echoing detected PII** back into responses, logs, or sitreps

---

## 📝 Exercises

Complete the following hands-on exercises to reinforce your understanding:

### 📚 Exercise 1a: Signal Classification
**File:** [exercises/01a-intent-classification.md](exercises/01a-intent-classification.md)

Build the QueryAgent classifier that turns a raw signal into a typed
`SignalClassification`. You will:
- 🏷️ Use the All Clear `SignalCategory` taxonomy (INFRASTRUCTURE_OUTAGE, FIELD_HAZARD, PUBLIC_SAFETY, CUSTOMER_INQUIRY, SERVICE_REQUEST, COMPLIANCE_REPORT, …)
- 📝 Create example signals for each category (downed line, gas leak, "when will power return?", recall report)
- 💻 Implement classification + entity extraction (`location`, `system`, `severity_indicators`)
- 🧪 Test against edge cases (ambiguous, multi-hazard, PII-bearing signals)

### ✏️ Exercise 1b: Prompt Engineering
**File:** [exercises/01b-prompt-engineering.md](exercises/01b-prompt-engineering.md)

Craft effective prompts for the LLM-backed stages. You will:
- 🔍 Write the QueryAgent classification prompt (structured output, no free-text parsing)
- ⚡ Write the ActionAgent sitrep prompt (every claim must cite a source record)
- 🚫 Confirm the RouterExecutor needs **no** prompt — it is deterministic code
- 🔄 Test prompt variations against the signal set

---

## ✅ Deliverables

By the end of this lab, you should have:

| 📋 Deliverable | ✅ Success Criteria |
|-------------|------------------|
| 🎯 Signal Classifier | >90% accuracy on test signals |
| 📝 Agent Prompts | Working QueryAgent and ActionAgent prompts (RouterExecutor needs none) |
| 🏗️ Architecture Diagram | Your own version showing the bounded-authority data flow |
| 🧪 Test Suite | At least 20 test signals with expected `SignalCategory` |

---

## 🔧 Troubleshooting Tips

### ⚠️ Common Issues

**Issue:** Intent classifier accuracy below 90%
- ✅ **Solution:** Review misclassified examples and add them to training data
- ✅ **Solution:** Check for overlapping intent definitions - make categories more distinct
- ✅ **Solution:** Add more diverse examples per intent (aim for 10+ each)

**Issue:** RouterExecutor producing the wrong severity or queue
- ✅ **Solution:** Verify QueryAgent is extracting the right `severity_indicators` and `intent_category`
- ✅ **Solution:** Review the deterministic routing rules for gaps or conflicts
- ✅ **Solution:** Add explicit handling for statutory-clock / SEV1-forcing phrases

**Issue:** Prompts generating inconsistent outputs
- ✅ **Solution:** Add output format examples to your prompts
- ✅ **Solution:** Use structured output (JSON) where possible
- ✅ **Solution:** Lower temperature for more deterministic results

**Issue:** Context getting lost between agents
- ✅ **Solution:** Ensure conversation history is passed through pipeline
- ✅ **Solution:** Check that entity extraction preserves all relevant data
- ✅ **Solution:** Add logging to trace data flow between agents

### 📋 Debugging Checklist

1. [ ] ✅ Verify Lab 00 setup is complete and working
2. [ ] 🔑 Check that all API keys/endpoints are configured
3. [ ] 📝 Enable verbose logging for each agent
4. [ ] 🧪 Test each agent in isolation before testing the pipeline
5. [ ] 🔍 Compare actual vs expected outputs at each stage
6. [ ] ⚠️ Review Azure OpenAI rate limits if seeing throttling

### 🆘 Getting Help

- 📖 Review the architecture diagram above
- 📄 Check the exercise files for hints
- 📚 Consult the main accelerator documentation
- 👋 Reach out to your instructor or lab assistant

---

## 🧠 Check Your Understanding

Before proceeding to Lab 02, verify you can answer these questions:

### 📝 Concept Check

| ❓ Question | 📝 Your Answer |
|----------|-------------|
| Why is a multi-agent architecture better than a monolithic agent for complex systems? | _[Write your answer]_ |
| What is the primary responsibility of the QueryAgent? | _[Write your answer]_ |
| Why does the RouterExecutor make zero LLM calls, and when must it escalate to a human queue? | _[Write your answer]_ |
| What is the difference between the `OPEN_INCIDENT` and `ATTACH_TO_INCIDENT` paths? | _[Write your answer]_ |

### ✅ Self-Assessment Checklist

Complete this checklist to confirm you're ready for Lab 02:

- [ ] 🗣️ I can explain the three-stage pipeline and bounded authority to someone new
- [ ] 🎯 My signal classifier achieves >90% accuracy on test signals
- [ ] ✏️ I have written prompts for QueryAgent and ActionAgent (and know why RouterExecutor needs none)
- [ ] 🔄 I understand why the RouterExecutor makes zero LLM calls
- [ ] 🎨 I can draw an architecture diagram showing the bounded-authority data flow
- [ ] 🧪 I have at least 20 test signals with expected `SignalCategory`

### 🧪 Quick Quiz

Test yourself with these scenarios:

1. **Scenario:** A signal reads "transformer fire on Oak Ave and people are trapped, call my cell 555-0123"
   - 🔍 Which stage extracts the `location`, the `severity_indicators`, and flags the phone number as PII?
   - 🚦 Why must this never be downgraded below SEV1?

2. **Scenario:** The QueryAgent classifies a signal but with only 60% confidence
   - ❓ What does the RouterExecutor do with a low-confidence classification?
   - 📊 Which `EscalationReason` applies?

3. **Scenario:** The 38th caller reports the same downed line already tracked as `AC-0007`
   - 🔄 Does the pipeline open a new incident?
   - ✅ What is the correct dedup outcome, and what happens to the incident's magnitude?

**Answers:** Discuss with your coach or see the
[Coach's Runbook](../../coach-runbook/index.html) for guidance.

---

## ➡️ Next Steps

Once you have completed this lab and achieved >90% accuracy on your intent classifier, proceed to:

**[Lab 02 - Azure MCP Setup](../02-azure-mcp-setup/README.md)** ☁️

In the next lab, you will configure Azure OpenAI and Azure AI Search services to power your agents.

---

## 📊 Version Matrix

| Component | Required Version | Tested Version |
|-----------|-----------------|----------------|
| 🐍 Python | 3.11+ | 3.12.10 |
| 🤖 Azure OpenAI | GPT-5.1 | 2025-01-01-preview |
| 🔧 Pydantic | 2.5+ | 2.6.1 |
| 📝 Prompt Engineering | N/A | Best practices |

---

<div align="center">

[← Lab 00](../00-setup/README.md) | **Lab 01** | [Lab 02 →](../02-azure-mcp-setup/README.md)

📅 Last Updated: 2026-02-04 | 📝 Version: 1.0.0

</div>
