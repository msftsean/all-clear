# All Clear Event Readiness Delivery Plan

**Audience:** facilitators and event owners  
**Decision:** run the mock-runnable participant spine in 390 minutes. Do not attempt the full lab catalog in one event day.

## Scope cut

The repository contains more workshop material than can honestly fit a 390-minute day. The event-ready path is the six-stage participant spine already represented in `participant-runbook/index.html`: setup, classification, spec discipline, grounded retrieval, orchestration/surge, and GitHub verification. This path is **315 minutes of working time plus 75 minutes of breaks/lunch**.

The required path intentionally cuts live cloud buildout from the completion contract. `labs/README.md` names `00 -> 01 -> 03 -> 04 -> 05` as the participant spine and marks Lab 02 and Labs 06-09 as optional extensions for a longer session. The current participant workbook keeps Lab 09 as the final required operating loop, so this plan treats Lab 09 as required but keeps Lab 02, Lab 06, Lab 07, Lab 08, voice, phone, and failover continuity as optional/facilitator-led.

## 390-minute run of show

| Clock | Minutes | Block | Status | Repository artifacts | Completion evidence | Facilitator fallback |
| --- | ---: | --- | --- | --- | --- | --- |
| 11:00-11:30 | 30 | **S0 - Setup and mock baseline** | Required | `participant-runbook/index.html#stage0`; `labs/00-setup/README.md`; `labs/00-setup/verify_environment.py`; `CONTEXT.md`; `.specify/memory/constitution.md` | Participant can open the repo, confirm Python 3.11+ and Node 18+, run the Lab 00 environment check, and reach `/api/health` on the local or shared backend. | Use Codespaces if local setup stalls. Keep `MOCK_MODE=true`. If a participant cannot start services, pair them to the facilitator shared backend and keep them in the workbook. |
| 11:30-12:15 | 45 | **S1 - Classify signals and bounded authority** | Required | `participant-runbook/index.html#stage1`; `labs/01-understanding-agents/README.md`; `labs/01-understanding-agents/exercises/01a-intent-classification.md`; `labs/01-understanding-agents/exercises/01b-prompt-engineering.md`; `labs/01-understanding-agents/test_lab01.py`; `CONTEXT.md` | Participant can explain QueryAgent, RouterExecutor, and ActionAgent boundaries; classification produces typed `SignalClassification`; RouterExecutor remains deterministic and prompt-free. Evidence command: `cd labs/01-understanding-agents && python test_lab01.py` where available. | If implementation time slips, coach from the bounded-authority matrix and use the provided test fixture or reference path for discussion, but require the participant to identify classify-only vs decide-only vs act-only responsibilities. |
| 12:15-12:30 | 15 | **Break** | Required break | N/A | Participants stop work; facilitators triage setup blockers. | Move unresolved environment blockers to shared backend path before S2 starts. |
| 12:30-1:15 | 45 | **S2 - Spec-driven capability** | Required | `participant-runbook/index.html#stage2`; `labs/03-spec-driven-development/README.md`; `labs/03-spec-driven-development/exercises/03a-write-spec.md`; `labs/03-spec-driven-development/exercises/03b-generate-from-spec.md`; `.specify/memory/constitution.md`; `CONTEXT.md`; `labs/03-spec-driven-development/test_lab03.py` | Participant produces or reviews a Spec Kit feature spec/plan/tasks that use All Clear language, preserves bounded authority, forces statutory-clock SEV1 escalation, and names verifiers before implementation. Evidence command: `cd labs/03-spec-driven-development && python test_lab03.py` where available. | If Copilot/Spec Kit commands are unavailable, use the README acceptance bullets as a manual review rubric and have participants mark violations against the constitution. |
| 1:15-2:15 | 60 | **S3 - Grounded retrieval and citations** | Required | `participant-runbook/index.html#stage3`; `labs/04-build-rag-pipeline/README.md`; `labs/04-build-rag-pipeline/verify_index.py`; `labs/04-build-rag-pipeline/test_rag.py`; `CONTEXT.md` | Participant verifies the pre-populated knowledge base and demonstrates that a response claim traces to a source record. Evidence commands: `cd labs/04-build-rag-pipeline && python verify_index.py` and `python test_rag.py`. | Use the pre-populated/mock knowledge index. Do not spend event time creating embeddings or re-provisioning search. If Azure credentials fail, run local verification and coach the citation contract. |
| 2:15-3:00 | 45 | **Lunch / reset** | Required lunch | N/A | Facilitators confirm every table has S0-S3 evidence or a fallback assignment before orchestration starts. | Triage participants into three groups: green path, shared-backend path, or observe-and-run-tests path. |
| 3:00-4:30 | 90 | **S4 - Three-agent orchestration and surge replay** | Required | `participant-runbook/index.html#stage4`; `labs/05-agent-orchestration/README.md`; `labs/05-agent-orchestration/test_lab05.py`; `labs/05-agent-orchestration/scenarios/surge/README.md`; `labs/05-agent-orchestration/scenarios/surge/smoke_test.py`; `CONTEXT.md`; `.specify/memory/constitution.md` | Participant shows QueryAgent -> RouterExecutor -> ActionAgent end-to-end; RouterExecutor has zero LLM calls; duplicate surge signals attach as reports to one incident; SEV1/statutory-clock cases escalate; sitreps are citation-grounded. Evidence commands: `cd labs/05-agent-orchestration && python test_lab05.py`, `python test_surge.py` if present, or `cd backend && PYTHONPATH=. python ../labs/05-agent-orchestration/scenarios/surge/smoke_test.py`. | If live services fail, keep the mock pipeline. If participants are behind, run the surge replay as a facilitator demo and require participants to identify dedup, severity/SLA, escalation, and citation evidence from the output. |
| 4:30-4:45 | 15 | **Break** | Required break | N/A | Facilitators confirm GitHub access before S5. | Participants without GitHub Actions access can run the local verifier and watch a facilitator fork run. |
| 4:45-5:30 | 45 | **S5 - GitHub workflow and bounded extension** | Required | `participant-runbook/index.html#stage5`; `labs/09-github-in-the-lab/README.md`; `.github/workflows/smoke-test.yml`; `scripts/smoke-test.sh`; `labs/09-github-in-the-lab/test_starter_red_to_green.py`; `labs/09-github-in-the-lab/participant_extension/` | Participant forks or uses an assigned repo, runs `smoke-test.yml` or the local equivalent, and completes one bounded extension under `participant_extension/` with a green starter verifier. Evidence command: `cd labs/09-github-in-the-lab && python -m pytest -q test_starter_red_to_green.py`; repository evidence is a green workflow run or local smoke result. | If GitHub Actions is unavailable, run the local verifier and show the offline smoke gate described in `labs/09-github-in-the-lab/README.md`. Keep RouterExecutor untouched. |

