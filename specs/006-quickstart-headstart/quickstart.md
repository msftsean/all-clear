# Quickstart: Validating This Feature

How to run and validate the cold-start quickstart tooling itself (for
developers/coaches building it). End-user lane docs live in
`docs/quickstart/HEADSTART.md`.

## Mock lane (no Azure, fastest to validate)

```bash
# From repo root
scripts/quickstart.sh --mock
```

Expected: backend mock pipeline + health checks pass; prints `✅ Scenario-ready`;
exit 0. This is the lane a credential-blocked participant uses.

## Live lane (against real Azure AI Search + OpenAI)

```bash
# Ensure env is set (e.g. via azd env or .env): AZURE_SEARCH_ENDPOINT,
# AZURE_SEARCH_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY
scripts/quickstart.sh
```

Expected: index `university-kb` created/updated; six AJCU articles embedded +
upserted; verify checks pass (count, keyword, filter, vector); backend smoke
green; `✅ Scenario-ready`; exit 0.

## Idempotency check

```bash
scripts/quickstart.sh            # first run
scripts/quickstart.sh            # second run — same green result, no dup docs
```

Verify document count is unchanged after the second run.

## Self-serve via azd (end-to-end)

```bash
azd up        # provisions infra, then postprovision auto-runs quickstart (non-fatal)
```

Expected: after provisioning, the console shows the `✅ Scenario-ready` banner.
A seed failure prints guidance but does NOT fail `azd up`.

## Non-regression

```bash
cd backend && python -m pytest -q          # backend tests unaffected
bash scripts/smoke-test.sh                  # existing smoke suite still passes
```

## "Scenario-ready" checklist

- [ ] `✅ Scenario-ready` printed by the chosen lane
- [ ] (live) `verify_index` reports count ≥ seeded articles + keyword/filter hits
- [ ] (mock) mock intent classification + KB search pass
- [ ] Backend `/api/health` responds
- [ ] No lab files modified; backend pytest green
