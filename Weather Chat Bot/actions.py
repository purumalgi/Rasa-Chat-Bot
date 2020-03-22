# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
#
#
# This is a simple example for a custom action which utters "Hello World!"
#
from typing import Any, Text, Dict, List

import requests
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class BingLocationExtractor:

    def __init__(self):
        self.bing_baseurl = "http://dev.virtualearth.net/REST/v1/Locations"
        self.bing_api_key = "AmLh1M2aXvCGrc3c2AxuqcttZvc2jVTYOvGjjbL7RwM7F-zBVNPEg696TtAlh0Mr"  ## Update Bing API key here

    def getLocationInfo(self, query, tracker):

        list_cities = []
        queryString = {
            "query": query,
            "key": self.bing_api_key
        }
        res = requests.get(self.bing_baseurl, params=queryString)

        res_data = res.json()

        if (res.status_code != 200 or "low" == (res_data["resourceSets"][0]["resources"][0]["confidence"]).lower()):
            return None, None
        else:
            if ("locality" in res_data["resourceSets"][0]["resources"][0]["address"]):
                return res_data["resourceSets"][0]["resources"][0]["address"]["locality"], \
                       res_data["resourceSets"][0]["resources"][0]["name"]
            else:
                return "that", res_data["resourceSets"][0]["resources"][0]["name"]


class ActionHelloWorld(Action):


    def name(self) -> Text:
        return "action_extract_location"

    def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message['text']

        le = BingLocationExtractor()
        locality, location_name = le.getLocationInfo(str(user_input), tracker)

        dispatcher.utter_message("Thanks for sharing you location. " + locality.capitalize() + " is pretty place.")
        return [SlotSet("location", location_name)]


class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot('location')

        api_key = "6c71b89e6dd27db61bca952bc18f1e15"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + location
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"] - float(273.15)
            z = x["weather"]
            weather_description = z[0]["description"]

            # print("Temperature (in Celcius) = " + str(current_temperature) + "\nDescription = " + str(
            #     weather_description))
            dispatcher.utter_message("Temperature (in Celcius) = " + str(current_temperature) + "\nDescription = " + str(
                 weather_description))

        else:
            print("City not found")
        return []