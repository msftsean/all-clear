# Challenge D — "The Phishing Storm"

**Difficulty:** ⭐⭐⭐ (two-ticket workflow)
**Primary intent:** `it`
**Key build challenge:** One message → two tickets (IT support + security incident)

---

## The Message

> *"My password isn't working and I just got an email saying my account
> is locked. I clicked the link."*

---

## What Your Agent Must Do

1. **Classify** as `it` (account/password issue)
2. **Detect** the security signal: "I clicked the link" → phishing compromise
3. **Create ticket 1** — IT support: password reset / account unlock
4. **Create ticket 2** — Security team: potential phishing compromise, account may be affected
5. **Respond** urgently: tell the student NOT to click anything else, change password immediately, confirm both tickets

**Security incident trigger:** `escalation_rules.py` `SECURITY_INCIDENT_KEYWORDS` — "clicked the link" / "clicked a link"

---

## Expected Pipeline Output

```json
{
  "classification": {
    "intent": "it",
    "confidence": "> 0.85"
  },
  "routing": {
    "target_queue": "it",
    "escalate": true,
    "escalation_reason": "security_incident"
  },
  "action": {
    "status": "escalated",
    "user_message": "urgent security language — change password, do not click, both tickets confirmed"
  }
}
```

---

## Smoke Test

```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-student-token" \
  -d '{"message": "My password isn'\''t working and I just got an email saying my account is locked. I clicked the link."}'
```

**Pass criteria:**
- `classification.intent` = `it`
- `routing.escalate` = `true`
- Response contains urgent security language

---

## Build Hints

- See `SECURITY_INCIDENT_KEYWORDS` in `backend/app/agents/escalation_rules.py`
- The two-ticket pattern is defined there with `SECURITY_INCIDENT_SECOND_QUEUE`
- See KB article: "Reporting a phishing email" + "Resetting your university password and enrolling in MFA"
