# History

## Project Context

All Clear is a bounded-authority incident-triage accelerator requested by
MARYLAND ADMIN 01.

## Learnings

## 2026-09-20 — Participant curriculum alignment

- The canonical participant constitution is `.specify/memory/constitution.md`;
  `shared/constitution.md` references were stale after the migration.
- The event workbook is now framed as six required blocks totaling 315 minutes
  of work plus 75 minutes of breaks, for a 390-minute window.
- Deployment, APIM, MCP, voice, phone, and reflection material are explicitly
  optional; required blocks link directly to the lab files participants should
  open.
- Lab 03 now teaches specification and review of implementation guidance rather
  than promising production-ready generated code or an arbitrary compliance
  percentage.
- **2026-09-20 — Curriculum flow evidence for Kranz's DELIVERY_PLAN.md**
  (requested by MARYLAND ADMIN 01, full report filed at
  `.squad/decisions/inbox/lovell-event-path.md`):
  - `participant-runbook/index.html` defines the canonical 390-minute Day 2
    agenda: S0 (Lab00+03, 45 min) → S1 (Lab01+05, 90 min) → S2 (Lab04, 60 min)
    → S3 (Lab07+02, 75 min) → S4 (Lab08, 60 min) → S5 (Lab06, 60 min), plus
    optional GH (Lab09) and appendices A1/A2 (voice/phone).
  - **Ordering bug:** runbook schedules Lab05 (S1) before Lab04 (S2), but
    `labs/05-agent-orchestration/README.md` prerequisite is "Lab 04
    completed," and Lab04's own prerequisite is "Labs 01 and 02 completed"
    while Lab02 is scheduled even later (S3). Needs Kranz's resolution
    (swap S1/S2 or explicitly narrate the deferral).
  - **Timing mismatch:** `labs/README.md`'s phase table, each lab's own
    header duration, and the runbook's compressed per-stage minutes disagree
    for Labs 01 (45/90/shared-90), 04 (60/120/60), 05 (90/120/shared-90), and
    06 (60/90/60). Lab08's 60 min is the one fully self-consistent duration.
  - Named exercises found: Lab01 "1a: Signal Classification" / "1b: Prompt
    Engineering"; Lab03 "03a: Write a Spec" (25 min) / "03b" (20 min, sums to
    the lab's stated 45 min — internally consistent); Lab05 "05x: Voice &
    Phone Extensions" (labeled Optional) and "05y: Model Continuity Under
    Failover" (not labeled optional — ambiguity flagged for the plan).
  - Recommended required/optional cut mirrors Haise's and Swigert's prior
    inbox notes: mock-mode spine 00→03→01→04→05→07 required; Lab02, Lab06,
    Lab08's deep-dive checkpoints, Lab09, Exercise 05x/05y, and appendices
    A1/A2 optional or coach-led.
