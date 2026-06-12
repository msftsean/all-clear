# Deck 1 — The Six Domains of a Production Agent

**Speaker:** Sean Gayle, Principal Solution Engineer
**Slot:** Day 1 · 1:30 – 2:15 PM ET · 13 slides
**Output file:** `ISV_Summit_Six_Domains.pptx`
**House style:** Antimetal — see `../design/DESIGN-antimetal.md` and `README.md` in this folder.
**Through-line:** ISVs are interested but not converting. This deck answers the question they keep
asking — *"Great, but what do we do next?"* — by naming the six things that turn a demo into a
product they can sell.
**Audience:** almost entirely **SLED ISVs** — software vendors selling to police, fire/EMS, courts,
child welfare, counties, and universities. ~50% public safety / law enforcement (**CJIS**), ~20%
government human services (**HIPAA**), ~10% courts & e-discovery (chain of custody), ~10% higher ed
(**FERPA**). Every "Why It Matters" should sound like it was written for a vendor whose buyer has a
compliance officer, an auditor, and an attorney.

> **Design rhythm:** Slides 1 and 13 are **navy hero** (dark gradient, serif display, white text).
> Everything in between is the **light technical surface** (canvas `#f8f9fc`, white cards with a 1px
> blue shadow-ring border). One chartreuse accent per slide, max. Never pure black text — use
> Midnight Navy `#1b2540`.

---

## Slide 1 — Title

- **Layout:** Full-bleed **navy hero gradient** (`#001033 → #0050f8 → #5fbdf7`). Centered.
- **Eyebrow (small caps, abcdFont):** SHIP IT! · ISV SUMMIT · DAY 1
- **Title (ivarTextFont serif, large, white):** The Six Domains of a Production Agent
- **Subtitle (abcdFont, light):** What separates a demo that wows from an agent you can ship to a government agency
- **Footer row:** Sean Gayle — Principal Solution Engineer · June 16, 2026
- **Design note:** A single thin chartreuse rule under the title. No logos competing with the
  gradient; ISV Summit lockup small, top-left.

---

## Slide 2 — Agenda

- **Layout:** Light surface. Five **numbered row cards** stacked vertically (circle numeral on the
  left in navy, label + one-liner on the right).
- **Rows:**
  1. **The demo-to-production gap** — why great demos stall before they ship
  2. **The six domains** — the checklist a real agent has to pass
  3. **Domain by domain** — what each one covers, why it matters to an ISV
  4. **Making it real** — three regulated verticals, the domains each demands
  5. **What to bring to Day 2** — how tomorrow's build exercises each domain
- **Design note:** Numerals in navy circles; active/last row can carry the chartreuse accent.

---

## Slide 3 — The Demo-to-Production Gap

- **Layout:** **Two-column comparison.** Left column header **"What demos have"** (muted red
  accent). Right column header **"What production agents need"** (blue/green accent). Equal-height
  cards.
- **Left — What demos have:**
  - A happy-path script and a clean dataset
  - One model call, one good answer on stage
  - "Trust me, it works" — no receipts
  - Runs on the presenter's laptop
  - No idea what it costs at 1,000 users
- **Right — What production agents need:**
  - Knows *who* is asking and what they're allowed to see
  - Telemetry you can debug at 2 a.m.
  - Evals that gate every change in CI
  - Guardrails against PII leaks, jailbreaks, bad actions
  - Memory that persists, and a cost ceiling that holds
- **Speaker line / callout (bottom):** "Every team in this room can demo. The gap is everything on
  the right — and your buyer has a compliance officer, an auditor, and an attorney reading the
  answer. It's the same six domains every time."
- **Design note:** This slide *sets up* the "what do we do next" question; the answer is Slide 4.

---

## Slide 4 — The Six Domains (overview)

- **Layout:** **2×3 card grid.** Each card: numbered circle (navy), domain name (abcdFont
  semibold), one-line definition. Uniform card styling, 20px radius, blue shadow ring.
