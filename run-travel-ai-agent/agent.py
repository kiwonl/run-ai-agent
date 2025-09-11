import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

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

weather_mcp_server_url = os.getenv("WEATHER_MCP_SERVER")
if not weather_mcp_server_url:
    raise ValueError("The environment variable WEATHER_MCP_SERVER is not set.")

weather_server_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        # Use the MCP server URL from the environment variable
        url=weather_mcp_server_url,
        # Use the id_token from the environment variable
        headers={
            "Authorization": f"Bearer {get_id_token(weather_mcp_server_url)}",
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
    name="weather_time_agent",
    model=model_name,
    description="Agent to answer questions about the time and weather in a city.",
    instruction="I can answer your questions about the time and weather in a city.",
    tools=[weather_server_toolset, get_current_time]
)



# import os
# import logging
# import google.cloud.logging
# from dotenv import load_dotenv

# from google.adk.agents import Agent
# from google.adk.agents import LlmAgent

# # --- Setup Logging and Environment ---
# cloud_logging_client = google.cloud.logging.Client()
# cloud_logging_client.setup_logging()

# load_dotenv()

# model_name = os.getenv("MODEL")
# # Get the MCP server URL from the environment variable
# currency_mcp_server_url = os.getenv("CURRNECY_MCP_SERVER_URL")
# weather_mcp_server_url = os.getenv("WEATHER_MCP_SERVER_URL")

# import subprocess
# # Get the id_token from the gcloud command
# id_token = subprocess.check_output(["gcloud", "auth", "print-identity-token"]).decode("utf-8").strip()

# travel_guide_agent = Agent(
#     name='TravelGuideAgent',
#     description="An agent that retrieves users' queries through Google Search.",
#     model=model_name,
#     instruction="""
#     You are a expert travel guide. Your goal is to create a simple, day-by-day itinerary. When a user inputs a destination city and their travel dates, you will generate a list of recommended tourist spots for each day of their trip.
#     """
# )

# weather_server_toolset = MCPToolset(
#     connection_params=StreamableHTTPConnectionParams(
#         # Use the MCP server URL from the environment variable
#         http_url=f"{weather_mcp_server_url}/mcp/",
#         # Use the id_token from the environment variable
#         headers={
#             "Authorization": f"Bearer {id_token}"
#         }
#     )
# )

# currency_server_toolset = MCPToolset(
#     connection_params=StreamableHTTPConnectionParams(
#         # Use the MCP server URL from the environment variable
#         http_url=f"{currency_mcp_server_url}/mcp/",
#         # Use the id_token from the environment variable
#         headers={
#             "Authorization": f"Bearer {id_token}"
#         }
#     )
# )

# root_agent = Agent(
#     name="RootAgent",
#     model=model_name,
#     description="The main entry point for the Zoo Tour Guide.",
#     instruction="""
#     - Let the user know you will help them learn about the animals we have in the zoo.
#     - When the user responds, use the 'add_prompt_to_state' tool to save their response.
#     After using the tool, transfer control to the 'tour_guide_workflow' agent.
#     """
# )