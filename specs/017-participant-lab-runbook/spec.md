# Feature Specification: Participant Lab Runbook — Day‑2 Build Track Reframe

**Branch**: `main` (docs/site-only change) | **Date**: 2026-06-12
**Status**: Active for the **"Ship It! Build a Production Azure Agent in Two Days"** ISV Summit — **Day 2, June 17, 2026, 11:00 AM – 5:30 PM ET**
**Presenters**: Sean Gayle, Adrian Wright
**Artifact**: `participant-runbook/` (deployed to SWA `swa-allclear-participant` → https://ashy-wave-04083e40f.7.azurestaticapps.net)

## Summary

The participant runbook (v1) was a **guided demo walkthrough**: it linked
participants straight to the finished All Clear app and walked them through
five exercises (E1–E5) of *using* that finished product — submit a signal,
read the board, open the receipt. That is the **wrong shape** for this event.
Day 2 is a **hands‑on build lab**, not a demo. Participants must **build and
deploy the agent themselves**; they should **not** see the finished reference
app.

This spec reframes the participant runbook around the **official Day‑2
run‑of‑show** from the event invite: **six stages (Stage 0–5), 390 minutes
total, filling the 11:00 AM – 5:30 PM ET window exactly.** Each stage maps to
the existing hands‑on lab content in `labs/`. The reference frontend link is
removed; the **API endpoints stay** so participants can test their *own*
builds.

## The Day‑2 schedule (authoritative — from the event invite)

> Day 2: June 17, 11 AM ET to 5:30 PM ET — Guided Build Lab. "A full‑day,
> hands‑on build where every attendee creates and deploys a regulated‑industry
> student‑services agent using a pre‑configured GitHub Codespaces environment
> and Azure services. Six stages, one repo, one deployed URL."

| Stage | Official content (from invite) | Min | Maps to repo lab(s) |
|---|---|---:|---|
| **0** | A spec'd scaffold, multi‑agent dev environment wired up, first eval stub passing in your Codespace | 45 | `labs/00-setup` + `labs/03-spec-driven-development` |
| **1** | A working agent on Agent Framework with the six production domains (model, memory, tools, orchestration, safety, evaluation) | 90 | `labs/01-understanding-agents` + `labs/05-agent-orchestration` |
| **2** | Multi‑source agentic retrieval over articles, policies, records via Foundry IQ | 60 | `labs/04-build-rag-pipeline` |
| **3** | Tools exposed through a discoverable MCP server with a red‑team pass | 75 | `labs/07-mcp-server` + `labs/02-azure-mcp-setup` |
| **4** | APIM in front as the AI gateway: rate limits, token budgets, JWT, full observability | 60 | `labs/08-apim-gateway` (new — Consumption SKU) |
| **5** | Deployed on Azure Container Apps with the eval suite gating CI | 60 | `labs/06-deploy-with-azd` |
| | **Total** | **390** | **= 6.5 h = 11:00 → 5:30 ET** |

The six stage durations sum to **exactly 390 minutes (6.5 hours)**, which is
the full Day‑2 window. "Make the lab the length of Day 2" is therefore
satisfied by adopting the invite's own six‑stage structure verbatim.

## Goals

- **G1** — Participants **build the agent themselves** through six stages; they
  do **not** see or link to the finished reference frontend.
- **G2** — The runbook is sized to **Day 2 = 390 min / 6.5 h (11:00–5:30 ET)**,
  with a visible per‑stage clock that sums to the full window.
- **G3** — The six stages match the **event invite's run‑of‑show** (Stage 0–5)
  and each deep‑links to the matching `labs/NN/README.md` for the detail.
- **G4** — **API endpoints remain** (Swagger `/docs`, health) so participants
  can verify their *own* running builds; the finished‑app UI link is removed.
- **G5** — The student edition stays visually distinct (cyan→teal→emerald,
  dark‑default, light/dark toggle) and works under the strict CSP
  (`script-src 'self'`).

## Non‑Goals / Preserve (do NOT touch)

- All application code (`backend/`, `frontend/`, `infra/`, `azure.yaml`,
  `scripts/`) and the `labs/` content itself — this is a runbook‑site change.
- The separate **Coach's Runbook** (`coach-guide/`, its own SWA).
- The brand palette / layout system in `participant-runbook/index.html`
  (`<style>` block) and `staticwebapp.config.json` CSP.

## Functional Requirements

- **FR‑1 — Remove the finished product.** Delete the `#uiBtn` "Open the All
  Clear app" link and every step that tells participants to open / drive /
  "read the board" of the finished frontend. No screenshot or link to the
  reference UI anywhere.
- **FR‑2 — Keep the APIs.** Retain `#apiBtn` (Swagger `/docs`) and `#healthBtn`
  (health), reframed as "test *your own* deployed API," not "peek under the
  hood of ours."
- **FR‑3 — Six stage sections.** Replace `#ex1…#ex5` with `#stage0…#stage5`.
  Each stage section states: objective, the build deliverable, the
  self‑check / acceptance criteria, the duration, and a deep‑link to the
  matching `labs/NN/README.md`. No solution code or finished output revealed.
- **FR‑4 — Day‑2 agenda block.** Add an agenda section showing the six stages
  with start/end clock times across 11:00 AM – 5:30 PM ET (incl. where breaks
  fall) and the 390‑min total.
- **FR‑5 — Stage 4 (APIM) lab.** Stage 4 maps to the new **`labs/08-apim-gateway`**
  (Consumption SKU). The runbook deep‑links to it like every other stage. The
  20‑concurrent‑create feasibility test is recorded in
  `docs/apim-consumption-loadtest.md`.
- **FR‑6 — Nav + counter.** Update the sidebar nav to the six stages and update
  `app.js` `EXERCISES` to `['stage0'…'stage5']` so the "/6 done" counter and
  per‑stage "Mark done" checklist track the stages.
- **FR‑7 — Voice/phone.** Keep the optional Voice / Phone sections as
  "on the roadmap / not enabled" — they are not Day‑2 build stages.
- **FR‑8 — Redeploy + verify.** Redeploy to the same SWA and verify live: 200,
  CSP header intact, `app.js`/SVG load, dark default, toggle works, no
  finished‑app link present, six stages render, deep‑links resolve.

## Acceptance Criteria

- [ ] No link to the reference frontend app anywhere in `participant-runbook/`.
- [ ] API (`/docs`) and health buttons present and labelled as "your own build."
- [ ] Exactly six stage sections `#stage0…#stage5`; durations 45/90/60/75/60/60
      summing to **390 min**; agenda block shows 11:00–5:30 ET.
- [ ] Each stage deep‑links to its `labs/NN/README.md`.
- [ ] Stage 4 deep‑links to `labs/08-apim-gateway` (Consumption SKU).
- [ ] Sidebar shows "/ 6"; checklist persists per stage.
- [ ] Live SWA returns 200 with `script-src 'self'` CSP and renders correctly.

## Open Questions / Assumptions

- **Assumption:** Day‑2 = the full 11:00–5:30 ET window = 390 min, adopted from
  the invite. Breaks are woven into the agenda block, not subtracted from stage
  budgets (the stage minutes are the invite's own numbers).
- **Assumption (resolved by autopilot decision + user request):** keep all
  **six** stages; Stage 4 (APIM) is now a full lab (`labs/08-apim-gateway`) on
  the **Consumption** SKU, verified to support 20 concurrent builders in the
  Cloudforce sub (see `docs/apim-consumption-loadtest.md`).
