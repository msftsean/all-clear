# AJCU KB Seed Corpus (Azure AI Search)

Seed knowledge-base articles for the six Jesuit-context departments, from
`47Doors-AJCU-Scenario.md` §3. Load these into your Azure AI Search index so the
RAG pipeline has real content to retrieve during the build sprint. Each AJCU
member institution can re-skin the titles, URLs, and policies to its own campus.

One JSON file per intent/department:

| File | Intent slug | Department |
|---|---|---|
| `financial_aid.json` | `financial_aid` | Bursar / Financial Aid |
| `registrar.json` | `registrar` | Registrar's Office |
| `campus_ministry.json` | `campus_ministry` | Office of Campus Ministry |
| `it.json` | `it` | University IT |
| `student_wellness.json` | `student_wellness` | Counseling & Health Services |
| `general.json` | `general` | Front-desk pool / Mission |

## Schema

Each file is `{ "articles": [ ... ] }`. Article fields match the existing
`labs/04-build-rag-pipeline/data/*_kb.json` corpus format:

- `article_id`, `title`, `url`, `content`, `snippet`
- `department` (the intent slug), `category`, `tags`, `last_updated`

> Path note: the scenario pack maps §3 to `infra/ai-search/seed-articles/`.
> This repo had no pre-existing `seed-articles/` folder, so the article schema
> here is borrowed from `labs/04-build-rag-pipeline/data/` (the repo's existing
> seed corpus format).
