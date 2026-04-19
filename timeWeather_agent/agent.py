import requests
import os
from datetime import datetime
import pytz

from google.adk.agents.llm_agent import Agent


def get_time(location: str) -> dict:
    try:
        timezone = pytz.timezone(location)
        now = datetime.now(timezone)

        return {
            "status": "success",
            "response": f"Current time in {location}: {now.strftime('%I:%M %p')}"
        }
    except:
        return {"status": "error", "response": "Invalid timezone"}


def get_weather(city: str) -> dict:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    res = requests.get(url).json()

    if res.get("cod") != 200:
        return {"status": "error", "response": "City not found"}

    return {
        "status": "success",
        "response": f"{city}: {res['weather'][0]['description']}, {res['main']['temp']}°C"
    }


def smart_agent(query: str) -> dict:
    query = query.lower()

    if "time" in query:
        return get_time("Asia/Kolkata")

    elif "weather" in query:
        return get_weather("Hyderabad")

    else:
        return {"status": "error", "response": "Ask about time or weather"}


root_agent = Agent(
    name="time_weather_agent",
    model="gemini-2.5-flash",
    description="Handles time and weather queries",
    instruction="Answer user queries about time and weather",
    tools=[smart_agent],
)