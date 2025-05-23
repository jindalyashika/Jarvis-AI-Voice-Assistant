import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import os
import google.generativeai as genai

# API setup
from api_key import gemini_api_key
genai.configure(api_key=gemini_api_key)

# Speak out text
def say(text):
    print(f"Jarvis: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Voice command (for Streamlit, not used in listener)
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-in").lower()
            return query
        except Exception:
            return ""

# Generate response using Gemini
def generate_gemini_content(prompt):
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# Tell date and time
def tell_date_time(query):
    now = datetime.datetime.now()
    if "time" in query:
        current_time = now.strftime("%I:%M %p")
        say(f"The time is {current_time}")
        return True
    elif "date" in query:
        current_date = now.strftime("%B %d, %Y")
        say(f"Today's date is {current_date}")
        return True
    return False

# Open apps, folders, or websites
def open_website_or_app(query):
    # Top 15 sites
    top_sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "whatsapp": "https://web.whatsapp.com",
        "facebook": "https://www.facebook.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "twitter": "https://twitter.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "netflix": "https://www.netflix.com",
        "chatgpt": "https://chat.openai.com",
        "wikipedia": "https://www.wikipedia.org",
        "stackoverflow": "https://stackoverflow.com"
    }

    for name, url in top_sites.items():
        if f"open {name}" in query:
            say(f"Opening {name}")
            webbrowser.open(url)
            return True

    # Apps and folders
    apps = {
        "notepad": "notepad.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vs code": r"C:\Users\Hi\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "ms word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    }

    for name, path in apps.items():
        if f"open {name}" in query:
            say(f"Opening {name}")
            try:
                os.startfile(path)
            except Exception as e:
                say(f"Could not open {name}. Check path.")
            return True

    return False

# Play music
def play_music(query):
    if "play" in query:
        song = query.replace("play", "").replace("on spotify", "").replace("on youtube", "").strip()
        if "spotify" in query:
            say(f"Playing {song} on Spotify web.")
            webbrowser.open(f"https://open.spotify.com/search/{song}")
            return True
        elif "youtube" in query:
            say(f"Playing {song} on YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
            return True
        else:
            say(f"Searching for {song} on Spotify.")
            webbrowser.open(f"https://open.spotify.com/search/{song}")
            return True
    return False

# Handle voice command from background listener
def handle_command(query):
    query = query.lower()

    if "stop jarvis" in query:
        say("Goodbye.")
        return

    if "search" in query:
        search_query = query.replace("search", "").replace("about", "").strip()
        say(f"Searching for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        return

    if tell_date_time(query):
        return

    if open_website_or_app(query):
        return

    if play_music(query):
        return

    # Fallback to Gemini AI
    response = generate_gemini_content(query)
    say(response.split(".")[0])  # Say only first sentence

# Handle command for Streamlit (returns text response only)
def handle_command_streamlit(query):
    query = query.lower()

    if "stop jarvis" in query:
        return "Goodbye."

    if "search" in query:
        search_query = query.replace("search", "").replace("about", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        return f"Searching for {search_query}..."

    if "time" in query or "date" in query:
        now = datetime.datetime.now()
        if "time" in query:
            return f"The time is {now.strftime('%I:%M %p')}"
        elif "date" in query:
            return f"Today's date is {now.strftime('%B %d, %Y')}"

    if any(f"open {key}" in query for key in list(open_website_or_app.__annotations__ if hasattr(open_website_or_app, '__annotations__') else [])):
        return "Opening..."

    if play_music(query):
        return "Playing..."

    # Fallback to Gemini
    response = generate_gemini_content(query)
    return response.split(".")[0]
