import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.agents import LlmAgent

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")
# Get the MCP server URL from the environment variable
currency_mcp_server_url = os.getenv("CURRNECY_MCP_SERVER_URL")
weather_mcp_server_url = os.getenv("WEATHER_MCP_SERVER_URL")

import subprocess
# Get the id_token from the gcloud command
id_token = subprocess.check_output(["gcloud", "auth", "print-identity-token"]).decode("utf-8").strip()

travel_guide_agent = Agent(
    name='TravelGuideAgent',
    description="An agent that retrieves users' queries through Google Search.",
    model=model_name,
    instruction="""
    You are a expert travel guide. Your goal is to create a simple, day-by-day itinerary. When a user inputs a destination city and their travel dates, you will generate a list of recommended tourist spots for each day of their trip.
    """
)

weather_server_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        # Use the MCP server URL from the environment variable
        http_url=f"{weather_mcp_server_url}/mcp/",
        # Use the id_token from the environment variable
        headers={
            "Authorization": f"Bearer {id_token}"
        }
    )
)

currency_server_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        # Use the MCP server URL from the environment variable
        http_url=f"{currency_mcp_server_url}/mcp/",
        # Use the id_token from the environment variable
        headers={
            "Authorization": f"Bearer {id_token}"
        }
    )
)

root_agent = Agent(
    name="RootAgent",
    model=model_name,
    description="The main entry point for the Zoo Tour Guide.",
    instruction="""
    - Let the user know you will help them learn about the animals we have in the zoo.
    - When the user responds, use the 'add_prompt_to_state' tool to save their response.
    After using the tool, transfer control to the 'tour_guide_workflow' agent.
    """
)