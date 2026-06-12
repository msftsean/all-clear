# 🔌 Lab 07 - MCP Server (Stretch Goal)

| 📋 Attribute | Value |
|-------------|-------|
| ⏱️ **Duration** | 60 minutes |
| 📊 **Difficulty** | ⭐⭐⭐⭐ Expert |
| 🎯 **Prerequisites** | Lab 05 completed |
| 🏆 **Points** | 10 (bonus) |

---

> 🌟 **STRETCH GOAL**: This lab is for participants who finish Labs 01-06 early. Completing this lab is optional and will not affect your ability to pass the builder track.

---

## 📈 Progress Tracker

```
Lab Progress: [░░░░░░░░░░] 0% - Not Started

Checkpoints:
□ Step 1: Install MCP Dependencies
□ Step 2: Create the MCP Server Module
□ Step 3: Create MCP Server Entry Point
□ Step 4: Configure VS Code for MCP
□ Step 5: Implement the 3 ActionAgent Tools
□ Step 6: Test with Copilot Agent Mode
```

---

## 🌟 Overview

Transform your All Clear FastAPI backend into a Model Context Protocol (MCP) server, enabling direct integration with AI assistants like GitHub Copilot in VS Code.

This lab exposes All Clear's incident-triage capabilities as bounded tools. External clients can help triage inbound **signals**, but they do not bypass the pipeline:

```
signal → QueryAgent (classify) → RouterExecutor (dedup → severity → SLA → escalate) → ActionAgent
```

ActionAgent has exactly three required tools: `create_incident`, `search_knowledge`, and `generate_sitrep`.

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. 📚 **Understand the MCP Tool/Resource Model** - Learn how AI assistants discover and invoke tools through MCP
2. 🔌 **Expose All Clear as an MCP Server** - Convert incident-triage capabilities into MCP-compatible tools
3. 🧪 **Test with Copilot Agent Mode** - Use your MCP server directly from VS Code's Copilot chat

## 🤔 What is MCP (Model Context Protocol)?

The Model Context Protocol (MCP) is an open standard that defines how AI assistants communicate with external tools and data sources. Think of it as a universal adapter that lets any AI assistant use any tool, similar to how USB lets any device connect to any computer.

### 🔑 Key Concepts

| 📋 Concept | 📝 Description |
|-----------|-------------|
| 🔧 **Tools** | Functions that AI can invoke (e.g., `create_incident`, `search_knowledge`, `generate_sitrep`) |
| 📚 **Resources** | Data sources that AI can read (e.g., open incidents, source records, runbooks, SOPs) |
| 📝 **Prompts** | Pre-defined templates for common interactions |
| 🖥️ **Server** | Your application that exposes tools and resources via MCP |

### 🌟 Why MCP Matters

Without MCP, every AI assistant needs custom integrations for every tool. With MCP:
- ✍️ Write once, use everywhere (Copilot, Claude, ChatGPT, etc.)
- 🔒 Standardized security and authentication
- 🔍 AI can discover what tools are available and how to use them
- 🧱 All Clear preserves **bounded authority**: QueryAgent classifies, RouterExecutor decides with zero LLM calls, and ActionAgent acts only through its tools

## 📋 Prerequisites

Before starting this lab, ensure you have:

- [ ] ✅ Lab 05 completed with working QueryAgent → RouterExecutor → ActionAgent orchestration
- [ ] 🤖 VS Code with GitHub Copilot extension installed
- [ ] 🐍 Python 3.11+ environment active
- [ ] 🔧 FastAPI backend running locally or mock mode configured

---

## 📝 Step-by-Step Instructions

### 🔹 Step 1: Install MCP Dependencies (5 minutes)

Add the MCP SDK to your project:

```bash
cd backend
pip install "mcp>=1.6.0"
```

Add to `requirements.txt`:

```text
mcp>=1.6.0
```

### 🔹 Step 2: Create the MCP Server Module (15 minutes)

Create a new file `backend/app/mcp_server.py`:

