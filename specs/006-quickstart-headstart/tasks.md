# Tasks: Cold-Start Quickstart (Labs 01 & 04 Head-Start)

**Input**: Design documents from `/specs/006-quickstart-headstart/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/quickstart-cli.md

**Tests**: Included — Constitution Principle V (Test-First) is mandatory in this
repo. Idempotency + mock-lane + non-regression checks are authored before the
scripts they validate.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 (self-serve azd hook), US2 (quickstart.sh entry), US3 (Day-0 guide)
- All paths are repo-root relative.

## Scope Guards (apply to EVERY task)

- Do NOT modify Labs 01–07 content, `start/`, or `solution/` code.
- Do NOT modify agents, `intent_classifier.py`, `escalation_rules.py`, or `/api/chat`.
- Do NOT modify hackathon-site/docs deploy workflows.
- No secrets committed; env read from environment/`.env`, values never printed.
- Only new files under `scripts/`, `docs/quickstart/`, `tests/quickstart/`,
  plus one surgical edit each to `azure.yaml` and `README.md`.

---

## Phase 1: Setup

- [ ] T001 Create directories `docs/quickstart/` and `tests/quickstart/` (with a
      `tests/quickstart/__init__.py` if Python tests are used).
- [ ] T002 [P] Add a `tests/quickstart/conftest.py` (or shared bash helper
      `tests/quickstart/_helpers.sh`) providing repo-root resolution and a
      helper to assert the `✅ Scenario-ready` stdout marker.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The seeder is the shared dependency of US1 and US2.

- [ ] T003 [US2] Author **failing** test `tests/quickstart/test_seed_index.py`
      (or `.sh`) asserting: (a) the seeder loads `infra/ai-search/seed-articles/`
      and parses the `{ "articles": [...] }` wrapper across all six files;
      (b) it maps `article_id → id` and the nine content/metadata fields per
      `data-model.md`; (c) a `--dry-run` mode lists the documents WITHOUT calling
      Azure (so the test needs no credentials). Run it — MUST fail (no seeder yet).
- [ ] T004 [US2] Implement `scripts/seed_search_index.py`:
      - `--data-dir` (default `infra/ai-search/seed-articles`), `--dry-run`,
        `--index-name` (env `AZURE_SEARCH_INDEX_NAME`, default `university-kb`).
      - Reuse the index schema + field mapping + embedding logic from
        `labs/04-build-rag-pipeline/setup_index.py` (do NOT edit that file).
      - Accept both `{ "articles": [...] }` and bare-list shapes.
      - Upsert keyed by `id = article_id` (idempotent); embedding deployment from
        `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` (default `text-embedding-ada-002`).
      - `--dry-run` prints document IDs/titles and exits 0 with NO Azure calls.
- [ ] T005 [US2] Make T003 pass (run the dry-run test green).

**Checkpoint**: Seeder works offline (dry-run) and is unit-tested.

---

## Phase 3: User Story 2 — Single `quickstart.sh` entry point (Priority: P1) 🎯 MVP

**Goal**: One idempotent command that takes a configured env to scenario-ready;
also the command the azd hook calls.
**Independent Test**: `scripts/quickstart.sh --mock` exits 0 and prints
`✅ Scenario-ready` with no Azure credentials.

- [ ] T006 [US2] Author **failing** test `tests/quickstart/test_quickstart_cli.py`
      (or `.sh`) per `contracts/quickstart-cli.md`: `--help` exits 0;
      missing live env (no `--mock`) exits 2 and names the missing vars without
      printing values; `--mock` exits 0 and emits the `✅ Scenario-ready` marker.
- [ ] T007 [US2] Implement `scripts/quickstart.sh`:
      - Flag parsing: `--mock`, `--no-smoke`, `--data-dir`, `-h|--help`.
      - Colored PASS/FAIL output matching `scripts/smoke-test.sh` style.
      - Live lane: validate required env (exit 2, fail closed) → call
        `seed_search_index.py` → run `labs/04-build-rag-pipeline/verify_index.py`
        → unless `--no-smoke`, run the backend portions of `scripts/smoke-test.sh`.
      - `--mock` lane: run mock pipeline + `/api/health` via `USE_MOCK_MODE=true`
        (reuse smoke-test mock sections); NO Azure required.
      - On full success print the `✅ Scenario-ready` banner with the Lab 05
        scenarios link; exit codes 0/1/2 per contract.
- [ ] T008 [US2] Make T006 pass (`--help`, missing-env exit 2, `--mock` green).
- [ ] T009 [US2] Idempotency test `tests/quickstart/test_idempotent.py`: invoke
      the seeder dry-run twice over the corpus and assert the produced ID set is
      identical and de-duplicated (no dup `article_id`). Implement/adjust to pass.

**Checkpoint**: US2 MVP usable standalone (mock lane fully green in CI).

---

## Phase 4: User Story 1 — Self-serve `azd` postprovision hook (Priority: P1) 🎯 MVP

**Goal**: `azd up` finishes scenario-ready; hook is non-fatal.
**Independent Test**: `azure.yaml` postprovision invokes `quickstart.sh` and is
wrapped so a non-zero exit still returns success to azd.

- [ ] T010 [US1] Edit `azure.yaml` `postprovision` hook ONLY: run
      `scripts/quickstart.sh --no-smoke || { echo "<guidance + manual command>"; true; }`
      with a clear comment explaining non-fatal intent. Keep `preprovision`/
      `postdeploy` semantics intact; do not alter `services`/`infra` blocks.
- [ ] T011 [US1] Validation test `tests/quickstart/test_azure_yaml.py`: parse
      `azure.yaml`, assert the postprovision hook references
      `scripts/quickstart.sh` and contains the non-fatal guard (`|| ` … `true`).

**Checkpoint**: Self-serve lane wired; provisioning cannot be broken by a seed error.

---

## Phase 5: User Story 3 — Tiered Day-0 guide (Priority: P2)

**Goal**: Cold participants know which lane to use and the exact commands.
**Independent Test**: `docs/quickstart/HEADSTART.md` documents 3 lanes + a
"scenario-ready" checklist; README links it without touching lab content.

- [ ] T012 [P] [US3] Write `docs/quickstart/HEADSTART.md`: cold-start framing,
      the three lanes (shared backend / self-serve azd / mock) with exact
      commands, Codespaces + Copilot + `azd auth login` Day-0 steps, and a
      "you are scenario-ready when…" checklist tied to verify/smoke output.
- [ ] T013 [P] [US3] Add ONE link to `HEADSTART.md` from `README.md` (e.g. a
      "Cold start? Read the Head-Start guide" line near the labs/prereqs section).
      Do NOT modify any lab README or lab content.
- [ ] T014 [US3] Doc-lint check `tests/quickstart/test_docs.py`: assert
      `HEADSTART.md` exists, names all three lanes, contains the scenario-ready
      checklist, and that `README.md` links to it.

---

## Phase 6: Polish & Validation

- [ ] T015 Run `chmod +x scripts/quickstart.sh scripts/seed_search_index.py` (if
      executable invocation is used) and `bash -n` syntax-check both scripts.
- [ ] T016 Run the full `tests/quickstart/` suite — all green.
- [ ] T017 Non-regression: `cd backend && python -m pytest -q` and
      `bash scripts/smoke-test.sh` — confirm no regression from this feature.
- [ ] T018 Confirm scope guards: `git diff --name-only origin/main` shows ONLY
      new files under `scripts/`, `docs/quickstart/`, `tests/quickstart/`,
      `specs/006-*`, plus `azure.yaml` and `README.md`. No `labs/**` changes.
- [ ] T019 (Optional, if Azure creds available) Live dry validation: real
      `scripts/quickstart.sh` against a throwaway index; confirm verify passes
      and a second run produces no duplicate docs (SC-002).

---

## Dependencies

- T003 → T004 → T005 (seeder TDD) blocks US1 and US2.
- T006 → T007 → T008, then T009 (US2).
- T010 → T011 (US1) depend on `quickstart.sh` existing (T007).
- US3 (T012–T014) is independent of US1/US2 and can run in parallel `[P]`.
- Phase 6 runs last.

## Parallel Opportunities

- T012 and T013 `[P]` (different files) can proceed alongside US1/US2 once the
  CLI contract is fixed.
- T002 `[P]` independent of T001 content.

## MVP Cutline

Phases 1–4 (US2 + US1) = MVP: a cold team reaches scenario-ready via `--mock`
today and via `azd up` once provisioned. US3 (docs) strongly recommended for the
"cold participant" goal but not code-blocking.
