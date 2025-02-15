from pyexpat import model
import speech_recognition as sr
import webbrowser
import pyttsx3 
import musicLibrary
import google.generativeai as genai
import config
import re 
from termcolor import colored

# pip install pocketsphinx
# pip install google.generativeai

recognizer = sr.Recognizer()
ttsx = pyttsx3.init()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):
   genai.configure(api_key=config.Api_key())
   model = genai.GenerativeModel("gemini-1.5-flash")
   response = model.generate_content(command)
   answer = response.text

   clean_answer = answer.replace("*","") #Remove asterisks
   clean_answer = re.sub(r"[*]+", "", clean_answer) #Remove multiple asterisks
   print(colored(clean_answer,"magenta"))
   speak(clean_answer)


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif c.lower().startswith("play"):
        song = c.lower().split("play", 1)[1]

        try:
            musicLibrary.search_and_play_song(song)
        except Exception as e:
            print(f"Failed to play song: {e}")

    else:
        try:
            output = aiProcess(c)
            speak(output)
        except Exception as e:
            print(f"AI processing failed: {e}")



if __name__ == "__main__":
    speak("Initializing Jarvis.......")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        print(colored("recognizing!...", "red", attrs=["bold"]))
        try:
            with sr.Microphone() as source:
                print(colored("Listening!....","yellow", attrs=["bold"]))
                audio = r.listen(source, timeout=2, phrase_time_limit=5)

            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yeah!")
                # Listen for command 
                with sr.Microphone() as source:
                    speak("Jarvis Activate")
                    print(colored("Jarvis Active....","green", attrs=["bold"]))
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    processCommand(command)
                    
        except Exception as e:
            print(f"An error occurred; {e}")