# Lab 00 Completion Specification

Lab 00 is complete when the participant reaches an offline All Clear first success with no Azure credentials.

## Required checks

```bash
npm run readiness
npm run quickstart:mock
```

Both commands must exit `0`.

## Acceptance criteria

- Python 3.11+ and Node.js 18+ are available.
- Backend dependencies import successfully.
- Mock knowledge search returns at least one incident-response article.
- `GET /api/health` returns HTTP 200 with `status=healthy` and `mock_mode=true`.
- `POST /api/chat` with a downed-line signal returns an `AC-*` incident id and a routing outcome.
- Frontend dependencies are installed or the readiness check reports the exact install command.

## Environment contract

Required:

```env
MOCK_MODE=true
ENVIRONMENT=test
VITE_API_BASE_URL=
```

Optional live-path values such as Azure OpenAI, Azure AI Search, Cosmos DB, Realtime, and ACS settings are not required for Lab 00 and must not be committed with real values.

## Reset contract

```bash
npm run reset:workshop
```

The reset command must back up local `.env` files, recreate mock defaults, remove build/test caches, and leave source files intact.
