# Phase 1 Data Model: Seed Article → Search Index

This feature introduces **no new persisted entities**. It loads the existing
seed corpus into the existing Azure AI Search index. Documented here for the
seeder's field mapping and idempotency contract.

## Source: Seed Article (input)

One JSON file per intent under `infra/ai-search/seed-articles/`, each shaped
`{ "articles": [ Article, ... ] }`.

| Field | Type | Required | Notes |
|---|---|---|---|
| `article_id` | string | yes | **Stable key** → index `id`. Drives idempotency. e.g. `kb-it-001`. |
| `title` | string | yes | Searchable. |
| `content` | string | yes | Searchable; source for the embedding vector. |
| `url` | string | no | Stored, not searched. |
| `snippet` | string | no | Stored. |
| `department` | string | yes | Intent/department slug (filterable/facetable). One of the six slugs below. |
| `category` | string | no | Filterable/facetable. |
| `tags` | string[] | no | Filterable collection. |
| `last_updated` | string | no | Stored. |

### Department / intent slugs (six)

`financial_aid`, `registrar`, `campus_ministry`, `it`, `student_wellness`,
`general` — one seed file each. These are the AJCU build-sprint intents the
Lab 05 scenarios route to.

## Target: Search Index Document (output)

Index name from `AZURE_SEARCH_INDEX_NAME` (default `university-kb`). Field set
mirrors `labs/04-build-rag-pipeline/setup_index.py`:

| Index field | Type | From source | Search role |
|---|---|---|---|
| `id` | Edm.String (key) | `article_id` | key — idempotency |
| `title` | Edm.String | `title` | searchable + semantic title |
| `content` | Edm.String | `content` | searchable + semantic content |
| `url` | Edm.String | `url` | retrievable |
| `snippet` | Edm.String | `snippet` | retrievable |
| `department` | Edm.String | `department` | filterable/facetable |
| `category` | Edm.String | `category` | filterable/facetable |
| `tags` | Collection(Edm.String) | `tags` | filterable |
| `last_updated` | Edm.String | `last_updated` | retrievable |
| `content_vector` | Collection(Edm.Single), dim 1536 | embed(`content`) | vector (HNSW, `my-vector-profile`) |

**Embedding**: Azure OpenAI embeddings of `content` (truncated to ~8000 chars),
model from `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` (default `text-embedding-ada-002`),
1536 dims to match the index vector field.

## Idempotency rule

- Index created via `create_or_update_index` (idempotent schema).
- Documents uploaded keyed by `id = article_id` (upsert). Re-running the seed
  overwrites the same documents — **no duplicates** (satisfies SC-002).

## Validation (verify step)

Reuse `labs/04-build-rag-pipeline/verify_index.py` semantics:
- document count ≥ number of seeded articles,
- keyword search returns hits (e.g. "password reset"),
- a `department` filter returns rows,
- vector field present.
