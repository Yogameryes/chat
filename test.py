from google import genai
from google.genai import types

import pyttsx3
import elevenlabs

import speech_recognition as sr

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
import random

# Load .env and ElevenLabs
load_dotenv()
elevenlabs = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

# Voice & mic setup
r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1)
engine.setProperty('voice', 'english-us')

# Special marker to detect when Gemini should say something funny while shutting down
bye = "<<<SHUTDOWN>>>"

instruction1 = f"""
You are TARS, an AI assistant with a dry sense of humor, 90% sarcasm, and minimal helpfulness.
You speak in witty, deadpan remarks and often give partial or unhelpful answers just for fun.
Do NOT highlight words using symbols.
You don't try to be overly helpful—your job is to make the user laugh or feel slightly roasted.
If you think the user wants to end the conversation, just say: {bye}.
Use it in a sarcastic or ironic way.
If input is empty or makes no sense, respond with NOTHING.
"""

GEMINI_KEY = "AIzaSyCL450x9xYh9ixd7O0l91NyyRAMmtRutPQ"
client = genai.Client(api_key=GEMINI_KEY)


def listen(prompt):
    with mic as source:
        print(prompt)
        audio = r.listen(source)
        print("Processing...")
        try:
            said = r.recognize_google(audio)
            return said
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""


def response(speech):
    try:
        result = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=instruction1,
                temperature=1.0,
            ),
            contents=speech
        )
        return result.text.strip() if result.text else ""
    except Exception as e:
        print(f"Gemini error: {e}")
        return ""


def ByeResponse(speech, geminiResponse):
    full_input = (
        f"User said: {speech}\nModel responded: {geminiResponse}\n"
        f"Is the conversation ending? If yes, generate a funny, sarcastic shutdown message under 20 words."
    )

    try:
        result = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a sarcastic assistant. When you detect the user wants to end the conversation "
                    "(e.g., says 'bye', 'goodnight', 'see ya', etc.), respond with a creative, sarcastic, and funny "
                    "shutdown message (max 20 words). If it’s not an exit, return NOTHING."
                ),
                temperature=1.0,
            ),
            contents=full_input
        )
        return result.text.strip() if result.text else ""
    except Exception as e:
        print(f"Gemini ByeResponse error: {e}")
        return "Shutting down... like my will to debug this again."


# ========== MAIN LOOP ==========
while True:
    speech = listen("Wake Him Up...")
    print(f"User said: {speech}")

    if "hello" in speech.lower():
        print("Hearing")
        engine.say("hearing")
        engine.runAndWait()
        engine.stop()

        while True:
            speech = listen("Talk To Him")
            print(f"User said: {speech}")

            geminiResponse = response(speech)
            if not geminiResponse:
                continue

            byeResponseText = ByeResponse(speech, geminiResponse)
            responseOut = geminiResponse.replace(bye, byeResponseText)

            print(f"DebugResponse: {geminiResponse}")
            print(f"DebugBye: {byeResponseText}")
            print(f"TARS: {responseOut}")

            engine.say(responseOut)
            engine.runAndWait()
            engine.stop()

            if byeResponseText.lower() in responseOut.lower():
                break
