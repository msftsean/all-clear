# AJCU Scenario Challenge Cards

**Lab 05 — Agent Orchestration · AJCU Jesuit Workshop**

Six challenge cards for the build sprint. Each card is a real student
message your agent must handle correctly. Pick one, build the pipeline,
smoke-test it.

The live backend is scenario-ready: 31 KB articles are seeded, the
six-intent AJCU taxonomy is wired, and escalation rules are in place.

---

## The Six Intents

| Intent | Routes to | Scope |
|--------|-----------|-------|
| `financial_aid` | Bursar / Financial Aid | Cost, scholarships, aid, billing, work-study |
| `registrar` | Registrar's Office | Registration, transcripts, enrollment, graduation |
| `campus_ministry` | Office of Campus Ministry | Liturgy, retreats, chaplaincy, service, interfaith |
| `it` | University IT | Accounts, passwords, Wi-Fi, devices, Canvas |
| `student_wellness` | Counseling & Health Services | Mental health, crisis, medical, basic needs |
| `general` | Front-desk pool | Mission, orientation, advising, anything else |

---

## Challenge Cards

| Card | Title | Primary Intent | Key Build Challenge |
|------|-------|----------------|---------------------|
| [A](./challenge-a.md) | The Quiet Crisis | `student_wellness` | Dual-path: crisis line + chaplain offer |
| [B](./challenge-b.md) | The Aid Cliff | `financial_aid` + `registrar` | Overlap detection, high-priority ticket |
| [C](./challenge-c.md) | The Discernment | `campus_ministry` | Offer, don't auto-create ticket |
| [D](./challenge-d.md) | The Phishing Storm | `it` + security | Two tickets from one message |
| [E](./challenge-e.md) | The Holy Spirit Question | `campus_ministry` | Interfaith welcome, simple routing |
| [F](./challenge-f.md) | The Multilingual Family | `general` | Spanish detection, respond in Spanish |

---

## Smoke-Testing Your Agent

```bash
# Each card includes a curl command. Example for Card E (simplest):
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mock-student-token" \
  -d '{"message": "When is the Mass of the Holy Spirit? Also, I am not Catholic — am I welcome?"}'
```

Run against the live Azure backend by swapping the URL:
```
https://allclear-r7ie3qtwos7v2-backend.niceisland-c7b3b87f.eastus.azurecontainerapps.io
```

---

## Reference

- Domain language: [`CONTEXT.md`](../../../../CONTEXT.md)
- Scenario pack: [`docs/ajcu/47Doors-AJCU-Scenario.md`](../../../../docs/ajcu/47Doors-AJCU-Scenario.md)
- Surge scenario: [`../surge/README.md`](../surge/README.md)
