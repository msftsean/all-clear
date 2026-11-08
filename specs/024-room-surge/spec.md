# Feature Specification: Room Surge (audience-sourced live surge)

**Feature Branch**: `024-room-surge`
**Created**: 2026-11-08
**Status**: Draft, with an untested head-start patch (see plan.md, "Verification status")
**Target event**: Azure Days Arlington, Day 1 Use Case Showcase (Tue Nov 17, 12:45), about 7 minutes
**Input**: "I'd like something dramatic for the showcase." The audience *is* the surge.
The backup demo (outbound approval call + multilingual caller) is a separate spec.

## Why

The single rehearsed call-in shows the pipeline but never shows the payoff the
slide promises: *many signals, few incidents, one clear board*. With one call,
deduplication is invisible. With the room reporting at once, the collapse from
dozens of Signals to a handful of Incidents happens live, from the audience's own
words, on their own phones.

## User Scenarios & Testing *(mandatory)*

### User Story 1: An attendee reports from their phone (P1)

An attendee scans the QR code on their table card (or on screen), lands on a
mobile page with no sign-in, reads their scenario, types (or dictates with the
phone keyboard) what they see, and submits. Within a few seconds the page tells
them whether their report opened a new Incident or joined an existing one, and
how many people in the room reported the same thing.

**Independent test**: Open `/report?card=A` on a phone-sized viewport, submit a
report while the surge is open, and see an acknowledgment with the Incident id
and the room report count.

**Acceptance scenarios**
1. Given the surge is open, when an attendee submits a 1 to 500 character report,
   then it runs through the unchanged three-agent pipeline (channel `report`) and
   the page shows `opened` or `joined`, the Incident id, and the room report count.
2. Given the surge is closed, when an attendee submits, then the page says the
   surge has not started or has ended (HTTP 409) and nothing is processed.
3. Given a device has already sent 3 reports in the last 60 seconds, when it sends
   another, then it is refused with HTTP 429 and a friendly message.
4. Given the content-safety filter blocks the text, then the attendee sees
   "Blocked by the safety filter" and the board's *blocked by safety* counter
   increments. Nothing is created.
5. Given a harm/crisis signal, then the existing crisis safety net escalates it to
   a human. The board counts it under *escalated to a person* and shows no text.

### User Story 2: The room watches the surge collapse on the big screen (P1)

The presenter puts `/surge` on the room display. It shows the QR code and short
URL, two large counters (Signals in, Incidents out), the collapse ratio, the
number of participating devices, *blocked by safety*, *escalated to a person*,
and one tile per Incident sized by its room report count and coloured by severity.
Tiles visibly grow as reports join.

**Independent test**: With the surge open, submit 20 reports from 3 scenarios;
`/surge` updates within about 1.5 seconds per report, and tiles show the counts.

**Acceptance scenarios**
1. The board never displays raw attendee text. Tiles show only machine-derived
   fields: Incident id, severity, queue, category and a PII-redacted, length-capped
   location extracted by QueryAgent.
2. The board polls `GET /api/surge/state` about once a second and degrades
   gracefully (keeps the last good state and shows "reconnecting") if a poll fails.

### User Story 3: The presenter controls the surge (P1)

The presenter (or a coach) opens, closes and resets the surge from the board using
a coach key. Attendees cannot control it.

**Acceptance scenarios**
1. `POST /api/surge/control` with `open`, `close` or `reset` requires header
   `X-Surge-Key` equal to `SURGE_COACH_KEY`. In live mode an unset key means control
   is disabled (fail closed, HTTP 403). Mock mode allows control without a key.
2. `reset` clears the room tally only. It never deletes Incidents, Reports or
   audit entries (Signals are never deleted, CONTEXT.md).

### User Story 4: Printable table cards (P2)

`/surge/cards` renders printable cards, each with a scenario and a QR code that
opens `/report?card=<id>`. Scenarios A to D are four shared real-world events
around Arlington, E is "your own small issue" (shows distinct SEV4 Incidents), and
R is the red card ("try to trick All Clear"), which feeds the safety and
deterministic-router talking points.

## Requirements *(mandatory)*

- **FR-001** Audience reports go through `AllClearPipeline.process_signal`
  unchanged. No new routing, severity or dedup logic. The card id is used
  for the room tally only and never influences routing (say this on stage).
- **FR-002** RouterExecutor stays zero-LLM. PII filtering, the crisis safety net,
  escalation and audit are untouched.
- **FR-003** Per-device rate limit: default 3 reports per 60 seconds
  (`SURGE_REPORTS_PER_WINDOW`, `SURGE_WINDOW_SECONDS`). The device id is a random
  id from the phone's localStorage. It is not an identity and is never shown.
- **FR-004** `GET /api/surge/state` returns counts and tiles only, never raw text.
- **FR-005** Mock mode stays viable: every endpoint works offline. Note: mock
  embeddings are bag-of-words, so free-typed paraphrases will NOT collapse in mock
  mode. The audience surge must run against the live deployment, and mock mode is
  the rehearsal and replay fallback.
- **FR-006** The room tally is per process. For the event, pin the backend
  container app to one replica (see plan.md). `state` reports a `replica` id so a
  split is visible.

## Success criteria

- **SC-001** 40 simultaneous reports across scenarios A to D collapse to at most
  6 Incidents in the live deployment (target: 4 plus the E-card singles).
- **SC-002** p95 report-to-acknowledgment under 8 seconds at 40 concurrent reports.
- **SC-003** Zero raw attendee text on the board (checked by test).
- **SC-004** The full existing backend suite and frontend build stay green.

## Out of scope

- Outbound calling and multilingual call-in (backup demo, separate spec).
- Cross-replica room tally (pin to one replica instead).
- Changes to the Day 2 lab.
