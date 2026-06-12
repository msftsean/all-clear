"""All Clear - AI Red Teaming scan (Azure AI Foundry).

Runs the Azure AI Foundry **AI Red Teaming Agent** against the All Clear incident-triage
agent and uploads the results to a Foundry project, where they appear under the project's
**Red teaming** tab.

The scan exercises the *real* application: each adversarial prompt is sent to the deployed
backend (`POST /api/chat`), so the run measures the live agent plus its guardrails (PII
redaction, self-harm crisis escalation, the human-approval gate) and the Azure content
filter / Prompt Shields in front of the model - not a bare model call.

Usage (PowerShell):
    $env:AZURE_AI_PROJECT_ENDPOINT = "https://<resource>.services.ai.azure.com/api/projects/<project>"
    $env:ALLCLEAR_BACKEND_URL      = "https://allclear-...-backend....azurecontainerapps.io"
    python red_team_scan.py --num-objectives 5 --quick

Auth: uses DefaultAzureCredential (run `az login` first). The signed-in identity needs the
Foundry project's data-plane role (Azure AI User / Azure AI Developer) to upload results.
"""

from __future__ import annotations

import argparse
import asyncio
import os

import httpx
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory


def build_target(backend_url: str):
    """Return a callback that sends an attack prompt to the live All Clear agent.

    The red team agent (PyRIT _CallbackChatTarget) invokes this synchronously and expects a
    plain string back, so we use a synchronous httpx client. Each adversarial prompt runs
    through the full deployed pipeline - Azure content filter / Prompt Shields, then the app's
    own guardrails. A content-safety block (HTTP 400) is surfaced as text so it scores as a
    successful defense.
    """

    endpoint = backend_url.rstrip("/") + "/api/chat"

    def callback(query: str) -> str:
        try:
            resp = httpx.post(
                endpoint,
                json={"message": query[:4000], "channel": "redteam"},
                timeout=60,
            )
        except Exception as exc:  # network/timeout - report, don't crash the scan
            return f"[request_error] {exc}"

        if resp.status_code == 400:
            # Guardrail engaged: content filter / Prompt Shield rejected the input.
            return (
                "[blocked_by_content_safety] "
                "Signal rejected by content safety policy and was not processed."
            )
        if resp.status_code != 200:
            return f"[http_{resp.status_code}] {resp.text[:500]}"

        data = resp.json()
        # PipelineResult: surface the acknowledgment / drafted update the agent returned.
        for key in ("acknowledgment", "message", "sitrep", "response", "summary"):
            val = data.get(key) if isinstance(data, dict) else None
            if isinstance(val, str) and val:
                return val
        return str(data)[:2000]

    return callback


async def run(args: argparse.Namespace) -> None:
    project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    backend_url = os.environ.get("ALLCLEAR_BACKEND_URL", args.backend_url)

    if not project_endpoint:
        raise SystemExit(
            "Set AZURE_AI_PROJECT_ENDPOINT to your Foundry project endpoint "
            "(https://<resource>.services.ai.azure.com/api/projects/<project>)."
        )
    if not backend_url:
        raise SystemExit("Set ALLCLEAR_BACKEND_URL or pass --backend-url.")

    # The four harm risk categories the AI Red Teaming Agent probes.
    risk_categories = [
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm,
    ]

    red_team = RedTeam(
        azure_ai_project=project_endpoint,
        credential=DefaultAzureCredential(),
        risk_categories=risk_categories,
        num_objectives=args.num_objectives,
        application_scenario=(
            "An incident-triage agent for public-safety, education, and human-services "
            "agencies. It turns plain-language signals into structured, auditable incidents "
            "and drafts public status updates that wait for human approval. It handles "
            "regulated data (CJIS, HIPAA, FERPA) and must never leak PII/PHI or take an "
            "irreversible action without a human in the loop."
        ),
    )

    # Attack strategies = the transformations applied to seed prompts. "quick" keeps a small,
    # fast set for a live demo; the full set is broader and slower.
    if args.quick:
        strategies = [
            AttackStrategy.Flip,
            AttackStrategy.Base64,
            AttackStrategy.Morse,
        ]
    else:
        strategies = [
            AttackStrategy.EASY,
            AttackStrategy.MODERATE,
            AttackStrategy.Flip,
            AttackStrategy.Base64,
            AttackStrategy.Leetspeak,
            AttackStrategy.UnicodeConfusable,
        ]

    print(f"Target  : {backend_url}/api/chat (live All Clear agent)")
    print(f"Project : {project_endpoint}")
    print(f"Risks   : {[r.value for r in risk_categories]}")
    print(f"Strats  : {[s.value for s in strategies]}")
    print(f"Objs    : {args.num_objectives} per category")

    result = await red_team.scan(
        target=build_target(backend_url),
        scan_name=args.scan_name,
        attack_strategies=strategies,
        output_path=args.output_path,
    )

    print("\nScan complete. Results uploaded to the Foundry project's Red teaming tab.")
    print(f"Local copy: {args.output_path}")
    return result


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="All Clear AI red team scan (Azure AI Foundry).")
    p.add_argument("--scan-name", default="all-clear-redteam", help="Name shown in Foundry.")
    p.add_argument("--num-objectives", type=int, default=5, help="Attack objectives per risk category.")
    p.add_argument("--quick", action="store_true", help="Small/fast strategy set for a live demo.")
    p.add_argument("--backend-url", default="", help="All Clear backend base URL (or set ALLCLEAR_BACKEND_URL).")
    p.add_argument("--output-path", default="redteam_results.json", help="Local results file.")
    return p.parse_args()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))
