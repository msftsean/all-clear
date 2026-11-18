# All Clear Boot Camp - Participant Guide

Welcome to the All Clear Boot Camp! This guide will help you get started and navigate through the labs.

---

## What You're Building

You will build **All Clear**, an incident-triage system that turns noisy inbound **signals** into deduplicated **incidents** with severity, SLA clocks, queues, and citation-grounded situation reports. Instead of operators manually reconciling duplicate reports during a surge, All Clear classifies each signal, uses a deterministic zero-LLM `RouterExecutor` for dedup/severity/SLA routing, and lets the bounded `ActionAgent` create incidents, search the knowledge base, and generate sitreps. By the end of this boot camp, you will have the pipeline running locally and deployed to Azure.

- 🎤 **Voice interaction** — speak to the same AI pipeline via browser microphone
- 📱 **Phone support** — optional instructor-led demonstration of the same pipeline over a phone channel

---

## Prerequisites Checklist

The lab runs entirely in mock mode without Azure credentials. Before starting Lab 00, verify:

- [ ] **Python 3.11+** - `python --version`
- [ ] **Node.js 18** (shipped in devcontainer) - `node --version`
- [ ] **VS Code** with GitHub Copilot extension installed
- [ ] **Git** - `git --version`
- [ ] **GitHub Enterprise access** to `established-corp-emu-enterprise.ghe.com` (for Copilot CLI sign-in)
- [ ] **Microphone** (optional for voice exercises in Lab 05)

**No Azure subscription needed.** The entire pipeline runs in mock mode with `MOCK_MODE=true`. All tests pass locally.

---

## Mock Mode Setup (No Azure Credentials Required)

All labs run in **mock mode**, which means the entire pipeline operates offline without Azure services, keys, or subscriptions.

### Environment

```bash
# Backend (Python)
cd backend && ENVIRONMENT=test MOCK_MODE=true python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Frontend (TypeScript/React)
cd frontend && npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Health check (both must return `mock_mode=true`):
```bash
curl http://127.0.0.1:8000/api/health
# Frontend opens at http://127.0.0.1:5173
```

The ClearBoard UI displays `MODEL: MOCK-CLASSIFIER` in the top-right model badge.

### Copilot CLI Setup (GitHub Enterprise)

The devcontainer ships with Node 18. GitHub Copilot CLI requires Node 22+ via npm, so we install the standalone binary:

```bash
curl -fsSL https://gh.io/copilot-install | bash
# Binary location: ~/.local/bin/copilot
# (npm requires Node 22+, so binary avoids version conflict)

# Sign in with GHE.com (never default GitHub or PAT)
copilot login --host established-corp-emu-enterprise.ghe.com
```

**Browser Auth Fallback**: If the browser auth dialog appears, select **"Open in VS Code Desktop"**. Never paste a personal access token (PAT).

### Copilot in VS Code

Ensure your `.vscode/settings.json` presets the GitHub Enterprise URI:

```json
{
  "github-enterprise.uri": "established-corp-emu-enterprise.ghe.com",
  "github.copilot.advanced.authProvider": "github-enterprise"
}
```

Then:
- Press `Ctrl+Shift+I` to open Copilot Chat
- Press `Ctrl+I` for inline suggestions
- Use `@workspace` to query your entire repository

### Copy/Paste Tips (Windows/Linux)

For long responses from Copilot or terminal output:
1. **Shift-drag** to select text in the terminal
2. **Right-click** and choose **Copy**
3. Allow browser clipboard permissions when prompted
4. For very long content, save to a file first: `command > output.txt`

### Test Coverage

The lab includes **347 backend tests** and **4 frontend tests** (verified November 17). Run the focused suite:

```bash
cd backend && PYTHONPATH=. python -m pytest tests/test_schemas.py tests/test_voice/test_safety_net.py tests/test_voice/test_endpoints.py -q
```

The **96% score** referenced in evaluations is a **surge-resilience metric** (how many signals collapse into incidents without crashing dedup/routing), not model accuracy. RouterExecutor makes **zero LLM calls by design**.

---

## Lab Overview

| Lab | Title | Duration | What You'll Do |
|-----|-------|----------|----------------|
| **00** | Environment Setup | 30 min | Configure credentials, verify tools, test health endpoint |
| **01** | Understanding AI Agents | 90 min | Learn three-agent pattern, build intent classifier |
| **02** | Azure MCP Setup | 30 min | Configure MCP Server for Copilot, test Azure queries |
| **03** | Spec-Driven Development | 45 min | Write SPEC.md, create constitution, generate code from spec |
| **04** | Build RAG Pipeline | 120 min | Set up Azure AI Search, create embeddings, build RetrieveAgent |
| **05** | Agent Orchestration | 120 min | Wire up three-agent pipeline, implement handoffs, add multi-turn; optional voice/phone extension |
| **06** | Deploy with azd | 90 min | Deploy with ACR remote build, seed knowledge, verify Cosmos persistence |
| **07** | MCP Server (Stretch) | 60 min | Expose All Clear as an MCP server for Copilot Agent Mode |

**Total Estimated Time:** 9+ hours (full day boot camp)

---

## How to Get Help

1. **Raise your hand** - Instructors and lab assistants are circulating
2. **Check the solution folder** - Each lab has a `solution/` directory with reference implementations
3. **Use the boot camp chat channel** - Post questions for peer support
4. **Review troubleshooting sections** - Each lab README includes common issues and fixes
5. **Pair with a neighbor** - Two heads are better than one!

---

## Assessment Criteria

Your progress will be evaluated on these deliverables:

| Lab | Key Deliverable | Success Criteria |
|-----|-----------------|------------------|
| 00 | Environment verification | `verify_environment.py` passes all checks |
| 01 | Signal classifier | >90% accuracy on sample incident-triage signals |
| 02 | MCP configuration | `@azure` queries work in Copilot |
| 03 | Specification document | Complete SPEC.md with acceptance criteria |
| 04 | RAG pipeline | Hybrid search returns relevant KB articles with citations |
| 05 | Agent orchestration | Full pipeline handles multi-turn conversations |
| 06 | Azure deployment | Pipeline deployed; `/api/chat` returns and persists an incident |
| **Bonus** | **Voice & Phone Extensions (Bonus):** 10 points | Browser voice works; instructor phone bridge demonstrates end-to-end |

---

## Important Links

| Resource | URL |
|----------|-----|
| Repository | `https://github.com/Public-sector-hacks-Org/all-clear` |
| API Documentation | `http://localhost:8000/docs` (after starting backend) |
| Azure Portal | `https://portal.azure.com` |
| Azure OpenAI Studio | `https://oai.azure.com` |
| GitHub Copilot Docs | `https://docs.github.com/copilot` |
| Azure AI Search Docs | `https://learn.microsoft.com/azure/search/` |
| FastAPI Documentation | `https://fastapi.tiangolo.com` |

---

## Tips for Success

1. **Read the full lab README** before starting each exercise
2. **Don't skip Lab 00** - environment issues will slow you down later
3. **Commit frequently** - save your progress as you go
4. **Ask for help early** - don't struggle alone for more than 10 minutes
5. **Use Copilot liberally** - that's what it's here for!

---

Good luck, and have fun building surge-scale incident triage!
