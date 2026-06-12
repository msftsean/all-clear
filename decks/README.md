# ISV Summit — Presentation Deck Scripts (Day-Before)

These are **build-ready scripts** for two decks Sean Gayle presents the day before the
"Ship It! Build a Production Azure Agent in Two Days" ISV Summit. Hand these three files to
**Manus** (deck builder) together — the design file is the house style, the two scripts are
the slide-by-slide content.

| File | Deck | Slides | Slot |
| ---- | ---- | ------ | ---- |
| `ISV_Summit_Six_Domains.md` | Deck 1 — The Six Domains of a Production Agent | 13 | 1:30 – 2:15 PM |
| `ISV_Summit_EnvPrep.md` | Deck 2 — Environment Prep for Day 2 | 11 | 4:15 – 5:15 PM |
| `../design/DESIGN-antimetal.md` | **House style** (Antimetal) — colors, type, components | — | apply to both |

## House style (Antimetal) — the short version

Full spec: [`../design/DESIGN-antimetal.md`](../design/DESIGN-antimetal.md). For slides, apply
these token roles:

| Slide role | Antimetal token |
| ---------- | --------------- |
| **Title / section dividers** | Deep-navy hero gradient `#001033 → #0050f8 → #5fbdf7`; display type in **ivarTextFont** (serif, ≥32px); white text |
| **Body / content slides** | Light technical surface — canvas `#f8f9fc`, cards `#ffffff` with a 1px blue shadow-ring border, card radius 20px |
| **All text** | Midnight Navy `#1b2540` — **never pure black**. UI/body type = **abcdFont** (Inter / DM Sans), tight tracking, weights 400–480 |
| **Primary CTA / "the one action"** | **Chartreuse Pulse `#d0f100`** fill, pill button (radius 9999px). Use sparingly — one per slide max |
| **Positive / "production has it"** | Blue/green accents on light cards |
| **Negative / "demo gap"** | Muted red on light cards (do not use chartreuse for negatives) |
| **Shadows** | Blue-tinted `rgba(0,39,80,…)`, soft |

Toggleable dark/light is **not** needed for these decks — they are presentation slides, not the
runbook. Default to the navy-hero + light-surface rhythm above.

## The through-line (every slide should reinforce it)

ISVs in the room are **interested but not converting** — they've sat through AI overviews before.
The message Sean & Adrian settled on in May answers the question they keep asking:

> "Great — but what do we do *next*?"

Deck 1 answers it conceptually (the six domains that separate a demo from a product). Deck 2
answers it operationally (be ready to *build* one tomorrow). Land that line; don't re-explain "what
is an agent."

## Ground truth — what was actually built (so the decks don't overpromise)

- **App:** *All Clear* — a regulated-industry incident-triage agent (signal → structured, auditable
  incident → drafted public update that **waits for human approval**). Built on **Microsoft Agent
  Framework**, deployed live on **Azure Container Apps**.
- **Day 2 = six stages, one repo, one deployed URL** (S0–S5): 45 / 90 / 60 / 75 / 60 / 60 min =
  **390 min**, filling 11:00 AM – 5:30 PM ET exactly.
- **Stage 4 (APIM gateway)** uses the **Consumption SKU** — load-tested at **20 simultaneous
  creates, 20/20 succeeded, ~3.5 min, $0** in the Cloudforce subscription. (Documented in
  `../docs/apim-consumption-loadtest.md`.) That test is why Deck 2 can promise every attendee gets
  their own gateway without quota fear.
- **Six Domains** (canonical, used in Deck 1 *and* the participant runbook): **Identity,
  Observability, Evals, Safety, Memory & State, Cost Governance.** (Day-2 Stage 1 builds the
  Agent Framework *building blocks* — model, tools, orchestration — distinct from the six domains.)
- Source runbook the decks must agree with: `../participant-runbook/index.html` (live Day-2 build
  lab) and the per-stage labs under `../labs/`.
