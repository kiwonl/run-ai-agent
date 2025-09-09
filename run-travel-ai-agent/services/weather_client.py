import os
import httpx
from typing import List
from dotenv import load_dotenv

load_dotenv()

WEATHER_SERVER_URL = os.getenv("WEATHER_SERVER_URL")

async def get_weather_forecast(city: str, dates: List[str]):
    """
    Retrieves weather forecast information from the weather MCP server.
    """
    if not WEATHER_SERVER_URL:
        return {"error": "Weather server URL not configured."}

    try:
        async with httpx.AsyncClient() as client:
            # Assuming the weather server has an endpoint like /forecast
            response = await client.post(f"{WEATHER_SERVER_URL}/forecast", json={"city": city, "dates": dates})
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        return {"error": f"Failed to connect to weather server: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
