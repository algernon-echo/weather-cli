import argparse  #标准库中，无需额外安装
import requests     #需安装
import os   #标准库中，无需额外安装
from dotenv import load_dotenv  #需安装. write as install python-dotenv

def get_weather(city, api_key, units):
    """Fetch weather data for a given city using OpenWeatherMap API."""
    #https://openweathermap.org/current#name 文档我给找到了捏。这下知道写什么参数和url了
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data["cod"] != 200:
            return None, f"Error: {data['message']}"
    
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"] #这里weather是个列表，[0]表示第一个元素
        }
        return weather, None
    except requests.exceptions.RequestException as e:
        return None, f"Error: Unable to fetch weather data ({str(e)})"

def display_weather(weather):
    """Display formatted weather information."""
    print(f"Weather in {weather['city']}:")
    print(f"Temperature: {weather['temperature']}°C") #这里有个bug。无论用的什么单位，最终展现的都是˚C
    print(f"Humidity: {weather['humidity']}%")
    print(f"Wind Speed: {weather['wind_speed']} m/s")
    print(f"Description: {weather['description'].capitalize()}")

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: API key not found. Please set OPENWEATHER_API_KEY in .env file.")
        return

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Command-line weather tool")
    parser.add_argument("city", help="Name of the city to get weather for")
    parser.add_argument("-u", "--units", choices=["metric", "imperial"], default="metric",
                        help="Unit system (metric or imperial)")
    args = parser.parse_args()

    # Fetch and display weather
    weather, error = get_weather(args.city, api_key, args.units)
    if weather:
        display_weather(weather)
    else:
        print(error)

if __name__ == "__main__":  #To avoid running the code when the file is imported
    main()