from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionInterpretEmotion(Action):
    def name(self):
        return "action_interpret_emotion"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()
        emotion_map = {
            "sad": "utter_emotion_sadness",
            "lost": "utter_emotion_sadness",
            "overwhelmed": "utter_emotion_anxiety",
            "tired": "utter_emotion_burnout",
            "drained": "utter_emotion_burnout",
            "anxious": "utter_emotion_anxiety"
        }
        for keyword, response in emotion_map.items():
            if keyword in user_message:
             dispatcher.utter_message(response=response)
        return []
        dispatcher.utter_message(text="Tell me more about what’s been happening lately.")
        return []

class ActionEmpathicRecovery(Action):
    def name(self):
        return "action_empathic_recovery"

    def run(self, dispatcher, tracker, domain):
        user_text = tracker.latest_message.get("text", "").lower()
        dispatcher.utter_message(text=f"It sounds like there’s a lot on your mind. Tell me more — what’s really behind '{user_text}'?")
        return []

class ActionReflectBeforeResponse(Action):
    def name(self):
        return "action_reflect_before_response"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message.get("text", "").lower()

        reflections = {
            "cry": "It sounds like you’re reaching a breaking point, and tears might be your body’s way of releasing pressure.",
            "stress": "You’re under emotional load — I can sense that you’ve been holding on for too long.",
            "angry": "That anger might be protecting a deeper hurt or disappointment."
        }

        for word, reflection in reflections.items():
            if word in message:
                dispatcher.utter_message(text=reflection)
                break

        dispatcher.utter_message(text="You can tell me what triggered it — I’ll stay with you through this.")
        return []
