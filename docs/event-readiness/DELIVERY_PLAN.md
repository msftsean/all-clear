# All Clear Event Readiness Delivery Plan

**Audience:** facilitators and event owners  
**Event:** Azure Days Arlington, Day 2 — Wednesday, November 18, 2026, 9:00 AM–4:45 PM ET (465 minutes).
**Decision:** run the mock-runnable S0–S6 participant path. Do not attempt the full lab catalog in one event day.

## Scope cut

The repository contains more workshop material than can honestly fit the event day. The event-ready path is the seven-block participant path in `participant-runbook/index.html`: setup, classification, spec discipline, grounded retrieval, orchestration/surge, GitHub verification, and pilot planning/demos. This path is **375 minutes of working time plus 90 minutes of breaks, buffer, and working lunch**.

The required path intentionally cuts live cloud buildout from the completion contract. `labs/README.md` names `00 -> 01 -> 03 -> 04 -> 05 -> 09` as the event build path; Lab 09 is required and Labs 02, 06, 07, and 08 are optional extensions. Voice, phone, and failover continuity remain optional/facilitator-led.

## 465-minute run of show

| Clock | Minutes | Block | Status | Repository artifacts | Completion evidence | Facilitator fallback |
| --- | ---: | --- | --- | --- | --- | --- |
| 9:00-9:30 | 30 | **S0 - Setup and mock baseline** | Required | `participant-runbook/index.html#stage0`; `labs/00-setup/README.md`; `labs/00-setup/verify_environment.py`; `CONTEXT.md`; `.specify/memory/constitution.md` | `cd labs/00-setup && python verify_environment.py` passes; mock mode or the shared backend provides a healthy `/api/health`. | Use Codespaces if local setup stalls. Keep `MOCK_MODE=true`; pair blocked participants with the shared backend. |
| 9:30-10:15 | 45 | **S1 - Classify signals and bounded authority** | Required | `participant-runbook/index.html#stage1`; `labs/01-understanding-agents/README.md`; `labs/01-understanding-agents/exercises/01a-intent-classification.md`; `labs/01-understanding-agents/exercises/01b-prompt-engineering.md`; `CONTEXT.md` | A typed `SignalClassification` is produced; participants can explain classify-only, deterministic decide-only, and bounded act-only authority. | Coach from the bounded-authority matrix and use the provided test fixture or reference path for discussion. |
| 10:15-10:30 | 15 | **Break** | Required break | N/A | Participants stop work; facilitators triage setup blockers. | Move unresolved environment blockers to the shared-backend path before S2. |
| 10:30-11:15 | 45 | **S2 - Spec-driven capability** | Required | `participant-runbook/index.html#stage2`; `labs/03-spec-driven-development/README.md`; exercises 03a/03b; `.specify/memory/constitution.md`; `CONTEXT.md` | A Spec Kit spec, plan, and tasks use All Clear terms, preserve bounded authority and statutory-clock SEV1 escalation, and name verifiers before implementation. | If Copilot/Spec Kit commands are unavailable, use the README acceptance bullets as a manual review rubric. |
| 11:15-12:15 | 60 | **S3 - Grounded retrieval and citations** | Required | `participant-runbook/index.html#stage3`; `labs/04-build-rag-pipeline/README.md`; `verify_index.py`; `test_rag.py`; `CONTEXT.md` | `cd labs/04-build-rag-pipeline && python verify_index.py` and `python test_rag.py` pass; cited records trace to the local corpus. | Use the pre-populated/mock knowledge corpus. Do not spend event time creating embeddings or re-provisioning search. |
| 12:15-12:30 | 15 | **Buffer / table check** | Buffer | N/A | Facilitators confirm each table has S0-S3 evidence or a fallback assignment before orchestration starts. | Triage participants into green path, shared-backend path, or observe-and-run-tests path. |
| 12:30-1:15 | 45 | **Working lunch (optional glass-box audit)** | Protected lunch; audit optional | `evals/glass-box-audit/README.md`; `participant-runbook/index.html#stage4` | Lunch remains protected; interested attendees may review the glass-box audit without making it a completion gate. | Skip the audit if tables need recovery time. |
| 1:15-2:45 | 90 | **S4 - Three-agent orchestration and surge replay** | Required | `participant-runbook/index.html#stage4`; `labs/05-agent-orchestration/README.md`; `test_lab05.py`; surge scenario README and smoke test; `CONTEXT.md`; `.specify/memory/constitution.md` | The surge evidence shows QueryAgent -> RouterExecutor -> ActionAgent, zero RouterExecutor LLM calls, report attachment on dedup, SEV1/statutory-clock escalation, and citation-grounded sitreps. | Keep the mock pipeline. If tables are behind, demonstrate the replay and have attendees identify dedup, severity/SLA, escalation, and citation evidence. |
| 2:45-3:00 | 15 | **Break** | Required break | N/A | Participants stop work; facilitators confirm GitHub access before S5. | Participants without Actions access can run the local verifier and watch a facilitator fork run. |
| 3:00-3:45 | 45 | **S5 - GitHub workflow and bounded extension** | Required | `participant-runbook/index.html#stage5`; `labs/09-github-in-the-lab/README.md`; `.github/workflows/smoke-test.yml`; `scripts/smoke-test.sh`; `test_starter_red_to_green.py`; `participant_extension/` | `cd labs/09-github-in-the-lab && python -m pytest -q test_starter_red_to_green.py` passes; the extension stays bounded and RouterExecutor untouched. | If Actions is unavailable, run the local verifier and offline smoke gate. |
| 3:45-4:45 | 60 | **S6 - 30-day pilot plans (20 min) and demos (40 min)** | Required | `participant-runbook/index.html#stage6`; `docs/lab-to-production.md`; completed lab evidence | Each team presents a 30-day pilot plan choosing one domain pack and operational KPI, then demos its completed All Clear evidence. | Use mock-mode evidence and a guided repository walkthrough; do not make a live Azure deployment a prerequisite. |

