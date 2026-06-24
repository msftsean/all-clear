# 📝 Lab 03 - Spec-Driven Development

| 📋 Attribute | Value |
|-------------|-------|
| ⏱️ **Duration** | 45 minutes |
| 📊 **Difficulty** | ⭐⭐ Intermediate |
| 🎯 **Prerequisites** | Lab 01 completed |

---

## 📈 Progress Tracker

```
Lab Progress: [░░░░░░░░░░] 0% - Not Started

Checkpoints:
□ Step 1: Read the All Clear source-of-truth docs
□ Step 2: Run the repo's Spec Kit workflow
□ Step 3: Generate tasks and implementation guidance
□ Produce a capability spec grounded in CONTEXT.md
□ Check requirements against shared/constitution.md
```

---

## 🌟 Overview

Spec-driven development is a methodology where you write detailed specifications *before* writing code. In this repo, we use the GitHub Spec Kit workflow through Copilot Chat commands that live under `.github/prompts/` and `.github/agents/`.

In this lab, you will use `/speckit.constitution`, `/speckit.specify`, `/speckit.plan`, and `/speckit.tasks` to produce artifacts that stay aligned to All Clear's incident-triage domain: signals → dedup → incidents → severity/SLA → sitrep.

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. 📋 **Create a Spec Kit feature spec** for an All Clear capability with requirements, constraints, and success criteria
2. 🛡️ **Apply the All Clear constitution** from [`../../shared/constitution.md`](../../shared/constitution.md)
3. 🧭 **Ground every term** in [`../../CONTEXT.md`](../../CONTEXT.md), especially Signal, Incident, Queue, Sitrep, `QueryAgent`, `RouterExecutor`, and `ActionAgent`
4. 💻 **Generate a plan and tasks** with the repo's Spec Kit commands before asking Copilot to implement

## 📋 Prerequisites

- ✅ Lab 01 completed (Development Environment Setup)
- 🤖 GitHub Copilot extension installed and authenticated
- 📝 Basic understanding of markdown formatting

## 🤔 What is Spec-Driven Development?

Spec-driven development inverts the traditional "code first, document later" approach. Instead, you:

1. 🎯 **Define the problem** using All Clear language from `CONTEXT.md`
2. 📋 **Specify behavior** with clear user stories and acceptance criteria
3. 🛡️ **Check the constitution** so bounded authority, escalation, and truth-over-fluency are preserved
4. 🧭 **Plan implementation** with Spec Kit design artifacts
5. ✅ **Generate tasks** that can be verified independently

### 🌟 Benefits for AI-Assisted Development

- 🚫 **Reduced hallucination** - Clear specs constrain AI output to your requirements
- ⚡ **Faster iteration** - Less back-and-forth when AI understands intent upfront
- 📊 **Verifiable output** - Success criteria provide objective measures
- 👥 **Team alignment** - Specs serve as documentation and contracts

## 📚 Lab Structure

This lab contains two exercises:

| 📋 Exercise | 📝 Title | ⏱️ Duration | 📖 Description |
|----------|-------|----------|-------------|
| 03a | Write a Spec Kit Spec | 25 min | Create a specification for an All Clear escalation or SLA capability |
| 03b | Plan and Task from Spec | 20 min | Use Spec Kit commands to produce plan/tasks before implementation |

## 📝 Step-by-Step Instructions

### 🔹 Step 1: Read the All Clear source-of-truth docs (5 minutes)

Open these files in VS Code so Copilot can use them as context:

- [`../../CONTEXT.md`](../../CONTEXT.md) — canonical domain language for signals, incidents, queues, severity/SLA, and sitreps
- [`../../shared/constitution.md`](../../shared/constitution.md) — non-negotiable All Clear engineering principles
- `.github/prompts/speckit.*.prompt.md` and `.github/agents/speckit.*.agent.md` — the available Spec Kit commands/agents

> Note: `.specify/memory/constitution.md` is a legacy template artifact. For this repo's All Clear work, use `shared/constitution.md` as the participant-facing constitution.

### 🔹 Step 2: Run the Spec Kit workflow (Exercise 03a - 25 minutes)

In Copilot Chat, run the repo commands in this order:

```text
/speckit.constitution
/speckit.specify Add a statutory-clock detector for inbound incident signals. It must classify regulated reporting deadlines, force SEV1 where CONTEXT.md says statutory clocks are SEV1-forcing, preserve every signal, and never let model output downgrade escalation.
```

Use the prompts to ensure your spec:

1. Uses **Signal**, **Incident**, **Queue**, **Severity**, **SLA clock**, and **Sitrep** exactly as defined in `CONTEXT.md`
2. Keeps `QueryAgent` classify-only, `RouterExecutor` deterministic and zero-LLM, and `ActionAgent` bounded to approved tools
3. Treats escalation as a safety control and statutory-clock incidents as SEV1
4. Includes concrete acceptance criteria and non-goals

