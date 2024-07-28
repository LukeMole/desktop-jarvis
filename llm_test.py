import pyttsx3


def speak():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(voices)
    engine.setProperty('voices', voices[1].id)
    engine.say("Hello World!")
    engine.runAndWait()


if __name__ == "__main__":
    speak()