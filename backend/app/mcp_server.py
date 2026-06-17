import asyncio
import time
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool

server = Server("allclear-incident-triage")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="create_incident",
            description="Open an All Clear incident from an inbound signal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "signal_text": {"type": "string"},
                    "severity": {"type": "string", "enum": ["SEV1", "SEV2", "SEV3", "SEV4"]},
                    "queue": {"type": "string", "enum": ["field-operations", "customer-comms", "compliance-desk", "engineering", "escalations"]},
                    "intent_category": {"type": "string"},
                },
                "required": ["signal_text", "severity", "queue"],
            },
        ),
        Tool(
            name="search_knowledge",
            description="Search All Clear runbooks and SOPs for guidance.",
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
            description="Generate a citation-grounded situation report.",
            inputSchema={
                "type": "object",
                "properties": {
                    "incident_id": {"type": "string"},
                    "include_citations": {"type": "boolean", "default": True},
                },
                "required": ["incident_id"],
            },
        ),
        Tool(
            name="classify_signal",
            description="Classify one signal. Authority: classify only.",
            inputSchema={
                "type": "object",
                "properties": {
                    "signal_text": {"type": "string"},
                    "channel": {"type": "string"},
                },
                "required": ["signal_text"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "create_incident":
        incident_id = f"AC-{int(time.time()) % 10000:04d}"
        return [TextContent(type="text", text=f"""## Incident Created

Incident ID: {incident_id}
Severity: {arguments["severity"]}
Queue: {arguments["queue"]}
Magnitude: 1 report
Signal: {arguments["signal_text"]}
""")]

    if name == "search_knowledge":
        return [TextContent(type="text", text=f"""## Knowledge Results

Query: {arguments["query"]}

- SOP-POWER-001 — Establish a perimeter and notify field-operations.
- RUNBOOK-SURGE-004 — Preserve every signal and attach duplicates as reports.
""")]

    if name == "generate_sitrep":
        incident_id = arguments["incident_id"]
        return [TextContent(type="text", text=f"""## Sitrep for {incident_id}

{incident_id} is open for field-operations review [incident:{incident_id}].

## Citations
- incident:{incident_id} — Incident record
- SOP-POWER-001 — Downed power line field safety SOP
""")]

    if name == "classify_signal":
        return [TextContent(type="text", text="""## SignalClassification

Intent category: FIELD_HAZARD
Target queue: field-operations
Severity indicators: downed line, public road
PII detected: false
""")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    return [
        Resource(
            uri="allclear://incidents/open",
            name="Open Incidents",
            description="Open All Clear incidents",
            mimeType="application/json",
        )
    ]


async def main():
    from mcp.server.models import InitializationOptions
    from mcp.server.lowlevel import NotificationOptions

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="allclear-incident-triage",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
