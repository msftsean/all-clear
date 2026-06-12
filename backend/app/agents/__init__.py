"""
Agent implementations for All Clear (001-maf-rehost).
Three-agent incident-triage pipeline with bounded authority:
- QueryAgent (build_query_agent): signal classification (LLM, structured output)
- RouterExecutor: deterministic dedup/severity/SLA routing (NO LLM)
- ActionAgent: incident creation, knowledge search, sitrep (LLM + tools)
"""

from app.agents.query_agent import build_query_agent

__all__ = ["build_query_agent"]

