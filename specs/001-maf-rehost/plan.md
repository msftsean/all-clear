# Implementation Plan: 001-maf-rehost

**Companion to spec.md. The Appendix A/B content was verified against the live `agent-framework==1.8.1` package on June 11, 2026 (installed and introspected, not recalled from training data). Treat it as ground truth over anything your coding agent "remembers" about MAF previews or Semantic Kernel.**

---

## Module Layout

```
backend/app/
  agents/                      # REPLACED CONTENTS, same package path
    __init__.py
    schemas.py                 # SignalClassification, RoutingDecision, IncidentAction, PipelineResult
    query_agent.py             # build_query_agent(client) -> Agent
    router_agent.py            # class RouterExecutor(Executor)
    action_agent.py            # build_action_agent(client, services) -> Agent
    pipeline.py                # AllClearPipeline adapter + workflow builder
  services/
    interfaces.py              # ADD: IncidentStoreInterface, EmbeddingFnProtocol
    mock/maf_chat_client.py    # MockChatClient(BaseChatClient)
    mock/embeddings.py         # deterministic mock embedding fn
    azure/embeddings.py        # OpenAIEmbeddingClient wrapper (text-embedding-3-large)
  core/dependencies.py         # extend factory: mock vs live chat/embedding clients
```

Existing `services/azure/llm_service.py` is retired by this feature (its prompts move into the agents); keep the file until tests are ported, then delete.

## Step Order (maps 1:1 to tasks.md)

1. Pin dependencies (Appendix A), clean venv, freeze `requirements-lock.txt`.
2. `schemas.py`: port existing Pydantic models, rename domain (Department→Queue, Ticket→Incident where scenario-facing).
3. `MockChatClient` + mock embeddings. Build mocks FIRST so every later step is testable offline.
4. `query_agent.py` with structured output. Port prompt from existing `QUERY_AGENT_SYSTEM_PROMPT`, swap taxonomy.
5. `RouterExecutor` with dedup + rules. Port CATEGORY_TO_DEPARTMENT and ESCALATION_INTENTS tables.
6. `action_agent.py` with the three tools delegating to existing service interfaces.
7. `pipeline.py`: workflow wiring + adapter + SSE event publication.
8. Wire `core/dependencies.py` and `api/routes.py` (import + schema names only).
9. Port test suites; add the replay checkpoint test and the no-LLM-in-router assertion.
10. Live smoke against your own Azure OpenAI deployment.

## Design Decisions (pre-made so Copilot CLI doesn't improvise)

- **RouterAgent stays out of the workflow's agent abstraction on purpose.** It is a plain `Executor`. If the coding agent proposes making it a ChatAgent "for consistency," reject.
- **Tools are plain async Python functions** closed over the service interfaces, passed via `Agent(tools=[...])`. Do not hand-construct `FunctionTool` unless you need approval_mode or invocation limits; the framework wraps callables.
- **Structured output over JSON-mode prompting.** `ChatOptions(response_format=SignalClassification)` replaces the old "return only JSON" prompt scaffolding and the manual `json.loads`. Delete the old parsing/retry code rather than porting it.
- **One workflow instance per process, stateless across runs**; session state remains in the existing SessionStore, not in MAF sessions, to keep the lab's mental model simple.
- **Embedding client is injected** as `async (str) -> list[float]`, never imported inside RouterExecutor, so mock mode and the lab's threshold-tuning exercise need no Azure.

## Loop Protocol (paste into the coding agent session, applies to every task)

This project is built with verification loops, not one-shot generation. Rules for the coding agent:

1. **Verifiers come first.** A task's test, eval set, or checkpoint script is built and committed before or alongside the implementation it verifies, never after. T4 (eval set + replay fixtures) is the verifier for T5 and T7; it blocks them.
2. **Every task ends with its verify command.** Each task in tasks.md has an executable verification command. Run it, read the exit code and output, and iterate until it passes. Do not declare a task done based on the code "looking correct."
3. **The maker never grades its own work.** The agent implementing a task may not modify that task's tests, eval thresholds, fixture data, or checkpoint scripts to make them pass. If a verifier seems wrong, stop and flag it as a finding instead of editing it.
4. **Environment over memory.** Appendix B and C below override prior knowledge of Microsoft Agent Framework. If an API is not listed there, introspect the installed package (`python -c "import agent_framework, inspect; ..."`) before writing code against it. Never write MAF code from recall.
5. **Stop conditions.** A task loop ends when its verify command passes, or after 3 failed iterations on the same error, at which point the agent writes up the blocker (what was tried, exact error, hypothesis) instead of trying a 4th variation.
6. **No collateral edits.** Fix only what the current task scopes. Unrelated improvements get logged as proposals in `.squad/decisions.md`, not implemented.

