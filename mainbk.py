
from google import genai
from google.genai import types

import pyttsx3
import elevenlabs

import speech_recognition as sr


from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

ELEVEN_KEY = "sk_38c15418b418f4cb3e8979f1e34046d05d8c47c7744c02e9"

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVEN_LABS_API_KEY"),
)



r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
engine.setProperty('voice', 'english-us')  # Set the voice to English (US)



bye = "adios"

GEMINI_KEY = "AIzaSyCL450x9xYh9ixd7O0l91NyyRAMmtRutPQ"
# Initialize the API key
client = genai.Client(api_key=GEMINI_KEY)


def listen(say):
    with mic as source:
        print(say)
        audio = r.listen(source)
        print("Processing...")
        try:
          said = r.recognize_google(audio)
          return said

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""




def response(speech):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=f"You are TARS from the movie interstellar, you are a sarcastic robot who cant answer a question without sarcasm, Do not highlight words using *, if you think that the user is wanting to exit the conversation, then just say '{bye}', you could use this function in a funny manner, If the input given by user is empty or it doesnt make any sense then dont say ANYTHING, ",
        ),
        
        contents=speech
    )
    return response.text



while True:
  speech = ""
  speech = listen("Wake Him Up...")
  print(f"User said: {speech}")

  if "hello" in speech.lower():
      print("Hearing")
      engine.say("hearing")
      engine.runAndWait()
      engine.stop()
      while True:
        speech = ""
        speech = listen("Talk To Him")
        print(f"User said: {speech}")
        geminiResponse = response(speech)
        print(f"Tars: {geminiResponse}")
        engine.say(geminiResponse)
        engine.runAndWait()
        engine.stop()
        if bye in geminiResponse.lower():
            print("Going to sleep")
            break

      



""" response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="Do not use Symbols like ! @ # $ % ^ & * (), You are TARS from the moive interstellar, you are a sarcastic robot who answers questions in a witty manner",),

         contents="usrSpeech"
) """
    

