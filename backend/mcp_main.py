"""
Entry point for running All Clear as an MCP server.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.mcp_server import main

if __name__ == "__main__":
    asyncio.run(main())
