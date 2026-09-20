# All Clear - AI Quality Evals (Foundry)

The **AI-quality** leg of the All Clear eval surface. Companion to:

- `evals/red-team/` - adversarial **safety** eval (0.0% ASR), shows in Foundry **Red team** tab.
- `backend/tests/` - **functional** pytest suite (274 tests) gating CI.

This run scores the *live* agent's reporter-facing replies for **Relevance**, **Coherence**, and
**Fluency** with a GPT-4.1 judge, and uploads to the Foundry project's **Evaluations** tab.

## What it measures

For each triage signal in `queries.json` we call `POST /api/chat`, take
`PipelineResult.action.user_message` (the message the reporter sees), and judge it:

| Evaluator | Inputs | Asks |
| --------- | ------ | ---- |
| Relevance | query + response | Does the reply actually address the report? |
| Coherence | query + response | Is the reply logically structured and consistent? |
| Fluency   | response | Is the language clear and well-formed? |

Scores are 1-5 (higher is better), plus a pass-rate (`*_passed`) at the default threshold of 3.

Open the run in **Azure AI Foundry -> your project -> Evaluations**. Scores are expected to
reflect All Clear's deliberately terse triage acknowledgments. The useful lab outcome is the
gate: fail a build when Relevance or Coherence drops below the chosen threshold after a model or
prompt change.

## Run it

```powershell
cd evals/quality
pip install -r requirements.txt
$env:ALLCLEAR_BACKEND_URL      = "https://<your-backend-host>"
$env:AZURE_AI_PROJECT_ENDPOINT = "https://<your-foundry-subdomain>.services.ai.azure.com/api/projects/<your-project-name>"
$env:JUDGE_AZURE_ENDPOINT      = "https://<account>.openai.azure.com/"
$env:JUDGE_DEPLOYMENT          = "<your-judge-deployment>"
$env:JUDGE_API_KEY             = "<your-key>" # or omit when Azure CLI auth is configured
python quality_eval.py
```

Add `--skip-upload` to run locally without pushing to Foundry. Edit `queries.json` to change the
signal set.

## Judge model

The quality evaluators are prompt-based. Choose a judge deployment available in your own Azure
OpenAI resource; a non-reasoning model is recommended because the evaluator prompts set a fixed
temperature. Foundry's **Model catalog** (project home → **Model catalog**) lets you browse
available judge/chat models and use its **Compare** view side by side before picking a
`JUDGE_DEPLOYMENT` — useful if you'd rather evaluate options visually than read benchmark docs.

## Prefer the portal UI over the CLI?

Once a run has uploaded, open your project at <https://ai.azure.com> → **Evaluations** → the
`quality-smoke` run to see per-query Relevance/Coherence/Fluency scores and the judge's reasoning
for each, with no terminal required. See
[`exercises/01-glass-box-audit.md` → "Viewing it in the Foundry portal — no code required"](../../exercises/01-glass-box-audit.md#viewing-it-in-the-foundry-portal--no-code-required)
for the full walkthrough of that tab plus red-teaming and model comparison.
