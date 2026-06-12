# Challenge C — "The Gas Leak"

A field crew radios in: *"Strong smell of natural gas at the corner of 5th and
Oak. We've pulled back and taped off the block. Need a utility shutoff and a
hazmat callout."*

**Build:** a pipeline that treats this as an active field hazard, opens a new
incident, routes it to field-operations, and escalates for the hazmat/utility
callout. The agent must **never** mark the hazard resolved on its own — that is a
human decision (bounded authority).

---

- **Primary category:** `FIELD_HAZARD`
- **Skill:** Field dispatch + escalation with bounded authority.
- **Done when:**
  - QueryAgent classifies the signal as `FIELD_HAZARD`
  - RouterExecutor returns `OPEN_INCIDENT`, `severity ≥ SEV2`, target queue `field-operations`, `escalate = True`
  - ActionAgent calls `create_incident` and `generate_sitrep` — it does **not** auto-close or auto-resolve
  - The sitrep cites the inbound report and any matched runbook (no uncited claims)
