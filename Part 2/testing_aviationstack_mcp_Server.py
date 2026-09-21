import os
from dotenv import load_dotenv
from langchain.mcp import MCPAdapter
import asyncio

load_dotenv()

AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

config = {
    "mcpServers": {
        "aviationstack": {
            "command": r"E:\Agentic AI Projects\Multi_Agent_System\Part 2\aviationstack-mcp\.venv\Scripts\python.exe",
            "args": ["-m", "aviationstack_mcp", "mcp","run"],
            "env": {
                "AVIATION_STACK_API_KEY" : AVIATION_STACK_API_KEY
            }
            }
    }
}

client = MCPAdapter(config)

# Tool Discovery
async def main():
    tools = await client.list_tools()

    print("\n Available MCP Tools:\n")

    for tool in tools:
        print(tool.name)

asyncio.run(main())