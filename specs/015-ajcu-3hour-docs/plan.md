# Implementation Plan: AJCU 3-Hour Workshop Documentation Reframe (Reversible)

**Branch**: `014-agent-framework` (docs-only) | **Date**: 2026-06-01 | **Spec**: [spec.md](spec.md)

## Summary

Reframe five participant-facing docs from the **7-hour / 8-lab hackathon** format
to the **3-hour AJCU pre-conference workshop** (azd-first). The change is
**documentation only** — no app code, infra, `azure.yaml`, `scripts/*`, AJCU
challenge cards, or the six-intent taxonomy are touched.

This plan is also the **format-switch runbook**. The two formats are mutually
exclusive presentations of the *same* repo. Switching between them is a pure
documentation operation with the procedures in [§ Format Switch Runbook](#format-switch-runbook).

---

## The two formats

| | **7-hour hackathon** (original) | **3-hour AJCU workshop** (current) |
|---|---|---|
| Duration | 9:00 AM – 4:00 PM | 1:00 – 4:00 PM |
| Mental model | 8 sequential labs (00→07); provision near the end | `azd up` first, then build scenarios |
| README top | "Build this entire system in 8 hours" + lab table | "Start here": `azd up` + 3-lane table |
| Manual Codespaces/CORS | Primary Quick Start | Appendix (fallback only) |
| 8-lab table | Primary curriculum | "Optional deep-dive labs (take-home)" |
| Lab 00 | Required first step | "Skip if you ran `azd up`" |
| Lab 06 (deploy) | Last lab, prereq Lab 05 | "Step one, not the last lab" |
| FACILITATION.md | 7-hour, lab-by-lab, lunch block | 3-hour run-of-show, no lunch |
| Voice/phone (+1 913) demo | Standard segment | OPTIONAL/stretch |

---

## Baseline (the 7-hour snapshot — DO NOT LOSE)

The **canonical 7-hour version** of every in-scope file is preserved in git at the
commit **immediately before** the reframe commit on `014-agent-framework`.

- **7-hour baseline commit (record on commit):** `b9033a1`
  *(verify with `git log --oneline -- README.md | head` — it is the last commit
  that does NOT mention "AJCU 3-hour reframe").*
- The reframe is delivered as **one commit** titled
  `docs(ajcu): reframe participant docs for 3-hour AJCU workshop (reversible)`.
  Its **parent** is the 7-hour baseline. This guarantees a clean, lossless revert.

> Because the 7-hour content lives in history (not deleted, not overwritten in a
> way git can't recover), switch-back is a `git checkout <baseline> -- <files>`
> and needs no manual re-authoring.

---

## In-scope files & the exact edits (change matrix)

| # | File | 7-hour → 3-hour edit | Revert anchor |
|---|------|----------------------|---------------|
| 1 | `README.md` | (a) Replace "Boot Camp Labs Overview / Build this entire system in 8 hours" intro with a **"🚀 Start here (3-hour AJCU workshop)"** section: `azd auth login` → `azd up`, note postprovision auto-seed. (b) Add **3-lane table** (Self-serve `azd` = default, Shared backend, Mock) linking HEADSTART. (c) Move the 8-lab table BELOW start, re-title **"Optional deep-dive labs (self-paced, after the workshop)"** + "you do NOT need these today". (d) Move the Codespaces/CORS/venv/VITE/IPv4-IPv6 Quick Start into **"Appendix: Manual local setup (only if not using azd)"** at the bottom — content unchanged. (e) Update footer "Last Updated" + changelog line. | Lab table heading text; "Appendix: Manual local setup" anchor; footer date. |
| 2 | `docs/quickstart/HEADSTART.md` | Mark **Lane 2 (Self-serve `azd`) as DEFAULT/recommended** for the workshop; add one top sentence that the postprovision hook auto-seeds the index so "scenario-ready" is reached when `azd up` finishes. Keep the "Scenario-ready when…" checklist. | "Pick your lane" table; the default tag. |
| 3 | `labs/00-setup/README.md` | Add a top **callout**: "If you ran `azd up`, you can skip this — the 11-step Codespaces/CORS checklist is only for the manual local lane." Steps remain below. | Top callout block. |
| 4 | `labs/06-deploy-with-azd/README.md` | Add a top **callout**: "In the 3-hour AJCU workshop, `azd up` is step one, not the last lab — see the README Start-here section." Soften `Prerequisites: Lab 05 completed` → optional/none. | Top callout; Prerequisites cell. |
| 5 | `coach-guide/FACILITATION.md` | Replace the **"## 7-Hour Timeline (9:00 AM - 4:00 PM)"** section and its lab-by-lab blocks with the **3-hour run-of-show** (table from spec). **Preserve** the "Coach Escalation Playbook", Room Setup, Intervention Framework, Contingency, Self-Care, Post-Event sections. Mark the +1 913 voice/phone demo OPTIONAL/stretch. | Timeline section header; escalation playbook (kept). |

**Format-agnostic (unchanged in both formats):** the six AJCU challenge cards,
the six-intent taxonomy, crisis-safety wording, version matrix, API reference,
architecture diagrams, cost tables, the actual `scripts/`, `azure.yaml`, bicep.

---

## Format Switch Runbook

> All commands are run from the repo root. These are **doc-only** operations and
> never touch code, infra, or scenarios.

### A) Switch BACK to the 7-hour hackathon format (revert this reframe)

**Preferred — restore the 7-hour docs from the baseline commit:**

```bash
# 1. Identify the 7-hour baseline (parent of the reframe commit). It is recorded
#    above as b9033a1; confirm it still holds 7-hour content:
git log --oneline -- README.md | head

# 2. Restore the five in-scope docs to their 7-hour version:
git checkout b9033a1 -- \
  README.md \
  docs/quickstart/HEADSTART.md \
  labs/00-setup/README.md \
  labs/06-deploy-with-azd/README.md \
  coach-guide/FACILITATION.md

# 3. (Optional) also restore the on-site run-of-show page to the 7-hour beats,
#    if the site is being used for a 7-hour event:
#    git checkout b9033a1 -- hackathon-site/src/pages/RunOfShow.tsx

# 4. Verify nothing else changed, then commit:
git status --short
git commit -am "docs(hackathon): switch documentation back to 7-hour format"
```

**Verify the switch-back:**
- README's first actionable section is the 8-lab Quick Start (not azd-first).
- `coach-guide/FACILITATION.md` shows "## 7-Hour Timeline (9:00 AM - 4:00 PM)".
- AJCU cards unchanged (always true): `git status` clean under
  `labs/05-agent-orchestration/scenarios/ajcu/`.

### B) Switch FORWARD to the 3-hour AJCU format (re-apply this reframe)

If you previously reverted to 7-hour and want the 3-hour framing again, restore
the docs from the **reframe commit** instead:

```bash
# REFRAME_SHA = the commit titled "reframe participant docs for 3-hour AJCU workshop"
git log --oneline -- README.md | head        # find REFRAME_SHA
git checkout <REFRAME_SHA> -- \
  README.md \
  docs/quickstart/HEADSTART.md \
  labs/00-setup/README.md \
  labs/06-deploy-with-azd/README.md \
  coach-guide/FACILITATION.md
git commit -am "docs(ajcu): switch documentation to 3-hour AJCU workshop format"
```

**Verify:** Acceptance Criteria AC1–AC4 in [spec.md](spec.md).

### C) Manual fallback (if git history is unavailable)

Use the **change matrix** above as a checklist — every row names the exact
heading/anchor to add (3-hour) or remove (7-hour). The 7-hour timeline content
and lab framing are fully described by the matrix + the spec's run-of-show table,
so either format can be reconstructed by hand.

---

## Validation

1. **Smoke (scenario plumbing intact):**
   ```bash
   cd backend && PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/ajcu/smoke_test.py
   ```
   Expect `6/6 challenges passed` (deterministic; no Azure needed).
2. **AJCU cards untouched:**
   `git status --short labs/05-agent-orchestration/scenarios/ajcu/` → empty.
3. **Acceptance Criteria AC1–AC7** in [spec.md](spec.md).

## Risks & Mitigations

- **Risk:** future doc edits drift the recorded baseline SHA. **Mitigation:** the
  runbook also shows how to re-find the baseline via `git log --oneline -- README.md`.
- **Risk:** someone deletes 7-hour content thinking it's stale. **Mitigation:**
  this plan + git history are the system of record; the change matrix lets a
  human rebuild either format losslessly.
