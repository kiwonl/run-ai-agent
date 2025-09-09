import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Configure the Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

async def generate_travel_plan(city: str, dates: List[str]):
    """
    Generates a travel plan using the Gemini API.
    """
    if not model:
        return {"error": "Gemini model is not available."}
        
    if not dates:
        return {"error": "Dates must be provided to generate a plan."}

    start_date = dates[0]
    end_date = dates[-1]
    num_days = len(dates)

    prompt = f"""
    Create a detailed {num_days}-day travel plan for a trip to {city}, from {start_date} to {end_date}.
    The plan should be structured day by day.
    For each day, please suggest activities for the morning, afternoon, and evening.
    Provide practical tips for traveling in {city}.
    The output should be in Korean.
    """

    try:
        response = await model.generate_content_async(prompt)
        return {"plan": response.text}
    except Exception as e:
        return {"error": f"Failed to generate travel plan from Gemini: {e}"}

