import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()


def get_id_token(url):
    """Get an ID token to authenticate with the MCP server."""
    target_url = url
    audience = target_url.split("/mcp/")[0]
    request = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(request, audience)
    return id_token


model_name = os.getenv("GOOGLE_GEMINI_MODEL")

currency_mcp_server = os.getenv("CURRENCY_MCP_SERVER")
if not currency_mcp_server:
    raise ValueError("The environment variable CURRENCY_MCP_SERVER is not set.")
if not currency_mcp_server.endswith("/mcp/"):
    currency_mcp_server = currency_mcp_server.rstrip("/") + "/mcp/"

currency_server_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        # Use the MCP server URL from the environment variable
        url=currency_mcp_server,
        # Use the id_token from the environment variable
        headers={
            "Authorization": f"Bearer {get_id_token(currency_mcp_server)}",
        },
    )
)

weather_mcp_server = os.getenv("WEATHER_MCP_SERVER")
if not weather_mcp_server:
    raise ValueError("The environment variable WEATHER_MCP_SERVER is not set.")
if not weather_mcp_server.endswith("/mcp/"):
    weather_mcp_server = weather_mcp_server.rstrip("/") + "/mcp/"

weather_server_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        # Use the MCP server URL from the environment variable
        url=weather_mcp_server,
        # Use the id_token from the environment variable
        headers={
            "Authorization": f"Bearer {get_id_token(weather_mcp_server)}",
        },
    )
)


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        dict: A dictionary containing the current time for a specified city information with a 'status' key ('success' or 'error') and a 'report' key with the current time details in a city if successful, or an 'error_message' if an error occurred.
    """
    import datetime
    from zoneinfo import ZoneInfo

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}.",
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return {
        "status": "success",
        "report": f"""The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}""",
    }


root_agent = Agent(
    name="greeter",
    model=model_name,
    description="Agent to answer questions about the time and weather in a city.",
    instruction="I can answer your questions about the time, weather and currency exchange rates in a city.",
    tools=[currency_server_toolset, weather_server_toolset, get_current_time],
)
