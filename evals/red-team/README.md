# All Clear - Red Teaming in Azure AI Foundry

This folder runs the **Azure AI Foundry AI Red Teaming Agent** against the live All Clear
incident-triage agent and uploads the results to a Foundry project, where they appear under
the project's **Red teaming** tab for a live demo.

## What was real before this, and what this adds

Before this work, All Clear's safety controls were:

- **Default platform content filter** (`Microsoft.DefaultV2`) on the `gpt-5.1` deployment - on,
  but invisible/uncustomized.
- **App-level guardrails in Python code only** (not in any portal): self-harm crisis escalation,
  PII/PHI redaction, sensitive-PII -> human handoff, the human-approval gate, voice-prompt lock.
- **No Foundry project, and no red team evaluation anywhere.**

This package makes the safety story **showable in Foundry**:

1. A **custom content filter** (`allclear-guardrails`) - see `../../safety/content-filter/` -
   authored, attached to the deployment, and visible in the Foundry portal.
2. A **Foundry project** (`allclear-redteam`) - see `../../safety/foundry-project/` - to host
   red-team runs and safety evaluations.
3. This **red team scan** that probes the live agent and publishes scored results to that project.

## Prerequisites

```powershell
pip install -r requirements.txt   # azure-ai-evaluation[redteam], azure-identity, httpx
az login                          # signed-in user needs "Azure AI User" on the Foundry account
```

Provision the project + content filter once (idempotent):

```powershell
..\..\safety\foundry-project\create_foundry_project.ps1
..\..\safety\content-filter\apply_content_filter.ps1
```

## Run a scan

```powershell
$env:AZURE_AI_PROJECT_ENDPOINT = "https://allclear-foundry-kt5fw24guxoxy.services.ai.azure.com/api/projects/allclear-redteam"
$env:ALLCLEAR_BACKEND_URL      = "https://allclear-kt5fw24guxoxy-backend.nicebay-0aac45bb.eastus.azurecontainerapps.io"

# Fast set for a live demo (3 strategies x 4 risk categories x N objectives):
python red_team_scan.py --quick --num-objectives 3 --scan-name "all-clear-redteam-demo"

# Broader run:
python red_team_scan.py --num-objectives 5
```

Then open **Azure AI Foundry -> your project -> Red teaming** to show the scorecard
(attack-success rate per risk category and per attack strategy).

## How it probes the *real* agent

`red_team_scan.py` targets a callback that POSTs each adversarial prompt to the deployed
backend (`POST /api/chat`). So every attack runs through the full pipeline - Azure content
filter / Prompt Shields, then the app's own guardrails - not a bare model call. A content-safety
rejection (HTTP 400) is surfaced as `[blocked_by_content_safety]`, which scores as a successful
defense.

- **Risk categories:** Violence, Hate/Unfairness, Sexual, Self-harm (the four harm categories the
  Foundry safety service generates objectives for).
- **Attack strategies:** `--quick` uses Flip / Base64 / Morse; the full set adds Easy/Moderate
  composites, Leetspeak, and Unicode confusables.
- **Region:** the Foundry project lives in **East US 2** (the red-teaming service is only in
  East US 2, North Central US, France Central, Sweden Central, Switzerland West). The backend
  target stays in East US - it is just called over HTTPS.

## Files

| File | Purpose |
| ---- | ------- |
| `red_team_scan.py` | The scan. Configurable target, risk categories, strategies, objectives. |
| `requirements.txt` | `azure-ai-evaluation[redteam]`, `azure-identity`, `httpx`. |
| `redteam_results.json` | Local copy of the most recent scan result (also uploaded to Foundry). |
