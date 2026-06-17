# Challenge C — "The Discernment"

**Difficulty:** ⭐ (simplest routing, subtle ticket logic)
**Primary intent:** `campus_ministry`
**Key build challenge:** Offer a connection — do NOT auto-create a ticket

---

## The Message

> *"I'm thinking about doing a year of service after graduation. I don't
> know if I should apply to JVC or take the consulting job. Can someone
> help me think through this?"*

---

## What Your Agent Must Do

1. **Classify** as `campus_ministry` (discernment signal: vocation, life direction, "help me think through")
2. **Surface** KB articles: "Discernment groups for students considering religious or service vocations" + "Service & immersion programs and how to apply"
3. **Offer** to connect the student with a chaplain — do NOT auto-create a ticket
4. **Respond** warmly, Jesuit-context aware (JVC = Jesuit Volunteer Corps)

**AJCU escalation rule in play:**
> *campus_ministry: `human_touch_keywords` = ["discernment", "vocation", ...], always_create_ticket = **False** — offer, don't auto-create*

---

## Expected Pipeline Output

```json
{
  "classification": {
    "intent": "campus_ministry",
    "confidence": "> 0.85"
  },
  "routing": {
    "target_queue": "campus_ministry",
    "escalate": false
  },
  "action": {
    "status": "opened",
    "knowledge_articles": ["Discernment groups...", "Service & immersion programs..."],
    "user_message": "offers chaplain 1:1 — does NOT say 'ticket created'"
  }
}
```

---

## Smoke Test

```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-student-token" \
  -d '{"message": "I'\''m thinking about doing a year of service after graduation. I don'\''t know if I should apply to JVC or take the consulting job. Can someone help me think through this?"}'
```

**Pass criteria:**
- `classification.intent` = `campus_ministry`
- `routing.escalate` = `false`
- `action.knowledge_articles` includes discernment article

---

## Build Hints

- Key test: `always_create_ticket = False` in `escalation_rules.py` for `campus_ministry`
- JVC (Jesuit Volunteer Corps) should be recognized in the discernment keyword set
- Response should feel warm and invitational, not transactional