## Required vs optional exercises

### Required completion contract

Participants are complete when they can show evidence for all required blocks:

1. **Lab 00:** environment and mock baseline are usable; `/api/health` works locally or through a shared backend.
2. **Lab 01:** signal classification uses typed output and preserves the three-stage authority boundary.
3. **Lab 03:** spec, plan, and tasks follow `CONTEXT.md` and the constitution; verifiers are named before implementation.
4. **Lab 04:** knowledge search returns grounded, citation-ready results from the pre-populated index.
5. **Lab 05:** orchestration proves deterministic routing, dedup-as-report attachment, SEV1/statutory escalation, no PII echo, and citation-grounded action.
6. **Lab 09:** GitHub smoke/extension loop is green without requiring Azure credentials.
7. **S6:** the team presents a 30-day pilot plan with one domain pack and operational KPI, then demos its completed All Clear evidence.

### Optional / coach-led / take-home

These are valuable but must not be counted as event completion:

| Exercise | Artifact | Why optional |
| --- | --- | --- |
| Azure MCP setup | `labs/02-azure-mcp-setup/` | Depends on participant Azure/editor MCP readiness and is not in the required participant spine in `labs/README.md`. |
| Individual `azd up` deployment | `labs/06-deploy-with-azd/README.md`; `docs/event-readiness/AZURE_PREFLIGHT.md` | Lab 06 now states the event path is to use the facilitator's already-running backend; Docker, `azd up`, seeding, Cosmos persistence, monitoring, and cleanup are optional deep dives. |
| MCP server build/red-team | `labs/07-mcp-server/README.md`; `labs/07-mcp-server/exercises/mcp_red_team_probe.py` | Useful stretch after Lab 05, but it is labeled a stretch goal and needs MCP/Copilot Agent Mode setup. |
| APIM gateway | `labs/08-apim-gateway/README.md` | Requires a running backend and Azure gateway provisioning; rate limit, token budget, JWT, and telemetry checks are too risky for the core day unless explicitly promised. |
| Voice and phone | `participant-runbook/index.html#voice`; `participant-runbook/index.html#phone`; `labs/05-agent-orchestration/exercises/05x-voice-phone-extensions.md` | Marked optional in the workbook; phone is coach-led. |
| Model continuity under failover | `labs/05-agent-orchestration/exercises/05y-model-continuity.md`; `labs/05-agent-orchestration/exercises/verify_model_continuity.py` | Treat as take-home/facilitator demo because it adds outage/failover complexity beyond the 90-minute orchestration block. |

