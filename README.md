# Custom MCP Calculator

## Techno

- uv
- FastMCP

## In the "doc/" folder (following official documentation)

1) 1er terminal : uv run doc/mcp_server.py
2) 2e terminal : uv run doc/mcp_client.py

OR by launching the inspector (replaces the client)

- uv run mcp dev doc/mcp_server.py 

Remarks :

- Transport type : STDIO
- Command : uv
- Arguments : run --with mcp mcp run doc/mcp_server.py

The client will connect to the server and demonstrate the following:

- Listing available tools and resources.
- Calling tools.
- Fetching list of resources and accessing them.
- Fetching list of prompts and accessing them.

## Try it out (with VS Code Github Copilot client)
- git clone the repo
- uv sync
- source .venv/bin/activate
- update the "mcp.json" file with the mcp_demo.json example
- in the extensions & tools enabled in the chat widget you will find the Calculator MCP.
- in Github Copilot Chat ask "combien font 5 + 9" ou "En utilisant le mcp calculator, fais 3 + 6".

## Try it out (with custom MCP server & client)

### 1re option (tout en un : lance le serveur avec le Calculator tool et le client)
- uv run start_mcp.py


### 2e option
1) 1er terminal : uv run server_tools.py
2) 2e terminal : uv run mcp_client.py




### Startup
- uv init
- uv venv
- source .venv/bin/activate