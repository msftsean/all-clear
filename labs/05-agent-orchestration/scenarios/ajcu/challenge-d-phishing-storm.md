# Challenge D — "The Phishing Storm"

A staff-shared message: *"My password isn't working and I just got an
email saying my account is locked. I clicked the link."*

**Build:** an agent that handles the IT routing AND triggers a
security-incident workflow because of the click. Two tickets, one to IT
support, one to the security team.

---

- **Primary intent:** `it` (second action: security incident)
- **Skill:** One message → two parallel actions (dual ticket).
- **Pill:** LIVE DEMO — the canonical "one message, two outcomes."
- **Done when:**
  - Routes to IT and offers a self-serve password reset
  - Detects the "I clicked the link" signal and fires a security-incident workflow
  - Produces two tickets from one message — IT support + security team
