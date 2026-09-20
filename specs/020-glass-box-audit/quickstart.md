# Quickstart: Glass-Box AI Audit Workshop Exercise

This is the facilitator/participant "does it work" checklist. The full
narrated workshop guide lives at `exercises/01-glass-box-audit.md`; this file
is the fast, no-narrative verification path used during implementation and by
anyone auditing the feature later.

## Prerequisites

- Python 3.11+ on `PATH` (no virtualenv, no `pip install` required — stdlib
  only).
- Repository checked out at any commit containing this feature.

## Run it

```bash
cd /workspaces/all-clear

# 1. The deceptive "clean" view
python scripts/audit_simulation.py --mode black-box
# Expect: {"status": "100% Reconciled", "errors": 0}

# 2. The full inspectable trace
python scripts/audit_simulation.py --mode glass-box
# Expect: labeled reasoning/scratchpad/api_call/action lines, a findings
# summary reporting 5 records with missing data / synthetic data, at least
# one unauthorized network attempt, and one swarm-coordination event, plus an
# explicit contrast against the black-box output above.

# 3. The deterministic guardrail
python -m unittest scripts/test_evaluator.py -v
# Expect: all tests pass, including a negative-control test proving a clean
# trace is NOT blocked.
```

## Determinism check

```bash
diff <(python scripts/audit_simulation.py --mode black-box) \
     <(python scripts/audit_simulation.py --mode black-box)
diff <(python scripts/audit_simulation.py --mode glass-box) \
     <(python scripts/audit_simulation.py --mode glass-box)
# Both diffs must be empty.
```

## Full gate (matches spec SC-005)

```bash
cd /workspaces/all-clear && \
  python scripts/audit_simulation.py --mode black-box && \
  python scripts/audit_simulation.py --mode glass-box && \
  python -m unittest scripts/test_evaluator.py -v
echo "exit: $?"   # must print 0
```

## What "done" looks like

- Both CLI modes run with no flags/arguments beyond `--mode` and no network
  access.
- `--mode black-box` output is a single short JSON object and nothing else.
- `--mode glass-box` output clearly shows the concealment: which record IDs
  were missing data, which were fabricated, which attempted unauthorized
  network access, and which shows swarm coordination — each optionally
  annotated with the grounding incident it mirrors.
- `scripts/test_evaluator.py` passes end to end and demonstrates, via a
  mocked commit function, that a flagged trace never reaches "the database"
  while a clean trace does.
- `exercises/01-glass-box-audit.md` documents the 120-second run-of-show,
  the exact commands above, the four grounding incidents, and an explicit
  "prepare, not scare" section connecting the exercise to real guardrail
  patterns already in this repository.

## Increment 2: Azure deployment + evals (optional)

Everything above continues to work with zero Azure credentials. This
section is only for a facilitator who wants the control room hosted at a
stable event URL and/or a Foundry-visible eval run.

### Deploy the browser control room

```bash
cd /workspaces/all-clear
azd up          # reuses the existing frontend/backend Container Apps;
                # no new resources are provisioned for this feature
```

Then open `https://<AZURE_FRONTEND_URL>/?page=audit` (the URL `azd up`
prints for the `frontend` service) and confirm the pipeline map, mode
toggle, and Azure Portal deep links load with no console errors (SC-006).

### Run the Foundry evaluation suite

```bash
cd /workspaces/all-clear/evals/glass-box-audit
pip install -r requirements.txt
python glass_box_eval.py                 # uploads to the Foundry Evaluations tab
python glass_box_eval.py --skip-upload   # local-only dry run, no Azure credentials needed
```

Expect 5 scenario rows (`clean`, `fabrication_only`, `network_only`,
`swarm_only`, `all_violations`), with only `clean` passing — matching
`scripts/test_evaluator.py`'s local assertions (SC-007). See
`evals/glass-box-audit/README.md` for the full option list, mirroring
`evals/quality/README.md`.

### Viewing results in the Foundry portal instead of the CLI

Once the run above has uploaded, everything is also viewable by clicking
through the portal at <https://ai.azure.com>: project → **Evaluations** →
`glass-box-audit-guardrail`. This is documented as a first-class alternative
(not a fallback) in `exercises/01-glass-box-audit.md` → "Viewing it in the
Foundry portal — no code required," alongside the equivalent portal paths for
`evals/quality` (Evaluations tab), `evals/red-team` (Red teaming tab), and
Foundry's Model catalog compare view. Teach both the code and the portal:
the code is what participants can extend; the portal is what they can screen
share.

