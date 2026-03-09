import asyncio
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
import sys
import json

async def run(method, params=None):
    from mcp import StdioServerParameters
    server_params = StdioServerParameters(
        command="npx.cmd",
        args=["-y", "mcp-remote", "https://stitch.googleapis.com/mcp", "--header", "X-Goog-Api-Key: AQ.Ab8RN6INM7BWKgxxR6h9UpigowVEHqsOkRCmen_aQyOLdDTdyQ"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Session initialized.", file=sys.stderr)

            if method == "list_tools":
                result = await session.list_tools()
                print(json.dumps(result.model_dump()))
            elif method == "call_tool":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result = await session.call_tool(tool_name, tool_args)
                print(json.dumps(result.model_dump()))
            else:
                print(f"Unknown method {method}")

if __name__ == "__main__":
    method = sys.argv[1]
    params_str = sys.argv[2] if len(sys.argv) > 2 else "{}"
    params = json.loads(params_str)
    asyncio.run(run(method, params))
