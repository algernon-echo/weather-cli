import os
from dotenv import load_dotenv
import argparse
import requests

def get_weather (api_key, city, units):
    params = {
        "q": city,
        "appid": api_key,
        "units": units    
    }
    url = "http://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["cod"] != 200:
            return None, f"Error: {data["message"]}"
        
        units_map = {
            "standard": "K",
            "metric": "˚C",
            "imperial": "˚F"   
        }
        
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "units": units_map.get(units)
        }
        return weather, None
    except requests.exceptions.RequestException as e:
        return None, f"Error: Unable to fetch weather data ({str(e)})"

def display_weather(weather):
    print(f"Weather in {weather["city"]}:")
    print(f"Temperature: {weather["temperature"]}{weather["units"]}")
    print(f"Humidity: {weather["humidity"]}%")
    print(f"Description: {weather["description"].capitalize()}")

def main():
    #load api_key
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: API key not found. Please set APi key in the .env file.")
        return
    
    #set up argument parser
    parser = argparse.ArgumentParser(description="Command-line weather tool")
    parser.add_argument("city", help="Name of the city you want to get weather for")
    parser.add_argument("-u", "--units", choices=["standard", "metric", "imperial"], default="metric", help="Unit system")
    args = parser.parse_args()

    weather, error = get_weather (api_key, args.city, args.units)
    if weather:
        display_weather(weather)
    else:
        print(error)


if __name__ == "__main__":
    main()