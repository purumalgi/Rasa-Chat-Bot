import requests
import json

api_key = "6c71b89e6dd27db61bca952bc18f1e15"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = input("Enter city name : ")
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
response = requests.get(complete_url)
x = response.json()

if x["cod"] != "404":
    y = x["main"]
    current_temperature = y["temp"] - float(273.15)
    z = x["weather"]
    weather_description = z[0]["description"]

    print ("Temperature (in Celcius) = " + str(current_temperature) + "\nDescription = " + str(weather_description))

else:
    print ("City not found")