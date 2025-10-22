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
# actions/actions.py
from __future__ import annotations
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

# ------------ Helpers: slice history & simple summarizer ------------
def _slice_events(tracker: Tracker, max_turns: int = 8) -> List[Dict[str, Any]]:
    """Keep system-ish start and the most recent turns; drop the noisy middle."""
    ev = tracker.events
    # Keep first ~2 events (often session_start etc.) and last N user/bot messages
    head = ev[:2]
    # filter to user/bot messages only for tail
    msg_events = [e for e in ev if e.get("event") in ("user", "bot")]
    tail = msg_events[-max_turns*2:]  # user+bot pairs
    return head + tail

def _extract_plain_dialogue(events: List[Dict[str, Any]]) -> Text:
    """Return a clean transcript: 'User: ...\nBimpe: ...'"""
    lines = []
    for e in events:
        if e.get("event") == "user":
            txt = e.get("text") or ""
            lines.append(f"User: {txt}")
        elif e.get("event") == "bot":
            txt = e.get("text") or ""
            lines.append(f"Bimpe: {txt}")
    return "\n".join(lines).strip()

def _basic_summarize(text: Text, max_chars: int = 600) -> Text:
    """Tiny heuristic summarizer (no external LLM): keeps key sentences, trims filler."""
    # crude sentence split
    sentences = re.split(r"(?<=[.!?])\s+", text)
    # prioritize first 3 + last 3 sentences
    keep = (sentences[:3] + sentences[-3:]) if len(sentences) > 6 else sentences
    summary = " ".join(keep)
    if len(summary) > max_chars:
        summary = summary[: max_chars - 3] + "..."
    return summary

# ------------ Actions ------------
class ActionUpdateLastUserMessage(Action):
    def name(self) -> Text:
        return "action_update_last_user_message"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        last_user_msg = tracker.latest_message.get("text", "")
        return [SlotSet("last_user_message", last_user_msg)]


class ActionSummarizeConversation(Action):
    def name(self) -> Text:
        return "action_summarize_conversation"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # get current short summary
        current_summary = tracker.get_slot("conversation_summary") or ""
        # slice recent events to avoid “lost in the middle”
        sliced = _slice_events(tracker, max_turns=8)
        transcript = _extract_plain_dialogue(sliced)

        # include prior summary as context header
        stitched = (f"Summary so far: {current_summary}\n\n" if current_summary else "") + transcript

        new_summary = _basic_summarize(stitched, max_chars=800)
        return [SlotSet("conversation_summary", new_summary)]
