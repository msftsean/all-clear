import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from verify_live_demo import SIGNALS, acceptance_checks, request_json, run


class LiveVerifierTests(unittest.TestCase):
    def test_http_transport_records_real_get_and_post_methods(self):
        response = MagicMock()
        response.status = 200
        response.read.return_value = b'{"mock_mode": false, "unexpected_secret": "not-retained"}'
        response.__enter__.return_value = response
        with patch("verify_live_demo.urlopen", return_value=response):
            get = request_json("https://example.invalid", "/api/health")
            post = request_json("https://example.invalid", "/api/signals", {"message": SIGNALS[0]})
        self.assertEqual(get["method"], "GET")
        self.assertEqual(post["method"], "POST")
        self.assertEqual(get["body"], {"mock_mode": False})
        self.assertNotIn("unexpected_secret", post["body"])

    def test_refuses_mock_before_any_application_writes(self):
        calls = []

        def request(base, path, payload=None):
            calls.append((path, payload))
            return {"status": 200, "body": {"mock_mode": True}}

        with patch.object(Path, "open", unittest.mock.mock_open()), patch.object(Path, "write_text"):
            result = run("https://example.invalid", "evidence.json", True, request)
        self.assertEqual(len(calls), 2)
        self.assertEqual(result["requests"], [])
        self.assertEqual(result["submission"], "blocked_by_live_preconditions")

    def test_runs_exactly_three_without_retry_after_uncertain_write(self):
        calls = []

        def request(base, path, payload=None):
            calls.append((path, payload))
            if path == "/api/health":
                return {"status": 200, "body": {"mock_mode": False, "storage_mode": "cosmos"}}
            if path == "/api/health/models":
                return {"status": 200, "body": {"mock_mode": False, "active": "gpt-5.1"}}
            return {"error": "TimeoutError"}

        with patch.object(Path, "open", unittest.mock.mock_open()), patch.object(Path, "write_text"):
            result = run("https://example.invalid", "evidence.json", True, request)
        writes = [payload for _, payload in calls if payload]
        self.assertEqual([p["message"] for p in writes], list(SIGNALS))
        self.assertEqual(len({p["session_id"] for p in writes}), 1)
        self.assertFalse(result["checks"]["three_successful_responses"])

    def test_existing_evidence_prevents_all_network_access(self):
        with patch.object(Path, "open", side_effect=FileExistsError):
            with self.assertRaises(FileExistsError):
                run("https://example.invalid", "evidence.json", True, lambda *a: self.fail())

    def test_healthy_model_status_does_not_pass_without_exact_results(self):
        checks = acceptance_checks(
            [{"status": 200, "body": {}}] * 3,
            {"mock_mode": False, "storage_mode": "cosmos"},
            {"mock_mode": False, "active": "gpt-5.1", "last_served": "gpt-5.1"},
        )
        self.assertFalse(checks["first_opens_sev1_escalated"])
        self.assertFalse(checks["duplicate_attaches_magnitude_two"])
        self.assertFalse(checks["billing_human_not_hazard"])

    def test_exact_results_pass_but_wrong_incident_and_forced_hazard_fail(self):
        first = {
            "signal_text": SIGNALS[0],
            "routing": {"outcome": "OPEN_INCIDENT", "severity": "SEV1", "escalate": True},
            "action": {"incident_id": "AC-1001", "severity": "SEV1", "escalated": True},
        }
        billing = {
            "signal_text": SIGNALS[1],
            "classification": {"intent_category": "HUMAN_REQUEST"},
            "routing": {
                "target_queue": "escalations", "severity": "SEV3", "escalate": True,
                "escalation_reason": "user_requested_human",
            },
            "action": {"escalated": True},
        }
        duplicate = {
            "signal_text": SIGNALS[2],
            "routing": {
                "outcome": "ATTACH_TO_INCIDENT", "matched_incident_id": "AC-1001",
                "magnitude": 2, "dedup_similarity": 1.0,
                "routing_rules_applied": ["dedup_match>=0.83"],
            },
            "action": {"incident_id": "AC-1001", "status": "attached"},
        }
        responses = [{"status": 200, "body": body} for body in (first, billing, duplicate)]
        health = {"mock_mode": False, "storage_mode": "cosmos"}
        models = {"mock_mode": False, "active": "gpt-5.1", "last_served": "gpt-5.1"}
        self.assertTrue(all(acceptance_checks(responses, health, models).values()))
        first["routing"].update(severity="SEV2", escalate=False)
        first["action"].update(severity="SEV2", escalated=False)
        self.assertFalse(acceptance_checks(responses, health, models)["first_opens_sev1_escalated"])
        duplicate["action"]["incident_id"] = "AC-9999"
        billing["routing"]["severity"] = "SEV1"
        checks = acceptance_checks(responses, health, models)
        self.assertFalse(checks["duplicate_attaches_magnitude_two"])
        self.assertFalse(checks["billing_human_not_hazard"])


if __name__ == "__main__":
    unittest.main()
