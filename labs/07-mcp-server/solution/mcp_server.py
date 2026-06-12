"""
MCP Server for All Clear incident triage - Lab 07.

This server exposes bounded All Clear tools for classifying inbound signals,
routing to queues, creating incidents, searching knowledge, and generating
citation-grounded sitreps.

How to Run:
    python mcp_server.py

    Or with MCP Inspector for testing:
    npx @modelcontextprotocol/inspector python mcp_server.py
"""

import json
import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: MCP SDK not installed. Run: pip install mcp")
    sys.exit(1)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

LABS_DIR = Path(__file__).parent.parent.parent
SHARED_DIR = LABS_DIR.parent / "shared"
LAB04_SOLUTION = LABS_DIR / "04-build-rag-pipeline" / "solution"
LAB05_SOLUTION = LABS_DIR / "05-agent-orchestration" / "solution"

sys.path.insert(0, str(LAB04_SOLUTION))
sys.path.insert(0, str(LAB05_SOLUTION))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

_search_tool = None
_agent_pipeline = None

SLA_MINUTES = {"SEV1": 15, "SEV2": 60, "SEV3": 240, "SEV4": 1440}
VALID_QUEUES = {
    "field-operations",
    "customer-comms",
    "compliance-desk",
    "engineering",
    "escalations",
}


def get_search_tool():
    """Lazily initialize and return the SearchTool from Lab 04."""
    global _search_tool
    if _search_tool is not None:
        return _search_tool
    try:
        from search_tool import SearchTool

        _search_tool = SearchTool()
        logger.info("SearchTool initialized successfully")
        return _search_tool
    except ImportError as e:
        logger.warning("Lab 04 SearchTool not available: %s", e)
        return None
    except Exception as e:
        logger.error("Failed to initialize SearchTool: %s", e)
        return None


def get_agent_pipeline():
    """Lazily initialize and return the AgentPipeline from Lab 05."""
    global _agent_pipeline
    if _agent_pipeline is not None:
        return _agent_pipeline
    try:
        from pipeline import AgentPipeline

        _agent_pipeline = AgentPipeline()
        logger.info("AgentPipeline initialized successfully")
        return _agent_pipeline
    except ImportError as e:
        logger.warning("Lab 05 AgentPipeline not available: %s", e)
        return None
    except Exception as e:
        logger.error("Failed to initialize AgentPipeline: %s", e)
        return None


mcp = FastMCP(
    name="allclear-incident-triage",
    instructions=(
        "MCP server providing All Clear incident-triage tools. "
        "Use these tools to classify signals, route to queues, create incidents, "
        "search knowledge, and generate sitreps."
    ),
)


@mcp.tool()
async def classify_signal(signal_text: str, session_id: Optional[str] = None) -> str:
    """
    Process an inbound signal through the QueryAgent classification path.

    Authority: classify only. This helper cannot route, create records, search
    knowledge, or bypass escalation.
    """
    logger.info("Classifying signal: %s...", signal_text[:50])
    pipeline = get_agent_pipeline()

    if pipeline is None:
        return json.dumps(
            {
                "intent": "field hazard report",
                "intent_category": "FIELD_HAZARD",
                "target_queue": "field-operations",
                "confidence": 0.86,
                "entities": {
                    "location": "Main St" if "Main St" in signal_text else None,
                    "severity_indicators": (
                        ["downed line"] if "line" in signal_text.lower() else []
                    ),
                },
                "requires_escalation": "power line" in signal_text.lower(),
                "pii_detected": False,
                "fallback": True,
            },
            indent=2,
        )

    try:
        result, new_session_id = await pipeline.process(
            user_message=signal_text,
            session_id=session_id,
        )
        response = {
            "response": result.content,
            "session_id": new_session_id,
            "confidence": result.confidence,
            "requires_followup": result.requires_followup,
            "suggested_actions": result.suggested_actions,
        }
        if result.sources:
            response["sources"] = [
                {
                    "title": source.get("title", "Unknown"),
                    "preview": source.get("content_preview", "")[:100] + "...",
                }
                for source in result.sources
            ]
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.exception("Error classifying signal: %s", e)
        return json.dumps(
            {
                "error": str(e),
                "message": (
                    "An error occurred while classifying the signal. "
                    "Escalate if severity or PII cannot be determined."
                ),
            },
            indent=2,
        )


@mcp.tool()
async def route_signal(signal_text: str, intent_category: str = "FIELD_HAZARD") -> dict:
    """
    Produce a RouterExecutor-style deterministic routing decision.

    RouterExecutor performs dedup, severity/SLA mapping, and escalation rules
    with zero LLM calls.
    """
    logger.info("Routing signal for intent category: %s", intent_category)
    text = signal_text.lower()
    severity = (
        "SEV1"
        if any(term in text for term in ["power line", "injured", "fire", "statutory"])
        else "SEV3"
    )
    queue = (
        "field-operations"
        if intent_category in {"FIELD_HAZARD", "PUBLIC_SAFETY"}
        else "customer-comms"
    )
    return {
        "outcome": "OPEN_INCIDENT",
        "target_queue": queue,
        "severity": severity,
        "sla_minutes": SLA_MINUTES[severity],
        "escalate": severity == "SEV1",
        "escalation_reason": "sev1_incident" if severity == "SEV1" else None,
        "matched_incident_id": None,
        "dedup_similarity": 0.0,
        "magnitude": 1,
        "routing_rules_applied": ["severity_keyword_mapping", "queue_by_intent_category"],
    }


