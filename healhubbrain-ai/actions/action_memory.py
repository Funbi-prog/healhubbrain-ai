from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionRememberUserFeeling(Action):

    def name(self):
        return "action_remember_user_feeling"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):

        last_message = tracker.latest_message.get('text')
        tracker.slots['last_feeling'] = last_message

        dispatcher.utter_message(
            text=f"Okay, I hear you — you said '{last_message}'. Let's work through that gently."
        )
        return []
