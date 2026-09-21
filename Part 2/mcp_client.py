import os

from dotenv import load_dotenv
from langchain.mcp import MCPAdapter
from langchain_groq import ChatGroq

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


class MCPClient:
    def __init__(self):
        self.client = MCPAdapter(
            {
                "tavily": {
                    "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}" 
                },

                "aviationstack": {
                    "command": r"E:\Agentic AI Projects\Multi_Agent_System\Part 2\aviationstack-mcp\.venv\Scripts\python.exe",
                    "args": ["-m","aviationstack_mcp","mcp","run",],
                    "env": {
                        "AVIATION_STACK_API_KEY": AVIATION_STACK_API_KEY
                    },
                },

                "weather": {
                    "command": r"E:\Agentic AI Projects\Multi_Agent_System\langgraph_Env\Scripts\python.exe",
                    "args": [ 
                        r"E:\Agentic AI Projects\Multi_Agent_System\Part 2\custom_weather_mcp_server.py"
                    ],
                    "env": {
                        "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
                    },
                },
            }
        )

        self._tools_cache = None
        # Serializes access so concurrent calls don't open overlapping
        # connect/disconnect cycles on the same underlying client.
        self._lock = __import__("asyncio").Lock()

    async def get_tools(self):
        """List tools once, in a single explicit connection, and cache them."""
        if self._tools_cache is None:
            async with self._lock:
                if self._tools_cache is None:  # re-check after acquiring lock
                    async with self.client:
                        self._tools_cache = await self.client.list_tools()
        return self._tools_cache

    async def get_tool(self, tool_name: str):
        tools = await self.get_tools()

        for tool in tools:
            if tool.name == tool_name:

                print("tool.name =====", tool.name)
                return tool

        raise ValueError(f"MCP tool '{tool_name}' not found")

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict | None = None,
    ):
        tool = await self.get_tool(tool_name)

        # Explicit, short-lived connection scope for the actual call.
        # This is what stops fastmcp from silently reusing one long-lived
        # session across every request (the source of the proxy warning).
        async with self._lock:
            async with self.client:
                return await tool.ainvoke(arguments or {})


mcp = MCPClient()


# -------------------------
# Tavily
# -------------------------

async def tavily_mcp_search(query: str):
    print("tavily_mcp_search ===")
    return await mcp.call_tool(
        "tavily_tavily_search",
        {"query": query},
    )


# -------------------------
# AviationStack
# -------------------------

async def aviation_mcp_call(
    tool_name: str,
    tool_args: dict | None = None,
):
    return await mcp.call_tool(
        tool_name,
        tool_args,
    )


async def get_airports():
    return await mcp.call_tool("aviationstack_list_airports")


async def get_airlines():
    return await mcp.call_tool("aviationstack_list_airlines")


# -------------------------
# Weather
# -------------------------

async def weather_mcp_search(city: str):
    return await mcp.call_tool(
        "weather_get_current_weather",
        {"city": city},
    )


async def forecast_mcp_search(city: str):
    return await mcp.call_tool(
        "weather_get_forecast",
        {"city": city},
    )


# -------------------------
# Destination Extractor
# -------------------------

llm = ChatGroq(model="openai/gpt-oss-20b")


async def extract_destination(query: str) -> str:
    prompt = f"""
Extract only the destination city or country.

Query:
{query}

Return only destination name.
"""
    response = await llm.ainvoke(prompt)
    return response.content.strip()