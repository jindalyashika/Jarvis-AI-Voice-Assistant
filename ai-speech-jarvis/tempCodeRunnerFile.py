import speech_recognition as sr
import os

def say(text):
    os.system(f"say{text}")
    
if __name__ == '__main__':

    print('pycham')
    say("hello i am jarvis a.i")