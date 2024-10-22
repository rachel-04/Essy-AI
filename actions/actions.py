from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
from fuzzywuzzy import fuzz
from rasa_sdk import Action


class ActionExtractSlots(Action):
    def name(self) -> Text:
        return "action_extract_slots"

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Example of extracting a slot from the user message
        maintenance_type = tracker.get_slot("maintenance_type")
        if not maintenance_type:
            # Assuming you want to set this slot from an entity
            maintenance_type = next(tracker.get_latest_entity_values("maintenance_type"), None)
        
        if maintenance_type:
            dispatcher.utter_message(text=f"Maintenance type is set to {maintenance_type}.")
        else:
            dispatcher.utter_message(text="I couldn't identify the maintenance type.")

        # Set the slot value
        return [SlotSet("maintenance_type", maintenance_type)]


class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # This is an example of a custom action that simply sends a greeting message
        dispatcher.utter_message(text="Hello! How can I assist you today?")
        return []

class ActionFuzzyMatch(Action):
    def name(self) -> str:
        return "action_fuzzy_match"

    def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message.get("text")
        intent = tracker.latest_message.get("intent").get("name")
        
        if fuzz.partial_ratio(user_input.lower(), "maintenance") > 80:
            dispatcher.utter_message(text="It looks like you need maintenance assistance.")
            # Perform other actions
        else:
            dispatcher.utter_message(text="I'm not sure what you mean. Could you clarify?")
        return []