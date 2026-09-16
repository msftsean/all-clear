# Lab 00 - Codespaces Setup and Offline First Success

| Attribute | Value |
| --- | --- |
| Duration | 20-30 minutes |
| Difficulty | Beginner |
| Required credentials | GitHub access only |
| Azure required? | No |

All Clear is Codespaces-first for the workshop. Your first success is the local/mock path: the backend imports, `/api/health` is healthy, and `/api/chat` returns an `AC-*` incident for a sample signal. Do not run `azd up` for Lab 00.

## 1. Open the Codespace

1. Open the `msftsean/all-clear` repository.
2. Select **Code -> Codespaces -> Create codespace on workshop-readiness**.
3. Wait for the post-create command to finish. It installs backend and frontend dependencies and creates mock-mode `.env` files when they are missing.

## 2. Run the readiness check

From the repository root:

```bash
npm run local-preflight
npm run readiness
```

Expected success marker:

```text
✅ Workshop-ready: mock pipeline works without Azure credentials.
Definition of done: backend health is healthy and /api/chat returns an AC-* incident.
```

If this fails, run the recovery steps below before continuing.

## 3. Run the offline quickstart

```bash
npm run first-success
```

Expected success marker:

```text
✅ Scenario-ready
Mock lane: incident pipeline validated with no Azure credentials.
```

## 4. Start the app

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

Open the forwarded port 5173. Submit:

```text
Power line down across Main St, sparking near the school
```

You are done when the response shows an `AC-*` incident, severity, queue, and action status.

## Environment variables

Required for Lab 00:

| Variable | Value |
| --- | --- |
| `MOCK_MODE` | `true` |
| `ENVIRONMENT` | `test` or `development` |
| `VITE_API_BASE_URL` | Empty; Vite proxies `/api` to the backend |

Optional live-path variables, not needed for first success:

| Area | Variables |
| --- | --- |
| Azure OpenAI chat/embeddings | `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT` |
| Azure AI Search | `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_KEY`, `AZURE_SEARCH_INDEX` |
| Cosmos DB | `AZURE_COSMOS_ENDPOINT`, `AZURE_COSMOS_KEY`, `AZURE_COSMOS_DATABASE` |
| Voice realtime | `AZURE_OPENAI_REALTIME_DEPLOYMENT`, `AZURE_OPENAI_REALTIME_ENDPOINT` |
| Phone/ACS | `PHONE_ENABLED`, `AZURE_ACS_ENDPOINT`, `ACS_PHONE_NUMBER` |
| Admin/demo routes | `ADMIN_API_TOKEN` |
| Live phone webhooks | `PHONE_WEBHOOK_SECRET`, `PHONE_CALLBACK_BASE_URL` |

Never paste credential values into docs, issues, screenshots, or commits.

## Coach reset and recovery

From the repository root:

```bash
npm run reset:workshop
npm run readiness
npm run quickstart:mock
```

The reset script backs up local `backend/.env` and `frontend/.env`, recreates mock-mode defaults from the examples, and removes build/test caches. It does not delete source code or `node_modules`.

Common recovery:

| Symptom | Recovery |
| --- | --- |
| Backend import fails | `cd backend && pip install -r requirements.txt`, then rerun `npm run readiness` |
| Frontend dependencies missing | `cd frontend && npm install` |
| Browser cannot reach API in Codespaces | Keep `VITE_API_BASE_URL` empty and restart `npm run dev` |
| Port already in use | Stop the old backend/frontend terminal with Ctrl+C and restart |
| Live Azure settings missing | Set `MOCK_MODE=true` for the workshop path |

## What is intentionally out of scope for Lab 00

- Azure deployment (`azd up`)
- Real ACS/PSTN phone intake
- Production security attestation
- Cost or billing validation

Those are live-path topics and are not required to begin the 180-minute workshop.
