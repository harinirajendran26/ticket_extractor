import os

from mcp.server.mcpserver import MCPServer

from lookup import get_order_status

mcp = MCPServer("orders")

# Identity comes from the environment of whoever launches the server, never from the model.
CUSTOMER_ID = os.environ.get("CUSTOMER_ID", "C1")


@mcp.tool()
def order_status(order_id: str) -> dict:
    """Look up the status of the current customer's order by its order ID."""
    return get_order_status(order_id, current_customer_id=CUSTOMER_ID)


if __name__ == "__main__":
    mcp.run()