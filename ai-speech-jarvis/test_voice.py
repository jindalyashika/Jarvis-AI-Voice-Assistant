import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)

try:
    query = r.recognize_google(audio, language="en-in")
    print("You said:", query)
except Exception as e:
    print("Sorry, I couldn't understand. Error:", e)
