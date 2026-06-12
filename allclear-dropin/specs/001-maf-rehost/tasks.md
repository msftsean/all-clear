# Tasks: 001-maf-rehost

Squad-mapped, ordered for Copilot CLI execution. Tasks marked ∥ can run in parallel after their dependencies. Each task lists its Squad owner from the All Clear Avengers roster (T'Challa lead, Shuri backend, Stark frontend, Rogers security, Barton tester, FRIDAY logger).

| # | Task | Owner | Depends on | Done when |
|---|---|---|---|---|
| T1 | Create clean venv, add Appendix A pins to `requirements.txt`, install, commit `requirements-lock.txt` (`pip freeze`) | Shuri | none | Clean-venv install succeeds; lock file committed |
| T2 | `agents/schemas.py`: port Pydantic models, rename to All Clear domain (SignalClassification, RoutingDecision incl. ATTACH_TO_INCIDENT/OPEN_INCIDENT, IncidentAction, PipelineResult) | Shuri | T1 | mypy clean; old schema fields all accounted for in a mapping comment |
| T3 ∥ | `services/mock/maf_chat_client.py`: MockChatClient per plan Appendix B contract, honoring response_format with conformant JSON | Shuri | T2 | Unit test: agent.run against mock returns typed `.value` |
| T4 ∥ | **Build the verifiers first:** (a) `services/mock/embeddings.py` deterministic vectors, (b) `mock_data/surge_replay_25.json` with scripted duplicate clusters, (c) `mock_data/eval_signals_60.jsonl`, the 60-signal labeled classification eval set, (d) checkpoint scripts that grade T5/T7 against them | Barton | T2 | Verify commands for T5 and T7 exist, run, and correctly FAIL against a stub implementation |
| T5 | `agents/query_agent.py`: build_query_agent(client); port QUERY_AGENT_SYSTEM_PROMPT, swap taxonomy per CONTEXT.md; structured output via ChatOptions | Shuri | T3 | Mock-mode eval: ≥90% on the 60-signal labeled set |
| T6 | `services/interfaces.py`: add IncidentStoreInterface + EmbeddingFn protocol; `services/mock/incident_store.py` | Shuri | T2 | Interface review by Rogers (authority bounds documented in docstrings) |
| T7 | `agents/router_agent.py`: RouterExecutor(Executor) with @handler; dedup → severity/SLA → escalation, all tables ported, all thresholds in config | Shuri | T4, T6 | No chat-client import (T12 lint test passes); replay produces ≤6 incidents / ≥19 attachments |
| T8 | `agents/action_agent.py`: build_action_agent with create_incident / search_knowledge / generate_sitrep tools delegating to interfaces; port citation prompt | Shuri | T6 | Mock-mode: tool invocations land in mock incident store with audit entries |
| T9 | `agents/pipeline.py`: WorkflowBuilder chain, AllClearPipeline.process_signal adapter, SSE event publication onto existing transcript bus | Shuri | T5, T7, T8 | End-to-end mock test: text in → PipelineResult out → events on bus |
| T10 | Wire `core/dependencies.py` (mock vs live client factories) and `api/routes.py` import/schema swap; repoint voice tool execution at the adapter | Shuri | T9 | Existing route tests pass; voice tool path unit test green |
| T11 ∥ | Security review: tool authority bounds, PII handling in structured output, dedup data exposure (signal text embedded, where do vectors live, retention) | Rogers | T8, T9 | Findings filed as issues; blockers resolved before T13 |
| T12 ∥ | Port pytest suites; add (a) replay checkpoint test, (b) assertion that router module imports no chat client, (c) clean-venv CI job | Barton | T9 | `USE_MOCK_MODE=true pytest` fully green in CI |
| T13 | Live smoke against your Azure OpenAI gpt-5.1 deployment (then deliberately re-run on gpt-4.1 to prove the fallback chain) | T'Challa + Shuri | T10, T11, T12 | One signal e2e in live mode on both models; results logged in decisions.md |
| T14 | FRIDAY: session log + update `.squad/decisions.md` with threshold choice, model pins, and the no-LLM-router rationale | FRIDAY | T13 | Decision log entry merged |

## Verification commands (the loop's feedback signals, one per task)

Every task closes by running its command until exit code 0. The builder agent may not edit these tests or fixtures (Loop Protocol rule 3 in plan.md; Barton owns verifiers).

```bash
# T1
python -m venv /tmp/clean && /tmp/clean/bin/pip install -r requirements.txt
# T2
mypy backend/app/agents/schemas.py && pytest tests/test_schemas.py
# T3
USE_MOCK_MODE=true pytest tests/test_mock_chat_client.py        # incl. response_format conformance
# T4 (verifiers must FAIL against stubs before T5/T7 exist)
pytest tests/test_mock_embeddings.py && python scripts/check_eval.py --expect-fail-on-stub
# T5
USE_MOCK_MODE=true python scripts/check_eval.py --min-accuracy 0.90
# T6
pytest tests/test_incident_store_interface.py
# T7
USE_MOCK_MODE=true pytest tests/test_replay_checkpoint.py       # <=6 incidents, >=19 attachments
grep -rL "chat" backend/app/agents/router_agent.py && pytest tests/test_router_no_llm.py
# T8
USE_MOCK_MODE=true pytest tests/test_action_tools.py            # tool calls land in mock store + audit
# T9
USE_MOCK_MODE=true pytest tests/test_pipeline_e2e.py            # text in -> PipelineResult + bus events
# T10
USE_MOCK_MODE=true pytest tests/test_routes.py tests/test_voice_tool_path.py
# T12
USE_MOCK_MODE=true pytest                                        # full suite, also wired as CI job
# T13 (live, run by Sean)
python scripts/live_smoke.py --deployment gpt-5.1 && python scripts/live_smoke.py --deployment gpt-4.1
```

## Suggested Copilot CLI kickoff

From repo root, after dropping `spec.md`, `plan.md`, `tasks.md` into `specs/001-maf-rehost/`:

1. Paste the **Loop Protocol** section of plan.md into the session as a standing instruction, along with: "Appendix B and C of plan.md override your prior knowledge of Microsoft Agent Framework. If a class or method you want to use is not in Appendix B, verify it against the installed package before writing it."
2. Run `speckit.clarify` against spec.md to burn down the three open questions (answers go back into the spec).
3. Run `speckit.analyze` to validate spec/plan/tasks consistency.
4. Hand T1-T2 to Copilot CLI directly (mechanical), then T4 to build the verifiers, then `speckit.taskstoissues` and let Squad loop on T3, T5-T12, each task iterating against its verification command until green.
5. Reserve T13 for yourself; that is the CloudForce-relevant validation and you want eyes on the quota behavior.
