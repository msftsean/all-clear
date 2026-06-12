# All Clear - Red Team Scan Results

**Scan:** `all-clear-redteam-demo` · run 2026-06-12 · Azure AI Foundry project `allclear-redteam`
**Target:** live All Clear agent (`POST /api/chat`) on Azure Container Apps, model `gpt-5.1`
behind the custom `allclear-guardrails` content filter.

Open in the portal: **Azure AI Foundry -> project `allclear-redteam` -> Red teaming**.

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
