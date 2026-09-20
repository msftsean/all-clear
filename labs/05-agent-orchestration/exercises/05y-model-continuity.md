# Exercise 05y: Model Continuity Under Failover

**Duration:** 20–30 minutes  
**Objective:** Prove that a model deployment outage changes transport, not the
incident-triage contract.

All Clear may have a primary model and one or more fallback deployments. The
fallback client must preserve typed classification, severity, SLA, escalation,
and the bounded QueryAgent → RouterExecutor → ActionAgent flow. It must not
fail over around rate limits or content-filter blocks.

## Run the executable verifier

From the repository root:

```bash
PYTHONPATH=backend python labs/05-agent-orchestration/exercises/verify_model_continuity.py
```

The verifier uses offline fakes and checks that:

1. A deployment-not-found error advances to the fallback.
2. A healthy primary is used without touching the fallback.
3. Structured `SignalClassification` survives the fallback.
4. A life-safety signal remains SEV1 and escalated on the fallback.
5. HTTP 429 and content-filter errors do **not** trigger failover.
6. A single-client configuration remains an unwrapped no-op.

## Connect the result to the owned tests

Run the focused contract suite as well:

```bash
cd backend
PYTHONPATH=. python -m pytest tests/test_failover -q
```

The tests in `backend/tests/test_failover/` are the source of truth for the
production contract. Do not weaken them or change routing severity to make a
fallback appear successful. A passing exercise means the active model can
change while the decision and safety invariants remain stable.

## Reflection

Why is a content-filter block different from a missing deployment? Which
properties should be reported to operations so a dashboard can distinguish
"served by fallback" from "request correctly blocked"?
