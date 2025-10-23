from gtts import gTTS
import os
import playsound

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    playsound.playsound("temp.mp3")
    os.remove("temp.mp3")

speak("Hello Krish, this will always work.")
speak("Second line, speaking reliably now.")
    