---

## Appendix A: Verified Version Pins (June 11, 2026)

```
# requirements.txt additions (GA line, verified installed together)
agent-framework==1.8.1          # meta package; pulls core 1.8.1
agent-framework-openai==1.8.1   # OpenAIChatClient / OpenAIEmbeddingClient (Azure-capable)
openai==2.41.1
azure-ai-projects==2.2.0        # only if FoundryChatClient path used
```

**Do NOT add** (beta/rc as of June 11, 2026, verified):
- `agent-framework-orchestrations` (1.0.0rc3)
- `agent-framework-azure-ai-search` (1.0.0b260521), `agent-framework-azure-cosmos` (1.0.0b260521): keep the existing azure-search-documents / azure-cosmos service code instead
- `agent-framework-a2a` (1.0.0b260604): Exercise 8 stretch only; flag as beta in the lab

## Appendix B: Verified API Surface (introspected from 1.8.1)

**There is no `AzureOpenAIChatClient`.** Azure OpenAI is reached through `OpenAIChatClient` with `azure_endpoint`, or through `agent_framework.foundry.FoundryChatClient`. Coding agents will hallucinate `AzureOpenAIChatClient` or Semantic Kernel class names; correct them with this appendix.

```python
# --- Clients (agent_framework.openai) ---
OpenAIChatClient(model, api_key, credential, org_id, base_url,
                 azure_endpoint, api_version, ...)
OpenAIEmbeddingClient(model, api_key, credential, ..., base_url,
                      azure_endpoint, api_version)
# Azure live mode:
client = OpenAIChatClient(model=settings.azure_openai_deployment,
                          azure_endpoint=settings.azure_openai_endpoint,
                          api_version=settings.azure_openai_api_version,
                          credential=DefaultAzureCredential())

# --- Agent (agent_framework) ---
Agent(client, instructions, id, name, description, tools,
      default_options, context_providers, middleware, ...)
resp = await agent.run(messages, options=ChatOptions(response_format=SignalClassification))
classification: SignalClassification = resp.value   # typed structured output
# ChatOptions accepts response_format: type[BaseModel] | Mapping | None

# --- Workflow (agent_framework) ---
class RouterExecutor(Executor):
    def __init__(self, id: str = "router", **deps): ...
    @handler                       # decorator: input/output types inferred from hints
    async def route(self, msg: SignalClassification,
                    ctx: WorkflowContext) -> None:
        ...
        await ctx.send_message(decision)      # forward to next node
        # or: await ctx.yield_output(result)  # terminal output

wf = (WorkflowBuilder()
      .add_chain([query_agent, RouterExecutor(...), action_agent])  # agents accepted directly
      .build())
result = await wf.run(initial_message)        # WorkflowRunResult; stream=True for events
# Builder also has: add_edge, add_fan_out_edges, add_fan_in_edges,
#                   add_switch_case_edge_group (use for ATTACH vs OPEN branch if desired)

# AgentExecutor(agent, session=None, id=None, context_mode=..., context_filter=...)
# available when you need explicit node ids for edges/conditions.

# --- Mock client contract (agent_framework) ---
class MockChatClient(BaseChatClient):
    # sole abstract method, exact signature:
    async def _inner_get_response(self, *, messages: Sequence[Message],
                                  stream: bool, options: Mapping[str, Any],
                                  **kwargs) -> ChatResponse: ...
    # When options carry a response_format, return JSON conforming to the model
    # so AgentResponse.value parses into the Pydantic type.

# --- WorkflowContext useful surface ---
# send_message, yield_output, add_event, get_state/set_state,
# request_info (HITL), is_streaming
```

## Appendix C: Known Hallucination Traps for the Coding Agents

| Your agent will probably write | Correct for 1.8.1 |
|---|---|
| `from agent_framework.azure import AzureOpenAIChatClient` | `from agent_framework.openai import OpenAIChatClient` (+ `azure_endpoint`) |
| `ChatAgent(...)` (preview-era name) | `Agent(...)` |
| `response.content` / manual `json.loads` for structured output | `response.value` with `ChatOptions(response_format=Model)` |
| `agent_framework.orchestrations.Sequential(...)` | `WorkflowBuilder().add_chain([...]).build()` (orchestrations is rc, banned) |
| Semantic Kernel `@kernel_function` tool decorators | plain async functions in `Agent(tools=[...])` |
| `workflow.invoke(...)` / `run_stream(...)` | `await workflow.run(msg)` or `workflow.run(msg, stream=True)` |
