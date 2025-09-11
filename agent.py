import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("GOOGLE_GEMINI_MODEL")

def get_id_token(url):
    """Get an ID token to authenticate with the MCP server."""
    target_url = url
    audience = target_url.split('/mcp/')[0]
    request = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(request, audience)
    return id_token

currency_mcp_serve = os.getenv("CURRENCY_MCP_SERVER")
if not currency_mcp_serve:
    raise ValueError("The environment variable CURRENCY_MCP_SERVER is not set.")

currency_server_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        # Use the MCP server URL from the environment variable
        url=currency_mcp_serve,
        # Use the id_token from the environment variable
        headers={
            "Authorization": f"Bearer {get_id_token(currency_mcp_serve)}",
        },
    )
)

def get_current_time(city:str) -> dict:
    """Returns the current time in a specified city.

    Args:
        dict: A dictionary containing the current time for a specified city information with a 'status' key ('success' or 'error') and a 'report' key with the current time details in a city if successful, or an 'error_message' if an error occurred.
    """
    import datetime
    from zoneinfo import ZoneInfo

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {"status": "error",
                "error_message": f"Sorry, I don't have timezone information for {city}."}

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return {"status": "success",
            "report": f"""The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}"""}

root_agent = Agent(
    name="greeter",
    model=model_name,
    description="Agent to answer questions about the time and weather in a city.",
    instruction="I can answer your questions about the time and weather in a city.",
    tools=[currency_mcp_serve, get_current_time]
)