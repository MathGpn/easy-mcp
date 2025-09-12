from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    print("MCP Serveur démarré")
    mcp.run(transport="stdio")