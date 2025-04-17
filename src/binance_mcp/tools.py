"""
Binance MCP Tools Module

This module contains utility functions for making requests to the Binance API
and formatting the responses.
"""

from typing import Any, Dict, Optional, List
import httpx
import os
import time
import hmac
import hashlib
from urllib.parse import urlencode

# API configuration
BINANCE_API_BASE = "https://api.binance.com"
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

async def make_binance_request(
    client: httpx.AsyncClient, 
    endpoint: str, 
    params: Optional[Dict[str, Any]] = None, 
    signed: bool = False,
    method: str = "GET"
) -> Dict[str, Any] | str:
    """Make a request to the Binance API with proper error handling.
    
    Args:
        client: An httpx AsyncClient instance
        endpoint: The API endpoint to call
        params: Parameters to include in the request
        signed: Whether the request requires authentication
        method: HTTP method (GET, POST, DELETE)
        
    Returns:
        Either a dictionary containing the API response, or a string with an error message
    """
    url = f"{BINANCE_API_BASE}{endpoint}"
    headers = {}
    
    # Prepare parameters
    if params is None:
        params = {}
        
    # Add API key to headers if available
    if BINANCE_API_KEY and (signed or endpoint.startswith('/api/v3/account')):
        headers['X-MBX-APIKEY'] = BINANCE_API_KEY
        
    # Sign the request if required
    if signed:
        if not BINANCE_API_SECRET:
            return "API secret is required for authenticated requests"
        
        # Add timestamp for signed requests
        params['timestamp'] = int(time.time() * 1000)
        
        # Create signature
        query_string = urlencode(params)
        signature = hmac.new(
            BINANCE_API_SECRET.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        params['signature'] = signature
        
    try:
        if method == "GET":
            response = await client.get(
                url,
                params=params,
                headers=headers,
                timeout=30.0
            )
        elif method == "POST":
            response = await client.post(
                url,
                params=params,
                headers=headers,
                timeout=30.0
            )
        elif method == "DELETE":
            response = await client.delete(
                url,
                params=params,
                headers=headers,
                timeout=30.0
            )
        else:
            return f"Unsupported HTTP method: {method}"

        # Check for specific error responses
        if response.status_code == 429:
            return f"Rate limit exceeded. Error details: {response.text}"
        elif response.status_code == 418:
            return f"IP has been auto-banned for violating rate limits. Error details: {response.text}"
        elif response.status_code == 403:
            return f"WAF limit exceeded or API key invalid. Error details: {response.text}"

        response.raise_for_status()

        return response.json()
    except httpx.TimeoutException:
        return "Request timed out after 30 seconds. The Binance API may be experiencing delays."
    except httpx.ConnectError:
        return "Failed to connect to Binance API. Please check your internet connection."
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {str(e)} - Response: {e.response.text}"
    except Exception as e:
        return f"Unexpected error occurred: {str(e)}"

def format_ticker_price(ticker_data: Dict[str, Any]) -> str:
    """Format ticker price data into a concise string.
    
    Args:
        ticker_data: The response data from the Binance ticker/price endpoint
        
    Returns:
        A formatted string containing the ticker price information
    """
    try:
        if not ticker_data:
            return "No ticker price data available in the response"

        if isinstance(ticker_data, list):
            # Multiple symbols returned
            formatted_data = []
            for ticker in ticker_data:
                formatted_data.append(
                    f"Symbol: {ticker.get('symbol', 'N/A')}\n"
                    f"Price: {ticker.get('price', 'N/A')}"
                )
            return "\n---\n".join(formatted_data)
        else:
            # Single symbol returned
            return (
                f"Symbol: {ticker_data.get('symbol', 'N/A')}\n"
                f"Price: {ticker_data.get('price', 'N/A')}"
            )
    except Exception as e:
        return f"Error formatting ticker price data: {str(e)}"