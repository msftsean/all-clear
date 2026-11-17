# all-clear Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-11-17

## Active Technologies
- Python 3.11+; TypeScript 5; React 18 + FastAPI, Pydantic, Microsoft Agent Framework; Vite 5, Tailwind, Vitest; local `qrcode` (024-room-surge)
- Process-local SurgeRoom and admission window; existing mock store offline, Cosmos incidents/reports/audit live (024-room-surge)



## Project Structure

```text
backend/
frontend/
specs/024-room-surge/
```

## Commands

```bash
(cd backend && PYTHONPATH=. MOCK_MODE=true python -m pytest -q)
(cd frontend && npm test -- --run src/allclear/surge/Surge.test.tsx)
(cd frontend && npm run build)
```

## Code Style

Follow `.specify/memory/constitution.md` and `CONTEXT.md`. Preserve the bounded
pipeline, privacy filtering, audit records, and mandatory escalation.

## Recent Changes
- 024-room-surge: Added Python 3.11+; TypeScript 5; React 18 + FastAPI, Pydantic, Microsoft Agent Framework; Vite 5, Tailwind, Vitest; local `qrcode`



<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
