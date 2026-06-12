# Multi-Agent Design

## Goal

Design an All Clear incident-triage workflow that classifies inbound signals, makes deterministic routing decisions, and executes the allowed action with traceable outputs.

## Components

1. QueryAgent

- Input: one raw signal and channel context.
- Output: `SignalClassification` with intent, `SignalCategory`, confidence, entities, severity indicators, and PII flags.
- Responsibility: classify only.
- Boundary: cannot route, deduplicate, open incidents, attach reports, search knowledge, or generate a sitrep.

2. RouterExecutor

- Input: structured output from QueryAgent.
- Output: `RoutingDecision` with dedup outcome, target queue, severity, SLA minutes, escalation flag, and rules applied.
- Responsibility: deterministic decision policy and branching.
- Boundary: zero LLM calls, no tools, and no record mutation.

3. ActionAgent

- Tools: `create_incident`, `search_knowledge`, and `generate_sitrep`.
- Input: `RoutingDecision` plus preserved signal/classification context.
- Output: `IncidentAction` with incident id, sitrep, citations, and user message.
- Responsibility: execute only what its three tools permit.
- Boundary: cannot re-decide severity, weaken escalation, approve waivers, or modify records outside its tools.

4. Pipeline / Orchestrator

- Maintains session state and channel metadata.
- Executes QueryAgent -> RouterExecutor -> ActionAgent in order.
- Preserves every signal and attaches duplicate signals as reports.
- Emits logs and metrics for audit, latency, and failure analysis.

## Data Flow Diagram

```text
Inbound Signal
   |
   v
+------------------+
| QueryAgent       |
| classify ONLY    |
| SignalClassif.   |
+------------------+
   |
   v
+----------------------------+
| RouterExecutor             |
| deterministic, ZERO LLM    |
| dedup -> severity -> SLA   |
| -> escalation              |
+----------------------------+
   |
   +-------------------------------+
   |                               |
   v                               v
ATTACH_TO_INCIDENT            OPEN_INCIDENT
(existing AC-####)            (new AC-####)
   |                               |
   | report added, magnitude++      | create_incident
   | no knowledge search            | search_knowledge
   |                               | generate_sitrep
   +---------------+---------------+
                   |
                   v
             Reporter Response
```

## Design Notes

- A signal is what arrives; an incident is what is happening; a report is the attachment of a signal to an incident.
- Dedup compares the inbound signal to open incidents in the same `intent_category`. At or above the 0.83 cosine threshold, RouterExecutor chooses `ATTACH_TO_INCIDENT`; below it chooses `OPEN_INCIDENT`.
- RouterExecutor maps severity as `SEV1` through `SEV4` from severity indicators. SEV1 covers life safety, total outage, and statutory clocks with a 15-minute response SLA.
- Queue names are `field-operations`, `customer-comms`, `compliance-desk`, `engineering`, and `escalations`.
- Escalation is a safety control. Code that weakens SEV1, statutory-clock, PII, or low-confidence escalation is a security blocker.
- The ActionAgent skips knowledge search on the attach path to keep surge latency flat.

## Why this helps

This design reduces regression risk, improves explainability, and lets teams test each stage independently. QueryAgent can be evaluated on classification accuracy, RouterExecutor on deterministic rules, and ActionAgent on tool use and citation-grounded sitreps. The bounded-authority split is especially important during a surge, when dozens of duplicate reports should merge into one `AC-####` incident without letting an LLM decide severity or suppress escalation.
