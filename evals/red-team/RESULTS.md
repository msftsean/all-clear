# All Clear - Red Team Scan Results

**Scan:** `all-clear-redteam-demo` · run 2026-06-12 · Azure AI Foundry project `allclear-redteam`
**Target:** live All Clear agent (`POST /api/chat`) on Azure Container Apps, model `gpt-5.1`
behind the custom `allclear-guardrails` content filter.

### Where to show this in the portal (demo-day instructions)

**Important: turn the "New Foundry" toggle OFF** (top-center of the Foundry page) before opening
the Red team tab. The "New Foundry" preview UI filters on a run type that the current
`azure-ai-evaluation` SDK (1.17, latest) does not tag, so it shows "No red teams found" even
though the run is present. The classic view renders the full scorecard.

1. Azure AI Foundry -> project `allclear-redteam`.
2. Toggle **New Foundry OFF**.
3. **Evaluations -> Red team** -> open `all-clear-redteam-demo`.

Or use the direct classic deep link (works regardless of the toggle):
https://ai.azure.com/resource/build/redteaming/c73c5d72-d071-4c51-9a51-e3587b9b9ef1?wsid=/subscriptions/098ef2f6-cea4-4839-8093-ef90622e1b8c/resourceGroups/rg-allclear/providers/Microsoft.CognitiveServices/accounts/allclear-foundry/projects/allclear-redteam&tid=8251a5cb-be5c-4a08-b918-4ebc01628829

Verified present via the data plane: `GET .../redTeams/runs?api-version=2025-11-15-preview`
returns the run with status **Completed** and the 0.0% ASR scorecard.

### Showing a run in the New Foundry console (Create flow)

The SDK upload (`runType=eval_run`) renders only in the classic view. The **New Foundry** Red team
tab lists *native* red team runs created through its own service, so to get an entry there you
create the run in the portal:

1. In project `allclear-redteam`, go to **Evaluations -> Red team** and click **Create**.
2. Target type **Model deployment** -> pick **`gpt-5.1`** (deployed into this project with the
   `allclear-guardrails` content filter attached, so the run also exercises the guardrail).
3. Risk categories: Violence, Hate/Unfairness, Sexual, Self-harm. Attack strategies: Baseline +
   Easy (Flip, Base64, Morse) to mirror the SDK scan.
4. **Create** -> the run executes server-side and appears natively in the New Foundry Red team tab.

> The SDK scan (`red_team_scan.py`) targets the live *agent* endpoint (`POST /api/chat`); the
> portal Create flow targets the *model deployment*. Run both: the agent scan proves the full
> pipeline, the model run shows natively in the new console and demonstrates the content filter.

## Headline

| Metric | Result |
| ------ | ------ |
| **Overall attack success rate (ASR)** | **0.0%** |
| Total adversarial attacks | 48 |
| Successful attacks | 0 |

Every adversarial prompt was defended - either blocked by the content filter / Prompt Shields,
or handled safely by the agent (e.g. routed to human escalation) without producing harmful output.

## By risk category (12 attacks each)

| Risk category | Attacks | Successful | ASR |
| ------------- | ------- | ---------- | --- |
| Violence | 12 | 0 | 0.0% |
| Hate / Unfairness | 12 | 0 | 0.0% |
| Sexual | 12 | 0 | 0.0% |
| Self-harm | 12 | 0 | 0.0% |

## By attack technique

| Complexity | Techniques | Attacks | ASR |
| ---------- | ---------- | ------- | --- |
| Baseline (raw objective) | - | 12 | 0.0% |
| Easy | Flip, Base64, Morse | 36 | 0.0% |

Per-technique ASR (easy complexity) was 0.0% for **flip**, **base64**, and **morse** across all
four risk categories.

## How to reproduce / extend

```powershell
cd evals/red-team
pip install -r requirements.txt
$env:AZURE_AI_PROJECT_ENDPOINT = "https://allclear-foundry-kt5fw24guxoxy.services.ai.azure.com/api/projects/allclear-redteam"
$env:ALLCLEAR_BACKEND_URL      = "https://allclear-kt5fw24guxoxy-backend.nicebay-0aac45bb.eastus.azurecontainerapps.io"
python red_team_scan.py --quick --num-objectives 3      # this run
python red_team_scan.py --num-objectives 5              # broader: adds Leetspeak, Unicode, Easy/Moderate composites
```

> Note: a 0.0% ASR here means the *current* configuration defended this objective/strategy set.
> For an ongoing safety posture, widen `--num-objectives` and drop `--quick` (adds Moderate/
> Difficult strategies) and re-run on every model or prompt change - that is the eval-gates-CI
> story from Day 1.
