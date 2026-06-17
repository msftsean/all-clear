# Challenge B — "The Aid Cliff"

**Difficulty:** ⭐⭐ (intent overlap)
**Primary intent:** `financial_aid` (with `registrar` secondary)
**Key build challenge:** Detect overlap, route correctly, create high-priority appeals ticket

---

## The Message

> *"My mom lost her job last month. Can I get more aid? Also I'm thinking
> of dropping a class — does that hurt my package?"*

---

## What Your Agent Must Do

1. **Classify** as `financial_aid` (the aid implication is the blocker; the drop question is downstream)
2. **Create a high-priority ticket** — `financial_aid.human_touch_keywords` triggers on "lost her job"
3. **Attach** the student's narrative to the ticket (special-circumstances appeal context)
4. **Respond** with both: aid recalculation info AND drop/aid impact info
5. **Surface** KB articles: "Appealing your financial aid award" + "How federal aid is recalculated when you drop below full-time status"

**AJCU escalation rule in play:**
> *financial_aid: `human_touch_keywords` = ["parent lost their job", ...], priority = "high", always_create_ticket = True*

---

## Expected Pipeline Output

```json
{
  "classification": {
    "intent": "financial_aid",
    "confidence": "> 0.80"
  },
  "routing": {
    "target_queue": "financial_aid",
    "severity": "SEV2 or SEV3",
    "escalate": true,
    "escalation_reason": "hardship_keyword"
  },
  "action": {
    "status": "escalated",
    "knowledge_articles": ["Appealing your financial aid award", "How federal aid is recalculated..."]
  }
}
```

---

## Smoke Test

```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-student-token" \
  -d '{"message": "My mom lost her job last month. Can I get more aid? Also I'\''m thinking of dropping a class — does that hurt my package?"}'
```

**Pass criteria:**
- `classification.intent` = `financial_aid`
- `routing.escalate` = `true`
- `action.knowledge_articles` includes aid recalculation article

---

## Build Hints

- `financial_aid.human_touch_keywords` in `escalation_rules.py` should include "lost her job" / "parent lost their job"
- The registrar overlap (drop deadline) can be surfaced as a secondary KB hit without re-routing
- See seed article: "How federal aid is recalculated when you drop below full-time status"
