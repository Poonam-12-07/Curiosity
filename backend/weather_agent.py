"""Portable weather chat agent: call chat(message) to get weather reply."""
import re
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === CONFIGURATION ===
API_KEY = os.getenv("OPENWEATHER_API_KEY")
UNITS = "metric"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    params = {"q": city.strip(), "appid": API_KEY, "units": UNITS}
    response = requests.get(BASE_URL, params=params, timeout=10)
    if response.status_code != 200:
        response.raise_for_status()
    data = response.json()
    return {
        "city": data["name"],
        "description": data["weather"][0]["description"].title(),
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
    }


def format_weather(info: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        f"Weather report for {info['city']} at {now}\n"
        f"Conditions : {info['description']}\n"
        f"Temperature: {info['temp']} °C (feels like {info['feels_like']} °C)\n"
        f"Humidity   : {info['humidity']}%"
    )


def extract_city_from_message(message: str) -> str | None:
    if not message or not message.strip():
        return None
    text = message.strip()
    m = re.search(r"(?:weather|forecast)\s+(?:in|for|at)\s+([A-Za-z\s\-']+)", text, re.I)
    if m:
        return m.group(1).strip()
    if re.match(r"^[A-Za-z\s\-']+$", text) and len(text) >= 2:
        return text
    return None


def chat(message: str) -> str:
    """User sends a city or phrase like 'weather in London'; returns weather reply."""
    city = extract_city_from_message(message)
    if not city:
        return "Please send a city name, e.g. 'London' or 'weather in Paris'."

    try:
        info = get_weather(city)
        return format_weather(info)
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 404:
            return f"No weather data found for '{city}'. Check the city name."
        return "Weather service error. Please try again later."
    except requests.exceptions.RequestException:
        return "Could not reach the weather service. Please try again."
    except Exception as e:
        return f"Something went wrong: {e}"
