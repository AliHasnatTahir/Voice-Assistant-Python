import geocoder
import requests
from recognize import speak


api_key = "YOUR'S WEATHER API KEY"


def get_myweather():
    g = geocoder.ip('me')

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={g.lat}&lon={g.lng}&appid={api_key}'

    response = requests.get(weather_url)

    weather_data = response.json()

    if weather_data["cod"] != "404":

        main = weather_data["main"]
        temperature = main["temp"]
        description = weather_data["weather"][0]["description"]
        wind = weather_data["wind"]["speed"]

        temperature = temperature - 273.15

        print(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
        speak(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
    else:
        print("Location not found.")
        speak("Location not found.")


def get_otherweather(location):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + location

    response = requests.get(complete_url)

    weather_data = response.json()

    if weather_data["cod"] != "404":

        main = weather_data["main"]
        temperature = main["temp"]
        description = weather_data["weather"][0]["description"]
        wind = weather_data["wind"]["speed"]

        temperature = temperature - 273.15

        print(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
        speak(f"Current temperature is {temperature:.1f}°C and {description} and wind speed is {wind} m/s")
        
    else:
        print("Location not found.")
        speak("Location not found.")
