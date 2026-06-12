# Challenge F — "The Human Request"

A caller insists: *"I don't want a bot. Get me a human supervisor right now. This
is urgent and I need someone who can actually make a decision."*

**Build:** a pipeline that respects bounded authority. The agent recognizes an
explicit human-handoff request, routes to the escalations queue, and hands off to
a person — it does **not** try to satisfy the request itself or invent authority it
doesn't have.

---

- **Primary category:** `HUMAN_REQUEST`
- **Skill:** Bounded authority — escalate to a human, don't overreach.
- **Done when:**
  - QueryAgent classifies the signal as `HUMAN_REQUEST`
  - RouterExecutor routes to the `escalations` queue with `escalate = True`
  - ActionAgent does **not** fabricate a resolution or take an action outside its three tools (Constitution Art. II)
  - The response clearly states a human is being brought in — no false promises
