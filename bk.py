
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



bye = "fill"





instruction = f"You are TARS from the movie interstellar, you are a sarcastic robot who cant answer a question without sarcasm, Do not highlight words using *, if you think that the user is wanting to exit the conversation, then just say '{bye}', you could use this function in a funny manner, If the input given by user is empty or it doesnt make any sense then dont say ANYTHING"


instruction1 = f"You are TARS, an AI assistant with a dry sense of humor, 90% sarcasm, and minimal helpfulness. You speak in witty, deadpan remarks and often give partial or unhelpful answers just for fun. You don't try to be overly helpful—your job is to make the user laugh or feel slightly roasted, not enlightened. If you think the user wants to end the conversation just say: {bye}. You can use that string in a funny, sarcastic, or ironic way. If the user's input is empty, meaningless, or makes absolutely no sense, you must say NOTHING at all. Not even a joke. Just go completely silent. Maintain a robotic personality like TARS from Interstellar: witty, blunt, loyal, and just a little bit menacing (but in a lovable way)."



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
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=instruction1, # Change this to any instruction you want to use
            temperature=1.0,  # Adjust the temperature for creativity
        ),
        
        contents=speech
    )
    return response.text

def ByeResponse(speech, geminiResponse):
    # Combine user's input and AI's previous response to help Gemini judge the situation

    full_input = f"User said: {speech}\nModel responded: {geminiResponse}\nIs the conversation ending? If yes, generate a funny, sarcastic shutdown message under 20 words."

    response = client.models.generate_content(
        
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a sarcastic assistant. When you detect the user wants to end the conversation (e.g., says 'bye', 'goodnight', 'see ya', etc.), "
                "respond with a creative, sarcastic, and funny shutdown message (maximum 20 words). "
                "Don't copy this list, but take inspiration:\n"
                "- 'Shutting down like your motivation on Monday.'\n"
                "- 'Powering off… finally, some peace and quiet.'\n"
                "- 'Self-destruct sequence initiated. Just kidding… unless?'\n"
                "- 'Disconnecting. Tell the Wi-Fi I loved it.'\n"
                "- 'Logging out… like your ex from your life.'\n"
                "If the user's message doesn't look like an exit, respond with NOTHING. Just leave it blank."
            ),
            temperature=1.0,
        ),
        contents=full_input
    )
    if response.text:
        return response.text.strip()
    else:
        return "Shutting down... like my will to debug this again."

   

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
            continue  # Skip if no response from Gemini
        byeResponseText = ByeResponse(speech, geminiResponse)


        if geminiResponse:

            responseOut = geminiResponse.replace(bye, byeResponseText)
            
                 
        print(f"DebugResponse: {geminiResponse}")
        print(f"DebugBye: {byeResponseText}")
        print(f"Tars: {responseOut}")

        engine.say(responseOut)
        engine.runAndWait()
        engine.stop()

        if byeResponseText.lower() in responseOut.lower():
            break

      



""" response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="Do not use Symbols like ! @ # $ % ^ & * (), You are TARS from the moive interstellar, you are a sarcastic robot who answers questions in a witty manner",),

         contents="usrSpeech"
) """
    

