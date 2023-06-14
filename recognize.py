import pyttsx3
import speech_recognition as sr
from vosk import Model,KaldiRecognizer
import pyaudio
import subprocess


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

def command():
    internet = is_internet_on()
    if internet is None:
        vosk()
    else:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            speak("Listening...")
            audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='en-in')
        except sr.UnknownValueError:
            speak("Say again...")
            return "None"
        except sr.RequestError as e:
            speak("Could not request results from Google Speech Recognition service; {0}".format(e))
            return "None"
        query = query.lower()
        return query


def vosk():
    model = Model("C:\\Users\\aliha\\Documents\\Python Projects\\Voice Assistant\\Vosk\\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)
    print("Listening...")
    stream.start_stream()

    while True:
        data = stream.read(4096)
        if len(data) == 0:
            speak("Mic not working")
            break
        if recognizer.AcceptWaveform(data):
            query = recognizer.Result()[14:-3]
            query = query.lower()
            speak(f"You said: {query}")
            if "what" in query or "how" in query or "who" in query or "which" in query:
                speak("Your Internet is off do not ask the question which use internet")
                query = "ok"
            return query


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def is_internet_on():
    try:
        response = subprocess.check_output(['ping', '-n', '1', '-w', '5000', 'google.com'])
        return True
    except subprocess.CalledProcessError:
        return False
    
