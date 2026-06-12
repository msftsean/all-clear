# Challenge B — "The Aid Cliff"

A junior asks: *"My mom lost her job last month. Can I get more aid? Also
I'm thinking of dropping a class — does that hurt my package?"*

**Build:** an agent that detects the financial_aid + registrar overlap,
routes correctly, and creates a high-priority appeals ticket with the
student's narrative attached.

---

- **Primary intent:** `financial_aid` (overlap: `registrar`)
- **Skill:** Multi-intent overlap + autonomous high-priority ticket.
- **Done when:**
  - Detects both intents and routes primarily to Financial Aid (the aid implication is the blocker)
  - Creates a high-priority appeals ticket carrying the student's narrative
  - Acknowledges the registrar/drop question
