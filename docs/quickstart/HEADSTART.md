# 🚪 Head-Start Guide — From Cold Start to Scenario-Ready

> **Goal:** get from *zero* to **scenario-ready** (Labs 01 & 04 effectively done)
> in minutes, so your time goes to the AJCU scenarios in
> [Lab 05](../../labs/05-agent-orchestration/scenarios/ajcu/README.md) — not setup.

If you have never used GitHub Codespaces, GitHub Copilot, or Azure AI tooling,
**start here.** The labs stay intact as optional deep-dives; this guide is the
fast lane that does the "plumbing" (intent classification + the RAG index) for
you so a cold team still reaches the scenarios.

> ⭐ **For the 3-hour AJCU workshop, the recommended lane is 🔵 Self-serve `azd`
> (Lane 2).** A single `azd up` provisions Azure **and** auto-seeds the AI Search
> index via the `azure.yaml` **`postprovision`** hook, so you reach
> **scenario-ready at the moment `azd up` finishes** — no extra seeding step. The
> Shared-backend and Mock lanes remain as alternatives.

---

## ⏱️ Day-0 (before the room) — 10 minutes

Do these once, ideally the day before:

1. **Open GitHub Codespaces** on this repo: green **`< > Code`** button →
   **Codespaces** tab → **Create codespace on `main`**. Everything (Python 3.11,
   Node, dependencies) is preinstalled — no local install required.
2. **Sign in to GitHub Copilot** in the Codespace (Copilot icon in the sidebar →
   *Sign in*). You'll use Copilot/Claude during the labs and scenarios.
3. **(Self-serve lane only) Authenticate to Azure** so `azd` can provision:
   ```bash
   azd auth login
   ```
   Skip this if you're using the **shared backend** or **mock** lane.

You are ready for Day-1 when the Codespace is open, Copilot is signed in, and
(optionally) `azd auth login` succeeded.

---

## 🛣️ Pick your lane

There are **three** ways to reach scenario-ready. For the 3-hour AJCU workshop the
**default is 🔵 Self-serve `azd` (Lane 2)**; otherwise pick the first one that fits.

| Lane | Use when | Azure needed? | Command |
|---|---|---|---|
| 🔵 **Self-serve azd** ⭐ *default* | Your team wants its own Azure stack | Yes (your sub) | `azd up` (auto-seeds via the postprovision hook) |
| 🟢 **Shared backend** | The coach has provisioned a shared stack and shared an endpoint out-of-band | No (uses shared) | configure `.env` with the shared values, then `bash scripts/quickstart.sh` |
| 🟡 **Mock (offline)** | You're blocked on Azure access (Conditional Access, quota) | **No** | `bash scripts/quickstart.sh --mock` |

### 🟢 Lane 1 — Shared backend (coach-provisioned)

The coach runs `azd up` once and distributes the AI Search + OpenAI
endpoint/keys **out-of-band** (never committed to the repo). Put them in your
environment or a local `.env`, then run the same one command everyone uses:

```bash
# Required env (values provided by your coach — never commit them):
#   AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY, AZURE_SEARCH_INDEX_NAME
#   AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_EMBEDDING_DEPLOYMENT
bash scripts/quickstart.sh
```

This seeds the index → verifies it → runs the backend smoke check, idempotently.

### 🔵 Lane 2 — Self-serve `azd` (your own stack)

One command provisions infra **and** auto-seeds the index so the environment is
"Lab-04-complete" when provisioning finishes:

```bash
azd auth login      # if you haven't already (Day-0)
azd up              # provisions, then runs the postprovision seed hook
```

The `postprovision` hook calls `scripts/quickstart.sh --no-smoke` and is
**non-fatal**: if seeding hiccups (quota, transient 429), provisioning still
succeeds and prints the exact manual re-run command. To seed/verify manually
afterward:

```bash
bash scripts/quickstart.sh
```

### 🟡 Lane 3 — Mock / offline (zero Azure credentials)

Blocked on Azure? You can still reach a working scenario lane with **no
credentials**:

```bash
bash scripts/quickstart.sh --mock
```

This validates the mock pipeline (intent classification + KB search) and the
backend `/api/health` endpoint with `USE_MOCK_MODE=true`.

---

## 🌱 Just the seeder (advanced)

`quickstart.sh` calls this for you, but you can run the seeder directly:

```bash
# Offline preview — lists the documents, makes NO Azure calls, needs no creds:
python scripts/seed_search_index.py --dry-run

# Live seed (idempotent upsert keyed by article_id):
python scripts/seed_search_index.py --data-dir infra/ai-search/seed-articles
```

Re-running never duplicates documents — each is upserted by its stable
`article_id`.

---

## ✅ You are *scenario-ready* when…

Tie this checklist to the actual `verify`/`smoke` output:

- [ ] **Live lanes (shared / self-serve):** `bash scripts/quickstart.sh` exits `0`
      and prints the **`✅ Scenario-ready`** banner.
- [ ] The verify step (`labs/04-build-rag-pipeline/verify_index.py`) reports the
      seeded document count and a working keyword search (e.g. *"password reset"*).
- [ ] The backend smoke check shows `✓ PASS: Backend /api/health responding`.
- [ ] **Mock lane:** `bash scripts/quickstart.sh --mock` exits `0` and prints
      **`✅ Scenario-ready`** with all three mock checks `✓ PASS`.
- [ ] You can open
      [`labs/05-agent-orchestration/scenarios/ajcu/README.md`](../../labs/05-agent-orchestration/scenarios/ajcu/README.md)
      and start a challenge.

When the banner shows **`✅ Scenario-ready`**, Labs 01 & 04 are effectively done —
go straight to the AJCU scenarios.

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---|---|
| `exit 2` naming missing vars | Set the named `AZURE_*` variables (or use `--mock`). Values are never printed — only names. |
| Seeding fails under `azd up` | It's non-fatal by design. Re-run `bash scripts/quickstart.sh` once env is set. |
| No Azure access at all | Use `bash scripts/quickstart.sh --mock` and continue with the mock lane. |
| Want to preview without seeding | `python scripts/seed_search_index.py --dry-run` (no credentials needed). |

> 🔐 **Secrets:** endpoints/keys come from your environment or `.env` and are
> **never** committed or printed. The shared-backend values are distributed
> out-of-band by your coach.
