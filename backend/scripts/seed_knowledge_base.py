"""Seed the All Clear knowledge base into Azure AI Search.

Creates (or updates) the `knowledge-base` index with a 1536-dim vector field and
uploads the All Clear incident-response articles from mock_data/sample_kb_articles.json,
generating embeddings with the deployed text-embedding-3-small model.

Auth:
- Azure AI Search: admin key (env SEARCH_ADMIN_KEY) or fetched via az by the caller.
- Azure OpenAI embeddings: AAD token (AzureCliCredential) because the OpenAI account
  has local auth disabled (managed identity / Entra only).

Env:
  SEARCH_ENDPOINT   e.g. https://allclear-...-search.search.windows.net
  SEARCH_ADMIN_KEY  Azure AI Search admin key
  SEARCH_INDEX      index name (default: knowledge-base)
  OPENAI_ENDPOINT   e.g. https://allclear-...-openai.openai.azure.com/
  EMBED_DEPLOYMENT  embedding deployment name (default: text-embedding-3-small)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import httpx
from azure.identity import AzureCliCredential

SEARCH_API_VERSION = "2023-11-01"
EMBED_API_VERSION = "2024-10-21"
VECTOR_DIM = 1536

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_PATH = ROOT / "mock_data" / "sample_kb_articles.json"


def _env(name: str, default: str | None = None) -> str:
    val = os.environ.get(name, default)
    if not val:
        print(f"ERROR: env {name} is required", file=sys.stderr)
        sys.exit(2)
    return val


def index_definition(name: str) -> dict:
    return {
        "name": name,
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
            {"name": "title", "type": "Edm.String", "searchable": True},
            {"name": "content", "type": "Edm.String", "searchable": True},
            {"name": "snippet", "type": "Edm.String", "searchable": True},
            {"name": "department", "type": "Edm.String", "filterable": True},
            {"name": "category", "type": "Edm.String", "filterable": True, "facetable": True},
            {"name": "queue", "type": "Edm.String", "filterable": True, "facetable": True},
            {
                "name": "tags",
                "type": "Collection(Edm.String)",
                "searchable": True,
                "filterable": True,
                "facetable": True,
            },
            {
                "name": "content_vector",
                "type": "Collection(Edm.Single)",
                "searchable": True,
                "dimensions": VECTOR_DIM,
                "vectorSearchProfile": "default-profile",
            },
        ],
        "vectorSearch": {
            "algorithms": [
                {"name": "hnsw-algo", "kind": "hnsw", "hnswParameters": {"metric": "cosine"}}
            ],
            "profiles": [{"name": "default-profile", "algorithm": "hnsw-algo"}],
        },
        "semantic": {
            "configurations": [
                {
                    "name": "default-semantic",
                    "prioritizedFields": {
                        "titleField": {"fieldName": "title"},
                        "prioritizedContentFields": [{"fieldName": "content"}],
                        "prioritizedKeywordsFields": [{"fieldName": "tags"}],
                    },
                }
            ]
        },
    }


def main() -> int:
    search_endpoint = _env("SEARCH_ENDPOINT").rstrip("/")
    search_key = _env("SEARCH_ADMIN_KEY")
    index_name = os.environ.get("SEARCH_INDEX", "knowledge-base")
    openai_endpoint = _env("OPENAI_ENDPOINT").rstrip("/")
    embed_deployment = os.environ.get("EMBED_DEPLOYMENT", "text-embedding-3-small")

    articles = json.loads(ARTICLES_PATH.read_text(encoding="utf-8"))["articles"]
    print(f"Loaded {len(articles)} articles from {ARTICLES_PATH.name}")

    cred = AzureCliCredential(process_timeout=30)
    token = cred.get_token("https://cognitiveservices.azure.com/.default").token

    client = httpx.Client(timeout=60.0)

    # 1. Create / update the index
    idx = index_definition(index_name)
    r = client.put(
        f"{search_endpoint}/indexes/{index_name}",
        params={"api-version": SEARCH_API_VERSION},
        headers={"api-key": search_key, "Content-Type": "application/json"},
        json=idx,
    )
    if r.status_code not in (200, 201):
        print(f"Index create/update failed {r.status_code}: {r.text}", file=sys.stderr)
        return 1
    print(f"Index '{index_name}' created/updated ({r.status_code})")

    # 2. Generate embeddings and build documents
    docs = []
    for a in articles:
        text = f"{a['title']}. {a.get('content', '')}"
        er = client.post(
            f"{openai_endpoint}/openai/deployments/{embed_deployment}/embeddings",
            params={"api-version": EMBED_API_VERSION},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"input": text[:8000]},
        )
        if er.status_code != 200:
            print(f"Embedding failed for {a['article_id']} {er.status_code}: {er.text}", file=sys.stderr)
            return 1
        vector = er.json()["data"][0]["embedding"]
        docs.append({
            "@search.action": "mergeOrUpload",
            "id": a["article_id"],
            "title": a["title"],
            "content": a.get("content", ""),
            "snippet": a.get("snippet", ""),
            "department": a.get("department"),
            "category": a.get("category", ""),
            "queue": a.get("queue", ""),
            "tags": a.get("tags", []),
            "content_vector": vector,
        })
        print(f"  embedded {a['article_id']} (dim={len(vector)})")

    # 3. Upload documents
    ur = client.post(
        f"{search_endpoint}/indexes/{index_name}/docs/index",
        params={"api-version": SEARCH_API_VERSION},
        headers={"api-key": search_key, "Content-Type": "application/json"},
        json={"value": docs},
    )
    if ur.status_code not in (200, 201):
        print(f"Upload failed {ur.status_code}: {ur.text}", file=sys.stderr)
        return 1
    results = ur.json().get("value", [])
    ok = sum(1 for x in results if x.get("status"))
    print(f"Uploaded {ok}/{len(docs)} documents to '{index_name}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
