# 47 Doors Boot Camp Facilitation Guide

This guide provides facilitators with a structured approach to leading the 47 Doors AI Agent workshop. The **3-hour AJCU format (1:00–4:00 PM)** is an azd-first, build-focused session: provision once with `azd up`, then spend the bulk of the time building and testing the AJCU challenge scenarios. *(For the original 7-hour boot-camp format, switch the docs back per `specs/015-ajcu-3hour-docs/plan.md`.)*

---

## Room Setup Checklist

Complete these items **before participants arrive**:

### Physical Environment

- [ ] Projector/screen tested and working
- [ ] Whiteboard markers available (at least 3 colors)
- [ ] Power strips at each table cluster
- [ ] Seating arranged in pairs or small groups (3-4 per table)
- [ ] Facilitator station near power and screen access
- [ ] Water/refreshments station identified

### Technical Environment

- [ ] Wi-Fi credentials posted visibly
- [ ] Test internet connectivity from multiple locations in room
- [ ] Azure subscription access verified for all participants
- [ ] GitHub Codespaces quota confirmed (if using cloud dev)
- [ ] Backup hotspot available for connectivity issues
- [ ] Shared screen/demo machine ready with all labs pre-loaded

### Materials

- [ ] Printed quick-reference cards (optional but helpful)
- [ ] Sticky notes for "parking lot" questions
- [ ] Name tags or table tents
- [ ] Feedback forms ready (digital or paper)

### Pre-Flight Verification

- [ ] Run through Lab 00 setup on a fresh account
- [ ] Verify Azure OpenAI endpoints are responding
- [ ] Confirm Azure AI Search index is accessible
- [ ] Test `azd` deployment flow end-to-end

---

## 3-Hour Timeline (1:00 – 4:00 PM) — AJCU Workshop

> **Format:** azd-first. Provision once, then build. The bulk of the afternoon is
> two build sprints and team demos — not configuration. The run-of-show below is
> the source of truth (also shown on the participant site `/runofshow`).

### Run of Show

| Time | Block | Lead | Min |
|------|-------|------|----:|
| 1:00–1:08 | Open & frame | Sean | 8 |
| 1:08–1:22 | The pattern — three agents | Sean | 14 |
| 1:22–1:32 | Live demo · Card D | Jake | 10 |
| 1:32–1:40 | Form teams · pick a card | All | 8 |
| 1:40–2:40 | Build sprint 1 | Teams + coaches | 60 |
| 2:40–2:50 | Break | — | 10 |
| 2:50–3:05 | Build sprint 2 · harden | Teams + coaches | 15 |
| 3:05–3:55 | Demos · 5 × 10 min | Teams | 50 |
| 3:55–4:00 | Close | Sean | 5 |

### Coach Escalation Playbook (Enterprise Azure Environments)

Use this rapid triage sequence when multiple participants are blocked by Azure access issues:

1. **Conditional Access block (`AADSTS53003`)**
   - Switch affected participants to service principal auth workflow.
2. **No subscription visibility for SP**
   - Confirm RBAC assignment at subscription or resource-group scope.
3. **`MissingSubscriptionRegistration` during `azd up`**
   - Ask subscription admin to register `Microsoft.App` and `Microsoft.Web`.
4. **Cosmos regional capacity errors**
   - Move Cosmos to an allowed region (for example `canadacentral`) and keep app hosting region unchanged.
5. **Mock-lane continuity strategy**
   - If a team is fully blocked on Azure, keep them progressing on the **mock lane**
     (`bash scripts/quickstart.sh --mock`) — scenarios, routing, and crisis-safety all
     run offline with zero credentials.

### 1:00 – 1:08 | Open & frame (Sean, 8 min)

**Objectives:** establish energy and the "47 front doors" problem; set the azd-first
expectation — *provision once, build the rest of the session*.

- Welcome, the one-sentence mission, and how the afternoon flows (two build sprints + demos).
- Confirm every team has run (or is running) `azd up` **or** is on the mock/shared lane.
- **Pacing:** by 1:08 every team knows their lane and has the repo open.

### 1:08 – 1:22 | The pattern — three agents (Sean, 14 min)

**Objectives:** build the mental model of QueryAgent → RouterAgent → ActionAgent and
the six-intent taxonomy (`financial_aid`, `registrar`, `campus_ministry`, `it`,
`student_wellness`, `general`); call out the **intent-independent crisis-safety net**.

- Whiteboard/slide the pipeline; emphasize routing + escalation as the gradable surface.
- **Pacing:** by 1:22 participants can explain why multi-agent > monolithic and where
  the escalation rule lives.

### 1:22 – 1:32 | Live demo · Card D (Jake, 10 min)

**Objectives:** show a working end-to-end scenario (Card D — the Phishing Storm) so teams
have a target. One student message ("my password isn't working… I clicked the link") drives
two parallel actions — an IT password-reset ticket *and* a security-incident workflow.

- Drive the text chat live: the Phishing Storm message → **two tickets** (IT reset +
  security incident) with KB articles, then a crisis phrase → human escalation with the
  988 lifeline (never answered with self-service articles).
