from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

class ActionRememberUserFeeling(Action):

    def name(self) -> Text:
        return "action_remember_user_feeling"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_message = tracker.latest_message.get("text")
        dispatcher.utter_message(text=f"I hear you — you said '{last_message}'. Let’s unpack that a bit, yeah?")
        return [{"event": "slot", "name": "last_feeling", "value": last_message}]