- **Cards:**
  1. **Identity** — Know who's calling and enforce what they can do.
  2. **Observability** — See every step: traces, logs, metrics, replay.
  3. **Evals** — Measure quality and gate changes before they ship.
  4. **Safety** — Block PII leaks, jailbreaks, and unsafe actions.
  5. **Memory & State** — Remember context and persist decisions durably.
  6. **Cost Governance** — Cap spend with budgets, limits, and routing.
- **Design note:** This grid is the deck's spine — reuse the same six labels/colors on Slides
  5–10 and 12 so the audience builds a mental map. Card 1's numeral can carry the chartreuse dot to
  cue "we start here."

---

> **Slides 5–10 — one slide per domain.** Same template each time: domain name + numeral in the
> header; **two columns** — left **"What It Covers"** (blue header card) and right **"Why It Matters
> for ISVs"** (green header card). 3–4 bullets per side. Keep them parallel so the six feel like one
> system, not six unrelated topics.

## Slide 5 — Domain 1: Identity

- **What It Covers (blue):**
  - Authenticate the caller — user, service, or another agent (JWT / Entra ID)
  - **Per-agency tenant isolation** so records never cross jurisdictions
  - Authorize actions and tool calls, not just the front door
  - On Day 2 this lands as **JWT validation at the APIM gateway** (Stage 4)
- **Why It Matters for ISVs (green):**
  - **Per-agency isolation is the contract** — Fulton County PD must never see DeKalb County's
    records, even on the same software
  - CJIS and procurement ask "who did this, on whose behalf?" — you need a name, not "the agent"
  - Identity is the foundation every other control hangs off of

## Slide 6 — Domain 2: Observability

- **What It Covers (blue):**
  - Distributed traces across model calls, tools, and agent hops
  - Structured logs and metrics — latency, tokens, error rates
  - Replay: reconstruct exactly what the agent saw and did
  - On Day 2: **Application Insights** behind the gateway (Stages 4–5)
- **Why It Matters for ISVs (green):**
  - **Audit logs are a standard RFP line item** — agencies ask "what did the agent do, when, and on
    whose behalf?"
  - Government auditors and attorneys will request the trail — you produce it on demand
  - Observability is the difference between "we'll look into it" and a defensible record

## Slide 7 — Domain 3: Evals

- **What It Covers (blue):**
  - A scored test set for agent quality — not just unit tests
  - Run on every change; **gate CI** on the score
  - Catch regressions in grounding, routing, and tone before users do
  - On Day 2: an **eval suite that gates CI** (Stages 0 → 5)
- **Why It Matters for ISVs (green):**
  - **You have annual certifications to protect** — a model update that changes how the agent
    handles a warrant request is a production incident
  - Prove to a compliance officer that behavior didn't drift between releases
  - "Scored every release, gated in CI" is what passes a government security review

## Slide 8 — Domain 4: Safety

- **What It Covers (blue):**
  - PII / PHI / CJI redaction on every path (REST, voice, phone)
  - Jailbreak & prompt-injection defense (Prompt Shields)
  - Action guardrails — a human-approval gate before anything irreversible
  - On Day 2: a **red-team pass** on your MCP tools (Stage 3)
- **Why It Matters for ISVs (green):**
  - **CJIS: criminal-justice data must never leave a controlled environment** — an agent that logs
    prompts to shared telemetry can fail a CJIS audit *(where AWS and GCP consistently struggle)*
  - One leak of a juvenile case file or criminal record is a federal compliance violation
  - "Waits for a human" before any irreversible action is what makes it deployable in a case file
    or a courtroom

## Slide 9 — Domain 5: Memory & State

- **What It Covers (blue):**
  - Session and conversation memory across turns
  - Durable state — incidents, decisions, audit records that outlive a request
  - Consistent reads/writes under concurrency (optimistic concurrency)
  - On Day 2: **agentic retrieval** over articles, policies, records (Stage 2)
- **Why It Matters for ISVs (green):**
  - **A case spans 40+ sessions over 18 months** — that's a record of care, not a chat context window
  - State *is* the product — the incident, the case file, the chain of custody
  - Grounded memory is what stops the agent from inventing facts about a real person

