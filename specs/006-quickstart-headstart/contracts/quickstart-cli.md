# Contract: `scripts/quickstart.sh` CLI

The single entry point that takes a configured environment to "scenario-ready".
Also the exact command the `azure.yaml` `postprovision` hook invokes.

## Synopsis

```text
scripts/quickstart.sh [--mock] [--no-smoke] [--data-dir <path>] [-h|--help]
```

## Flags

| Flag | Default | Meaning |
|---|---|---|
| `--mock` | off | Offline lane. Skip Azure seed; validate the mock pipeline + backend health. Requires **no** Azure credentials. |
| `--no-smoke` | off | Run seed + verify only; skip the backend smoke check (used by the azd hook to keep it fast/non-fatal). |
| `--data-dir <path>` | `infra/ai-search/seed-articles` | Seed corpus directory. |
| `-h`, `--help` | — | Print usage and exit 0. |

## Required environment (live lane, i.e. not `--mock`)

| Var | Purpose |
|---|---|
| `AZURE_SEARCH_ENDPOINT` | AI Search endpoint |
| `AZURE_SEARCH_API_KEY` (or `AZURE_SEARCH_KEY`) | AI Search admin key |
| `AZURE_SEARCH_INDEX_NAME` | optional, default `university-kb` |
| `AZURE_OPENAI_ENDPOINT` | embeddings endpoint |
| `AZURE_OPENAI_API_KEY` | embeddings key |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | optional, default `text-embedding-ada-002` |

If any required var is missing in the live lane, the script prints the **exact
missing variable names** and exits `2` (fail closed). Secret **values** are
never printed.

## Behavior

1. Parse flags; `--help` → usage, exit 0.
2. `--mock`: run mock-pipeline checks (reuse `scripts/smoke-test.sh` mock
   sections / backend `USE_MOCK_MODE=true` health) → banner → exit 0/1.
3. Live: validate env (exit 2 if missing) → `seed_search_index.py --data-dir …`
   (create index + upsert embedded docs, idempotent) → verify index → unless
   `--no-smoke`, backend smoke check → banner.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Scenario-ready (all selected steps passed). |
| `1` | A step ran but failed (seed/verify/smoke returned error). |
| `2` | Pre-flight failure (missing required env / bad args). |

> The `postprovision` hook wraps the call so azd still succeeds even on `1`/`2`:
> `scripts/quickstart.sh --no-smoke || { echo "<guidance>"; true; }`.

## Success banner (stdout contract)

On exit 0 the script prints a block containing the literal marker
`✅ Scenario-ready` followed by next-step links to the Lab 05 scenarios, e.g.:

```text
==================================================
✅ Scenario-ready
   Index: university-kb (6 articles seeded)
   Next:  labs/05-agent-orchestration/scenarios/ajcu/README.md
==================================================
```

Automated checks key off the literal `✅ Scenario-ready` marker.

## Idempotency

Re-running with the same corpus overwrites the same `article_id`-keyed
documents — no duplicates, same green result (SC-002).
