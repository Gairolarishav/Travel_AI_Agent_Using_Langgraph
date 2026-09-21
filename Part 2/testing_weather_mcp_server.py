import os
from dotenv import load_dotenv
import asyncio

from langchain.mcp import MCPAdapter

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

client = MCPAdapter(
    {
        "weather": {
            "command": r"E:\Agentic AI Projects\Multi_Agent_System\langgraph_Env\Scripts\python.exe",
            "args": [
                r"E:\Agentic AI Projects\Multi_Agent_System\Part 2\custom_weather_mcp_server.py"
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
            }
        }
    }
)

async def main():

    print("Loading tools...")

    tools = await client.list_tools()

    print("Tools loaded!")

    for tool in tools:
        print(tool.name)

if __name__ == "__main__":
    asyncio.run(main())