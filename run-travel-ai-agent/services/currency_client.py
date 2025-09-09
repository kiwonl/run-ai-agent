import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CURRENCY_SERVER_URL = os.getenv("CURRENCY_SERVER_URL")

async def get_currency_info(target_currency: str = "KRW"):
    """
    Retrieves currency exchange rate information from the currency MCP server.
    Assumes the server provides rates against USD.
    """
    if not CURRENCY_SERVER_URL:
        return {"error": "Currency server URL not configured."}

    try:
        async with httpx.AsyncClient() as client:
            # Assuming the currency server has an endpoint like /rates/latest?base=USD&symbols=KRW
            response = await client.get(f"{CURRENCY_SERVER_URL}/rates/latest", params={"base": "USD", "symbols": target_currency})
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        return {"error": f"Failed to connect to currency server: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
