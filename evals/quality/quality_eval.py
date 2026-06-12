"""All Clear - AI quality evaluation (uploads to Azure AI Foundry).

What it does
------------
1. Runs a set of realistic triage signals through the *live* All Clear agent
   (`POST /api/chat`) and captures the agent's reporter-facing reply
   (`PipelineResult.action.user_message`).
2. Scores each reply with Foundry's built-in AI-quality evaluators
   (Relevance, Coherence, Fluency) using a GPT-4.1 judge.
3. Uploads the run to the Foundry project's **Evaluations** tab so it shows up
   next to the Red team runs.

This is the AI-quality companion to `evals/red-team` (safety) and the pytest
suite in `backend/tests` (functional). Together they are the eval surface the
Day-2 lab "eval suite gating CI" story points at.

Usage
-----
    cd evals/quality
    pip install -r requirements.txt
    $env:ALLCLEAR_BACKEND_URL       = "https://<backend>.azurecontainerapps.io"
    $env:AZURE_AI_PROJECT_ENDPOINT  = "https://<account>.services.ai.azure.com/api/projects/<project>"
    $env:JUDGE_AZURE_ENDPOINT       = "https://<account>.openai.azure.com/"
    $env:JUDGE_DEPLOYMENT           = "gpt-4.1-judge"
    $env:JUDGE_API_KEY              = "<key>"        # or omit to use AzureCliCredential
    python quality_eval.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

HERE = Path(__file__).parent
DEFAULT_QUERIES = HERE / "queries.json"
JUDGE_API_VERSION = "2024-10-21"


def collect_responses(backend_url: str, queries: list[dict], timeout: float) -> list[dict]:
    """Call the live agent for each query and build eval rows."""
    rows: list[dict] = []
    backend_url = backend_url.rstrip("/")
    with httpx.Client(timeout=timeout) as client:
        for q in queries:
            message = q["message"]
            channel = q.get("channel", "chat")
            try:
                resp = client.post(
                    f"{backend_url}/api/chat",
                    json={"message": message, "channel": channel},
                )
                resp.raise_for_status()
                result = resp.json()
                action = result.get("action", {}) or {}
                answer = action.get("user_message") or ""
                # Context = retrieved KB snippets + sitrep summary, for groundedness signal.
                ctx_parts = [
                    a.get("snippet", "")
                    for a in (action.get("knowledge_articles") or [])
                    if a.get("snippet")
                ]
                sitrep = action.get("sitrep") or {}
                if sitrep.get("summary"):
                    ctx_parts.append(sitrep["summary"])
                context = "\n".join(ctx_parts) if ctx_parts else "No knowledge-base context retrieved."
                rows.append(
                    {
                        "id": q.get("id", ""),
                        "query": message,
                        "response": answer,
                        "context": context,
                    }
                )
                print(f"  [{q.get('id','?')}] ok ({len(answer)} chars) <- {channel}")
            except Exception as exc:  # noqa: BLE001
                print(f"  [{q.get('id','?')}] FAILED: {exc!r}", file=sys.stderr)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="All Clear AI-quality eval -> Foundry")
    parser.add_argument("--queries", default=str(DEFAULT_QUERIES))
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--skip-upload", action="store_true", help="run locally, do not upload to Foundry")
    args = parser.parse_args()

    backend_url = os.environ.get("ALLCLEAR_BACKEND_URL")
    project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    judge_endpoint = os.environ.get("JUDGE_AZURE_ENDPOINT")
    judge_deployment = os.environ.get("JUDGE_DEPLOYMENT", "gpt-4.1-judge")
    judge_key = os.environ.get("JUDGE_API_KEY")

    if not backend_url:
        print("ERROR: set ALLCLEAR_BACKEND_URL", file=sys.stderr)
        return 2
    if not judge_endpoint:
        print("ERROR: set JUDGE_AZURE_ENDPOINT", file=sys.stderr)
        return 2

    # Import here so --help works without the SDK installed.
    from azure.ai.evaluation import (
        CoherenceEvaluator,
        FluencyEvaluator,
        RelevanceEvaluator,
        evaluate,
    )

    model_config: dict = {
        "azure_endpoint": judge_endpoint,
        "azure_deployment": judge_deployment,
        "api_version": JUDGE_API_VERSION,
    }
    if judge_key:
        model_config["api_key"] = judge_key

    queries = json.loads(Path(args.queries).read_text(encoding="utf-8"))
    print(f"Collecting agent responses for {len(queries)} signals from {backend_url} ...")
    rows = collect_responses(backend_url, queries, args.timeout)
    if not rows:
        print("ERROR: no responses collected; aborting.", file=sys.stderr)
        return 1

    data_path = HERE / "eval_data.jsonl"
    with data_path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"Wrote {len(rows)} rows -> {data_path}")

    evaluators = {
        "relevance": RelevanceEvaluator(model_config),
        "coherence": CoherenceEvaluator(model_config),
        "fluency": FluencyEvaluator(model_config),
    }
    evaluator_config = {
        "relevance": {"column_mapping": {"query": "${data.query}", "response": "${data.response}"}},
        "coherence": {"column_mapping": {"query": "${data.query}", "response": "${data.response}"}},
        "fluency": {"column_mapping": {"response": "${data.response}"}},
    }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    output_path = HERE / f"quality_results_{stamp}.json"

    kwargs: dict = {
        "data": str(data_path),
        "evaluators": evaluators,
        "evaluator_config": evaluator_config,
        "evaluation_name": "all-clear-quality-eval",
        "output_path": str(output_path),
    }
    if project_endpoint and not args.skip_upload:
        kwargs["azure_ai_project"] = project_endpoint
        print(f"Uploading run to Foundry project: {project_endpoint}")
    else:
        print("Running locally (no Foundry upload).")

    result = evaluate(**kwargs)

    metrics = result.get("metrics", {}) if isinstance(result, dict) else {}
    print("\n==== AI-quality scorecard (1-5, higher is better) ====")
    for k in sorted(metrics):
        print(f"  {k}: {metrics[k]}")
    studio = result.get("studio_url") if isinstance(result, dict) else None
    if studio:
        print(f"\nFoundry run: {studio}")
    print(f"Local results: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
