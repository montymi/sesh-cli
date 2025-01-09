import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def record_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def recognize_speech(audio):
    try:
        text = recognizer.recognize_sphinx(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        text = ""  # Default return value
    except sr.RequestError:
        print("Sorry, there was an error processing your request.")
        text = ""  # Default return value
    return text

def speak_text(command):
    engine.say(command)
    engine.runAndWait()

if __name__ == "__main__":
    audio = record_audio()
    text = recognize_speech(audio)
    if text:
        speak_text(text)

