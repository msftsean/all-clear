# Lab 09 — GitHub-in-the-Lab Path

This lab operationalizes the workshop path: fork, run Actions, make one bounded extension with Copilot, and keep tests green.

## Outcomes

1. Run `smoke-test.yml` in your fork.
2. Complete one extension exercise:
   - Add one bounded ActionAgent tool, **or**
   - Add one scenario pack.
3. Turn the starter test from red to green.

## Step 1: Fork and run CI

1. Fork `Public-sector-hacks-Org/all-clear`.
2. Push any branch to your fork.
3. Open **Actions** and run `smoke-test.yml`.

The workflow is the repository's offline smoke gate. It sets mock-mode
environment variables, installs backend requirements, installs frontend
dependencies, then runs `npm run smoke-test`. That script runs the backend
pytest suite with `PYTHONPATH=.` and the frontend unit tests with Vitest. It
does not require Azure credentials and runs on pushes, pull requests, and
manual workflow dispatches.

## Step 2: Pick an extension exercise

Choose one:

1. **Tool path** — add one ActionAgent tool with bounded authority and docs.
2. **Scenario path** — add one deterministic scenario pack with mock-mode parity.

Keep RouterExecutor deterministic and untouched.

## Step 3: Run the completion verifier

The completion verifier is in
`labs/09-github-in-the-lab/test_starter_red_to_green.py`.

- Add or edit a bounded artifact under `participant_extension/`.
- Add tests for that artifact in the same directory.
- The verifier proves both files exist and runs the artifact's own tests in a
  subprocess. It deliberately ignores `ALL_CLEAR_LAB09_COMPLETE`; an
  environment variable alone cannot complete the lab.

## Suggested command

```bash
cd labs/09-github-in-the-lab
python -m pytest -q test_starter_red_to_green.py
```

The repository includes a small `participant_extension/` example so the gate
is executable immediately. Replace it with your own bounded ActionAgent tool or
scenario pack, keep its tests passing, and rerun the same command.
