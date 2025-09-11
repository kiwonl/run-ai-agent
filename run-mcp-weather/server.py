import asyncio
import logging
import os

import httpx
from fastmcp import FastMCP

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Weather MCP Server ☀️")

@mcp.tool()
def get_weather(
    city: str,
    date: str = "",
):
    """Use this to get the weather for a specific city and optional date.

    Args:
        city: The city to get the weather for (e.g., "Seoul").
        date: The date to get the weather for (e.g., "2025-09-09"). Defaults to today.

    Returns:
        A dictionary containing the weather data, or an error message if the request fails.
    """
    logger.info(
        f"--- 🛠️ Tool: get_weather called for {city} on {date if date else 'today'} ---"
    )
    try:
        # wttr.in provides a simple JSON API for weather information
        url = f"https://wttr.in/{city}"
        if date:
            url += f"/{date}"
        
        response = httpx.get(url, params={"format": "j1"})
        response.raise_for_status()

        data = response.json()
        logger.info(f"✅ API response: {data}")
        return data
    except httpx.HTTPError as e:
        return {"error": f"API request failed: {e}"}
    except ValueError:
        return {"error": "Invalid JSON response from API."}


if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )