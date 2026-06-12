# Lab 07: MCP Server - Completion Specification

> **STRETCH GOAL**: This lab is optional. Participants who skip this lab can still pass the builder track with full marks on Labs 01-06.

## What "Done" Looks Like

A successfully completed Lab 07 demonstrates:

1. **MCP Server Running**: The All Clear backend runs as an MCP server using stdio transport
2. **Tools Exposed**: The three required ActionAgent tools are discoverable by MCP clients
3. **VS Code Integration**: Copilot chat can invoke tools via Copilot Agent Mode
4. **Knowledge Integration**: The `search_knowledge` tool returns citation-ready runbooks and SOPs for incident triage

## Deliverables

### Deliverable 1: MCP Server Implementation

| Criterion | Requirement |
|-----------|-------------|
| File Location | `backend/app/mcp_server.py` |
| Server Name | `allclear-incident-triage` |
| Transport | stdio (standard input/output) |
| Dependencies | `mcp` in requirements.txt |

**Acceptance Criteria**:
- [ ] Server starts without errors when run via `python backend/mcp_main.py`
- [ ] Server exports `list_tools()` handler returning the ActionAgent tools
- [ ] Server exports `call_tool()` handler that invokes tool logic
- [ ] Server preserves the QueryAgent → RouterExecutor → ActionAgent authority boundary

### Deliverable 2: Required MCP Tools

| Tool Name | Input Schema | Expected Output |
|-----------|--------------|-----------------|
| `create_incident` | `{signal_text: string, severity: "SEV1".."SEV4", queue: string, intent_category?: string}` | Incident confirmation with `AC-####` id, severity, queue, SLA, magnitude |
| `search_knowledge` | `{query: string, queue?: string, max_results?: number}` | Citation-ready runbooks/SOPs with relevance scores |
| `generate_sitrep` | `{incident_id: string, include_citations?: boolean}` | Citation-grounded sitrep for the incident |

Optional helper tools may include:

| Tool Name | Input Schema | Expected Output |
|-----------|--------------|-----------------|
| `classify_signal` | `{signal_text: string, channel?: string}` | `SignalClassification` from QueryAgent |
| `route_signal` | `{signal_text: string, classification?: object}` | `RoutingDecision` from RouterExecutor: dedup outcome, severity, SLA, escalation |

**Acceptance Criteria**:
- [ ] `create_incident` uses `AC-####` incident ids and never emits legacy ids
- [ ] `create_incident` accepts severity as `SEV1`, `SEV2`, `SEV3`, or `SEV4`
- [ ] `create_incident` uses queues such as `field-operations`, `customer-comms`, `compliance-desk`, `engineering`, or `escalations`
- [ ] `search_knowledge` returns source records suitable for citations
- [ ] `generate_sitrep` includes citations for factual claims

### Deliverable 3: VS Code MCP Configuration

| Criterion | Requirement |
|-----------|-------------|
| File Location | `.vscode/mcp.json` |
| Server Key | `allclear` |
| Environment Variables | Properly references Azure credentials and/or `MOCK_MODE` |

**Acceptance Criteria**:
- [ ] VS Code recognizes the MCP server configuration
- [ ] Copilot Agent Mode shows the All Clear MCP tools
- [ ] Environment variables are passed correctly to MCP server

### Deliverable 4: Working Integration

**Acceptance Criteria**:
- [ ] Typing `Classify this signal: Power line down across Main St` returns a `SignalClassification`
- [ ] Creating an incident for that signal returns `AC-0001`-style output with `SEV1` and `field-operations`
- [ ] Searching knowledge for field safety guidance returns citation-ready sources
- [ ] Generating a sitrep for `AC-0001` returns only cited factual claims
- [ ] Error cases (unknown queue, empty signal, invalid severity) are handled gracefully

## Assessment Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| MCP Server Starts | 2 | Server runs without errors, stdio transport works |
| Tools Discoverable | 2 | `list_tools()` returns required tools with correct schemas |
| ActionAgent Tools Work | 3 | `create_incident`, `search_knowledge`, and `generate_sitrep` return useful outputs with citations where required |
| VS Code Integration | 2 | Copilot Agent Mode can invoke the All Clear tools |
| Error Handling | 1 | Graceful handling of edge cases and errors |
| **Total** | **10** | **Stretch goal bonus points** |

## Grading Notes

### This is a Stretch Goal

- **Skipping Lab 07 does NOT affect your builder track score**
- Labs 01-06 are worth 100% of the required points
- Lab 07 is bonus credit for participants who finish early
- Attempting Lab 07 shows advanced understanding even if incomplete

### Partial Credit

| Completion Level | Points Awarded |
|------------------|----------------|
| MCP server runs with at least 1 working ActionAgent tool | 4 |
| All required tools work but VS Code integration incomplete | 7 |
| Full completion | 10 |
| Exceptional (custom resources, prompts, `classify_signal`, or `route_signal`) | 10 + recognition |

## Verification Checklist

Before submitting, verify:

```bash
# 1. MCP server starts
python backend/mcp_main.py
# Should start without errors (Ctrl+C to stop)

# 2. Dependencies installed
pip show mcp
# Should show package info

# 3. VS Code config exists
cat .vscode/mcp.json
# Should show allclear server configuration
```

In VS Code:
1. Open Copilot Chat (Ctrl+Shift+I)
2. Open the Tools picker and verify the All Clear server appears
3. Send: `Create an incident for Power line down across Main St with severity SEV1 and queue field-operations`
4. Verify response includes an `AC-####` incident id and no uncited sitrep claims

## Common Issues That Block Completion

| Issue | Resolution |
|-------|------------|
| Knowledge service not initialized | Ensure Lab 04/05 search components are importable or run in mock mode |
| Environment variables missing | Check `.env` file and `mcp.json` env section |
| VS Code doesn't see MCP server | Restart VS Code (full restart, not just reload) |
| Tool schema validation fails | Verify inputSchema matches MCP spec exactly |
| Azure connection errors | Confirm Lab 05 tests pass before attempting Lab 07, or set `MOCK_MODE=true` |
| Unsupported sitrep claims | Add citations or remove the claim |

## Success Indicators

You have successfully completed Lab 07 when:

1. You can invoke All Clear tools in VS Code Copilot Agent Mode
2. Incidents use `AC-####`, severity uses `SEV1` through `SEV4`, and queue uses the All Clear queue set
3. Source citations appear in sitreps and response claims
4. The demo works reliably for multiple signals, including a surge-style duplicate path

This demonstrates mastery of:
- MCP protocol and tool design
- Integration between multiple systems (MAF pipeline + MCP + VS Code)
- Production-ready AI assistant patterns with bounded authority
