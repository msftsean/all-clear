"""T003/T005 — Unit tests for scripts/seed_search_index.py (feature 006).

These tests run with ZERO Azure credentials. They exercise corpus loading,
field mapping (data-model.md), and the offline `--dry-run` mode only.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from conftest import REPO_ROOT, SEED_DIR

SEEDER_PATH = REPO_ROOT / "scripts" / "seed_search_index.py"

# The six AJCU intent/department slugs (data-model.md).
EXPECTED_DEPARTMENTS = {
    "financial_aid",
    "registrar",
    "campus_ministry",
    "it",
    "student_wellness",
    "general",
}

# Nine source->index content/metadata fields (excluding the vector).
EXPECTED_DOC_FIELDS = {
    "id",
    "title",
    "content",
    "url",
    "snippet",
    "department",
    "category",
    "tags",
    "last_updated",
}


def _load_seeder():
    spec = importlib.util.spec_from_file_location("seed_search_index", SEEDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def seeder():
    assert SEEDER_PATH.exists(), f"seeder not implemented yet: {SEEDER_PATH}"
    return _load_seeder()


def test_loads_all_six_seed_files_with_articles_wrapper(seeder):
    """(a) Loads infra/ai-search/seed-articles/ and unwraps {"articles": [...]}."""
    articles = seeder.load_articles(SEED_DIR)
    # 31 articles across the six canonical files.
    assert len(articles) >= 25
    departments = {a.get("department") for a in articles}
    assert EXPECTED_DEPARTMENTS.issubset(departments)


def test_accepts_bare_list_shape(seeder, tmp_path):
    """Seeder is robust to a bare-list JSON shape as well as the wrapper."""
    bare = tmp_path / "bare.json"
    bare.write_text(json.dumps([{"article_id": "x-1", "title": "t", "content": "c"}]))
    articles = seeder.load_articles(tmp_path)
    assert len(articles) == 1
    assert articles[0]["article_id"] == "x-1"


def test_field_mapping_article_id_to_id_and_nine_fields(seeder):
    """(b) article_id -> id plus the nine content/metadata fields (no Azure)."""
    article = {
        "article_id": "kb-it-001",
        "title": "Reset your password",
        "content": "Steps to reset your password.",
        "url": "https://it.university.edu/kb/it-001",
        "snippet": "Steps to reset",
        "department": "it",
        "category": "accounts",
        "tags": ["password", "login"],
        "last_updated": "2026-02-02T10:00:00Z",
    }
    doc = seeder.build_document(article)
    assert set(doc.keys()) == EXPECTED_DOC_FIELDS
    assert doc["id"] == "kb-it-001"
    assert doc["title"] == "Reset your password"
    assert doc["department"] == "it"
    assert doc["tags"] == ["password", "login"]
    # No embedding/vector should be produced in the offline mapping.
    assert "content_vector" not in doc


def test_dry_run_lists_documents_and_exits_zero(seeder, capsys):
    """(c) --dry-run lists documents WITHOUT any Azure calls and exits 0."""
    rc = seeder.main(["--dry-run", "--data-dir", str(SEED_DIR)])
    assert rc == 0
    out = capsys.readouterr().out
    # Lists at least some known IDs/titles.
    assert "kb-" in out
