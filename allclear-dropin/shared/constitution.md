# All Clear Constitution

Non-negotiable principles. These outrank convenience, deadlines, and demo polish. Amendments require a decisions.md entry approved by the Lead.

## Article I: Data Discipline (CJIS mindset, everywhere)

1. PII detected in a signal is flagged, never echoed back in responses, logs, or sitreps.
2. Least privilege: agents and services hold only the access their bounded authority requires.
3. Every action that creates or mutates a record is audit-logged with actor, timestamp, and cause.
4. Signal text sent to embeddings is a data flow: what is vectorized, where vectors live, and retention are documented and reviewed by Security.

## Article II: Bounded Authority

1. QueryAgent classifies. It cannot route, create, search, or act.
2. RouterExecutor decides. It makes zero LLM calls, holds no tools, and touches no records.
3. ActionAgent acts only through its three tools. No tool may approve waivers, modify records outside its scope, or suppress escalation.
4. New agents or tools require a one-sentence justification in decisions.md and a Security review before merge.

## Article III: Escalation Is a Safety Control

1. Escalation rules route humans to humans. Code that weakens, bypasses, or deprioritizes escalation is a blocker, never a finding.
2. SEV1 and statutory-clock incidents always escalate. No model output can downgrade them.

## Article IV: Truth Over Fluency

1. Sitreps and responses cite source records for every factual claim. No citation, no claim.
2. Classification uses structured output with typed schemas, never free-text parsing.
3. When the system does not know, it says so and escalates. Confident invention is a defect.

## Article V: Build Discipline

1. Mock twins exist for every live service and stay in lockstep. The full pipeline runs offline.
2. The Loop Protocol (specs/001-maf-rehost/plan.md) governs all build work: verifiers first, makers never grade their own work, every task ends at its verification command.
3. Dependencies are pinned. requirements-lock.txt is frozen after the dress rehearsal; no upgrades after freeze.
4. Every signal is preserved. Dedup attaches; it never deletes.
