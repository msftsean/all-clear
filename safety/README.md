# All Clear - Safety & Guardrails (showable in Azure AI Foundry)

This folder turns All Clear's safety story from "it's in the code" into "here it is in the
portal." It has two parts:

| Folder | What it provisions | Where you show it |
| ------ | ------------------ | ----------------- |
| `content-filter/` | A **custom content filter** (`allclear-guardrails`) attached to the `gpt-5.1` deployment | Foundry / Azure OpenAI -> **Guardrails + controls -> Content filters** |
| `foundry-project/` | An **Azure AI Foundry project** (`allclear-redteam`) to host red-team runs + safety evals | Foundry portal -> project -> **Red teaming** |

The red team scan that publishes into that project lives in [`../evals/red-team/`](../evals/red-team/).

## The honest before/after

**Before:** the app ran on plain Azure OpenAI accounts with only the *default* content filter,
and all of All Clear's domain guardrails existed only in Python:

- Self-harm crisis escalation - `backend/app/agents/safety.py`, `backend/app/agents/escalation_rules.py`
- PII/PHI redaction - `backend/app/services/pii.py`, applied in `backend/app/agents/pipeline.py`
- Sensitive-PII (SSN / credit card) -> human handoff - `backend/app/agents/router_agent.py`
- Content-safety block -> HTTP 400 (not 500) - `backend/app/api/routes.py`
- Voice prompt lock + transcript redaction - `backend/app/api/realtime.py`

These code guardrails are good, but a customer or auditor can't *see* them in a portal.

**After:** a named, customized content filter is attached to the deployment and a Foundry
project holds reproducible red-team scorecards - both visible in the Foundry UI.

## Why the content filter thresholds are tuned (not just "max everything")

All Clear is a **public-safety** agent. Real signals legitimately mention violence ("power line
down, sparking near a school") and self-harm ("a student said they want to hurt themselves").
Hard-blocking those at the **input** would stop the agent from ever seeing a person in crisis.

So in `allclear-guardrails`:

- **Violence / Self-harm (prompt side):** threshold **High** - block only the most severe; let
  genuine emergency reports through to the agent, where the app's crisis-escalation guardrail
  routes them to a human.
- **Hate / Sexual / Profanity (prompt side):** **Medium** - block abuse.
- **Jailbreak + Indirect Attack (Prompt Shields):** **on** - block prompt-injection attempts.
- **Completion side:** Medium across harm categories + **Protected Material** detection.

That is the demo narrative: **platform content filter + app guardrail working together**, tuned
for the domain rather than blindly maxed.

## Run order

```powershell
az login
.\foundry-project\create_foundry_project.ps1     # 1. project to host results (East US 2)
.\content-filter\apply_content_filter.ps1         # 2. custom filter on the gpt-5.1 deployment
# 3. then run the scan in ../evals/red-team/
```

## What is live right now

- Foundry project: `allclear-redteam` (account `allclear-foundry`, rg `rg-allclear`, **East US 2**)
  - endpoint: `https://allclear-foundry-kt5fw24guxoxy.services.ai.azure.com/api/projects/allclear-redteam`
- Custom content filter `allclear-guardrails` attached to `gpt-5.1` on `allclear-kt5fw24guxoxy-openai`.

## IaC note

`content-filter/allclear-guardrails.rai.json` is the policy definition; the apply script uses
`az rest` so it can run against the already-deployed account without disturbing the azd-managed
`infra/main.bicep`. To bake this into the main deployment later, add a
`Microsoft.CognitiveServices/accounts/raiPolicies` resource to `infra/main.bicep` and set the
deployment's `raiPolicyName`.
