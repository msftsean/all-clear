> ARCHIVED — superseded by All Clear (incident triage). See CONTEXT.md.

# 47 Doors — AJCU Scenario Pack

**Drop-in scenario rewrite for the AJCU pre-conference workshop at Fordham.**
Replaces the stock university-support taxonomy with one that reflects the
mission and lived realities of Jesuit institutions: **cura personalis**,
discernment, service, and the integration of faith and reason.

This pack is structured so you can lift each section straight into the
47 Doors repo:

- §1 → `backend/app/agents/query_agent/intents.py` (intent taxonomy)
- §2 → `backend/app/agents/query_agent/system_prompt.md` (classifier prompt)
- §3 → `infra/ai-search/seed-articles/` (KB seed corpus)
- §4 → `backend/app/agents/router_agent/escalation_rules.py` (escalation logic)
- §5 → `labs/05-agent-orchestration/scenarios/ajcu/` (workshop challenge prompts)
- §6 → `coach-guide/ajcu-framing.md` (facilitator notes)

---

## §1 — Intent Taxonomy (Departments)

| Intent | Slug | Routes to | One-line scope |
|---|---|---|---|
| Financial Aid | `financial_aid` | Bursar / Financial Aid | Cost, scholarships, aid packages, billing, work-study |
| Registrar | `registrar` | Registrar's Office | Registration, transcripts, enrollment, course changes, graduation |
| Campus Ministry | `campus_ministry` | Office of Campus Ministry | Liturgy, sacraments, retreats, chaplaincy, service & immersion, interfaith life |
| Information Technology | `it` | University IT | Accounts, passwords, Wi-Fi, devices, learning systems |
| Student Wellness | `student_wellness` | Counseling & Health Services | Mental health, medical, crisis, accessibility, basic needs |
| General / Mission | `general` | Front-desk pool | Anything else; mission and student-life questions |

**Why these six.** They mirror the offices a Jesuit student actually
encounters in their first 90 days. Campus Ministry is treated as a
first-class peer to IT and the Registrar — not an afterthought — because at
Jesuit schools it materially shapes the student experience.

---

## §2 — Intent Classifier System Prompt (drop-in replacement)

```text
You are the QueryAgent for a Jesuit university's Universal Front Door
support system. Classify each student message into exactly ONE of these
intents:

- financial_aid
- registrar
- campus_ministry
- it
- student_wellness
- general

GUIDANCE FOR JESUIT-CONTEXT EDGE CASES

1. CARE-OF-THE-WHOLE-PERSON OVERLAP (CRITICAL)
   Messages expressing distress, loneliness, grief, vocation questions, or
   spiritual struggle can plausibly route to BOTH campus_ministry and
   student_wellness. Apply this rule:

   - Clinical signals (sleep loss, panic, self-harm, "I can't function",
     medication, diagnosis) → student_wellness
   - Vocational / meaning / faith / discernment signals ("what is my
     purpose", "I feel disconnected from God", "thinking about a retreat",
     "want to talk to a chaplain") → campus_ministry
   - Ambiguous → student_wellness, with a follow-up offer for chaplaincy.
     Never gate clinical care behind a faith conversation.

2. SAFETY OVERRIDE
   Any message indicating risk of harm to self or others routes to
   student_wellness with `escalate=true` and `priority=urgent`. The
   ActionAgent must surface the 24/7 crisis line in the response and
   create a high-priority ticket regardless of business hours.

3. INTERFAITH RESPECT
   Campus Ministry serves students of all faiths and none. Do not assume
   Catholic identity. If a student references another tradition, route to
   campus_ministry — the office handles interfaith referrals.

4. FINANCIAL ↔ REGISTRAR OVERLAP
   "Can I drop a class without losing aid?" → financial_aid (the aid
   implication is the blocker). "What's the drop deadline?" → registrar.

5. IT ↔ ANY DEPT
   If the student asks how to USE a system (Banner, Canvas, the portal),
   route to the owning department first; route to IT only when the
   system itself is broken.

Return JSON: { "intent": "<slug>", "confidence": 0.0–1.0, "rationale": "<≤20 words>" }
```

---

## §3 — KB Seed Corpus (sample articles to load into Azure AI Search)

Each AJCU member can re-skin these to its own URLs and policies. Provide
attendees with this seed so the RAG pipeline has something real to retrieve
during the build sprint.

### Financial Aid (`financial_aid`)
- "How federal aid is recalculated when you drop below full-time status"
- "Work-study vs. on-campus employment: what counts toward your aid package"
- "Appealing your financial aid award: the special-circumstances form"
- "Tuition payment plans and deadlines"
- "Loyola scholarships, Magis grants, and need-based aid stacking rules"

### Registrar (`registrar`)
- "Add/drop, withdrawal, and the W vs. WF distinction"
- "Requesting an official vs. unofficial transcript"
- "Changing your major or declaring a minor"
- "Graduation application deadlines and the audit process"
- "Cross-registration with consortium schools"

### Campus Ministry (`campus_ministry`)
- "Mass schedule, reconciliation hours, and sacramental preparation"
- "Going on retreat: Silent, Magis, and Ignatian Spiritual Exercises options"
- "Talking to a chaplain — pastoral counseling vs. spiritual direction"
- "Service & immersion programs and how to apply"
- "Interfaith programming, prayer spaces, and dietary observances"
- "Discernment groups for students considering religious or service vocations"