### 🔹 Step 3: Generate plan and tasks (Exercise 03b - 20 minutes)

After `/speckit.specify` finishes, continue in Copilot Chat:

```text
/speckit.plan
/speckit.tasks
```

Review the generated artifacts before implementation:

1. 📄 Confirm the plan references `CONTEXT.md` and `shared/constitution.md`
2. 🧪 Confirm tasks include verifiers before implementation work
3. ✅ Confirm no task asks `QueryAgent` to route or write records
4. 🔄 If the artifacts drift into student-support terms or generic "department" language, rerun `/speckit.specify` with corrected All Clear wording

## ✅ Deliverables

By the end of this lab, you will have created:

### 1. 📋 Spec Kit feature spec
   - ✅ Complete feature specification generated from `/speckit.specify`
   - 👤 User stories covering reporter, operator, compliance, and system perspectives
   - 📋 Functional requirements written in All Clear terminology
   - 📊 Measurable success criteria

### 2. 🧭 Plan and tasks
   - 📜 Plan generated by `/speckit.plan`
   - 🧪 Verification-first tasks generated by `/speckit.tasks`
   - 🚧 Clear agent boundaries aligned to `QueryAgent` → `RouterExecutor` → `ActionAgent`
   - 🔐 CJIS-mindset privacy, audit, and no-PII-echo considerations

## 🏗️ Key Concepts

### 📊 The Specification Hierarchy

```
🏛️ Constitution (organization-wide principles)
    |
    v
📋 Feature Spec (specific All Clear requirements)
    |
    v
🧭 Plan + Tasks (then implementation)
```

### 💡 Effective Spec Writing Tips

1. 🎯 **Be specific** - Vague specs produce vague code
2. 📝 **Include examples** - Show expected inputs and outputs
3. ⚠️ **Define edge cases** - What happens in unusual situations?
4. 🚫 **Set constraints** - What must the solution NOT do?
5. 📊 **Make success measurable** - How do you know it works?

## 🔧 Troubleshooting

### ❌ Spec Kit output doesn't match All Clear terminology

- 📄 Open `CONTEXT.md` and `shared/constitution.md` in editor tabs
- 💬 Rerun `/speckit.specify` with explicit corrections such as "use Queue, not department"
- ✂️ Keep the feature focused on one incident-triage capability
- 📝 Add acceptance criteria that mention Signal, Incident, Severity/SLA, and Sitrep where relevant

### ❌ My spec is too vague

- 📝 Add concrete examples with expected inputs/outputs
- ⚠️ Include error scenarios and edge cases
- 🔗 Reference existing similar features for consistency
- 👀 Have a teammate review for clarity

### ❌ Constitution principles conflict with requirements

- ⚖️ Prioritize principles (which takes precedence?)
- 📋 Add explicit exception handling in the spec
- 📝 Document the conflict resolution approach
- 🔄 Consider if the feature needs redesign

### ❌ Generated code is too complex

- ✂️ Simplify your spec to essential requirements only
- 🎯 Remove "nice to have" features for initial generation
- 📈 Generate incrementally (core first, then enhancements)
- 🔍 Use Copilot's explain feature to understand the output

## 📚 Additional Resources

- 📖 [Specification by Example](https://en.wikipedia.org/wiki/Specification_by_example) - Background on spec-driven approaches
- 🤖 [GitHub Copilot Documentation](https://docs.github.com/en/copilot) - Official Copilot guides
- 🧭 [`../../CONTEXT.md`](../../CONTEXT.md) - All Clear domain language
- 🛡️ [`../../shared/constitution.md`](../../shared/constitution.md) - All Clear constitution: bounded authority, escalation safety, truth over fluency

## ➡️ Next Steps

After completing this lab, proceed to:

**[Lab 04 - Build RAG Pipeline](../04-build-rag-pipeline/README.md)** 🔍

In Lab 04, you'll build production-ready AI agents with your specs.

---

## 🚀 Ready to Begin?

Start with **[Exercise 03a: Write a Spec](exercises/03a-write-spec.md)** 📝

---

## 📊 Version Matrix

| Component | Required Version | Tested Version |
|-----------|-----------------|----------------|
| 🤖 GitHub Copilot | Latest | 1.x |
| 🖥️ VS Code | 1.96+ | 1.99+ |
| 📝 Markdown | CommonMark | 0.30 |

---

<div align="center">

[← Lab 02](../02-azure-mcp-setup/README.md) | **Lab 03** | [Lab 04 →](../04-build-rag-pipeline/README.md)

📅 Last Updated: 2026-06-12 | 📝 Version: 1.1.0

</div>
