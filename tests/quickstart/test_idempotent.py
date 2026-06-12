"""T009 — Idempotency test for the seeder (feature 006, SC-002).

The dry-run document ID set produced over the canonical corpus must be stable
and de-duplicated across repeated runs. Because seeding upserts keyed by
``id = article_id``, a stable + unique ID set proves re-runs cannot duplicate.
Runs with ZERO Azure credentials.
"""

from __future__ import annotations

import importlib.util

from conftest import REPO_ROOT, SEED_DIR

SEEDER_PATH = REPO_ROOT / "scripts" / "seed_search_index.py"


def _load_seeder():
    spec = importlib.util.spec_from_file_location("seed_search_index", SEEDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dry_run_id_set_is_stable_and_deduplicated():
    seeder = _load_seeder()

    # Two independent loads/builds over the same corpus.
    docs_run1 = seeder.build_documents(seeder.load_articles(SEED_DIR))
    docs_run2 = seeder.build_documents(seeder.load_articles(SEED_DIR))

    ids_run1 = [d["id"] for d in docs_run1]
    ids_run2 = [d["id"] for d in docs_run2]

    # Stable: identical ordered ID lists across runs.
    assert ids_run1 == ids_run2

    # De-duplicated: no duplicate article_id within the corpus.
    assert len(ids_run1) == len(set(ids_run1)), "duplicate article_id found in corpus"

    # The upsert key set is identical between runs (no growth on re-run).
    assert set(ids_run1) == set(ids_run2)