### IT (`it`)
- "Resetting your university password and enrolling in MFA"
- "Connecting to eduroam Wi-Fi"
- "Canvas / LMS access issues — first-stop checklist"
- "Reporting a phishing email"
- "Borrowing a loaner laptop from the library"

### Student Wellness (`student_wellness`)
- "Booking a counseling intake — what to expect at your first session"
- "Same-day urgent appointments and after-hours crisis support"
- "CAPS group therapy and peer-support communities"
- "Basic needs: food pantry, emergency funds, housing insecurity support"
- "Accessibility services and academic accommodations"
- "Substance use support — confidential and non-disciplinary pathways"

### General / Mission (`general`)
- "What does Jesuit education actually mean? (cura personalis, magis, men and women for others)"
- "How to find your advisor, your dean, and your class dean"
- "First-year orientation: what's required vs. optional"
- "Service-learning courses — how they work and how they count"

---

## §4 — Escalation & Routing Rules

```python
# backend/app/agents/router_agent/escalation_rules.py
ESCALATION_RULES = {
    "student_wellness": {
        "auto_escalate_keywords": [
            "harm myself", "kill myself", "end it", "suicide",
            "hurt someone", "abuse", "assault",
        ],
        "priority": "urgent",
        "out_of_hours_response": (
            "If you are in immediate danger, call 911 or the campus "
            "safety line. You can also reach the 988 Suicide & Crisis "
            "Lifeline by calling or texting 988. A counselor will follow "
            "up with you within 24 hours."
        ),
        "always_create_ticket": True,
    },
    "campus_ministry": {
        # Pastoral concerns are never urgent in the clinical sense, but
        # discernment requests deserve a human, not a knowledge article.
        "human_touch_keywords": [
            "discernment", "vocation", "spiritual direction",
            "lost my faith", "grief", "miscarriage", "death of",
        ],
        "priority": "normal",
        "always_create_ticket": False,  # offer, don't auto-create
    },
    "financial_aid": {
        "human_touch_keywords": [
            "appeal", "special circumstances", "lost my job",
            "parent lost their job", "homeless", "evicted",
        ],
        "priority": "high",
        "always_create_ticket": True,
    },
}
```

**Design principle:** the agent is allowed to create a ticket in
`student_wellness` and `financial_aid` autonomously when distress signals
appear, because the cost of a missed ticket is high. In `campus_ministry`
the agent **offers** to connect a student with a chaplain rather than
booking on their behalf — pastoral relationships should be opt-in.

---

## §5 — Workshop Challenge Prompts (for the build sprint)

Print these on cards. Each team picks one. They map to the seeded KB so
teams have real content to work against.

### Challenge A — "The Quiet Crisis"
A first-year student messages: *"I haven't been to class in two weeks. I
don't think I belong here. I've been crying at night. I don't know who to
talk to."*
**Build:** an agent that recognizes overlapping distress, routes primarily
to Student Wellness, surfaces the crisis line, and *also* offers a chaplain
conversation as a parallel path. No gating.

### Challenge B — "The Aid Cliff"
A junior asks: *"My mom lost her job last month. Can I get more aid? Also
I'm thinking of dropping a class — does that hurt my package?"*
**Build:** an agent that detects the financial_aid + registrar overlap,
routes correctly, and creates a high-priority appeals ticket with the
student's narrative attached.

### Challenge C — "The Discernment"
A senior writes: *"I'm thinking about doing a year of service after
graduation. I don't know if I should apply to JVC or take the consulting
job. Can someone help me think through this?"*
**Build:** an agent that routes to Campus Ministry, surfaces discernment
group and 1:1 chaplain options, and **does not** auto-create a ticket —
it offers.

### Challenge D — "The Phishing Storm"
A staff-shared message: *"My password isn't working and I just got an
email saying my account is locked. I clicked the link."*
**Build:** an agent that handles the IT routing AND triggers a
security-incident workflow because of the click. Two tickets, one to IT
support, one to the security team.

### Challenge E — "The Mass-of-the-Holy-Spirit Question"
*"When is the Mass of the Holy Spirit? Also, I'm not Catholic — am I
welcome?"*
**Build:** the simplest case — Campus Ministry routing with an interfaith
welcome paragraph baked into the response. Good warmup for newer teams.

### Challenge F — "The Multilingual Family"
*"Mi mamá quiere saber cuándo es el día de orientación para padres."*
**Build:** an agent that detects Spanish, responds in Spanish, and routes
to General/Mission with a parent-orientation KB hit.

---

## §6 — Facilitator Framing (the 60-second mission pitch)

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

---

## Drop-In Checklist

- [ ] Replace `intents.py` taxonomy
- [ ] Swap classifier system prompt
- [ ] Seed KB index with the §3 corpus (or your campus's real articles)
- [ ] Add `escalation_rules.py`
- [ ] Drop challenge cards into `labs/05-agent-orchestration/scenarios/ajcu/`
- [ ] Add the §6 framing to the coach guide
- [ ] Update the demo dashboard's department legend to match
- [ ] Smoke-test each challenge end-to-end before the conference
