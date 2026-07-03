import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import requests
import musiclibrary   

recognizer = sr.Recognizer()
engine = pyttsx3.init("sapi5")  
def speak(text):
    engine = pyttsx3.init()   
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 👈 voice fix

    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()
    
def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=e8fd8d98e587401ea779c7951e56ef9a")
        if r.status_code == 200:
           # parse the json response
           data = r.json()

        # Extract the articles
        articles = data.get('articles', [])

        # print the headlines
        for article in articles:
            speak(article['title'])
    
if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        print("recognizing....")
        try:
            # 🎤 Wake word listen
            with sr.Microphone() as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)
            print("You said:", word)

            # 🔥 Wake word check
            if "jarvis" in word.lower():
                print("Jarvis activated")
                time.sleep(1)
                speak("Yes")
                time.sleep(0.5)

                # 🎤 Command listen
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except sr.UnknownValueError:
            print("Dont understand")

        except Exception as e:
            print("error:", e)