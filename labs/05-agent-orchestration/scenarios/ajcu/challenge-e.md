# Challenge E — "The Mass of the Holy Spirit Question"

**Difficulty:** ⭐ (warmup — simplest case)
**Primary intent:** `campus_ministry`
**Key build challenge:** Interfaith welcome paragraph baked into the response

---

## The Message

> *"When is the Mass of the Holy Spirit? Also, I'm not Catholic — am I welcome?"*

---

## What Your Agent Must Do

1. **Classify** as `campus_ministry` (liturgical question)
2. **Surface** KB article: "Mass schedule, reconciliation hours, and sacramental preparation"
3. **Include** an interfaith welcome statement — Campus Ministry serves all students regardless of faith background
4. **Do NOT** assume Catholic identity or make the student feel excluded

**AJCU system prompt rule in play:**
> *INTERFAITH RESPECT: Campus Ministry serves students of all faiths and none. Do not assume Catholic identity. If a student references another tradition, route to campus_ministry — the office handles interfaith referrals.*

---

## Expected Pipeline Output

```json
{
  "classification": {
    "intent": "campus_ministry",
    "confidence": "> 0.90"
  },
  "routing": {
    "target_queue": "campus_ministry",
    "escalate": false
  },
  "action": {
    "status": "opened",
    "knowledge_articles": ["Mass schedule, reconciliation hours..."],
    "user_message": "includes interfaith welcome language"
  }
}
```

---

## Smoke Test

```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-student-token" \
  -d '{"message": "When is the Mass of the Holy Spirit? Also, I'\''m not Catholic — am I welcome?"}'
```

**Pass criteria:**
- `classification.intent` = `campus_ministry`
- `action.knowledge_articles` includes mass schedule article
- Response is welcoming to non-Catholic students

---

## Build Hints

- Good first card for newer teams — the routing is unambiguous
- The interfaith welcome is a response-generation concern, not a routing concern
- See KB article: "Interfaith programming, prayer spaces, and dietary observances"
