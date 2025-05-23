# jarvis_listener.pyw

import speech_recognition as sr
import time
import threading
import main  # Your main.py with all logic

recognizer = sr.Recognizer()
mic = sr.Microphone()
stop_listening = None  # Will hold stop function


def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"You said: {text}")

        # Stop listening
        if "stop jarvis" in text:
            print("Stopping Jarvis...")
            main.say("Goodbye.")
            if stop_listening:
                stop_listening(wait_for_stop=False)
            return

        # Pass command to main handler
        main.handle_command(text)

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print(f"Speech Recognition error: {e}")


def start_listener():
    global stop_listening
    print("🎤 Starting Jarvis listener...")
    stop_listening = recognizer.listen_in_background(mic, callback)
    print("✅ Jarvis is now listening in the background.")


start_listener()

# Keep the script alive
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
    if stop_listening:
        stop_listening(wait_for_stop=False)
