import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === CONFIGURATION ===
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = os.getenv("CITY", "Tracy")             # Default to Tracy if not set
UNITS = "metric"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": UNITS,
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
  
# If the API returned an error (like 401), show it clearly

    if response.status_code != 200:
        print("Error response from OpenWeatherMap:")
        print("Status code:", response.status_code)
        print("Body       :", response.text)
        response.raise_for_status()  # still raise so we can handle it in main


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
        f"Temperature: {info['temp']} °C "
        f"(feels like {info['feels_like']} °C)\n"
        f"Humidity   : {info['humidity']}%"
    )


def main():
    try:
        weather_info = get_weather(CITY)
    except requests.exceptions.HTTPError as e:
        print("\nHTTP error while calling OpenWeatherMap:")
        print(e)
        print("\nMost common causes:")
        print("- Invalid or inactive API key")
        print("- Typo in the key")
        print("- Problem with your OpenWeatherMap account")
        return
    except Exception as e:
        print("\nUnexpected error occurred:")
        print(e)
        return

    message = format_weather(weather_info)
    print("\n" + message)


if __name__ == "__main__":
    main()