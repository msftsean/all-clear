# Contract: Content Map (Section → Source)

This content site has no network API; its "contract" is the mapping from each rendered **Section** to its
**authoritative source** in the repo. Content MUST be presented faithfully from these sources (FR-002);
this table is the drift-control contract and is asserted by a content test (each `Section.source` must
resolve to a real file).

| Section `id` | Nav title | Source of truth | What is surfaced |
|--------------|-----------|-----------------|------------------|
| `prepare` | Prepare | `coach-guide/FACILITATION.md` → "Room Setup Checklist" (Physical, Technical, Materials, Pre-Flight) | The pre-arrival checklists as scannable, unchecked lists. |
| `timeline` | Timeline | `coach-guide/FACILITATION.md` → "7-Hour Timeline (9:00 AM – 4:00 PM)" + "Coach Escalation Playbook" | The day's schedule and the Azure-access triage sequence. |
| `framing` | Framing | `coach-guide/ajcu-framing.md` | The 60-second mission pitch (cura personalis) and the six-intent rationale. |
| `help` | Help Participants | `docs/quickstart/HEADSTART.md` (three lanes + scenario-ready) | Shared-backend / self-serve azd / mock lanes and the "scenario-ready" definition, with a link to the full HEADSTART guide. |
| `troubleshooting` | Troubleshooting | `coach-guide/TROUBLESHOOTING.md` | Common Lab 00+ issues as symptom → cause → quick fix (<5 min). |
| `assess` | Assess | `coach-guide/ASSESSMENT_RUBRIC.md` + `coach-guide/TALKING_POINTS.md` | Rubric criteria summary + phase-transition talking points, linking to the full guides. |

## Faithfulness rules

- The site MAY reformat (lists, cards, headings) and lightly tighten wording for the web, but MUST NOT
  introduce new facilitation policy, change timings, or alter the escalation guidance.
- Where the source is long (rubric, talking points), the site MAY summarize and MUST link to the full
  markdown for depth.
- Each `src/content/*.ts` module MUST declare `source: '<path>'` matching this table.

## Test obligation

A content test (unit or part of e2e setup) iterates the six sections and asserts:
1. `source` resolves to an existing repo file.
2. `blocks` is non-empty.
3. All six `id`s in this table are present exactly once.