```python
"""
🔌 MCP Server for All Clear incident triage.
Exposes bounded ActionAgent tools via Model Context Protocol.
"""
import asyncio
import time
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool

server = Server("allclear-incident-triage")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """📋 List available tools for the AI assistant."""
    return [
        Tool(
            name="create_incident",
            description="🚨 Open an All Clear incident from an inbound signal. Use after RouterExecutor returns OPEN_INCIDENT.",
            inputSchema={
                "type": "object",
                "properties": {
                    "signal_text": {"type": "string", "description": "Raw inbound signal, e.g. Power line down across Main St"},
                    "severity": {"type": "string", "enum": ["SEV1", "SEV2", "SEV3", "SEV4"]},
                    "queue": {"type": "string", "enum": ["field-operations", "customer-comms", "compliance-desk", "engineering", "escalations"]},
                    "intent_category": {"type": "string"},
                },
                "required": ["signal_text", "severity", "queue"],
            },
        ),
        Tool(
            name="search_knowledge",
            description="📚 Search All Clear runbooks and SOPs for citation-grounded guidance.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "queue": {"type": "string"},
                    "max_results": {"type": "integer", "default": 3},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="generate_sitrep",
            description="📝 Generate a citation-grounded situation report. Every factual claim must cite a source record.",
            inputSchema={
                "type": "object",
                "properties": {
                    "incident_id": {"type": "string", "description": "All Clear incident id, format AC-####"},
                    "include_citations": {"type": "boolean", "default": True},
                },
                "required": ["incident_id"],
            },
        ),
        Tool(
            name="classify_signal",
            description="🔎 Optional helper that asks QueryAgent to classify one signal. Authority: classify only.",
            inputSchema={
                "type": "object",
                "properties": {
                    "signal_text": {"type": "string"},
                    "channel": {"type": "string", "description": "chat, voice, phone, or report"},
                },
                "required": ["signal_text"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """⚡ Handle tool invocation from the AI assistant."""
    if name == "create_incident":
        incident_id = f"AC-{int(time.time()) % 10000:04d}"
        response_text = f"""## 🚨 Incident Created

**Incident ID**: {incident_id}
**Severity**: {arguments["severity"]}
**Queue**: {arguments["queue"]}
**Magnitude**: 1 report
**Signal**: {arguments["signal_text"]}
"""
        return [TextContent(type="text", text=response_text)]

    if name == "search_knowledge":
        response_text = f"""## 📚 Knowledge Results

Query: {arguments["query"]}

- SOP-POWER-001 — Establish a perimeter and notify field-operations.
- RUNBOOK-SURGE-004 — During a surge, preserve every signal and attach duplicates as reports.
"""
        return [TextContent(type="text", text=response_text)]

    if name == "generate_sitrep":
        incident_id = arguments["incident_id"]
        response_text = f"""## 📝 Sitrep for {incident_id}

{incident_id} is open for field-operations review [incident:{incident_id}].

## Citations
- incident:{incident_id} — Incident record
- SOP-POWER-001 — Downed power line field safety SOP
"""
        return [TextContent(type="text", text=response_text)]

    if name == "classify_signal":
        response_text = """## 🔎 SignalClassification

Intent category: FIELD_HAZARD
Target queue: field-operations
Severity indicators: downed line, public road
PII detected: false
"""
        return [TextContent(type="text", text=response_text)]

    return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """📚 List available resources for the AI assistant."""
    return [
        Resource(
            uri="allclear://incidents/open",
            name="Open Incidents",
            description="Open All Clear incidents with severity, queue, SLA clock, magnitude, and status",
            mimeType="application/json",
        )
    ]


async def main():
    """🚀 Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
```

### 🔹 Step 3: Create MCP Server Entry Point (5 minutes)

Create `backend/mcp_main.py` to run the MCP server:

```python
"""
🚀 Entry point for running All Clear as an MCP server.
"""
import asyncio
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app.mcp_server import main

if __name__ == "__main__":
    asyncio.run(main())
```

