from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(
    lambda:stdio_client(
    StdioServerParameters(
       command= "uv",
       args= ["run", "main.py"]
    ),
)
)

with stdio_mcp_client:
    tools = stdio_mcp_client.list_tools_sync()
    agent = Agent(tools=tools)
    while True:
        user_input = input("\n You: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye")
            break
        if not user_input:
            continue
        print("Assistant:")
        agent(user_input)