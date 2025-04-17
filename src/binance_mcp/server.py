from typing import Any, List, Dict, Optional
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import os

# Import functions from tools.py
from .tools import (
    make_binance_request,
    format_ticker_price,
    BINANCE_API_BASE,
    BINANCE_API_KEY,
    BINANCE_API_SECRET
)

# Initialize the MCP server
server = Server("binance_crypto")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-ticker-price",
            description="Get the current price for a cryptocurrency symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
                    },
                },
                "required": ["symbol"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can fetch cryptocurrency data from the Binance API.
    """
    if not arguments:
        return [types.TextContent(type="text", text="Missing arguments for the request")]

    if name == "get-ticker-price":
        symbol = arguments.get("symbol")
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]

        symbol = symbol.upper()

        async with httpx.AsyncClient() as client:
            ticker_data = await make_binance_request(
                client,
                "/api/v3/ticker/price",
                {"symbol": symbol}
            )

            if isinstance(ticker_data, str):
                return [types.TextContent(type="text", text=f"Error: {ticker_data}")]

            formatted_ticker = format_ticker_price(ticker_data)
            ticker_text = f"Current price for {symbol}:\n\n{formatted_ticker}"

            return [types.TextContent(type="text", text=ticker_text)]
    
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="binance_crypto",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# This is needed if you'd like to connect to a custom client
if __name__ == "__main__":
    asyncio.run(main())