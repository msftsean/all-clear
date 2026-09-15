# Quickstart: All Clear Workshop Readiness

This quickstart describes the verified local/mock path. It does not require Azure credentials and does not deploy resources.

## Prerequisites

- Python 3.11+
- Node.js 18+
- GitHub Codespaces or a dev container/host with Bash

## Setup

```bash
# From the repository root after the devcontainer post-create command:
npm run readiness
npm run quickstart:mock
```

The expected success markers are:

```text
✅ Workshop-ready: mock pipeline works without Azure credentials.
✅ Scenario-ready
```

## Manual app run

Terminal 1:

```bash
cd backend
MOCK_MODE=true ENVIRONMENT=test uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2:

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

Submit this signal in the UI or with curl:

```bash
curl -s http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Power line down across Main St and sparking"}'
```

Definition of done: the response includes an `AC-*` incident id, a severity, a queue, and an action status.

## Optional live path

Azure OpenAI, Azure AI Search, Cosmos DB, Realtime, and ACS settings are optional live-path configuration. Keep `MOCK_MODE=true` for the event first success. Do not paste real credential values into docs or commits.

## Reset

```bash
npm run reset:workshop
npm run readiness
```

The reset command backs up local `.env` files, restores mock defaults, and clears local build/test caches.
