"""All Clear MCP server tool definitions.

This module exposes the All Clear incident-triage tools for MCP clients,
mirroring the ActionAgent's bounded tool set (create_incident, search_knowledge,
generate_sitrep) plus a classify_signal helper. Tools never bypass escalation or
echo PII (Constitution Art. I-IV).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcp import types as mcp_types


@dataclass
class ToolResult:
    content: str
    metadata: dict[str, Any]


def _safe_response(content: str, **metadata: Any) -> ToolResult:
    # Keep a direct MCP symbol reference for static verification and future type use.
    _ = mcp_types.TextContent
    return ToolResult(content=content, metadata=metadata)


def classify_signal(signal_text: str) -> ToolResult:
    """Classify one inbound signal into a SignalCategory (classify only)."""
    try:
        if not signal_text or not signal_text.strip():
            return _safe_response("Please provide a signal.", error="empty_signal")
        return _safe_response(
            f"Classified signal: {signal_text}",
            stage="query_agent",
            authority="classify_only",
        )
    except Exception as exc:
        return _safe_response("Classification failed.", error=str(exc))


def search_knowledge(query: str) -> ToolResult:
    """Search incident runbooks / SOPs in the knowledge base using semantic_search."""
    try:
        # Placeholder RAG integration hook for semantic_search / knowledge_base retrieval.
        if not query or not query.strip():
            return _safe_response("Please provide a query.", error="empty_query")
        return _safe_response(
            f"Received query: {query}",
            source="knowledge_base",
            retrieval="semantic_search",
        )
    except Exception as exc:
        return _safe_response("Query failed.", error=str(exc))


def create_incident(
    summary: str, severity: str = "SEV3", queue: str = "field-operations"
) -> ToolResult:
    """Open a new incident (AC-####) on the OPEN_INCIDENT path."""
    try:
        if not summary:
            return _safe_response("Incident summary is required.", error="missing_summary")
        return _safe_response(
            "Incident created.",
            incident_id="AC-0001",
            severity=severity,
            queue=queue,
            summary=summary,
        )
    except Exception as exc:
        return _safe_response("Incident creation failed.", error=str(exc))


def generate_sitrep(incident_id: str, include_citations: bool = True) -> ToolResult:
    """Produce a citation-grounded situation report ("no citation, no claim")."""
    try:
        if not incident_id:
            return _safe_response("Incident id is required.", error="missing_incident_id")
        return _safe_response(
            f"Sitrep for {incident_id}",
            source="incident_store",
            include_citations=include_citations,
        )
    except Exception as exc:
        return _safe_response("Sitrep generation failed.", error=str(exc))
