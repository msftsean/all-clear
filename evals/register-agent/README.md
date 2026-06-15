# Register All Clear as a Foundry agent

Registers All Clear as a Foundry **prompt agent** in the `allclear-redteam` project so it
becomes a selectable target in the New Foundry **Red team** and **Evaluation** _Create_ flows,
and for the `microsoft-foundry` skill's MCP eval tools.

## What gets registered

- **Agent name:** `all-clear-triage`
- **Kind:** `prompt` (model-backed)
- **Model:** `gpt-5.1` (already carries the `allclear-guardrails` content filter / Prompt Shields)
- **Instructions:** All Clear's reporter-facing incident-triage prompt (from
  `backend/app/agents/action_agent.py`) extended with the safety-override, PII/PHI,
  and human-in-the-loop rules the app enforces at runtime.

## Fidelity caveat (important)

This is the **model surface** of All Clear — instructions + content filter. It is **not** the
full live pipeline (QueryAgent → deterministic RouterExecutor → ActionAgent) or the app
guardrails (PII redaction, runtime crisis override, human-approval gate). Use it for portal-based
red team / eval **Create** flows and quick model-surface checks.

For the **higher-fidelity safety test** that exercises the real guardrails, keep using
[`../red-team/red_team_scan.py`](../red-team/red_team_scan.py), which red-teams the live
`/api/chat` backend. To make the *real pipeline* the registered target, register it as a
**hosted agent** (containerize per Foundry's hosted-agent protocol) — see the
`microsoft-foundry` skill's `create` → `deploy` workflow.

## Usage

```powershell
az login
$env:AZURE_AI_PROJECT_ENDPOINT = "https://allclear-foundry-kt5fw24guxoxy.services.ai.azure.com/api/projects/allclear-redteam"

pip install -r requirements.txt
python register_agent.py            # create/update the agent version
python register_agent.py --list     # list existing versions
```

Auth uses `DefaultAzureCredential`. The signed-in identity needs the Foundry project's
data-plane role (**Azure AI User** / **Azure AI Developer**) to create agent versions.

## Where to use the registered agent

- **Foundry portal** (New Foundry ON): **Red team** or **Evaluation** tab → **Create** →
  pick target **Agent** → `all-clear-triage`.
- **microsoft-foundry skill** (from VS Code with Azure MCP): the `observe` / red team workflows
  resolve this agent via [`../../.foundry/agent-metadata.yaml`](../../.foundry/agent-metadata.yaml).
