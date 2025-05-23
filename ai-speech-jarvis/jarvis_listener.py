import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import google.generativeai as genai
from jarvis_config import GEMINI_API_KEY

chat_history = ""

# Initialize text-to-speech engine
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Capture voice input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception:
            say("Sorry, I didn't catch that.")
            return ""

# Generate response using Gemini API
def generate_gemini_content(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# Handle time/date requests
def tell_date_time(query):
    now = datetime.datetime.now()
    if "time" in query:
        say(f"The time is {now.strftime('%I:%M %p')}")
        return True
    elif "date" in query:
        say(f"Today's date is {now.strftime('%B %d, %Y')}")
        return True
    return False

# Open sites/apps
def open_website_or_app(query):
    sites = {
        "youtube": "https://www.youtube.com/",
        "wikipedia": "https://www.wikipedia.com/",
        "google": "https://www.google.com/",
        "instagram": "https://www.instagram.com/",
        "linkedin": "https://www.linkedin.com/",
        "spotify": "https://open.spotify.com/",
    }
    for name, link in sites.items():
        if f"open {name}" in query:
            say(f"Opening {name}")
            webbrowser.open(link)
            return True

    apps = {
        "notepad": "notepad.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vs code": r"C:\Users\Hi\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }
    for name, path in apps.items():
        if f"open {name}" in query:
            say(f"Opening {name}")
            os.startfile(path)
            return True
    return False

# Play music via browser
def play_music(query):
    if "play music" in query or "play song" in query:
        say("Playing music on YouTube")
        webbrowser.open("https://www.youtube.com/results?search_query=lofi+beats+playlist")
        return True
    return False

# Voice assistant loop
def run_jarvis():
    global chat_history
    say("Jarvis is now active. How can I help you?")
    jarvis_active = True

    while True:
        query = takeCommand()

        if "stop jarvis" in query or "exit" in query:
            say("Goodbye!")
            break

        elif "start jarvis" in query:
            say("Jarvis activated again.")
            continue

        if jarvis_active:
            if tell_date_time(query):
                continue
            elif open_website_or_app(query):
                continue
            elif play_music(query):
                continue
            elif "search" in query:
                search_query = query.replace("search", "").strip()
                say(f"Searching for {search_query}")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                continue
            else:
                chat_history += f"You: {query}\n"
                response = generate_gemini_content(query)
                say(response)
                print(f"Jarvis: {response}")
                chat_history += f"Jarvis: {response}\n"

if __name__ == "__main__":
    run_jarvis()
