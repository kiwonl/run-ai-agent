import logging
import asyncio
from adk.context import ToolContext
from adk.tool import tool

from services import currency_client, weather_client, travel_planner


@tool
def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Added to PROMPT: {prompt}")
    return {"status": "success"}


@tool
async def plan_trip(tool_context: ToolContext, city: str, dates: list[str], target_currency: str = "KRW"):
    """
    Receives a city and dates, and returns a comprehensive travel plan
    including a generated itinerary, currency exchange information, and weather forecasts.
    """
    logging.info(f"Received trip request for {city} on {dates}")

    # Concurrently fetch all required information
    tasks = [
        travel_planner.generate_travel_plan(city, dates),
        currency_client.get_currency_info(target_currency),
        weather_client.get_weather_forecast(city, dates),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    travel_plan_result, currency_result, weather_result = results

    # Error handling for each service
    if isinstance(travel_plan_result, Exception) or travel_plan_result.get("error"):
        logging.error(f"Error generating travel plan: {travel_plan_result}")
        travel_plan = {"error": f"Could not generate travel plan: {travel_plan_result}"}
    else:
        logging.info("Travel plan generated successfully.")
        travel_plan = travel_plan_result

    if isinstance(currency_result, Exception) or currency_result.get("error"):
        logging.error(f"Error retrieving currency data: {currency_result}")
        currency_info = {
            "error": f"Could not retrieve currency data: {currency_result}"
        }
    else:
        logging.info("Currency data retrieved successfully.")
        currency_info = currency_result

    if isinstance(weather_result, Exception) or weather_result.get("error"):
        logging.error(f"Error retrieving weather data: {weather_result}")
        weather_forecasts = {
            "error": f"Could not retrieve weather data: {weather_result}"
        }
    else:
        logging.info("Weather data retrieved successfully.")
        weather_forecasts = weather_result

    return {
        "city": city,
        "dates": dates,
        "travel_plan": travel_plan,
        "currency_info": currency_info,
        "weather_forecasts": weather_forecasts,
    }