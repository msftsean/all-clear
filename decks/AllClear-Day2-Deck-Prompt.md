# Deck-generation prompt — All Clear, Maryland Azure Days (Day 2)
# 45-minute, two-part talk · English · 1 live Copilot CLI demo + slides

Paste everything inside the fenced block into Manus, OpenDesign, or Claude (Design/Artifacts).

```
ROLE
You are a senior presentation designer and developer-experience writer. Produce a presenter-ready slide deck (~16 slides) for a single 45-minute, hands-on workshop talk delivered live in TWO parts. Include concise speaker notes on every slide and a running time budget so the speaker can stay on pace.

EVENT CONTEXT
- Event: Azure Days for Government (Maryland State & Local Government), Day 2.
- Venue/date: Maritime Conference Center, Linthicum, MD — June 24, 2026.
- Format: a 45-minute talk that frames a hands-on hackathon. Audience = State, Local & Education (SLED) builders: public safety, 311/911 city ops, water/utilities, transportation, courts, higher ed. Policy- and CJIS-minded; mostly mid-level developers and architects, not AI specialists.
- Speaker/host: Sean Gayle (Microsoft / Cloudforce). Same-day production CTA references "Sean & Tracy's team."
- Deck language: English.

TALK SHAPE (STRICT — 45 minutes, two parts)
- Opening (~3 min)
- PART 1 — "The Lab & All Clear: what it is, its parts, and how to run it" (~20 min)
- PART 2 — "The Tools: GitHub Copilot CLI, Codespaces, Microsoft Foundry, Microsoft Agent Framework" (~20 min). Part 2 includes ONE short LIVE DEMO of GitHub Copilot CLI; the other three tools are explainer slides.
- Close (~2 min)

THE PRODUCT THE LAB BUILDS ON: "All Clear"
- One line: "Many signals. Few incidents. One clear board." All Clear is surge-grade incident triage.
- The problem (hero scenario = a SURGE): when a storm, outage, cyber alert-storm, or recall makes dozens of people report the same thing, responders drown in duplicate noise.
- What it does: inbound SIGNALS (chat, voice, phone, submitted reports) are classified, DEDUPLICATED against open INCIDENTS, assigned a SEVERITY + SLA, and acted on — so the responder queue stays proportional to real incidents, not signal volume. A live map (the "ClearBoard") shows incident pins visibly MERGE as duplicate reports attach, and flips green at the terminal "all clear" state.
- Built on the Microsoft Agent Framework (MAF). It is the production pivot of a prior app called "47 Doors."

THE PIPELINE (use this exact shape in a diagram)
QueryAgent (classify only) -> RouterExecutor (DETERMINISTIC, ZERO LLM calls) -> ActionAgent (acts only via 3 tools: create_incident, search_knowledge, generate_sitrep). Response flows back out to the ClearBoard.

THE PARTS OF ALL CLEAR (use for the "parts" slide)
- The 3-agent pipeline (above), running on MAF.
- The ClearBoard — the live situational-awareness map/board where pins merge on dedup.
- Backend — Python / FastAPI hosting the MAF pipeline.
- Frontend — React / TypeScript (the ClearBoard + briefing UI).
- Knowledge / RAG — Azure AI Search index of runbooks & SOPs powering grounded, cited sitreps.
- Channels — chat, voice, phone, and submitted reports all enter the SAME pipeline.
- Mock mode — the whole pipeline runs OFFLINE and deterministically with no Azure credentials (this is how the lab is graded).

DOMAIN VOCABULARY (use these exact words; one canonical term per concept)
- Signal = one inbound communication; never deduplicated away, always attributable.
- Incident = the real-world event signals describe; ID format AC-#### ; has severity, queue, SLA clock, magnitude, status.
- Report = attaching a signal to an incident; increments magnitude.
- Magnitude = count of reports on an incident; proxy for scale.
- Queue = destination work stream: field-operations, customer-comms, compliance-desk, engineering, escalations.
- Severity = SEV1 (life-safety / total outage / statutory clock; 15-min SLA; always escalates) down to SEV4 (informational; next business day). Rule-based, never "model vibes."
- Dedup = embedding-similarity match within the same intent category; >= 0.83 cosine ATTACHES to an open incident, below OPENS a new one.
- Sitrep = citation-grounded situation report from generate_sitrep; no citation, no claim.
- Surge = volume spike where most signals duplicate a few incidents. The hero scenario.
- All clear = terminal state: every incident resolved, every SLA met. Also the product name.

THE THREE GOVERNANCE RULES THAT OUTRANK EVERYTHING (the guardrails participants must NOT break)
1. Bounded authority — each agent does only what its role allows; enforced by code structure, not prompt hope.
2. Escalation is a safety control — SEV1 / statutory-clock incidents ALWAYS escalate; no model output can downgrade them. Weakening escalation is a security blocker, not a finding.
3. Truth over fluency — every factual claim cites a source record; classification uses typed structured output; when the system doesn't know, it says so and escalates.
PLUS: The RouterExecutor is UNTOUCHABLE — zero LLM calls by design and by test. No change may add a model call, randomness, or "smart" routing to it.

HOW TO RUN IT — THE PARTICIPANT PATH (use for the "how to run it" slides; time-boxed)
1. Confirm the environment in Codespaces and run mock mode offline (quick check).
2. Run the pipeline + a surge: watch dedup attach duplicate reports and the ClearBoard pins merge.
3. Lab 08 — APIM as the AI Gateway (Consumption tier): rate-limit, token-budget the LLM spend, require a JWT, wire telemetry to App Insights.
4. Lab 09 — GitHub-in-the-lab: fork -> run smoke-test.yml in Actions -> use Copilot to complete ONE bounded extension (add an ActionAgent tool OR add a Maryland scenario pack) -> turn the starter test from red to green.
5. Capstone "Make It Yours": capture your surge; download your record; review the lab-to-production handoff.

THE PASS/FAIL ORACLE (how a participant KNOWS they succeeded — emphasize this)
- The whole pipeline runs OFFLINE in deterministic "mock mode" — no Azure credentials needed to build or test.
- Backend test suite must stay 100% green in mock mode: `cd backend && MOCK_MODE=true PYTHONPATH=. python -m pytest tests/ -q` (currently 380 passing).
- CI gate: `smoke-test.yml` in GitHub Actions must be green.
- Nothing "counts" until the gate is green. This is the safety net that makes the hack low-risk.

WHAT'S NEW AND LIVE FOR TODAY (mention briefly; all shipped, tested, mock-mode safe)
- Maryland scenario packs (pick one — "see your own world"): SOC / Microsoft Sentinel alert-storm, 311/911 city ops, water-utility leak surge, traffic/transportation.
- Azure footprint & cost panel (clearly-labeled ESTIMATE; never fabricated pricing).
- Responsible-AI control map mapped to Maryland policy (SB 818, DoIT Responsible Use Policy).
- Capstone "Make It Yours" + lead capture (name, agency, three prompts: what's your surge? what signals flood you? what's the real incident underneath?).
- GitHub-in-the-lab path and a lab-to-production leave-behind.

=== PART 2 SOURCE MATERIAL: THE FOUR TOOLS (define each accurately) ===
- GitHub Copilot CLI — an agentic AI assistant that lives in your terminal. You talk to it in natural language and it can read and search the repo, edit files, run commands and tests, and carry out multi-step coding tasks using tools — keeping you in control. In this lab it is the build accelerator: it adds the bounded extension and drives CI to green. (This is the tool used for the LIVE DEMO.)
- GitHub Codespaces — cloud-hosted development environments: a full VS Code + dev container running in the browser, with zero local setup. The lab runs in Codespaces so every participant has an identical, ready-to-go environment. Launch via the repo's "Code -> Codespaces -> Create codespace."
- Microsoft Foundry (Azure AI Foundry) — Microsoft's platform to build, evaluate, and GOVERN AI: a model catalog and deployments, content filters, AI red-teaming, and evaluations. All Clear uses Foundry for its guardrails — a custom content filter, red-team scans, and evals on its model — which is how the responsible-AI story is proven, not just claimed.
- Microsoft Agent Framework (MAF) — Microsoft's framework/runtime for building AI agents and multi-agent workflows. All Clear is built on MAF: the three agents (QueryAgent, RouterExecutor, ActionAgent) are MAF constructs with bounded, role-specific tools. MAF is what makes "bounded authority" enforceable in code.

LIVE DEMO SPEC (Part 2, GitHub Copilot CLI — ~3-4 min, scripted + safe)
- Goal: show Copilot CLI doing real, deterministic work in the Codespace — no flaky live coding.
- Suggested happy path (pick ONE):
  (a) Ask Copilot CLI to run the mock test suite and confirm it's green: "Run the backend tests in mock mode and tell me the result." -> it runs pytest and reports "380 passed."
  (b) Red-to-green: open the Lab 09 starter test (intentionally failing), ask Copilot CLI to explain why it fails, then show it pass after the bounded change / env flag. 
- ALWAYS have a pre-recorded backup clip of the same demo in case of Wi-Fi/CLI issues. Add a small "DEMO" badge to this slide and a one-line fallback note in speaker notes.

OBJECTIVE OF THE DECK
In 45 minutes: (Part 1) make the audience understand what the lab is, the parts of All Clear, and exactly how to run it to a green finish; (Part 2) give them a working mental model of the four tools and SEE Copilot CLI in action. By the end they can start the hack confident and unblocked.

SLIDE-BY-SLIDE OUTLINE (~16 slides; keep the time budget visible)
OPENING (~3 min)
1. Title — "All Clear — Day 2: Build It, Run It, Prove It Green." Event, venue, date, speaker.
2. Agenda + the 45-min plan — Part 1 (the lab & All Clear) and Part 2 (the tools); one live demo.

PART 1 — THE LAB & ALL CLEAR (~20 min)
3. What is this lab? The mission: tame a SURGE; ship a small, governed extension and prove it green.
4. All Clear in 60 seconds — "Many signals. Few incidents. One clear board," with the surge problem.
5. The parts of All Clear — the 3-agent pipeline diagram + ClearBoard, backend, frontend, RAG, channels, mock mode.
6. Speak the language — the vocabulary table (signal / incident / report / dedup / severity / sitrep / surge / all-clear).
7. The rules that outrank everything — bounded authority, escalation-as-control, truth over fluency; and the untouchable zero-LLM RouterExecutor.
8. How to run it — the time-boxed path (Codespaces + mock mode -> run a surge -> Lab 08 -> Lab 09 -> capstone).
9. The oracle — mock mode + pytest 380 green + smoke-test.yml; "nothing counts until it's green."

PART 2 — THE TOOLS (~20 min)
10. Part 2 title + why these four tools — how Copilot CLI, Codespaces, Foundry, and MAF map onto the lab.
11. GitHub Copilot CLI — what it is and how it's used in the lab (the build accelerator).
12. LIVE DEMO — Copilot CLI in the Codespace (badge it "DEMO"; include the scripted steps + fallback note).
13. GitHub Codespaces — cloud dev environment, zero local setup; how to launch the lab.
14. Microsoft Foundry (Azure AI Foundry) — model catalog, red-team, evals, content filters; how All Clear proves its guardrails.
15. Microsoft Agent Framework (MAF) — the runtime All Clear runs on; the 3-agent shape and bounded authority.

CLOSE (~2 min)
16. Make It Yours + next step — capstone reflection ("what's your surge?") and the same-day CTA to engage Sean & Tracy's team. End on "All clear."

DESIGN & BRAND DIRECTION
- Aesthetic: a calm, government-credible "command center / situational awareness" look — NOT flashy startup gradients. Operations dashboard meets clean civic design.
- Palette: deep navy/blue base (calm, trust) with a single decisive incident-red accent for severity/alerts, and a clear "all-clear" green used sparingly for resolved / green-gate states. High contrast, accessible (WCAG AA).
- Motifs: a map/board with pins that MERGE (visualize dedup); severity chips (SEV1-SEV4); monospace for incident IDs (AC-####) and code/commands; a subtle "flips to green" metaphor on the oracle/success slides; a small "DEMO" badge on slide 12.
- Typography: one strong geometric/grotesk sans for headings, a clean humanist sans for body, monospace for code/IDs. Generous whitespace; one idea per slide; short scannable bullets; presenter expands verbally.
- Every slide: a crisp headline (5-8 words), 3-5 short bullets max, one visual anchor (diagram, chip row, table, icon), and a visible time cue.

CONTENT ACCURACY RULES (do not violate)
- Use the exact vocabulary and the exact pipeline shape above. Do not invent agents, tools, or steps.
- Do NOT fabricate dollar pricing; the cost panel is an ESTIMATE and must be labeled as such.
- Do not imply the RouterExecutor uses an LLM; it is deterministic by design.
- Define the four tools accurately per the source material above; do not overstate capabilities.
- Keep the tone respectful of a regulated/public-sector audience; emphasize governance, auditability, and human accountability.

DELIVERABLE FORMAT
- ~16 slides with per-slide speaker notes and a running time budget that sums to ~45 minutes.
- If the tool supports it, output editable slides (and offer an export). If it produces code/HTML, use a single self-contained, responsive layout.
- Provide a short title and one-line subtitle for the title slide.
```
