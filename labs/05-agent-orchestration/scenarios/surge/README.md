# All Clear Surge Challenge Cards

Build-sprint challenge prompts grounded in the real All Clear domain (`CONTEXT.md`)
and the shipped pipeline (`backend/app/agents/`). Each team picks one card and
extends the **QueryAgent → RouterExecutor → ActionAgent** pipeline to satisfy it.

Every card maps to the canonical `SignalCategory` taxonomy in
`backend/app/agents/schemas.py` and the deterministic severity / dedup / escalation
rules in `RouterExecutor` (`backend/app/agents/router_agent.py`). The goal is always
the same: turn an inbound **Signal** into the right **Incident** (`AC-####`) action
with bounded authority and a citation-grounded sitrep.

| Card | Title | Primary category | Key behavior |
|---|---|---|---|
| [A](challenge-a-downed-line.md) | The Downed Line | `PUBLIC_SAFETY` | SEV1 life-safety → `OPEN_INCIDENT`, always escalates, 15-min SLA |
| [B](challenge-b-storm-surge.md) | The Storm Surge | `INFRASTRUCTURE_OUTAGE` | Dedup storm: many reports → one incident, Magnitude climbs |
| [C](challenge-c-gas-leak.md) | The Gas Leak | `FIELD_HAZARD` | Field-operations dispatch + escalation, no auto-resolve |
| [D](challenge-d-phishing-to-incident.md) | The Phishing Report | `COMPLIANCE_REPORT` | PII redaction + compliance-desk routing, statutory escalation |
| [E](challenge-e-status-check.md) | The Status Check | `STATUS_CHECK` | Read-only sitrep, **no** new incident, citation-grounded |
| [F](challenge-f-human-request.md) | The Human Request | `HUMAN_REQUEST` | Bounded authority: hand off to a human, never auto-act |

## Run the dedup smoke test

The smoke test streams the 25-signal surge replay fixture
(`backend/mock_data/surge_replay_25.json`) through the real pipeline in mock mode and
asserts the Exercise 5 dedup checkpoint: **≤ 6 open incidents and ≥ 19 attachments**.

```bash
cd backend
PYTHONPATH=. ENVIRONMENT=test MOCK_MODE=true python ../labs/05-agent-orchestration/scenarios/surge/smoke_test.py
```

On Windows PowerShell:

```powershell
cd backend
$env:ENVIRONMENT="test"; $env:MOCK_MODE="true"; $env:PYTHONPATH="."
.\.venv\Scripts\python.exe ..\labs\05-agent-orchestration\scenarios\surge\smoke_test.py
```

Card text is the build spec — keep behavior locked to `CONTEXT.md` and the
Constitution (`shared/constitution.md`): bounded authority (Art. II), escalation
safety (Art. III), and "no citation, no claim" (Art. IV).
