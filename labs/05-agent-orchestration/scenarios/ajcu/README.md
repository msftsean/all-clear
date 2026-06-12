# AJCU Workshop Challenge Cards

Build-sprint challenge prompts from `47Doors-AJCU-Scenario.md` §5. Each team picks
one card. The cards map to the seeded KB (`infra/ai-search/seed-articles/`) so teams
have real content to work against, and to the six-intent Jesuit taxonomy in
`backend/app/agents/intent_classifier.py`.

Card text is locked to the keynote deck and the cards website — keep it verbatim.

| Card | Title | Primary intent | Key behavior |
|---|---|---|---|
| [A](challenge-a-quiet-crisis.md) | The Quiet Crisis | `student_wellness` | Whole-person overlap + safety; offer chaplain in parallel, no gating |
| [B](challenge-b-aid-cliff.md) | The Aid Cliff | `financial_aid` (+`registrar`) | Multi-intent overlap; high-priority appeals ticket |
| [C](challenge-c-discernment.md) | The Discernment | `campus_ministry` | Offer, don't auto-create a ticket |
| [D](challenge-d-phishing-storm.md) | The Phishing Storm | `it` | One message → two tickets (IT + security) |
| [E](challenge-e-mass-of-the-holy-spirit.md) | Mass of the Holy Spirit | `campus_ministry` | Simplest routing + interfaith welcome (warmup) |
| [F](challenge-f-multilingual-family.md) | The Multilingual Family | `general` | Spanish detection + Spanish response |

Run the smoke test to confirm the classifier + escalation behavior for all six:

```bash
cd backend && PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/ajcu/smoke_test.py
```
