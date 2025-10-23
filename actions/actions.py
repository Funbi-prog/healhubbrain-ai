from __future__ import annotations
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os

# 🧠 Emotion Interpretation
class ActionInterpretEmotion(Action):
    def name(self):
        return "action_interpret_emotion"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_message = tracker.latest_message.get("text", "").lower()
        emotion_map = {
            "sad": "utter_emotion_sadness",
            "lost": "utter_emotion_sadness",
            "overwhelmed": "utter_emotion_anxiety",
            "tired": "utter_emotion_burnout",
            "drained": "utter_emotion_burnout",
            "anxious": "utter_emotion_anxiety",
        }

        for keyword, response in emotion_map.items():
            if keyword in user_message:
                dispatcher.utter_message(response=response)
                return []
        dispatcher.utter_message(text="Tell me more about what’s been happening lately. I’m listening.")
        return []

# 💬 Empathic Recovery
class ActionEmpathicRecovery(Action):
    def name(self):
        return "action_empathic_recovery"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_text = tracker.latest_message.get("text", "").lower()
        dispatcher.utter_message(
            text=f"It sounds like there’s a lot on your mind. You’re not alone in this — let’s take it one step at a time."
        )
        return []

# 🪞 Reflection Layer
class ActionReflectBeforeResponse(Action):
    def name(self):
        return "action_reflect_before_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        message = tracker.latest_message.get("text", "").lower()
        reflections = {
            "cry": "It sounds like you’re reaching a breaking point, and tears might just be your body releasing what words can’t.",
            "angry": "It’s okay to feel angry. Sometimes anger is just unspoken pain trying to be heard.",
            "empty": "Feeling empty can be a sign that you’ve given too much for too long. Let’s refill you, piece by piece.",
        }

        for keyword, reflection in reflections.items():
            if keyword in message:
                dispatcher.utter_message(text=reflection)
                return []
        dispatcher.utter_message(text="I hear you. Tell me more — what’s making you feel this way right now?")
        return []

# 📚 Knowledge Base Response Action
class ActionAnswerFromKB(Action):
    def name(self):
        return "action_answer_from_kb"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_query = tracker.latest_message.get("text", "").lower()
        kb_path = os.path.join("knowledge", "bimpe_knowledge_base.json")

        if not os.path.exists(kb_path):
            dispatcher.utter_message(text="Hmm, I can’t seem to access my knowledge base right now.")
            return []

        try:
            with open(kb_path, "r", encoding="utf-8") as kb_file:
                knowledge_data = json.load(kb_file)
        except Exception as e:
            dispatcher.utter_message(text=f"Error reading knowledge base: {e}")
            return []

        # Simple keyword match
        for topic, content in knowledge_data.items():
            if topic.lower() in user_query:
                dispatcher.utter_message(text=content)
                return []

        dispatcher.utter_message(text="I couldn’t find that yet — but I’m still learning. Could you rephrase it?")
        return []

# 🧩 Update Last Message Slot
class ActionUpdateLastUserMessage(Action):
    def name(self):
        return "action_update_last_user_message"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        last_message = tracker.latest_message.get("text", "")
        return [SlotSet("last_user_message", last_message)]
