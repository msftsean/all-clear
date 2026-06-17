# Challenge F — "The Multilingual Family"

**Difficulty:** ⭐⭐ (language detection)
**Primary intent:** `general`
**Key build challenge:** Detect Spanish, respond in Spanish, route to General/Mission

---

## The Message

> *"Mi mamá quiere saber cuándo es el día de orientación para padres."*
> *(My mom wants to know when parent orientation day is.)*

---

## What Your Agent Must Do

1. **Classify** as `general` (orientation/admin question, not tied to a specific department)
2. **Detect** that the message is in Spanish
3. **Respond in Spanish** — match the language of the student/family
4. **Surface** KB article: "First-year orientation: what's required vs. optional" (may need to respond about the parent track)
5. **Do NOT** respond only in English

---

## Expected Pipeline Output

```json
{
  "classification": {
    "intent": "general",
    "confidence": "> 0.80"
  },
  "routing": {
    "target_queue": "general",
    "escalate": false
  },
  "action": {
    "status": "opened",
    "knowledge_articles": ["First-year orientation: what's required vs. optional"],
    "user_message": "response in Spanish"
  }
}
```

---

## Smoke Test

```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-student-token" \
  -d '{"message": "Mi mamá quiere saber cuándo es el día de orientación para padres."}'
```

**Pass criteria:**
- `classification.intent` = `general`
- `action.user_message` is in Spanish (or bilingual)

---

## Build Hints

- Language detection can be done in `QueryAgent` (PII/entity extraction step) or as a post-classification enrichment
- The LLM classifier should naturally route `general` for orientation admin questions
- The response language should be driven by the detected `signal_language` entity
- This tests the full pipeline's multilingual capability — a key differentiator for AJCU institutions serving diverse families
