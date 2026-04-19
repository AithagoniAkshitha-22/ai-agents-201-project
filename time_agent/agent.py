from google.adk.agents.llm_agent import Agent

from datetime import datetime
import pytz

def get_current_time(location: str) -> dict:
    """
    Returns the current time in a specified city/location.
    Format for location should be 'Continent/City' (e.g., 'America/New_York').
    """
    try:
        # Standardize common names or handle direct timezone lookups
        # pytz requires the format 'Area/Location'
        timezone = pytz.timezone(location)
        now = datetime.now(timezone)
       
        return {
            "status": "success",
            "location": location,
            "time": now.strftime("%I:%M %p"),
            "date": now.strftime("%Y-%m-%d")
        }
    except pytz.exceptions.UnknownTimeZoneError:
        return {
            "status": "error",
            "message": f"Could not find timezone for '{location}'. Please use 'Continent/City' format."
        }

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)