### 🔹 Step 4: Configure VS Code for MCP (10 minutes)

Create or update `.vscode/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "allclear": {
      "command": "python",
      "args": ["backend/mcp_main.py"],
      "env": {
        "AZURE_OPENAI_ENDPOINT": "${env:AZURE_OPENAI_ENDPOINT}",
        "AZURE_OPENAI_API_KEY": "${env:AZURE_OPENAI_API_KEY}",
        "AZURE_SEARCH_ENDPOINT": "${env:AZURE_SEARCH_ENDPOINT}",
        "AZURE_SEARCH_API_KEY": "${env:AZURE_SEARCH_API_KEY}",
        "MOCK_MODE": "${env:MOCK_MODE}"
      }
    }
  }
}
```

### 🔹 Step 5: Implement the 3 ActionAgent Tools (15 minutes)

Your MCP server should expose these three required tools:

| 🔧 Tool | 📝 Purpose | 📥 Input |
|------|---------|-------|
| `create_incident` | Open an incident when RouterExecutor returns `OPEN_INCIDENT` | signal_text, severity, queue, optional intent_category |
| `search_knowledge` | Retrieve runbooks/SOPs with citations | query, optional queue, max_results |
| `generate_sitrep` | Produce a citation-grounded sitrep | incident_id, include_citations |

Optional helpers are useful but must preserve authority boundaries:

| 🔧 Tool | 📝 Purpose | 📥 Input |
|------|---------|-------|
| `classify_signal` | Ask QueryAgent for `SignalClassification` | signal_text, optional channel |
| `route_signal` | Ask RouterExecutor for dedup, severity, SLA, escalation | signal_text, classification |

Keep the rules intact: QueryAgent classifies only; RouterExecutor is deterministic and uses zero LLM calls; ActionAgent acts only through the three required tools.

### 🔹 Step 6: Test with Copilot Agent Mode (10 minutes)

1. 🔄 **Restart VS Code** to load the MCP configuration

2. 💬 **Open Copilot Chat** and switch to **Agent Mode** (click the mode selector at the top of the chat panel and choose "Agent")

3. ✅ **Verify MCP Server Connection**:
   - In the chat input, click the **Tools** icon to see available MCP tools
   - You should see tools from your `allclear` MCP server listed (e.g., `create_incident`, `search_knowledge`, `generate_sitrep`)
   - MCP tools are automatically discovered in Agent Mode -- no `@` prefix is needed

4. 🧪 **Test Each Tool**:

   ```
   Classify this signal: Power line down across Main St
   ```
   Expected: `SignalClassification` with `FIELD_HAZARD`, severity indicators, and `field-operations` ✅

   ```
   Create an incident for Power line down across Main St with severity SEV1 and queue field-operations
   ```
   Expected: Incident `AC-####`, severity `SEV1`, queue `field-operations`, magnitude `1` ✅

   ```
   Search knowledge for downed power line field safety SOPs
   ```
   Expected: Runbooks/SOPs with source records ✅

   ```
   Generate a sitrep for AC-0001
   ```
   Expected: Citation-grounded sitrep ✅

5. 🐛 **Debug if Needed**:
   - Check VS Code Output panel (select "MCP" from dropdown)
   - Run MCP server manually to see logs:
     ```bash
     python backend/mcp_main.py
     ```

---

## ✅ Deliverables

When you complete this lab, verify the following:

- [ ] 🚀 MCP server starts without errors
- [ ] 🔧 `create_incident` opens incidents with `AC-####` ids
- [ ] 📚 `search_knowledge` returns citation-ready source records
- [ ] 📝 `generate_sitrep` produces a grounded sitrep
- [ ] 💬 Copilot Agent Mode invokes your MCP tools correctly
- [ ] ✅ All required tools are discoverable and functional

---

## 🔧 Troubleshooting

### ❌ MCP Server Won't Start

