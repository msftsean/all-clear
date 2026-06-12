# Deck 2 — Environment Prep for Day 2

**Speakers:** Sean Gayle (Principal Solution Engineer) & Adrian Wright (Sr. Solution Engineer)
**Slot:** Day 1 · 4:15 – 5:15 PM ET · 11 slides
**Output file:** `ISV_Summit_EnvPrep.pptx`
**House style:** Antimetal — see `../design/DESIGN-antimetal.md` and `README.md` in this folder.
**Through-line:** Tomorrow is hands-on. *"Great — but what do we do next?"* → **be ready to build.**
Walk out of this room with a green checkmark on every prerequisite so Stage 0 starts on time.

> **Design rhythm:** Slides 1 and 11 are **navy hero** (dark gradient, serif display, white).
> Everything else is the **light technical surface** (canvas `#f8f9fc`, white cards, 1px blue
> shadow-ring border, 20px radius). One chartreuse accent per slide. Midnight Navy text, never black.
> Numbered-step lists use circled numerals connected by a thin connector line.

> **Ground truth this deck rests on (don't drift from it):**
> - Day 2 = **six stages, one repo, one deployed URL**: S0 45m · S1 90m · S2 60m · S3 75m · S4 60m ·
>   S5 60m = **390 min**, 11:00 AM – 5:30 PM ET.
> - Everything runs in **GitHub Codespaces** (Python 3.11+, Node 18+, deps + Copilot pre-installed) —
>   **no local install required**.
> - **`azd up` provisions everything**; the manual CORS/port checklist is the fallback lane.
> - Stage 4's gateway uses **APIM Consumption SKU** — load-tested at **20 simultaneous creates,
>   20/20 succeeded, ~3.5 min, $0**. Everyone gets their own gateway; no quota anxiety.

---

## Slide 1 — Title

- **Layout:** Full-bleed **navy hero gradient** (`#001033 → #0050f8 → #5fbdf7`). Centered.
- **Eyebrow:** SHIP IT! · ISV SUMMIT · DAY 1 · ENVIRONMENT PREP
- **Title (serif, white):** Environment Prep for Day 2
- **Subtitle:** Get every prerequisite green tonight so we start building at 11:00 sharp
- **Footer:** Sean Gayle & Adrian Wright · June 16, 2026
- **Design note:** Two presenter names balanced on the footer row; thin chartreuse rule under title.

---

## Slide 2 — Agenda

- **Layout:** Light surface. **Six numbered rows** (circled numerals + label).
- **Rows:**
  1. **End state** — what "ready" looks like across the six stages
  2. **Hard requirements** — Azure, GitHub, and the nice-to-haves
  3. **Foundry project setup** — model + retrieval, six steps
  4. **Codespaces setup** — your whole dev box in the browser, six steps
  5. **Tooling checklist** — the eight boxes to tick
  6. **Common blockers** — what breaks, why, and the fix
- **Design note:** Last row (blockers) can carry the chartreuse accent — it's the "save your morning"
  payoff.

---

## Slide 3 — End State (six stages, with times)

- **Layout:** **Six stage cards** (Stage 0 – Stage 5) in a 2×3 or 3×2 grid. Each card: stage number
  (navy circle), title, **time allocation badge**, one-line outcome.
- **Cards:**
  - **Stage 0 · 45 min** — *Scaffold ready.* Spec'd repo, multi-agent dev env wired, first eval stub
    passing in your Codespace.
  - **Stage 1 · 90 min** — *Working agent.* On Agent Framework — model, tools, orchestration, and the
    human-approval gate.
  - **Stage 2 · 60 min** — *Agentic retrieval.* Multi-source grounding over articles, policies, and
    records via Foundry IQ.
  - **Stage 3 · 75 min** — *Discoverable tools.* Exposed through an MCP server, with a red-team pass.
  - **Stage 4 · 60 min** — *AI gateway.* APIM in front: rate limits, token budgets, JWT, full
    observability.
  - **Stage 5 · 60 min** — *Shipped.* Deployed on Azure Container Apps with the **eval suite gating
    CI**.
- **Footer line:** "390 minutes. One repo. One deployed URL. Every attendee leaves with a running
  agent."
- **Design note:** Time badges are the visual anchor — make them prominent pills.

---

## Slide 4 — Hard Requirements

- **Layout:** **Three columns** with check (✓) / cross (✗) marks. Headers: **Azure Access**,
  **GitHub**, **Nice-to-Have**.
- **Azure Access (✓ required):**
  - ✓ Azure subscription with **Contributor** rights
  - ✓ **Azure OpenAI** access — chat model (gpt-4.1 / gpt-5.1) + embeddings
  - ✓ **Azure AI Search** available in your region
  - ✓ Quota in **East US** (or coach-provided shared credentials)
- **GitHub (✓ required):**
  - ✓ GitHub account
  - ✓ **Active GitHub Copilot** subscription
  - ✓ Access to **`EstablishedCorp/all-clear`** repo
  - ✓ **Codespaces** enabled on your account
- **Nice-to-Have (✗ not required tomorrow):**
  - ✗ `az` CLI + `azd` installed locally
  - ✗ Docker Desktop (Codespaces handles it)
  - ✗ Microphone (only for the optional voice exercise)
  - ✗ Second monitor (just nicer)
- **Callout:** "If a row is red for you, see Adrian at the break — we have shared credentials."
- **Design note:** Green ✓ on required columns; muted-grey ✗ (not red) on nice-to-haves so it reads
  "optional," not "broken."

---

## Slide 5 — Foundry Project Setup

- **Layout:** **Six numbered steps** with a connector line (left-to-right or top-down).
- **Steps:**
  1. **Create / select an Azure AI Foundry project** (hub + project) in East US
  2. **Deploy the chat model** — gpt-4.1 (or gpt-5.1); note the deployment name
  3. **Deploy an embeddings model** — `text-embedding-3-large` for retrieval
  4. **Add an Azure AI Search connection** — this powers Stage 2 / Foundry IQ
  5. **Capture endpoint + auth** — endpoint, deployment name, API version
     `2025-04-01-preview` (prefer Entra ID over keys where you can)
  6. **Drop values into `.env`** — `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT_NAME`,
     `AZURE_SEARCH_ENDPOINT`, then **verify with a health call**
- **Callout:** "`azd up` wires most of this for you tomorrow — this slide is so you understand what's
  under the hood (and can fix it if a value is wrong)."
- **Design note:** Step 6 (the verify) carries the chartreuse accent — it's the "you're done"
  moment.

---

## Slide 6 — Codespaces Setup

- **Layout:** **Six numbered steps**, **teal circles** (per the user's spec for this slide), connector
  line.
- **Steps:**
  1. **Launch** — go to `EstablishedCorp/all-clear` → green **Code** button → **Codespaces** tab →
     **Create codespace on main**
  2. **Wait for the prebuilt env** — Python 3.11+, Node 18+, all deps, Copilot extension, ready to go
  3. **Verify** — `python --version`, `node --version`; `pip list | grep fastapi`
  4. **Configure CORS** — set `CORS_ORIGINS` in `backend/.env` to your
     `https://$CODESPACE_NAME-5173.app.github.dev` / `-8000` URLs
  5. **Start the backend + make port 8000 public** —
     `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`, then
     `gh codespace ports visibility 8000:public`
  6. **Start the frontend + smoke-test** — `npm run dev`, open port **5173**, submit a test signal
     ("Power line down across Main St…") → expect an incident ID, severity, queue
- **Callout:** "No local installs. Your whole dev box is a browser tab — same environment for every
  person in the room."
- **Design note:** Teal circles distinguish this from the Foundry steps (navy) on Slide 5. Step 6 =
  chartreuse accent (the green-light smoke test).

---

## Slide 7 — Tooling Checklist

- **Layout:** **2×4 checkbox grid** (eight boxes). Each: checkbox + tool + one-word role.
- **Boxes:**
  - ☑ **GitHub account** — identity
  - ☑ **GitHub Copilot** — pair programmer
  - ☑ **Codespaces** — your dev box
  - ☑ **Modern browser** (Chrome / Edge / Firefox) — everything runs here
  - ☑ **Azure subscription / access** — where it deploys
  - ☑ **Azure OpenAI + AI Search** — model + retrieval
  - ☑ **`azd` (optional, local)** — one-command deploy
  - ☑ **Microphone (optional)** — voice exercise in Stage 1+
- **Footer line:** "Tick all eight tonight. Six are required, two are optional — know which is which."
- **Design note:** Required boxes pre-checked in green; optional two in a lighter tint with
  "(optional)" tag.

---

## Slide 8 — Common Blockers

- **Layout:** **Three-column table** — **Issue / Cause / Fix** — **five rows**.
- **Rows:**
  | Issue | Cause | Fix |
  | ----- | ----- | --- |
  | CORS errors in the browser console | Port 8000 private, or wrong `CORS_ORIGINS` | Set port 8000 **public**; add your `$CODESPACE_NAME` URLs to `CORS_ORIGINS`; restart backend |
  | "Failed to fetch" / service unavailable | `VITE_API_BASE_URL` is set | Leave it **empty** so `/api` proxies through Vite; hard-refresh |
  | API calls 500 through the frontend | Vite proxy hitting IPv6 `::1` | Point proxy target at **`127.0.0.1:8000`** in `vite.config.ts` |
  | Copilot not suggesting | Not signed in / no active subscription | GitHub: Sign In; confirm Copilot is active; reload window |
  | Codespace slow or timed out | 30-min idle timeout / resource pressure | Resume from github.com/codespaces; rebuild container; restart servers |
- **Callout:** "And on Azure quota: Stage 4's gateway is **APIM Consumption** — we tested **20 people
  creating one simultaneously: 20/20 succeeded, ~3.5 min, $0.** You won't run out."
- **Design note:** Keep the table airy; the APIM callout sits in a chartreuse-edged info box below —
  it's the confidence-builder.

---

## Slide 9 — Q&A / Live Troubleshooting

- **Layout:** **Three panels** side by side.
- **Panels:**
  - **If you're blocked** — "Raise a hand or drop it in the chat. Sean & Adrian are circulating.
    Don't burn 20 minutes silently."
  - **If you're green** — "Run the Stage 0 smoke test now: submit a signal, confirm you get an
    incident ID back. Then help a neighbor."
  - **If you need access** — "No Azure sub or quota? We have **shared coach credentials** and a
    mock-mode lane (`MOCK_MODE=true`) so you can build everything but the live model calls."
- **Design note:** Three equal cards; the "If you need access" panel carries the chartreuse accent
  (it removes the #1 anxiety).

---

## Slide 10 — Day 2 Timeline

- **Layout:** **Time-stamped event row** with connectors (a horizontal timeline). All times ET.
- **Timeline:**
  - **11:00** — Doors / setup check (everyone green before we start)
  - **11:00 – 11:45** — **Stage 0** · Scaffold + first eval stub
  - **11:45 – 1:15** — **Stage 1** · Working agent on Agent Framework
  - **1:15 – 2:15** — **Stage 2** · Agentic retrieval (Foundry IQ)
  - **2:15 – 3:30** — **Stage 3** · MCP server + red-team
  - **3:30 – 4:30** — **Stage 4** · APIM AI gateway
  - **4:30 – 5:30** — **Stage 5** · Deploy on ACA, eval suite gates CI
  - **5:30** — **Shipped** — deployed URL, working repo, eval suite in CI
- **Footer line:** "Breaks float between stages — but the clock is real. Starting green is how we
  finish on time."
- **Design note:** Put a chartreuse marker on the **5:30 "Shipped"** node — that's the finish line.

---

## Slide 11 — Closing

- **Layout:** Return to the **navy hero gradient**. Centered.
- **Headline (serif, white):** Come back tomorrow ready to build.
- **Line:** Green checkmarks tonight = a deployed agent by 5:30.
- **Primary CTA (chartreuse pill):** Stage 0 starts 11:00 AM ET
- **Footer:** Sean Gayle · Adrian Wright · Ship It! ISV Summit
- **Design note:** Mirrors Deck 1's closing — chartreuse CTA is the single hero element on the navy
  field.
