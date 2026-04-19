import requests
import os
from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv
load_dotenv()
def get_weather(city: str) -> dict:
    """
    Fetches real-time weather information for a given city.
    """
    API_KEY =os.getenv("OPENWEATHER_API_KEY")
    # 1. Fetch Weather Data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(weather_url).json()
    except requests.exceptions.RequestException:
        return {
            "status": "error",
            "error_message": "Network error. Please try again later."
        }

    # 2. Handle invalid city or API response
    if response.get("cod") != 200:
        return {
            "status": "error",
            "error_message": f"Could not find weather data for '{city}'."
        }

    # 3. Extract Weather Details
    temp = response["main"]["temp"]
    feels_like = response["main"]["feels_like"]
    humidity = response["main"]["humidity"]
    desc = response["weather"][0]["description"]

    # 4. Create Weather Report
    report = (
        f"Weather in {city.title()}:\n"
        f"- Condition: {desc}\n"
        f"- Temperature: {temp}°C\n"
        f"- Feels Like: {feels_like}°C\n"
        f"- Humidity: {humidity}%"
    )

    return {
        "status": "success",
        "report": report
    }


# Updated Agent (weather-only tool)
root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="An agent that provides real-time weather information for any city.",
    instruction="Use the get_weather tool to provide weather updates.",
    tools=[get_weather],
)