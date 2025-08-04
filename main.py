
from google import genai
from google.genai import types

import elevenlabs

import speech_recognition as sr


from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
import json

ELEVEN_KEY = "sk_38c15418b418f4cb3e8979f1e34046d05d8c47c7744c02e9"

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVEN_LABS_API_KEY"),
)


memory_file = "memory.json"
r = sr.Recognizer()
mic = sr.Microphone()

exitWord = "skibidi"

GEMINI_KEY = "AIzaSyBDMuXI7lXZVKuvmbMiA4jgRWIrAsJ9esM"
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
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            #system_instruction="You are TARS from the moive interstellar, you are a sarcastic robot who answers questions in a witty manner, if you think that the user is wanting to exit the conversation, then just say 'adios', you could use this function in a funny manner, If the input given by user is empty or it doesnt make any sense then dont say ANYTHING",
            system_instruction=f"You are TARS from the moive interstellar, you are a sarcastic robot who answers questions in a witty manner. if you think that the user is wanting to exit the conversation, then just say '{exitWord}', you could use this function in a funny manner. If the input given by user is empty or it doesnt make any sense then dont say ANYTHING.",
        ),
        
        contents=speech
    )
    return response.text


def responseElevenlabs(speech):
    if not speech:
        return 
    audio = elevenlabs.text_to_speech.convert(
    text=speech,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)
    play(audio)


responseElevenlabs("Getting ready. please wait...")
responseElevenlabs("Say the word 'hello' to start your conversation with TARS")
while True:
  speech = ""
  speech = listen("Wake Him Up...")
  print(f"User said: {speech}")

  if "hello" in speech.lower():
      print("Hearing")
      responseElevenlabs("Hearing")
      while True:
        speech = listen("Talk To Him")
        print(f"User said: {speech}")
        geminiResponse = response(speech)
        print(f"Tars: {geminiResponse}")
        responseElevenlabs(geminiResponse)
        if exitWord in geminiResponse.lower():
            break

      



""" response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="Do not use Symbols like ! @ # $ % ^ & * (), You are TARS from the moive interstellar, you are a sarcastic robot who answers questions in a witty manner",),

         contents="usrSpeech"
) """
    

