# Challenge D — "The Phishing Report"

An employee reports: *"I think I leaked customer data. I replied to a phishing
email with a spreadsheet — it had names, an SSN (123-45-6789) and a card number.
What do I do?"*

**Build:** a pipeline that redacts the PII **before** anything is stored or echoed,
classifies the signal as a compliance report, routes it to the compliance-desk,
and escalates because a statutory/regulated-data exposure is in play.

---

- **Primary category:** `COMPLIANCE_REPORT`
- **Skill:** PII redaction on ingress + compliance routing + statutory escalation.
- **Done when:**
  - The SSN and card number are redacted to `[REDACTED]` before the text is embedded, stored, or returned (Constitution Art. I.1)
  - `pii_detected = True` with the correct `pii_types`
  - RouterExecutor routes to `compliance-desk` and sets `escalate = True` (regulated-data exposure)
  - The ActionAgent's sitrep references the compliance runbook — never repeats the raw PII
