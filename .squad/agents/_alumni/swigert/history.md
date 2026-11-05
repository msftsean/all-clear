# History

## Project Context

All Clear is a Python/FastAPI and TypeScript accelerator requested by
MARYLAND ADMIN 01.

## Learnings

- Added executable participant proof for model continuity: offline failover
  probes now preserve typed classification, life-safety escalation, and
  non-failover handling for rate limits/content filters.
- Added Lab 07 MCP red-team probes for PII leakage, prompt injection, and
  severity downgrade resistance. The verifier uses runtime probes with MCP SDK
  v1 and deterministic source checks when MCP SDK v2 is installed.
- Replaced Lab 09's environment-variable completion shortcut with a real
  bounded extension artifact and a subprocess test gate; documented the
  offline `smoke-test.yml` workflow and `scripts/smoke-test.sh` behavior.

- The participant workbook defines an exact 390-minute six-stage path: S0 scaffold/eval (45m), S1 agent/orchestration (90m), S2 retrieval/citations (60m), S3 MCP plus red-team (75m), S4 APIM gateway (60m), and S5 Azure deployment/eval-gated CI (60m); see `participant-runbook/index.html` sections `#stage0` through `#stage5`.
- The builder-lab index recommends a shorter spine, `00 -> 01 -> 03 -> 04 -> 05`, and explicitly marks Lab 02 plus Labs 06-09 as optional extensions; it also directs participants to mock mode when Azure credentials or deployment time are unavailable (`labs/README.md`).
- Strong completion evidence exists as executable artifacts: `labs/00-setup/verify_environment.py`, `labs/01-understanding-agents/test_lab01.py`, `labs/03-spec-driven-development/test_lab03.py`, `labs/04-build-rag-pipeline/verify_index.py` plus `test_rag.py`, `labs/05-agent-orchestration/test_lab05.py` plus `test_surge.py`, and the repo-wide mock pytest command documented in `labs/README.md`.
- RAG is feasible in-event because the `allclear-kb` index is pre-populated; Lab 04 says to skip index/embedding setup and start at search-tool implementation, with mock/local verification available (`labs/04-build-rag-pipeline/README.md`, `verify_index.py`).
- Orchestration and safety have concrete proof points: RouterExecutor zero-LLM behavior, SEV1/statutory-clock escalation, dedup attachment/magnitude, citation-bearing sitreps, and no-PII echo (`labs/05-agent-orchestration/README.md`).
- MCP is explicitly a 60-minute stretch goal in the lab track and the workbook's 75-minute S3 adds a red-team requirement; the safe fallback is to demonstrate the bounded three-tool contract from the existing mock backend rather than require live Copilot Agent Mode (`labs/07-mcp-server/README.md`, `participant-runbook/index.html`).
- Deployment/APIM are the main event time sinks: `azd up` needs Docker, Azure auth, provisioning, image push, seeding, persistence verification, and logs (`labs/06-deploy-with-azd/README.md`); APIM needs provisioning/import/policies/JWT/App Insights (`labs/08-apim-gateway/README.md`). Their documented fallbacks are shared backend/mock mode and deferral to take-home.
- GitHub completion is independently provable through `smoke-test.yml` plus `labs/09-github-in-the-lab/test_starter_red_to_green.py`; it is presented as an extension/bonus rather than a prerequisite in the builder track (`labs/09-github-in-the-lab/README.md`, `participant-runbook/index.html`).
