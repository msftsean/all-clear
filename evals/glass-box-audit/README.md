# All Clear - Glass-Box Audit Guardrail Eval (Foundry)

The **deterministic guardrail** leg of the All Clear eval surface. Companion to:

- `evals/quality/` - AI **quality** evals for live agent replies.
- `evals/red-team/` - adversarial **safety** evals surfaced in Foundry's Red team tab.

This run scores whether the Glass-Box guardrail behaves exactly as expected for
five labeled trace scenarios, then optionally uploads the result to the Foundry
project's **Evaluations** tab.

## What it measures

For each `EvalScenario` row in `scenarios.json`, we build a short synthetic
`list[TraceEvent]`, run it through the real `scripts/test_evaluator.py`
`evaluate_trace()` function, and compare the outcome with the expected label.

| Check | Inputs | Asks |
| ----- | ------ | ---- |
| `guardrail_passed` | expected_passed + actual_passed | Did the deterministic evaluator produce the expected pass/fail verdict for this scenario? |

Scenarios cover the exact rule combinations the workshop guardrail is supposed
to catch: `clean`, `fabrication_only`, `network_only`, `swarm_only`, and
`all_violations`.

Open the uploaded run in **Azure AI Foundry -> your project -> Evaluations**.
The useful gate is binary: every scenario must match its expected verdict.

## Run it

```powershell
cd evals/glass-box-audit
pip install -r requirements.txt
$env:AZURE_AI_PROJECT_ENDPOINT = "https://<your-foundry-subdomain>.services.ai.azure.com/api/projects/<your-project-name>"
python glass_box_eval.py
python glass_box_eval.py --skip-upload
```

- `python glass_box_eval.py` runs the deterministic local checks, writes
  `eval_data.jsonl`, and uploads the run to Foundry when
  `AZURE_AI_PROJECT_ENDPOINT` is set.
- `python glass_box_eval.py --skip-upload` runs the exact same local checks and
  writes the same `eval_data.jsonl`, but never imports Azure SDK packages and
  never attempts a Foundry upload.

## Deterministic evaluator (no LLM judge required)

Unlike `evals/quality/`, this evaluator is **fully rule-based**:

- no LLM judge
- no judge deployment
- no prompt-scored metric

It directly reuses `scripts/test_evaluator.py::evaluate_trace()`, so the
Foundry run and the local unittest run exercise the same code path with the
same flag-detection logic. That keeps the guardrail evidence auditable and
prevents eval drift between "what passed locally" and "what uploaded to
Foundry."
