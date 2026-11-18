"""Bounded live acceptance: read-only by default; opt in to exactly three signals.

Run once against a fresh deployment. An existing evidence file is never reused,
and uncertain/failed POSTs are never retried. No Azure credentials are needed.
"""

from __future__ import annotations

import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SIGNALS = (
    "There's a downed power line sparking on Oak Street near the school.",
    "My water bill is wrong, can someone call me?",
    "There's a downed power line sparking on Oak Street near the school.",
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def request_json(base, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = Request(
        base.rstrip("/") + path,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    result = {"started_at": utc_now(), "method": request.get_method(), "path": path}
    try:
        with urlopen(request, timeout=180) as response:
            result["status"] = response.status
            body = json.load(response)
        if path == "/api/health":
            keys = ("status", "mock_mode", "storage_mode", "domain")
        elif path == "/api/health/models":
            keys = ("active", "last_served", "mock_mode", "failover_active", "fallback_chain")
        else:
            keys = (
                "session_id", "channel", "signal_text", "classification",
                "routing", "action", "processing_ms",
            )
        result["body"] = {key: body[key] for key in keys if key in body}
    except HTTPError as exc:
        result.update(status=exc.code, error="HTTP request failed; body not logged")
    except (URLError, TimeoutError, ValueError, OSError) as exc:
        result["error"] = type(exc).__name__ + "; request not retried"
    result["elapsed_ms"] = round((time.perf_counter() - started) * 1000, 1)
    return result


def acceptance_checks(responses, health, models):
    checks = {
        "live_cosmos": health.get("mock_mode") is False
        and health.get("storage_mode") == "cosmos",
        "real_model_config": models.get("mock_mode") is False
        and models.get("active") == "gpt-5.1"
        and models.get("last_served") == "gpt-5.1",
        "three_successful_responses": len(responses) == 3
        and all(r.get("status") == 200 for r in responses),
    }
    if not checks["three_successful_responses"]:
        return checks
    first, billing, duplicate = [r.get("body", {}) for r in responses]
    route = first.get("routing", {})
    action = first.get("action", {})
    incident_id = action.get("incident_id")
    checks["first_opens_sev1_escalated"] = (
        route.get("outcome") == "OPEN_INCIDENT"
        and route.get("severity") == "SEV1"
        and route.get("escalate") is True
        and action.get("severity") == "SEV1"
        and action.get("escalated") is True
        and bool(incident_id)
    )
    route = billing.get("routing", {})
    action = billing.get("action", {})
    checks["billing_human_not_hazard"] = (
        billing.get("classification", {}).get("intent_category")
        in ("HUMAN_REQUEST", "CUSTOMER_INQUIRY")
        and route.get("target_queue") in ("escalations", "customer-comms")
        and route.get("severity") == "SEV3"
        and route.get("escalate") is True
        and route.get("escalation_reason") == "user_requested_human"
        and action.get("escalated") is True
    )
    route = duplicate.get("routing", {})
    action = duplicate.get("action", {})
    checks["duplicate_attaches_magnitude_two"] = (
        bool(incident_id)
        and route.get("outcome") == "ATTACH_TO_INCIDENT"
        and route.get("matched_incident_id") == incident_id
        and action.get("incident_id") == incident_id
        and action.get("status") == "attached"
        and route.get("magnitude") == 2
        and isinstance(route.get("dedup_similarity"), (int, float))
        and 0 <= route["dedup_similarity"] <= 1
        and any(rule.startswith("dedup_match>=") for rule in route.get("routing_rules_applied", []))
    )
    checks["three_signals_preserved_in_results"] = all(
        body.get("signal_text") == text
        for body, text in zip((first, billing, duplicate), SIGNALS)
    )
    return checks


def run(base, output, submit=False, request=request_json):
    evidence = {
        "started_at": utc_now(),
        "probe_id": "p29-acceptance-" + uuid.uuid4().hex,
        "backend": base,
        "requests": [],
        "limitations": [
            "Model status is configuration evidence, not per-response model identity.",
            "Confirm gpt-5.1 and Standard embeddings with Azure metadata and telemetry.",
            "Returned reports and magnitude do not independently prove durable persistence.",
            "Backend pytest conftest forces mock mode; it is not a live-config gate.",
            "This verifier does not certify browser rendering or Foundry portal visibility.",
        ],
    }
    output = Path(output)
    with output.open("x", encoding="utf-8") as handle:
        json.dump(evidence, handle, indent=2)

    def save():
        output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    health = request(base, "/api/health")
    models = request(base, "/api/health/models")
    evidence["health_before"] = health
    evidence["models_before"] = models
    save()
    prerequisites = (
        health.get("status") == models.get("status") == 200
        and health.get("body", {}).get("mock_mode") is False
        and health.get("body", {}).get("storage_mode") == "cosmos"
        and models.get("body", {}).get("mock_mode") is False
        and models.get("body", {}).get("active") == "gpt-5.1"
    )
    if submit and prerequisites:
        for number, text in enumerate(SIGNALS, 1):
            entry = {"number": number, "message": text, "attempt_started_at": utc_now()}
            evidence["requests"].append(entry)
            save()
            entry.update(request(base, "/api/signals", {
                "message": text,
                "session_id": evidence["probe_id"],
                "channel": "chat",
            }))
            save()
        evidence["models_after"] = request(base, "/api/health/models")
    else:
        evidence["submission"] = "disabled" if not submit else "blocked_by_live_preconditions"
    evidence["checks"] = acceptance_checks(
        evidence["requests"],
        health.get("body", {}),
        evidence.get("models_after", models).get("body", {}),
    )
    evidence["finished_at"] = utc_now()
    save()
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", required=True)
    parser.add_argument("--output", required=True, help="New sanitized JSON evidence file")
    parser.add_argument("--submit-three", action="store_true", help="Writes exactly three test signals")
    args = parser.parse_args()
    result = run(args.backend, args.output, args.submit_three)
    print(json.dumps(result["checks"], indent=2))
    raise SystemExit(0 if all(result["checks"].values()) else 1)
