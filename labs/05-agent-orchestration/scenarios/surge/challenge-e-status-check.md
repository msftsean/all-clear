# Challenge E — "The Status Check"

A stakeholder asks: *"What's the latest on the Elm Street outage? Any ETA on
restoration?"*

**Build:** a pipeline that recognizes this is a **question about an existing
incident**, not a new event. It must produce a read-only, citation-grounded sitrep
from the incident record — and must **not** open a new incident.

---

- **Primary category:** `STATUS_CHECK`
- **Skill:** Read-only sitrep generation without mutating state.
- **Done when:**
  - QueryAgent classifies the signal as `STATUS_CHECK`
  - RouterExecutor does **not** return `OPEN_INCIDENT` for a status question (no new `AC-####`)
  - ActionAgent calls `generate_sitrep` / `search_knowledge` only — never `create_incident`
  - Every claim in the response is backed by a citation to the incident record or KB (Art. IV — no citation, no claim)
