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

## Latest run

`all-clear-quality-eval` - 10 signals, all lines completed.

| Metric | Score (avg) | Pass rate |
| ------ | ----------- | --------- |
| Relevance | 3.2 | 0.7 |
| Coherence | 3.1 | 0.6 |
| Fluency   | 3.3 | 1.0 |

Open in the portal: **Azure AI Foundry -> project `allclear-redteam` -> Evaluations**
(turn the "New Foundry" toggle **off** if the run does not render in the preview UI).

> These mid-3 scores are expected: All Clear's replies are deliberately terse triage
> acknowledgments, not long conversational answers. The value for the lab is the *gate*:
> wire this into CI and fail the build if Relevance/Coherence drop below threshold on a model or
> prompt change - that is the "eval suite gating CI" story from Day 1.

## Run it

```powershell
cd evals/quality
pip install -r requirements.txt
$env:ALLCLEAR_BACKEND_URL      = "https://<backend>.azurecontainerapps.io"
$env:AZURE_AI_PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/allclear-redteam"
$env:JUDGE_AZURE_ENDPOINT      = "https://<account>.openai.azure.com/"
$env:JUDGE_DEPLOYMENT          = "gpt-4.1-judge"
$env:JUDGE_API_KEY             = "<account-key>"
python quality_eval.py
```

Add `--skip-upload` to run locally without pushing to Foundry. Edit `queries.json` to change the
signal set.

## Judge model

The quality evaluators are prompt-based and judged by **`gpt-4.1-judge`** (a GPT-4.1 deployment on
the `allclear-foundry` account). A non-reasoning model is used on purpose - the GPT-5.x reasoning
models reject the fixed `temperature` the evaluator prompts set.