- **OPTIONAL / stretch (only if time allows):** the live voice/phone demo (LivePage +
  the +1 (913) 217-1946 number). In the 3-hour format this is a *nice-to-have*, not a
  required segment — skip it if the demo clock is tight.
- **Pacing:** by 1:32 every team has seen Card D's dual-action path and a crisis escalation.

### 1:32 – 1:40 | Form teams · pick a card (All, 8 min)

**Objectives:** 5 teams formed; each picks an AJCU challenge card.

- Teams choose from `labs/05-agent-orchestration/scenarios/ajcu/challenge-{a..f}.md`.
- Coaches confirm each team is scenario-ready (`azd up` finished / mock lane green).
- **Pacing:** by 1:40 all 5 teams have a card and a working backend.

### 1:40 – 2:40 | Build sprint 1 (Teams + coaches, 60 min)

**Objectives:** get routing working end to end for the chosen card; one escalation rule lands.

- Coaches circulate; keep teams to the **Build Contract**: *working beats perfect — routing
  works end to end · one escalation rule lands · you can demo it live.*
- Watch for teams over-scoping; steer to a demoable slice.
- **Pacing markers:** by 2:10 routing returns a department for the happy path; by 2:40 each
  team can run their scenario at least once.

### 2:40 – 2:50 | Break (10 min)

- Don't troubleshoot during the break unless a team is hard-blocked.

### 2:50 – 3:05 | Build sprint 2 · harden (Teams + coaches, 15 min)

**Objectives:** harden the demo — edge cases, the escalation/crisis path, and a clean run-through.

- Teams freeze scope and rehearse their 10-minute demo once.
- **Pacing:** by 3:05 every team has a rehearsed, demoable path.

### 3:05 – 3:55 | Demos · 5 × 10 min (Teams, 50 min)

**Objectives:** each of the 5 teams demos live (10 min each, hard stop).

- Keep a visible timer; one coach timekeeps. Reinforce: *did routing work, did the
  escalation rule land, was it demoed live?*
- **Pacing:** 10 minutes per team, no exceptions — protect the close.

### 3:55 – 4:00 | Close (Sean, 5 min)

**Objectives:** celebrate, point to take-home deep-dive labs, gather quick feedback.

- Name the pattern they just shipped; link the optional labs (00–07) and the Student Runbook.
- Collect feedback; thank the room.

---

## Intervention Decision Framework

Use this framework to decide when to intervene:

### Green Zone - Productive Struggle

- Participant is engaged and making attempts
- Error messages are being read and researched
- Questions are specific and show understanding
- **Action:** Observe, encourage, let them work through it

### Yellow Zone - Consider Intervening

- Same error for 5+ minutes without progress
- Visible frustration or disengagement
- Asking very broad questions ("Why doesn't it work?")
- **Action:** Check in with open question, offer hint, pair with peer

### Red Zone - Immediate Intervention

- Technical blocker affecting multiple participants
- Participant visibly upset or shutting down
- Error that cannot be resolved without facilitator help
- 10+ minutes stuck on same issue
- **Action:** Direct assistance, provide solution, or note for post-session

### Intervention Techniques

1. **The Drive-By Check:** "How's it going? What are you working on?"
2. **The Rubber Duck:** "Talk me through what you've tried"
3. **The Breadcrumb:** "Have you looked at line 42?" (don't give answer)
4. **The Pair-Up:** "Alex just solved something similar - Alex, can you share?"
5. **The Reset:** "Let's close everything and start fresh from checkpoint X"
6. **The Demo:** "Watch me do this one, then you'll try the next"

---

## Contingency Plans

### If 30+ minutes behind schedule:

- Skip extension exercises in current and remaining labs
- Convert hands-on to live coding with participation
- Compress breaks (minimum 5 min for each scheduled break)
- Lab 07 becomes take-home only

### If Azure services have outage:

- Switch to local development mode (mock endpoints)
- Use cached responses for demo purposes
- Focus on code structure and patterns over working API calls
- Document issue for post-boot camp support

### If significant portion (>30%) struggling:

- Pause for group teaching moment
- Create impromptu help tables (those ahead help those behind)
- Simplify remaining exercises
- Ensure everyone completes core path even if reduced scope

### If Voice/Phone Demo fails:

- **Voice/Phone Demo Failure:** If Azure OpenAI Realtime or ACS is unavailable, switch to mock mode (`MOCK_MODE=true`) and demonstrate the mock responses. Emphasize that mock mode uses the same code paths—only the Azure service calls are simulated.

### If running ahead:

- Allow more exploration time
- Add extension exercises
- Deeper Q&A sessions
- Start Lab 07 in-session

---

## Facilitator Self-Care

- Take breaks when participants take breaks
- Stay hydrated
- Don't absorb participant frustration
- Celebrate small wins (yours and theirs)
- It's okay if not everyone finishes everything

---

## Post-Event Checklist

- [ ] Collect all feedback forms
- [ ] Note any Azure resources that need cleanup
- [ ] Document common issues for curriculum improvement
- [ ] Send follow-up email with resources and Lab 07 materials
- [ ] Thank yourself for facilitating!
