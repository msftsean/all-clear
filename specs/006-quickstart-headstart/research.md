# Phase 0 Research: Cold-Start Quickstart

## R1 — Which seed corpus is canonical?

**Decision**: Seed from `infra/ai-search/seed-articles/*.json`.

**Rationale**: Per its README, this is the AJCU six-intent corpus mapped from
`47Doors-AJCU-Scenario.md` §3, one file per intent/department
(`financial_aid`, `registrar`, `campus_ministry`, `it`, `student_wellness`,
`general`). It is the content the Lab 05 scenarios are written against. Each
file is `{ "articles": [ ... ] }` with article fields
`article_id, title, url, content, snippet, department, category, tags,
last_updated` — matching the field set `setup_index.py` already maps.

**Alternatives rejected**:
- `labs/04-build-rag-pipeline/data/*_kb.json` (older 32-doc set:
  financial_aid, housing, it_support, policies, registration) — not aligned to
  the six AJCU intents the scenarios use; would seed the "wrong" KB for the
  build sprint.

## R2 — Reuse `setup_index.py` or add a dedicated seeder?

**Decision**: Add a thin `scripts/seed_search_index.py` that imports/mirrors the
index-creation + embedding logic but defaults its `--data-dir` to
`infra/ai-search/seed-articles/` and understands the `{ "articles": [...] }`
wrapper.

**Rationale**: `labs/04-build-rag-pipeline/setup_index.py` is **the Lab 04
exercise**; its `main()` hardcodes `data_dir = Path(__file__).parent / "data"`.
Editing it risks breaking the lab. A small dedicated seeder keeps Lab 04 intact
(scope guard) while reusing the exact same field mapping and embedding model.
The seeder will `load` both shapes (`{"articles": [...]}` and bare list) so it is
robust to either corpus.

**Alternatives rejected**:
- Editing `setup_index.py` default — violates the "labs intact" scope guard.
- Duplicating the whole index schema — acceptable but we keep the seeder small
  and reference the same field names to minimize drift.

## R3 — Which azd hook, and how do we keep it non-fatal?

**Decision**: Call `scripts/quickstart.sh` from `azure.yaml`'s **`postprovision`**
hook, guarded so a failure logs guidance and still exits 0 for azd.

**Rationale**: After `postprovision`, AI Search + OpenAI exist and azd has
exported their endpoints/keys to the environment — the earliest point seeding can
succeed. Provisioning must never roll back because of a content-seed hiccup
(quota, transient 429), so the hook wraps the call:
`scripts/quickstart.sh || { echo "guidance…"; true; }`. The script itself still
returns accurate exit codes when invoked directly (for CI/local use).

**Alternatives rejected**:
- `postdeploy` — too late and tied to app deploy; seeding should be ready before
  the app is exercised.
- Failing hard on seed error — would destroy the provision and frustrate cold
  users (the exact pain we're removing).

## R4 — Mock/offline lane

**Decision**: `quickstart.sh --mock` validates the pipeline via existing
`backend/app/services/mock/` and the health/smoke checks in
`scripts/smoke-test.sh`, requiring **no Azure credentials**.

**Rationale**: Graceful Degradation (Constitution VII) and the project's
mock-mode principle. A participant blocked on Azure access (Conditional Access,
quota) can still reach a working scenario lane. `smoke-test.sh` already starts
the backend with `USE_MOCK_MODE=true` and asserts mock intent + KB search work.

## R5 — Idempotency

**Decision**: Use the article's stable `article_id` as the search index key and
`upload_documents` (upsert semantics). Re-running seeds the same IDs → no
duplicates; index `create_or_update_index` is itself idempotent.

**Rationale**: SC-002 requires re-runs to be safe and produce the same green
result. Azure AI Search `mergeOrUpload`/upload on a fixed key overwrites rather
than appends.

## R6 — Env/credential handling

**Decision**: Read all endpoints/keys from environment / `.env` (as the existing
scripts do). When required vars are missing for the live lane, print the exact
variable names to set and exit non-zero (fail closed). Never echo secret values.

**Rationale**: FR-006 + Privacy-First. Matches `verify_index.py` behavior which
already checks `AZURE_SEARCH_ENDPOINT` / key and prints guidance.

## Open questions / follow-ups

- The shared-backend lane requires the coach to actually run `azd up` once and
  distribute the endpoint — operational, out of scope for code (documented in
  HEADSTART.md).
- Embedding model name (`text-embedding-ada-002`) is hardcoded in
  `setup_index.py`; the seeder will accept `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`
  override to match whatever the bicep provisions.
