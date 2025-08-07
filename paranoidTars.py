from google import genai
from google.genai import types

import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1)
engine.setProperty('voice', 'english-us')

# Special marker to detect when Gemini should say something funny while shutting down
bye = "<<<SHUTDOWN>>>"

instruction1 = f"""
You are currently talking to yourself as the programmer decided to see a paranoid Tars as he's just watching you
go insane while talking to youself.
You speak in witty
If input is empty or makes no sense, respond with NOTHING.
"""

GEMINI_KEY = "AIzaSyCL450x9xYh9ixd7O0l91NyyRAMmtRutPQ"
client = genai.Client(api_key=GEMINI_KEY)



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

# ========== MAIN LOOP ==========
while True:
    speech = input("Say Something to start the chaos: ")
    print(f"User said: {speech}")
    print("Tars: I dont think you are ready for this...")
    engine.say("I dont think you are ready for this...")
    engine.runAndWait()
    engine.stop()

    while True:
            
        print(f"User said: {speech}")

        geminiResponse = response(speech)
        if not geminiResponse:
            continue

        print(f"DebugResponse: {geminiResponse}")

        engine.say(geminiResponse)
        engine.runAndWait()
        engine.stop()
        speech = geminiResponse
        if bye.lower() in geminiResponse.lower():
            break
