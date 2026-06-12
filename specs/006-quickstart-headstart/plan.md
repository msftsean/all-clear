# Implementation Plan: Cold-Start Quickstart (Labs 01 & 04 Head-Start)

**Branch**: `006-quickstart-headstart` | **Date**: 2026-05-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/006-quickstart-headstart/spec.md`

## Summary

Give cold AJCU hackathon participants a **tiered quickstart** that lands them in
a "scenario-ready" state (Labs 01 & 04 effectively done) in minutes, so their
time goes to the AJCU scenarios rather than plumbing. The approach is to
**orchestrate assets the repo already has** — `infra/ai-search/seed-articles/`
(canonical six-intent corpus), `labs/04-build-rag-pipeline/setup_index.py` /
`verify_index.py`, `backend/app/services/mock/` (offline pipeline), and
`scripts/smoke-test.sh` — behind one idempotent entry point
(`scripts/quickstart.sh`), wire it into the existing `azure.yaml`
`postprovision` hook (non-fatal), and document three lanes (shared backend /
self-serve `azd` / mock) in `docs/quickstart/HEADSTART.md`. No lab content,
agents, taxonomy, or deploy workflow is modified.

## Technical Context

**Language/Version**: Bash (POSIX) for the entry script; Python 3.11+ for the
seed/verify steps it invokes (reusing existing scripts).
**Primary Dependencies**: `azure-search-documents>=11.4.0`, `openai>=1.10.0`,
`python-dotenv` (already in `backend/requirements.txt`); Azure Developer CLI
(`azd`) for the self-serve lane; existing mock services for the offline lane.
**Storage**: Azure AI Search index (`AZURE_SEARCH_INDEX_NAME`, default
`university-kb`) seeded from `infra/ai-search/seed-articles/`. No new storage.
**Testing**: bats-free bash self-checks + reuse of `scripts/smoke-test.sh`;
backend `pytest` for non-regression; a `tests/quickstart/` shell/Python check
for idempotency and mock-lane success.
**Target Platform**: GitHub Codespaces / Linux dev container; Azure (AI Search +
OpenAI) for the live lanes.
**Project Type**: Tooling/CLI + docs over an existing web application.
**Performance Goals**: ≤ 15 min hands-on to scenario-ready (excl. unattended
`azd` provisioning). Seed of ~6–32 docs completes in well under 2 min.
**Constraints**: Idempotent; non-fatal to `azd up`; zero secrets in repo; must
run offline in `--mock` mode; must not regress labs/tests/workflows.
**Scale/Scope**: 6 seed-article files (six intents); ~30 participants; 3 lanes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Bounded Agent Authority | ✅ N/A | No agent code touched; only seeds the KB the existing ActionAgent already reads. No new authority path. |
| II. Human Escalation | ✅ N/A | No routing/escalation logic changed. |
| III. Privacy-First | ✅ PASS | Seed corpus is synthetic public KB content; no PII. Scripts never print/commit secrets; env read from `.env`, never echoed. |
| IV. Stateful Context | ✅ N/A | No session behavior changed. |
| V. Test-First | ✅ PASS | Idempotency + mock-lane + non-regression checks authored **before** the script per Phase 2 ordering. |
| VI. Accessibility | ✅ N/A | No UI surface. Docs use clear headings/checklists. |
| VII. Graceful Degradation | ✅ PASS | `--mock` lane works with zero Azure creds; `azd` hook is non-fatal and prints actionable guidance on failure. |

**Security & Compliance**: No secrets in repo; shared-backend endpoint/keys
distributed out-of-band. Scripts fail closed with guidance when creds missing.

**Result**: PASS — no violations, no Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/006-quickstart-headstart/
├── spec.md              # Feature spec (already written)
├── plan.md              # This file
├── research.md          # Phase 0 — decisions & alternatives
├── data-model.md        # Phase 1 — seed-article schema + index mapping
├── quickstart.md        # Phase 1 — how to run/validate this feature
├── contracts/
│   └── quickstart-cli.md # Phase 1 — script CLI + exit-code contract
└── tasks.md             # Phase 2 — created by /speckit.tasks (NOT here)
```

