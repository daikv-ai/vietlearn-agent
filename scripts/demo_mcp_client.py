"""Launch the VietLearn MCP server and demonstrate a real stdio tool call."""

from __future__ import annotations

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_demo() -> None:
    """Connect, list the read-only tools, and retrieve Day 2."""
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.course_server"],
    )

    async with stdio_client(server_parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])

            result = await session.call_tool("get_lesson", {"day": 2})
            if result.structuredContent is None:
                raise RuntimeError("Expected a structured MCP response.")

            print(
                "Day 2 result:",
                json.dumps(result.structuredContent, ensure_ascii=False, indent=2),
            )


if __name__ == "__main__":
    asyncio.run(run_demo())
