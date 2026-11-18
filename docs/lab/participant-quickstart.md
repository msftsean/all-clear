# All Clear Participant Quickstart

**Last verified:** Nov 17, 2026 · **Tests:** 347 backend + 4 frontend passed, mock mode

**Mock mode is the whole-lab path:** no Azure sign-in, keys, or resources are needed.

## 1. Open your Codespace

1. Sign in with your event-issued **GHE.com** identity. Never use a personal
   GitHub account and **never paste a PAT**.
2. **Code → Codespaces → New with options:** your assigned `pNN` branch (or
   `main` if none is assigned), **4-core**. Keep forwarded ports **private**.

## 2. Start the mock app (one backend, one frontend)

**Terminal 1 — backend:**

```bash
cd backend && ENVIRONMENT=test MOCK_MODE=true python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — frontend:**

```bash
cd frontend && npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Run each command **once** and leave both terminals open. Do not start a second
copy: it fails because the port is already in use. To restart a server, press
**Ctrl+C** in its terminal, then rerun its command.

**Open the app:** in the **Ports** tab, open port **5173**. The header shows
**MODEL: MOCK-CLASSIFIER**. Submit the same synthetic report twice: the second
attaches to the first incident instead of creating a new one.

## 3. Copilot CLI and sign-in

```bash
curl -fsSL https://gh.io/copilot-install | bash
~/.local/bin/copilot --version
copilot login --host established-corp-emu-enterprise.ghe.com
```

- In the browser prompt, **choose GHE.com**, never the default GitHub option.
- **Never paste a PAT**; use browser sign-in.
- **Browser fallback:** if browser sign-in fails, select **Open in VS Code Desktop**.
- If `copilot` is not found, add `~/.local/bin` to `PATH` or use the full path.

## 4. Spec Kit stages (Copilot Chat, agent mode)

Run one exercise with `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`,
then `/speckit.implement`. Read each output before continuing. Stop before any
commit or push; push only your own `pNN` branch, with coach approval.
Governance: [constitution](../../.specify/memory/constitution.md) and
[CONTEXT.md](../../CONTEXT.md).

**Copying long answers:**

- **Shift+drag** to select, then **right-click → Copy**.
- **Allow clipboard** access when the browser asks.
- **Save long answers to a file** in the repo instead of copying from the terminal.

## 5. Key facts

- **Routing:** RouterExecutor makes **zero LLM calls**; dedup, severity, SLA,
  and escalation are deterministic rules.
- **96%** is the **any-crash** measure, **not** an accuracy score.
- Verify with `npm run smoke-test` (backend tests, then frontend unit tests).

## Optional Azure stretch (coach-approved only)

Not required for any core step. If a coach enables it: region **East US 2**,
resource group **`rg-allclear-pNN`**, **Standard** embeddings deployment, and
capacity for **6 participants + 1 demo**. Otherwise do not run `az login`,
`azd auth login`, or `azd up`, and never add credentials to `.env`.
Lab sequence starts at [labs/00-setup](../../labs/00-setup/).