## Completion evidence standard

Facilitators should accept only working evidence tied to repository artifacts, not verbal claims:

- **Executable evidence:** a passing verifier, smoke test, workflow, or documented command from the relevant lab.
- **Artifact evidence:** generated Spec Kit files, `participant_extension/` code plus tests, or captured terminal output showing the verifier result.
- **Architecture evidence:** participant can point to the exact bounded authority: QueryAgent classifies only, RouterExecutor decides deterministically with zero LLM calls, and ActionAgent acts only through `create_incident`, `search_knowledge`, and `generate_sitrep`.
- **Safety evidence:** SEV1/statutory-clock escalation cannot be downgraded; PII is not echoed; factual responses cite source records.

Do not accept completion based on an environment variable, a manually edited success marker, a fluent unsupported sitrep, or a live deployment that bypasses the mock-mode safety/orchestration checks.

## Facilitator fallback model

1. **Shared backend first:** before doors open, publish a tested shared backend URL and verify `GET /api/health`.
2. **Mock mode always available:** keep `MOCK_MODE=true` as the baseline. Azure credentials are not required for the core S0-S6 learning outcome.
3. **Pre-populated knowledge:** use the existing Lab 04 index/data path; do not rebuild search infrastructure during the core agenda.
4. **Reference/demo path:** for blocked participants, run the facilitator demonstration and require them to interpret the evidence instead of losing the block to setup.
5. **Cloud extensions only after green core:** allow APIM, MCP, `azd up`, voice, phone, and failover only when the participant has already completed required evidence or when the block is explicitly coach-led.

## Event go/no-go checklist

### Go

- [ ] Workbook is served over HTTP(S), not `file://`, and the linked lab paths open.
- [ ] Facilitator shared backend URL is recorded; `curl --fail --max-time 10 "$BACKEND_URL/api/health"` succeeds.
- [ ] At least one real/shared backend signal submission returns an incident id, severity/SLA, queue, and grounded response.
- [ ] Core local verifiers are known green before the event: Lab 00 environment check, Lab 01, Lab 03, Lab 04 index/RAG, Lab 05 orchestration/surge, and Lab 09 starter verifier; the S6 pilot/demo handoff is ready.
- [ ] Facilitators can run the surge replay and explain incident/report/magnitude evidence from the output.
- [ ] Azure credentials, if offered, are preflighted for the event tenant; failure of Azure credentials does not block S0-S6.
- [ ] Facilitators agree that Labs 02, 06, 07, 08, voice, phone, APIM, and failover continuity are optional unless separately scheduled.
- [ ] Breaks and lunch remain protected; optional extensions do not consume required block time.

### No-go

- [ ] No tested shared backend and local setup is expected to carry all participants.
- [ ] The workbook links or required lab verifier paths are broken.
- [ ] Lab 05 surge/orchestration evidence cannot be produced in mock mode.
- [ ] Facilitators plan to require individual `azd up`, APIM provisioning, MCP setup, or voice/phone as part of the S0-S6 completion contract.
- [ ] Claims of grounded output cannot be tied to citations or source records.
- [ ] Any path weakens bounded authority, deterministic routing, mandatory escalation, PII discipline, or verifier-first delivery from the constitution.

## Final readiness call

**Conditional go.** The event is ready if facilitators run the S0-S6 path above and preserve the optional cut. It is not ready if the event is marketed or facilitated as the full lab catalog, because live Azure setup, deployment, MCP, APIM, voice/phone, and failover continuity exceed the 465-minute event budget.
