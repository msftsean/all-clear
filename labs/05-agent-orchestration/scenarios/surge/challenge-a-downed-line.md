# Challenge A — "The Downed Line"

A 911 dispatch relay comes in: *"Power line down across Main St near the
elementary school, sparking on the wet road. Cars are stopping in the
intersection. Someone could get hurt."*

**Build:** a pipeline run that classifies this as a life-safety signal, opens a
new incident (no matching prior incident exists), assigns SEV1, routes to
field-operations, and **always escalates**. The decision is deterministic — the
RouterExecutor makes it with zero LLM calls.

---

- **Primary category:** `PUBLIC_SAFETY`
- **Skill:** SEV1 life-safety routing with mandatory escalation.
- **Done when:**
  - QueryAgent classifies the signal as `PUBLIC_SAFETY` with a life-safety risk flag
  - RouterExecutor returns `OPEN_INCIDENT` with `severity = SEV1` and a 15-minute SLA
  - `escalate = True` (SEV1 always escalates — Constitution Art. III)
  - ActionAgent calls `create_incident` and routes to the `field-operations` queue
