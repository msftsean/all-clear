"""Entry point for the All Clear MCP server."""

from __future__ import annotations

from backend.app import mcp_server


def run() -> int:
    # In a production implementation this would start stdio_server / MCP runtime.
    # Keeping it lightweight for lab validation.
    _ = mcp_server.search_knowledge("downed line on Main St")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