### Source Code (repository root)

```text
scripts/
├── quickstart.sh         # NEW — single entry point (seed → verify → smoke); --mock lane
├── seed_search_index.py  # NEW (or adapted) — seeds index from infra/ai-search/seed-articles/
├── smoke-test.sh         # EXISTING — reused for the backend/mock validation
└── validate-lab-00.sh    # EXISTING — unchanged

azure.yaml                # MODIFIED — postprovision hook calls scripts/quickstart.sh (non-fatal)

infra/ai-search/seed-articles/   # EXISTING — canonical six-intent corpus (read-only source)
labs/04-build-rag-pipeline/      # EXISTING — setup_index.py/verify_index.py reused, NOT modified

docs/quickstart/
└── HEADSTART.md          # NEW — three-lane tiered guide + "scenario-ready" checklist
README.md                 # MODIFIED — single link to HEADSTART.md (no lab content changed)

tests/quickstart/         # NEW — idempotency + mock-lane + non-regression checks
└── test_quickstart.py    # (or .sh) authored before quickstart.sh per Constitution V
```

**Structure Decision**: Tooling-over-existing-app. New code is confined to
`scripts/`, `docs/quickstart/`, `tests/quickstart/`, plus one surgical edit each
to `azure.yaml` (hook) and `README.md` (one link). The seed logic prefers a
small dedicated `scripts/seed_search_index.py` that reads
`infra/ai-search/seed-articles/` (the canonical corpus) so we do not modify the
Lab 04 teaching script; if reuse of `setup_index.py` is cleaner we adapt via a
`--data-dir` argument without changing its default lab behavior.

## Phase 0 — Research

See [research.md](research.md). Key decisions:
1. **Seed source** = `infra/ai-search/seed-articles/` (canonical AJCU six-intent
   corpus, `{ "articles": [...] }`), not `labs/04/data/` (older 32-doc set).
2. **Don't edit `setup_index.py`** — its default reads `labs/04/data/` and is the
   lab exercise. Add a thin `scripts/seed_search_index.py` (or pass `--data-dir`)
   to avoid breaking Lab 04.
3. **Hook = `postprovision`, non-fatal** — wrap in a guard so a seed error prints
   guidance but returns success to `azd` (provisioning must not roll back).
4. **Mock lane** reuses `app/services/mock/` + `scripts/smoke-test.sh` (already
   proven offline) — no Azure required.
5. **Idempotency** via stable `article_id` as the index key (upserts, no dupes).

## Phase 1 — Design & Contracts

- [data-model.md](data-model.md): seed-article JSON schema → search index field
  mapping; key = `article_id`; six intent/department slugs.
- [contracts/quickstart-cli.md](contracts/quickstart-cli.md): `quickstart.sh`
  flags (`--mock`, `--no-smoke`, `-h`), required env vars, exit codes, and the
  "✅ Scenario-ready" banner contract.
- [quickstart.md](quickstart.md): how to run and validate this feature locally
  (mock lane) and against Azure (live lane).

**Post-design Constitution re-check**: still PASS — design adds no agent
authority, persists no PII, and preserves graceful degradation via `--mock`.

## Phase 2 — Tasks (handled by /speckit.tasks, not here)

Test-first ordering: author `tests/quickstart/` checks (idempotency, mock-lane
green, no lab/test regression) → implement `scripts/seed_search_index.py` →
`scripts/quickstart.sh` → wire `azure.yaml` hook → write `HEADSTART.md` + README
link → validate (mock + backend pytest) → (optional) live Azure dry-run.

## Complexity Tracking

No constitution violations — table intentionally empty.

## Coordination Note

`azure.yaml` and `infra/` are actively iterated by a parallel CLI instance
(voice/deploy work). This feature touches **only** the `azure.yaml` hook bodies
(currently `echo`-only placeholders) and adds new files under `scripts/`,
`docs/quickstart/`, `tests/quickstart/`. `git fetch` before branching; keep the
hook edit minimal and clearly commented so a rebase is trivial.
