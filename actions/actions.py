# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests
import re
OPENWEATHER_API_KEY = "857dd1493b500c6066dddd7e0939640f"

class ValidateTravelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_travel_form"

    def validate_destination_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if len(slot_value) < 2:
            dispatcher.utter_message(text="Please provide a valid destination.")
            return {"destination_city": None}
        return {"destination_city": slot_value}

    def validate_start_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Please provide a valid start date.")
            return {"start_date": None}
        return {"start_date": slot_value}

    def validate_end_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if not slot_value:
            dispatcher.utter_message(text="Please provide a valid end date.")
            return {"end_date": None}
        return {"end_date": slot_value}

class ActionConfirmTrip(Action):
    def name(self) -> Text:
        return "action_confirm_trip"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        destination = tracker.get_slot("destination_city")
        start_date = tracker.get_slot("start_date")
        end_date = tracker.get_slot("end_date")

        dispatcher.utter_message(text=f"Great! Your trip to {destination} is planned from {start_date} to {end_date}.")
        dispatcher.utter_message(text="Do you want me to check the weather and suggest what to pack?")
        return []

import re
import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

OPENWEATHER_API_KEY = "857dd1493b500c6066dddd7e0939640f"

logger = logging.getLogger(__name__)

class ActionFetchWeather(Action):
    def name(self) -> Text:
        return "action_fetch_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text", "").lower()

        # Try to extract city from user message (e.g., "weather in Delhi")
        match = re.search(r"weather in ([a-zA-Z\s]+)", user_message)
        if match:
            destination = match.group(1).strip().title()
            dispatcher.utter_message(text=f"Got it! Fetching weather for {destination}.")
        else:
            destination = tracker.get_slot("destination_city")

        # Log the destination for debugging (not shown to user)
        logger.info(f"Fetching weather for destination: {destination}")

        if not destination:
            dispatcher.utter_message(text="I don't know your destination yet. Could you please tell me where you are traveling?")
            return []

        url = f"http://api.openweathermap.org/data/2.5/weather?q={destination}&units=metric&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            dispatcher.utter_message(text=f"Sorry, I couldn't fetch the weather for {destination} right now.")
            return []

        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']

        dispatcher.utter_message(text=f"The current weather in {destination} is {weather_desc} with a temperature of {temp}°C.")

        # Packing advice
        if temp < 10:
            packing_advice = "It's quite cold. Pack warm clothes, jackets, and sweaters."
        elif 10 <= temp < 20:
            packing_advice = "The weather is cool. Take a light jacket or sweater."
        elif 20 <= temp < 30:
            packing_advice = "The weather is pleasant. Pack comfortable clothes."
        else:
            packing_advice = "It's hot. Pack light clothes, sunglasses, and sunscreen."

        dispatcher.utter_message(text=packing_advice)

        # Return slot set for packing advice if you want to use it elsewhere
        return [SlotSet("packing_suggestion", packing_advice)]

class ActionFaq(Action):
    def name(self) -> Text:
        return "action_faq"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()
        faq_answers = {
            "what is rasa": "Rasa is an open-source framework for building AI assistants.",
            "who built you": "I was built for the Yoliday internship assignment!",
            "how can i plan my trip": "Just say 'I want to plan my trip' and I’ll help!",
            "who are you": "I'm your Yoliday travel assistant.",
            "what is your name": "I’m your travel assistant bot, always ready to help!",
            "what can you do": "I can help you plan trips, check weather, and suggest packing tips."
        }

        for question, response in faq_answers.items():
            if question in user_message:
                dispatcher.utter_message(text=response)
                return []

        # Default response for unmatched FAQ
        dispatcher.utter_message(text="I'm here to help with travel planning, weather, and packing tips!")
        return []
