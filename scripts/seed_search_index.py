#!/usr/bin/env python3
"""Seed the Azure AI Search index from the canonical six-intent corpus.

Feature 006 (Cold-Start Quickstart). A thin, dedicated seeder that mirrors the
index schema, field mapping, and embedding logic of
``labs/04-build-rag-pipeline/setup_index.py`` (which is the Lab 04 *exercise* and
must remain untouched), but defaults its data directory to the canonical AJCU
corpus at ``infra/ai-search/seed-articles`` and adds an offline ``--dry-run``
mode that needs NO Azure credentials.

Idempotency: documents are upserted keyed by ``id = article_id`` (Azure AI Search
``upload_documents`` overwrites on a fixed key), so re-runs never duplicate.

Usage::

    python scripts/seed_search_index.py [--data-dir DIR] [--index-name NAME]
                                        [--dry-run]

Exit codes:
    0  success (or dry-run listed documents)
    1  a step failed (load / Azure error)
    2  missing required env for the live lane
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Embedding model / dims mirror labs/04-build-rag-pipeline/setup_index.py.
DEFAULT_INDEX_NAME = "university-kb"
DEFAULT_EMBEDDING_DEPLOYMENT = "text-embedding-ada-002"
EMBEDDING_DIMENSIONS = 1536
CONTENT_TRUNCATE_CHARS = 8000

# The nine content/metadata fields mapped from a seed article (data-model.md).
# The vector field (content_vector) is added separately in the live lane only.


def load_articles(data_dir: Path) -> list[dict]:
    """Load all KB articles from JSON files under ``data_dir``.

    Accepts both the ``{"articles": [...]}`` wrapper used by the canonical AJCU
    corpus and a bare top-level list (older lab corpora). Mirrors the loader in
    ``setup_index.py`` but understands the wrapper.
    """
    data_dir = Path(data_dir)
    articles: list[dict] = []
    for file_path in sorted(data_dir.glob("*.json")):
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "articles" in data:
            articles.extend(data["articles"])
        elif isinstance(data, list):
            articles.extend(data)
        elif isinstance(data, dict):
            # A single bare article object.
            articles.append(data)
    return articles


def build_document(article: dict, index: int = 0) -> dict:
    """Map a seed article to a search document (without the embedding vector).

    Field mapping mirrors ``setup_index.index_documents`` exactly. The stable
    ``article_id`` becomes the index key ``id`` (drives idempotency).
    """
    return {
        "id": article.get("article_id", f"kb-{index}"),
        "title": article.get("title", ""),
        "content": article.get("content", ""),
        "url": article.get("url", ""),
        "snippet": article.get("snippet", ""),
        "department": article.get("department", ""),
        "category": article.get("category", ""),
        "tags": article.get("tags", []),
        "last_updated": article.get("last_updated", ""),
    }


def build_documents(articles: list[dict]) -> list[dict]:
    """Map a list of articles to search documents (offline, no embeddings)."""
    return [build_document(a, i) for i, a in enumerate(articles)]


def _missing_live_env() -> list[str]:
    """Return the names of required env vars missing for the live lane."""
    missing: list[str] = []
    if not os.environ.get("AZURE_SEARCH_ENDPOINT"):
        missing.append("AZURE_SEARCH_ENDPOINT")
    # Accept either AZURE_SEARCH_API_KEY or AZURE_SEARCH_KEY.
    if not (os.environ.get("AZURE_SEARCH_API_KEY") or os.environ.get("AZURE_SEARCH_KEY")):
        missing.append("AZURE_SEARCH_API_KEY")
    if not os.environ.get("AZURE_OPENAI_ENDPOINT"):
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not os.environ.get("AZURE_OPENAI_API_KEY"):
        missing.append("AZURE_OPENAI_API_KEY")
    return missing


def _create_index(index_client, index_name: str) -> None:
    """Create/update the index. Mirrors setup_index.create_index schema."""
    from azure.search.documents.indexes.models import (
        HnswAlgorithmConfiguration,
        SearchableField,
        SearchField,
        SearchFieldDataType,
        SearchIndex,
        SemanticConfiguration,
        SemanticField,
        SemanticPrioritizedFields,
        SemanticSearch,
        SimpleField,
        VectorSearch,
        VectorSearchProfile,
    )

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="title", type=SearchFieldDataType.String),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="url", type=SearchFieldDataType.String),
        SimpleField(name="snippet", type=SearchFieldDataType.String),
        SimpleField(name="department", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchField(
            name="tags",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            filterable=True,
        ),
        SimpleField(name="last_updated", type=SearchFieldDataType.String),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIMENSIONS,
            vector_search_profile_name="my-vector-profile",
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="my-hnsw")],
        profiles=[
            VectorSearchProfile(
                name="my-vector-profile",
                algorithm_configuration_name="my-hnsw",
            )
        ],
    )

    semantic_search = SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="my-semantic-config",
                prioritized_fields=SemanticPrioritizedFields(
                    content_fields=[SemanticField(field_name="content")],
                    title_field=SemanticField(field_name="title"),
                ),
            )
        ]
    )

    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )
    print(f"Creating/updating index '{index_name}'...")
    index_client.create_or_update_index(index)
    print(f"Index '{index_name}' ready.")


def _generate_embedding(text: str, openai_client, deployment: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=deployment,
        input=text[:CONTENT_TRUNCATE_CHARS],
    )
    return response.data[0].embedding


def seed_live(articles: list[dict], index_name: str, data_dir: Path) -> int:
    """Create the index and upsert embedded documents. Returns an exit code."""
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from openai import AzureOpenAI

    search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    search_key = os.environ.get("AZURE_SEARCH_API_KEY") or os.environ.get("AZURE_SEARCH_KEY")
    openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    openai_key = os.environ["AZURE_OPENAI_API_KEY"]
    embedding_deployment = os.environ.get(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", DEFAULT_EMBEDDING_DEPLOYMENT
    )

    credential = AzureKeyCredential(search_key)
    index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
    search_client = SearchClient(
        endpoint=search_endpoint, index_name=index_name, credential=credential
    )
    openai_client = AzureOpenAI(
        azure_endpoint=openai_endpoint,
        api_key=openai_key,
        api_version="2024-02-15-preview",
    )

    _create_index(index_client, index_name)

    documents = build_documents(articles)
    for i, (article, doc) in enumerate(zip(articles, documents)):
        print(f"Embedding {i + 1}/{len(documents)}: {doc['title'][:50]}...")
        doc["content_vector"] = _generate_embedding(
            doc["content"], openai_client, embedding_deployment
        )

    print(f"\nUpserting {len(documents)} documents into '{index_name}'...")
    result = search_client.upload_documents(documents)
    succeeded = sum(1 for r in result if r.succeeded)
    print(f"Successfully upserted {succeeded}/{len(documents)} documents.")
    return 0 if succeeded == len(documents) else 1


def run_dry_run(articles: list[dict], index_name: str) -> int:
    """List the documents that would be seeded. NO Azure calls. Returns 0."""
    documents = build_documents(articles)
    print(f"[dry-run] Target index: {index_name}")
    print(f"[dry-run] {len(documents)} documents from corpus (no Azure calls):")
    for doc in documents:
        print(f"  - {doc['id']:<28} [{doc['department']}] {doc['title'][:60]}")
    # Idempotency note: stable, de-duplicated by article_id.
    unique_ids = {d["id"] for d in documents}
    print(f"[dry-run] {len(unique_ids)} unique document IDs (upsert keyed by id).")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed the Azure AI Search index from the AJCU seed corpus."
    )
    repo_root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--data-dir",
        default=str(repo_root / "infra" / "ai-search" / "seed-articles"),
        help="Seed corpus directory (default: infra/ai-search/seed-articles).",
    )
    parser.add_argument(
        "--index-name",
        default=os.environ.get("AZURE_SEARCH_INDEX_NAME", DEFAULT_INDEX_NAME),
        help=f"Search index name (default: env AZURE_SEARCH_INDEX_NAME or {DEFAULT_INDEX_NAME}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List documents without calling Azure (no credentials required).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data_dir = Path(args.data_dir)

    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}", file=sys.stderr)
        return 1

    try:
        articles = load_articles(data_dir)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"❌ Failed to load corpus: {exc}", file=sys.stderr)
        return 1

    if not articles:
        print(f"❌ No articles found in {data_dir}", file=sys.stderr)
        return 1

    if args.dry_run:
        return run_dry_run(articles, args.index_name)

    missing = _missing_live_env()
    if missing:
        print("❌ Missing required environment variables for the live seed lane:", file=sys.stderr)
        for name in missing:
            print(f"   - {name}", file=sys.stderr)
        print("   (Use --dry-run for an offline check.)", file=sys.stderr)
        return 2

    try:
        return seed_live(articles, args.index_name, data_dir)
    except Exception as exc:  # noqa: BLE001 - surface any Azure/runtime error as exit 1
        print(f"❌ Seeding failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
