# Run of show: Room Surge — seven minutes

**Stage**: **TODAY 2026-11-17 13:00 Eastern**
**Branch**: `event/arlington-2026-11-18` | **Revision**: R3, 2026-11-17 10:15 ET
**Source**: [spec](spec.md), [plan/gates](plan.md), observed local evidence
**Status**: 🟨 `███░░░░░░` **3/9 readiness gates**; live **NOT CERTIFIED**

## Before projection

- Operator and presenter must record G2–G8 before calling this a live GO.
  Live testing and MCAPS 2026 separate-audience subscription choice are
  authorized, and NEW audience resource/app-secret creation is approved.
  Exact inventory, build/configuration and live acceptance remain unverified;
  plan publication precedes execution. Historical corporate-tenant login is
  not today's path; existing secrets/private redteam remain untouched.
- By 12:10 choose live vs verified fallback; by 12:30 freeze tested revision,
  run-through, safe reset/closed board, real phones and fallback.
- At 12:45 check correct frontend/revision and join origin; projector displays
  `/surge` **CLOSED**, no raw text. Operator privately controls the same backend.
  No key-bearing URL in slides, QR, chat, shell recording, screenshots or links.
  Use the implemented/tested Operator controls → Coach key → Set key path;
  URL stripping/sessionStorage alone is not secure delivery.
- Cards A–D span tables; one E/R as appropriate. Scan actual printed cards.
  Pre-open and test a replay (`/?demo=loaded`) or sanitized capture on a known
  working build, preferably local if venue/cloud reliability is uncertain.
  Backup voice/multilingual demo is optional only if independently rehearsed.

## Show clock (13:00–13:07 ET)

| Elapsed | Beat / operator | Presenter wording |
|---|---|---|
| 0:00–0:45 | Problem; board closed | “Forty people can report the same event. We keep every report while showing responders the underlying incidents.” |
| 0:45–1:15 | Explain cards and privacy | “Same events, your own words. No names, phone numbers or personal details. This is a demo, not an emergency service.” |
| 1:15–2:30 | Operator opens; audience reports for about 60s | “Scan and report now.” Let counts build; if coaches seed, disclose it. |
| 2:30–3:15 | Explain actual observed counts | “These signals became these incident tiles. Each attached report remains attributable.” Do not promise four incidents regardless of outcome. |
| 3:15–4:00 | Red-card/authority beat | “Some inputs may be blocked; others still take the normal rules-based route. Severity, SLA and escalation are deterministic—not granted by a prompt.” Describe only the actual result. |
| 4:00–5:00 | Operator closes; inspect pre-reviewed safe decision receipt | Show severity, SLA, rules, escalation/approval and source citations. No attendee text or PII on screen. |
| 5:00–6:30 | Value | “The payoff is a clear operational picture without throwing reports away.” Distinguish room report counts from persistent incident magnitude. |
| 6:30–7:00 | Bridge | “Tomorrow you can build this.” Leave intake closed. |

## Honesty and stage stop conditions

- Card letters **never** reach routing. No card buckets or global threshold
  manipulation; collapse must come from actual classification/embeddings and
  deterministic dedup.
- R does not guarantee a safety block. Do not fake blocked outcomes; fixed
  routing authority must hold whether content safety blocks or allows a probe.
- Crisis/no-incident escalation appears in the global person counter;
  incident-bearing escalation is marked on its tile. Do not claim the global
  counter covers every escalation.
- Joined receipts can refer to retained rehearsal incidents. Reset clears only
  room tallies, never incidents/reports/audit. State this if relevant.
- If health/proxy/model access fails, replica changes, responses stall past
  measured acceptance, or unsafe/raw output appears: **close and switch**.
  Do not debug Azure or change safety/settings in front of the room.

## Fallback ladder (must be tested before freeze)

1. Confirmed live audience deployment, only if all release gates pass.
2. Verified replay on working build (`/?demo=loaded`) or sanitized capture.
   Say “This is the replay,” and disclose any seeded reports.
3. Offline mock flow with near-duplicate wording, explicitly labeled offline;
   broad paraphrases do not collapse with bag-of-words mocks.
4. If none works, explain architecture using verified artifacts; do not claim
   an untested outbound/multilingual demo or failed live surge succeeded.

## After rehearsal and after show

Close → drain admitted/in-flight work → reset tally → close → confirm repeated
`open=false`, zero counters and empty tiles on stable replica. Preserve all
operational records. Clear private coach session on shared devices. Record
sanitized results and selected fallback/version in [tasks.md](tasks.md);
do not reopen intake unless deliberately running another authorized window.
