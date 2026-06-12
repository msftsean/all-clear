# Challenge B — "The Storm Surge"

A wind storm rolls through. Within ten minutes the briefing room fills with
reports: *"Power's out on Elm Street,"* *"No electricity near Elm and 3rd,"*
*"Lights just went out by the Elm St substation,"* *"Outage on Elm — third one
I've reported."*

**Build:** a pipeline that recognizes these are the **same real-world event** and
attaches the later reports to the first incident instead of opening five separate
ones. Each attached report increments the incident's **Magnitude**.

---

- **Primary category:** `INFRASTRUCTURE_OUTAGE`
- **Skill:** Semantic dedup — many Signals → one Incident.
- **Done when:**
  - The first Elm St report yields `OPEN_INCIDENT` (a fresh `AC-####`)
  - Subsequent near-duplicate reports yield `ATTACH_TO_INCIDENT` (cosine ≥ `DEDUP_THRESHOLD` = 0.83)
  - The incident's Magnitude climbs with each attached report — no duplicate incidents
  - Run `smoke_test.py`: the 25-signal surge replay collapses to **≤ 6 open incidents, ≥ 19 attachments**
