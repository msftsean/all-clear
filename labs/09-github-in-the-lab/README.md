# Lab 09 — GitHub-in-the-Lab Path

This lab operationalizes the workshop path: fork, run Actions, make one bounded extension with Copilot, and keep tests green.

## Outcomes

1. Run `smoke-test.yml` in your fork.
2. Complete one extension exercise:
   - Add one bounded ActionAgent tool, **or**
   - Add one scenario pack.
3. Turn the starter test from red to green.

## Step 1: Fork and run CI

1. Fork `EstablishedCorp/all-clear`.
2. Push any branch to your fork.
3. Open **Actions** and run `smoke-test.yml`.

## Step 2: Pick an extension exercise

Choose one:

1. **Tool path** — add one ActionAgent tool with bounded authority and docs.
2. **Scenario path** — add one deterministic scenario pack with mock-mode parity.

Keep RouterExecutor deterministic and untouched.

## Step 3: Run the starter test

The starter test is in `labs/09-github-in-the-lab/test_starter_red_to_green.py`.

- It intentionally starts red.
- Make your exercise change.
- Re-run until green.

## Suggested command

```bash
cd labs/09-github-in-the-lab
python -m pytest -q test_starter_red_to_green.py
```

