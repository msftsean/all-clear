# AJCU Facilitator Framing

Framing notes for the AJCU pre-conference workshop at Fordham, from
`47Doors-AJCU-Scenario.md` §6. Use the 60-second mission pitch to open the build
sprint; it sets up the Jesuit framing (cura personalis) and the six-intent
taxonomy the teams will build against.

## The 60-second mission pitch

> "Every Jesuit university already has 47 doors. The Bursar, the
> Registrar, IT, Counseling, Campus Ministry, your advisor, your RA, your
> dean. A student in distress doesn't know which door is the right one,
> and *cura personalis* breaks down at the front desk.
>
> Today you're going to build the door behind the door. One agent, one
> conversation, that knows when to send a student to financial aid, when
> to send them to a chaplain, and when — quietly, urgently — to send them
> to the counseling center. The agent doesn't replace any of those
> offices. It makes sure the student actually gets to the right one.
>
> By 1:30 you'll have a working prototype. By the end of the conference
> you'll have a pattern you can take back to your campus."

## Framing notes

- **Why these six intents.** Financial Aid, Registrar, Campus Ministry, IT,
  Student Wellness, and General / Mission mirror the offices a Jesuit student
  actually encounters in their first 90 days. Campus Ministry is a first-class
  peer to IT and the Registrar — not an afterthought — because at Jesuit schools
  it materially shapes the student experience.

- **Cura personalis at the routing layer.** The escalation rules
  (`backend/app/agents/escalation_rules.py`) encode care for the whole person:
  Student Wellness and Financial Aid create tickets autonomously when distress
  signals appear (the cost of a missed ticket is high), while Campus Ministry
  *offers* to connect a student with a chaplain rather than booking on their
  behalf — pastoral relationships should be opt-in.

- **Never gate clinical care behind a faith conversation.** When a message is an
  ambiguous mix of distress and meaning, route to Student Wellness first and
  offer chaplaincy in parallel (Challenge A).

- **The live demo.** Challenge D ("The Phishing Storm") is the on-stage moment —
  the canonical "one message, two outcomes": IT routing *and* a parallel
  security-incident ticket from a single sentence.

## Run the build sprint

- Challenge cards: `labs/05-agent-orchestration/scenarios/ajcu/`
- KB seed corpus: `infra/ai-search/seed-articles/`
- Smoke test (verify all six end-to-end):

  ```bash
  cd backend && PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/ajcu/smoke_test.py
  ```
