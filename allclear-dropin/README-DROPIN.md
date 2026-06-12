# All Clear Drop-In Kit (June 12, 2026)

Apply over your 47 Doors fork in EstablishedCorp/all-clear.

## What this contains

- `.squad/` Avengers cast: team.md, routing.md, decisions.md seed, six agent charters (T'Challa, Shuri, Stark, Rogers, Barton, FRIDAY), casting/history-addition.json
- `CONTEXT.md` for the repo root (domain ubiquitous language)
- `shared/constitution.md` (replaces the FERPA university constitution)
- `specs/001-maf-rehost/` spec, plan (with Loop Protocol + verified MAF 1.8.1 API appendices), tasks (Avengers-mapped with verification commands)

## How to apply

1. Copy CONTEXT.md to repo root, shared/constitution.md over the existing one, specs/ in as-is.
2. In .squad/: replace team.md, routing.md; copy the six agents/* directories in alongside the old ones, then retire the Matrix agent directories; append casting/history-addition.json's assignment object into casting/history.json's assignments array; merge decisions.md seed rows into the existing decisions.md.
3. Keep ceremonies.md, templates/, identity/, skills/, config.json as-is (update teamRoot path in config.json to your local clone path).
4. Kickoff: paste the Loop Protocol from specs/001-maf-rehost/plan.md into your Copilot CLI session, then speckit.clarify -> speckit.analyze -> T1.
