import os
import pyttsx3


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def print_and_speak(text):
    print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