```
Error: ModuleNotFoundError: No module named 'mcp'
```
**Solution**: Ensure you installed the MCP SDK: `pip install "mcp>=1.6.0"`

### ❌ MCP Tools Don't Appear in Agent Mode

1. 📄 Check that `.vscode/mcp.json` exists and has valid JSON
2. 🔄 Restart VS Code completely (not just reload window)
3. 📦 Check VS Code version supports MCP (1.96+ recommended)
4. 📋 Look for errors in Output > MCP

### ❌ Tool Invocation Fails

```
Error: Connection refused
```
**Solution**:
1. ✅ Verify environment variables are set correctly
2. 🔧 Ensure your All Clear services are properly initialized
3. ☁️ Check that Azure services are accessible, or set `MOCK_MODE=true` for offline work

### ❌ Knowledge Search Errors

```
Error: Azure AI Search endpoint not configured
```
**Solution**: Ensure your `.env` file has all required variables and they're passed to the MCP server via the config. In mock mode, verify the mock twin for knowledge search is enabled.

### ❌ Sitrep Has Unsupported Claims

**Solution**: Every factual claim in a sitrep needs a citation. If you cannot cite a source record, remove the claim or escalate to a human queue.

---

## 🏗️ Architecture Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                         VS Code                                  │
│  ┌──────────────────┐    ┌─────────────────────────────────┐   │
│  │  GitHub Copilot  │───▶│      MCP Client (built-in)      │   │
│  └──────────────────┘    └─────────────────────────────────┘   │
│                                        │                         │
└────────────────────────────────────────│─────────────────────────┘
                                         │ stdio
                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    All Clear MCP Server                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     mcp_server.py                         │  │
│  │  • 📋 list_tools() → Expose ActionAgent tools            │  │
│  │  • ⚡ call_tool() → Handle invocations                   │  │
│  │  • 📚 list_resources() → Expose incident resources       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ QueryAgent → RouterExecutor → ActionAgent                │  │
│  │ classify → dedup/severity/SLA/escalate → act             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
└──────────────────────────────│───────────────────────────────────┘
                               │
                               ▼
┌──────────────────┐    ┌──────────────────┐
│  Azure OpenAI    │    │  Azure AI Search │
│  (classification │    │  (Vector Store   │
│   + embeddings)  │    │   for SOPs)      │
└──────────────────┘    └──────────────────┘
```

---

## ➡️ Next Steps

After completing this lab, you have built a full-stack AI-powered incident-triage application:

1. 🎨 **Labs 01-02**: Understanding agents and Azure MCP setup
2. 🔧 **Labs 03-04**: Spec-driven development and RAG / knowledge
3. 🔍 **Lab 05**: Orchestration with dedup, severity, SLA, and escalation
4. 🚀 **Lab 06**: Deployment to Azure
5. 🔌 **Lab 07**: MCP server for AI assistant integration

Consider these extensions:
- 🔒 Add authentication to your MCP server
- 📊 Implement MCP resources for real-time ClearBoard data
- 📝 Create custom MCP prompts for surge triage workflows
- 🔗 Explore other MCP clients (Claude Desktop, custom integrations)

---

## 📚 Resources

- 📖 [MCP Specification](https://spec.modelcontextprotocol.io/)
- 🐍 [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- 💻 [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/mcp)
- 🏗️ [Building MCP Servers](https://modelcontextprotocol.io/docs/concepts/servers)

---

## 📊 Version Matrix

| Component | Required Version | Tested Version |
|-----------|-----------------|----------------|
| 🐍 Python | 3.11+ | 3.12.10 |
| 🔌 MCP SDK | 1.6+ | 1.6.0 |
| 🤖 GitHub Copilot | Latest | 1.x |
| 🖥️ VS Code | 1.96+ | 1.99+ |

---

<div align="center">

[← Lab 06](../06-deploy-with-azd/README.md) | **Lab 07** | 🏆 Builder Track Complete!

📅 Last Updated: 2026-06-12 | 📝 Version: 2.0.0

</div>