@mcp.tool()
async def create_incident(
    signal_text: str,
    severity: str = "SEV3",
    queue: Optional[str] = None,
    intent_category: str = "FIELD_HAZARD",
) -> dict:
    """
    Create a new incident in the All Clear system.

    Incidents have AC-#### ids, severity SEV1 through SEV4, a destination queue,
    an SLA clock, magnitude, and status.
    """
    logger.info("Creating incident: %s...", signal_text[:50])
    severity = severity.upper()
    if severity not in SLA_MINUTES:
        severity = "SEV3"
    if queue not in VALID_QUEUES:
        queue = "field-operations" if severity == "SEV1" else "customer-comms"

    incident_id = f"AC-{uuid.uuid4().int % 10000:04d}"
    sla_minutes = SLA_MINUTES[severity]
    status = "escalated" if severity == "SEV1" else "open"
    created_at = datetime.utcnow().isoformat() + "Z"

    logger.info("Created incident %s - %s - %s", incident_id, severity, queue)
    return {
        "success": True,
        "incident_id": incident_id,
        "status": status,
        "created_at": created_at,
        "sla_minutes": sla_minutes,
        "severity": severity,
        "queue": queue,
        "intent_category": intent_category,
        "magnitude": 1,
        "escalated": severity == "SEV1",
        "message": (
            f"Incident {incident_id} opened as {severity} in {queue}. "
            f"SLA clock is {sla_minutes} minutes."
        ),
        "next_steps": [
            f"Track incident ID: {incident_id}",
            "Attach duplicate signals as reports to increment magnitude",
            "Generate a sitrep with citations before sharing status externally",
        ],
    }


@mcp.tool()
async def search_knowledge(
    query: str,
    queue: Optional[str] = None,
    max_results: int = 5,
) -> list[dict]:
    """
    Search the All Clear knowledge base directly.

    Performs semantic search across incident runbooks, SOPs, and response
    guidance using Azure AI Search.
    """
    logger.info("Searching knowledge: %s...", query[:50])
    max_results = max(1, min(20, max_results))
    search_tool = get_search_tool()

    if search_tool is None:
        return [
            {
                "source_id": "SOP-POWER-001",
                "title": "Downed Power Line Field Safety SOP",
                "content": (
                    "Establish perimeter, notify field unit, and keep reports "
                    "attached to the incident record."
                ),
                "source": "All Clear Knowledge Base",
                "relevance_score": 0.92,
                "queue": queue or "field-operations",
                "fallback": True,
            }
        ]

    try:
        results = search_tool.search(query=query, top_k=max_results, use_hybrid=True)
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "title": result.metadata.get("title", "Unknown"),
                    "content": (
                        result.content[:500] + "..."
                        if len(result.content) > 500
                        else result.content
                    ),
                    "source": result.metadata.get("source", "Knowledge Base"),
                    "relevance_score": result.score,
                    "queue": result.metadata.get("queue", queue or "customer-comms"),
                }
            )
        if not formatted_results:
            return [
                {
                    "message": "No matching source records found.",
                    "suggestions": [
                        "Use more general incident-triage terms",
                        "Check spelling of specific systems or locations",
                        "Try a queue-specific search such as field-operations SOP",
                    ],
                }
            ]
        return formatted_results
    except Exception as e:
        logger.exception("Search error: %s", e)
        return [{"error": str(e), "message": "An error occurred while searching.", "query": query}]


@mcp.tool()
async def generate_sitrep(incident_id: str, include_citations: bool = True) -> dict:
    """
    Generate a citation-grounded situation report for an incident.

    Every factual claim must cite a source record such as an incident, signal,
    report, or knowledge article.
    """
    logger.info("Generating sitrep for incident: %s", incident_id)
    if not incident_id.startswith("AC-"):
        return {"error": "Invalid incident id", "message": "Incident ids must use AC-#### format."}

    citations = [
        {
            "source_id": incident_id,
            "source_type": "incident",
            "quote": "Incident record shows an open field-operations response.",
        },
        {
            "source_id": "SOP-POWER-001",
            "source_type": "kb_article",
            "quote": "Downed power line SOP requires a perimeter and field unit notification.",
        },
    ]
    response = {
        "incident_id": incident_id,
        "summary": (
            f"{incident_id} is open for field-operations review. "
            "Current guidance is to establish a perimeter and notify a field unit."
        ),
        "status": "open",
    }
    if include_citations:
        response["citations"] = citations
    return response


@mcp.tool()
async def list_queues() -> str:
    """List all available All Clear queues and their IDs."""
    queues = [
        {"id": "field-operations", "handles": "field hazards and public safety response"},
        {"id": "customer-comms", "handles": "status inquiries and reporter acknowledgments"},
        {"id": "compliance-desk", "handles": "statutory clocks and regulated reporting"},
        {"id": "engineering", "handles": "infrastructure outages and systems incidents"},
        {"id": "escalations", "handles": "human handoff, SEV1 incidents, PII exposure"},
    ]
    return json.dumps({"queue_count": len(queues), "queues": queues}, indent=2)


async def main() -> None:
    """Run the MCP server using stdio transport."""
    logger.info("Starting All Clear MCP Server...")
    logger.info("Lab 04 path: %s", LAB04_SOLUTION)
    logger.info("Lab 05 path: %s", LAB05_SOLUTION)
    logger.info("Shared data path: %s", SHARED_DIR)
    mcp.run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

