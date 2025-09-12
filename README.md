# Custom MCP Calculator

## Techno

- uv
- FastMCP

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