## Slide 10 — Domain 6: Cost Governance

- **What It Covers (blue):**
  - Token budgets and rate limits per tenant / per key
  - Model routing — cheap model for easy calls, premium only when needed
  - Spend visibility before the invoice, not after
  - On Day 2: **token limits + rate-limit-by-key at the gateway** (Stage 4)
- **Why It Matters for ISVs (green):**
  - **You sell on per-agency contracts** — you need to know exactly what each county costs you
  - One runaway loop can erase the margin on a government contract
  - A predictable per-tenant cost ceiling is what lets you price each agency

---

## Slide 11 — Making It Real for ISV Builders

- **Layout:** **Three scenario cards** side by side. Each card: vertical name + regulation badge, a
  one-line scenario, and **"Domains it demands"** chips (reuse the six labels/colors).
- **Speaker framing (top):** "Look around — this room is SLED. You build for police, courts, child
  welfare, and universities. Here's how the six domains land in *your* contracts."
- **Cards:**
  - **Public Safety & Law Enforcement — CJIS** *(~half this room; the app you build tomorrow)*
    *Records, CAD/RMS, incident & patient-care reports for police, fire, and EMS. All Clear is your
    hands-on instance.*
    Demands → **Identity** (per-agency isolation) · **Safety** (CJIS) · **Observability** (audit) ·
    **Evals**
  - **Government Human Services — HIPAA / case files**
    *Case management for social workers, child welfare, and child support — sensitive family data
    tracked across years.*
    Demands → **Safety** · **Memory & State** (18-month case) · **Identity** · **Observability**
  - **Higher Education — FERPA**
    *Student information, advising, financial aid — leak a GPA or aid status to the wrong person and
    it's a compliance event.*
    Demands → **Identity** · **Safety** · **Evals** · **Memory & State**
- **Callout (bottom):** "Different agencies, same six domains in a different mix. For courts and
  e-discovery, add **chain of custody** — prove the agent didn't alter the evidence. And CJIS, HIPAA,
  and FERPA are exactly where Azure carries the compliance story that AWS and GCP struggle with."
- **Design note:** Regulation badges (CJIS / HIPAA / FERPA) as small pill tags. The Public Safety
  card gets the chartreuse accent — it's the majority of the room *and* the app they build.

---

## Slide 12 — What to Bring to Day 2

- **Layout:** **Five numbered rows**, each mapping a Day-2 build stage to the domains it exercises.
  Reuse the six-domain chips on the right of each row.
- **Rows:**
  1. **Stage 1 · Agent on Agent Framework** → exercises **Memory & State**, **Safety**
     *(model, tools, orchestration in place; first human-approval gate)*
  2. **Stage 2 · Agentic retrieval (Foundry IQ)** → **Memory & State**, **Evals**
  3. **Stage 3 · MCP server + red-team pass** → **Safety** (prove data stays inside the controlled
     boundary — the CJIS test), **Identity**, **Evals**
  4. **Stage 4 · APIM as the AI gateway** → **Identity** (JWT), **Cost Governance** (token
     budgets / rate limits), **Observability**
  5. **Stage 5 · Deploy on ACA + eval suite gates CI** → **Observability**, **Evals**,
     **Cost Governance**
- **Footer line:** "By 5:30 tomorrow you'll have touched all six — in one repo, one deployed URL."
- **Design note:** Every one of the six domains appears at least once across the five rows — that's
  the proof that the build covers the whole framework.

---

## Slide 13 — Closing

- **Layout:** Return to the **navy hero gradient**. Centered.
- **Headline (ivarTextFont serif, white):** Great — but what do we do *next*?
- **Answer line (abcdFont):** Build one. Tomorrow. Across all six domains.
- **Primary CTA (chartreuse pill):** See you Day 2 → 11:00 AM ET
- **Footer:** Sean Gayle · Adrian Wright · Ship It! ISV Summit
- **Design note:** This is the only slide where the chartreuse CTA is the hero element — it mirrors
  the "one primary action" rule from the Antimetal system.