## Required vs optional exercises

### Required completion contract

Participants are complete when they can show evidence for all required blocks:

1. **Lab 00:** environment and mock baseline are usable; `/api/health` works locally or through a shared backend.
2. **Lab 01:** signal classification uses typed output and preserves the three-stage authority boundary.
3. **Lab 03:** spec, plan, and tasks follow `CONTEXT.md` and the constitution; verifiers are named before implementation.
4. **Lab 04:** knowledge search returns grounded, citation-ready results from the pre-populated index.
5. **Lab 05:** orchestration proves deterministic routing, dedup-as-report attachment, SEV1/statutory escalation, no PII echo, and citation-grounded action.
6. **Lab 09:** GitHub smoke/extension loop is green without requiring Azure credentials.

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
2. **Mock mode always available:** keep `MOCK_MODE=true` as the baseline. Azure credentials are not required for the core S0-S5 learning outcome.
3. **Pre-populated knowledge:** use the existing Lab 04 index/data path; do not rebuild search infrastructure during the core agenda.
4. **Reference/demo path:** for blocked participants, run the facilitator demonstration and require them to interpret the evidence instead of losing the block to setup.
5. **Cloud extensions only after green core:** allow APIM, MCP, `azd up`, voice, phone, and failover only when the participant has already completed required evidence or when the block is explicitly coach-led.

## Event go/no-go checklist

### Go

- [ ] Workbook is served over HTTP(S), not `file://`, and the linked lab paths open.
- [ ] Facilitator shared backend URL is recorded; `curl --fail --max-time 10 "$BACKEND_URL/api/health"` succeeds.
- [ ] At least one real/shared backend signal submission returns an incident id, severity/SLA, queue, and grounded response.
- [ ] Core local verifiers are known green before the event: Lab 00 environment check, Lab 01, Lab 03, Lab 04 index/RAG, Lab 05 orchestration/surge, and Lab 09 starter verifier.
- [ ] Facilitators can run the surge replay and explain incident/report/magnitude evidence from the output.
- [ ] Azure credentials, if offered, are preflighted for the event tenant; failure of Azure credentials does not block S0-S5.
- [ ] Facilitators agree that Labs 02, 06, 07, 08, voice, phone, APIM, and failover continuity are optional unless separately scheduled.
- [ ] Breaks and lunch remain protected; optional extensions do not consume required block time.

### No-go

- [ ] No tested shared backend and local setup is expected to carry all participants.
- [ ] The workbook links or required lab verifier paths are broken.
- [ ] Lab 05 surge/orchestration evidence cannot be produced in mock mode.
- [ ] Facilitators plan to require individual `azd up`, APIM provisioning, MCP setup, or voice/phone as part of the 390-minute completion contract.
- [ ] Claims of grounded output cannot be tied to citations or source records.
- [ ] Any path weakens bounded authority, deterministic routing, mandatory escalation, PII discipline, or verifier-first delivery from the constitution.

## Final readiness call

**Conditional go.** The event is ready if facilitators run the S0-S5 spine above and preserve the optional cut. It is not ready if the event is marketed or facilitated as the full lab catalog, because the repository artifacts show that live Azure setup, deployment, MCP, APIM, voice/phone, and failover continuity exceed the honest 390-minute completion budget.
