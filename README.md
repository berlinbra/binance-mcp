# Binance MCP

MCP Server for the Binance API. This server provides tools for accessing cryptocurrency market data through the Binance exchange API.

## Installation

### Using Smithery (Recommended)

To install Binance MCP Server for Claude Desktop automatically via Smithery:

```bash
npx -y @smithery/cli install @berlinbra/binance-mcp --client claude
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/berlinbra/binance-mcp.git
   cd binance-mcp
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

1. Create a Binance account at [binance.com](https://www.binance.com) if you don't already have one.
2. Generate an API key and secret from your Binance account settings.
3. Set the following environment variables:
   ```bash
   export BINANCE_API_KEY="your_api_key"
   export BINANCE_API_SECRET="your_api_secret"
   ```

## Running the MCP Server

After connecting Claude client with the MCP tool via json file and installing the packages, Claude should see the server's mcp tools.

You can run the server yourself via:

```bash
# In binance-mcp repo:
uv run src/binance_mcp/server.py
# or with inspector:
npx @modelcontextprotocol/inspector uv --directory /Users/{INSERT_USER}/YOUR/PATH/TO/binance-mcp run src/binance_mcp/server.py
```

## Available Tools

### get-ticker-price

Retrieves the current price for a cryptocurrency trading pair.

Example:
```
Current price for BTCUSDT:

Symbol: BTCUSDT
Price: 65432.10
```

## Claude Configuration

To configure Claude to use this MCP server, add the following to your MCP configuration:

```json
{
  "mcpServers": {
    "binance-mcp": {
      "command": "uv", 
      "args": [
        "--directory", 
        "/Users/{INSERT_USER}/YOUR/PATH/TO/binance-mcp", 
        "run", 
        "src/binance_mcp/server.py"
      ],
      "env": {
        "BINANCE_API_KEY": "<your-binance-api-key>",
        "BINANCE_API_SECRET": "<your-binance-api-secret>"
      }
    }
  }
}
```

## Future Tools

We plan to add the following tools in future updates:

1. `get-ticker-book`: Get order book data for a symbol
2. `get-ticker-24hr`: Get 24-hour price statistics for a symbol
3. `get-klines`: Get candlestick data for a trading pair
4. `get-account-info`: Get account information (requires authentication)
5. `get-open-orders`: Get all open orders (requires authentication)
6. `place-test-order`: Place a test order on the Binance API
7. `get-exchange-info`: Get exchange information and trading rules

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License.